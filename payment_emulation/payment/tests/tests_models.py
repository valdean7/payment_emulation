from payment_emulation.payment.models import Account, Card
from django.test import TestCase
from pycpfcnpj.gen import cpf, cnpj
from unittest.mock import patch, Mock as M
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class TestModels(TestCase):
    def setUp(self):
        def get_account(holder_name: str) -> Account:
            account = Account.objects.get(account_holder_name=holder_name)
            return account
        
        self.get_account = get_account


    @patch('payment_emulation.utils.generators.generate_account_number')
    def test_should_create_the_account_generating_an_account_number(self, m: M):
        probatus = self.get_account('PROBATUS')
        probatus.account_number = '402532629764'
        probatus.save()

        m.side_effect = ['402532629764', '768452749127']
        holder = 'test'

        account = Account.objects.create(
            cpf=cpf(),
            account_holder_name=holder,
            balance=10
        )
        self.assertEqual(holder.upper(), account.__str__())
        self.assertEqual('768452749127', account.account_number)
        self.assertEqual(m.call_count, 2)


    def test_must_validate_the_accounts_CPF(self):
        with self.assertRaises(ValidationError):
            CPF = '88388852094'
            account = Account.objects.create(
                cpf=CPF,
                account_holder_name='TEST',
                balance=10
            )


    def test_must_validate_the_account_number(self):
        with self.assertRaises(ValidationError):
            account = Account.objects.create(
                cpf=cpf(),
                account_holder_name='TEST',
                account_number='162d65636fbv6564',
                balance=10
            )


    def test_must_validate_the_account_holder_name(self):
            with self.assertRaises(ValidationError):
                account = Account.objects.create(
                    cpf=cpf(),
                    account_holder_name='TEST1',
                    balance=10
                )


    def test_should_create_account_with_cnpj(self):
        account = Account.objects.create(
            cnpj=cnpj(),
            account_holder_name='TEST'
        )
        self.assertEqual(account.__str__(),'TEST')


    def test_should_create_a_card(self):
        probatus = self.get_account('PROBATUS')

        card = Card.objects.create(
            account=probatus,
            card_holder_name=probatus.__str__().lower(),
            card_flag='VISA',
            pin='1234'
        )

        self.assertEqual(probatus.__str__(), card.__str__())


    @patch('payment_emulation.utils.generators.generate_card_number')
    def test_should_generate_another_card_number_if_the_same_exists(self, mock):
        reprobi = self.get_account('REPROBI')
        card_number = '1231436472485781'
        Card.objects.create(
            account=reprobi,
            card_holder_name=reprobi.__str__(),
            card_number=card_number,
            card_flag='VISA',
            pin='1234'
        )
        mock.side_effect = [card_number, '5453465736376376']

        probatus = self.get_account('PROBATUS')

        card = Card.objects.create(
            account=probatus,
            card_holder_name=probatus.__str__(),
            card_flag='VISA',
            pin='1234'
        )

        self.assertEqual('5453465736376376', card.card_number)
        self.assertEqual(mock.call_count, 2)


    def test_should_check_the_pin(self):
        probatus = self.get_account('PROBATUS')

        card = Card.objects.create(
            account=probatus,
            card_holder_name=probatus.__str__(),
            card_flag='VISA',
            pin='1234'
        )

        self.assertTrue(card.check_pin('1234'))


    def test_should_validate_the_card_holder_name(self):
        with self.assertRaises(ValidationError):
            probatus = self.get_account('PROBATUS')
            Card.objects.create(
                account=probatus,
                card_holder_name='test1',
                card_flag='VISA',
                pin='1234'
            )


    def test_should_validate_the_card_pin(self):
        with self.assertRaises(ValidationError):
            probatus = self.get_account('PROBATUS')
            Card.objects.create(
                account=probatus,
                card_holder_name='test',
                card_flag='VISA',
                pin='1234a'
            )


    def test_should_validate_the_pin_length(self):
        with self.assertRaises(ValidationError):
            probatus = self.get_account('PROBATUS')
            Card.objects.create(
                account=probatus,
                card_holder_name='test',
                card_flag='VISA',
                pin='123'
            )


    def test_should_validate_the_card_number(self):
        with self.assertRaises(ValidationError):
            probatus = self.get_account('PROBATUS')
            Card.objects.create(
                account=probatus,
                card_holder_name='test',
                card_number='6752gfhgf364b6',
                card_flag='VISA',
                pin='1234'
            )


    def test_should_validate_the_card_cvv(self):
        with self.assertRaises(ValidationError):
            probatus = self.get_account('PROBATUS')
            Card.objects.create(
                account=probatus,
                card_holder_name='test',
                card_flag='VISA',
                pin='1234',
                cvv='12a'
            )


    def test_should_get_readonly_fields(self):
        User.objects.create_superuser(username='test', password='1q2w3e4r')
        self.client.login(username='test', password='1q2w3e4r')
        response = self.client.get('/admin/payment/card/1/change/')
        self.assertIn(
            'Administração do Django',
            response.content.decode() 
        )


    def test_should_raise_validation_error_if_provide_cpf_and_cnpj(self):
        with self.assertRaises(ValidationError):
            Account.objects.create(
                cpf=cpf(), 
                cnpj=cnpj(),
                account_holder_name='TEST'
            )


    def test_should_raise_validation_error_if_cnpj_is_invalid(self):
        with self.assertRaises(ValidationError):
            Account.objects.create(
                cnpj='897454546754',
                account_holder_name='TEST'
            )
