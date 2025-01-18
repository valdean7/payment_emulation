from payment_emulation.utils import generators
import pytest
from datetime import date


def test_should_generate_an_account_number():
    number = generators.generate_account_number()
    assert number.isdigit() == True


@pytest.mark.parametrize(
    ('flag',),
    (
        ('VISA',), 
        ('ELO',), 
        ('MC',), 
        ('OTHER',)
    )
)
def test_should_generate_a_card_number(flag):
    number = generators.generate_card_number(flag)
    assert number.isdigit() == True


def test_should_raise_value_error_if_flag_is_not_supported():
    flag = 'TESTE'
    match = 'Flag not supported.'
    with pytest.raises(ValueError, match=match):
        generators.generate_card_number(flag)


def test_should_validate_card_number_returning_zero_if_is_ok():
    card_number = generators.generate_card_number('VISA')
    assert generators.luhn_checksum(card_number) == 0


def test_should_invalidate_card_number_returning_a_number_greater_than_zero():
    card_number = '1648679804658173'
    assert generators.luhn_checksum(card_number) >= 0


def test_should_generate_a_cvv():
    card_number = '1648679804658173'
    date_delta = date(2030,1,1)
    secret = 'secrettest'
    cvv = generators.generate_cvv(card_number, date_delta, secret)
    assert cvv.isdigit() == True
    assert len(cvv) == 3


def test_should_validate_a_cvv():
    card_number = '1648679804658173'
    date_delta = date(2001,1,1)
    secret = 'secrettest'
    cvv = generators.generate_cvv(card_number, date_delta, secret)
    cvv_validation = generators.verify_cvv(
        card_number, date_delta, secret, cvv
    )
    assert cvv_validation == True


def test_should_implement_a_new_prefixe():
    prefix = {'NEW': ['1']}
    generators.prefixes.update(prefix)

    card_number = generators.generate_card_number('NEW')
    assert card_number[:1] == '1'
