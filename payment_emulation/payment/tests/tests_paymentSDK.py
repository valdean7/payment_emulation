from django.test import TestCase
from payment_emulation.payment.paymentSDK import PaymentSDK
from unittest.mock import patch, Mock as M
from payment_emulation.payment.models import Card, Account
from decimal import Decimal
import json
from pycpfcnpj.gen import cnpj


class TestPaymentSDK(TestCase):

    def setUp(self):
        def get_card(holder: str):
            card = Card.objects.get(card_holder_name=holder)
            return card

        self.item = [
            {'id': 1, 'title': 'test', 'quantity': 1, 'unit_price': 10}
        ]

        self.get_card = get_card


    def test_should_validate_the_items_passed_in_the_initializer(self):
        for n in range(1,3):
            with self.subTest():
                if n == 1:
                    self.item[0].pop('quantity')
                    self.assertRaises(KeyError, PaymentSDK, self.item)

                elif n == 2:
                    self.item[0].pop('unit_price')
                    self.assertRaises(KeyError, PaymentSDK, self.item)


    @patch('payment_emulation.payment.paymentSDK.PaymentSDK._set_response')
    def test_should_check_if_the_response_has_been_seted(self,mock: M):
        PaymentSDK(self.item)
        self.assertEqual(mock.call_count, 1)


    def test_should_check_if_the_params_passed_on_init_are_not_none(self):
        keys = ['items', 'redirect_urls', 'address', 'payer', 'token']

        payment = PaymentSDK(
            items=self.item,
            redirect_urls={'success': '', 'failure': '', 'pending': ''},
            address={'city': '', 'number': '', 'street': ''},
            payer={'name': '', 'email': ''},
            token='test'
        )
        for key in keys:
            with self.subTest():
                self.assertIsNotNone(payment.RESPONSE.get(key))

    
    def test_should_check_if_the_card_credentials_are_correct(self):
        card = self.get_card('PROBATUS')

        data = f'{card.validity.month}/{str(card.validity.year)[2:]}'
        payment = PaymentSDK(self.item)

        credentials = payment.card_credentials(
            cpf=card.account.cpf, 
            card_number=card.card_number, 
            validity=data,
            cvv=card.cvv,
            holder=card.card_holder_name
        )
        self.assertIsNotNone(credentials)


    def test_should_return_none_if_the_credentials_are_incorrect(self):
        card = self.get_card('PROBATUS')

        data = f'{card.validity.month + 1}/{str(card.validity.year)}'
        payment = PaymentSDK(self.item)

        credentials = payment.card_credentials(
            cpf='00000000000', 
            card_number=card.card_number, 
            validity=data,
            cvv='000',
            holder='probatus'
        )
        self.assertIsNone(credentials)


    def test_should_raise_value_error_if_cpf_and_cnpj_are_none(self):
        card = self.get_card('PROBATUS')

        payment = PaymentSDK(self.item)
        with self.assertRaises(ValueError):
            payment.card_credentials(
            card_number=card.card_number,
            validity=f'{card.validity.month}/{str(card.validity.year)[2:]}',
            cvv=card.cvv,
            holder=card.card_holder_name
            )


    def test_should_be_ok_if_validity_month_start_with_zero(self):
        card = self.get_card('PROBATUS')

        payment = PaymentSDK(self.item)
        response = payment.card_credentials(
            card_number=card.card_number,
            validity=f'0{card.validity.month}/{str(card.validity.year)[2:]}',
            cvv=card.cvv,
            holder=card.card_holder_name,
            cpf=card.account.cpf
        )
        self.assertIsNotNone(response)

    
    def test_should_be_none_if_card_credentials_cnpj_is_not_correct(self):
        account = Account.objects.create(
            cnpj=cnpj(),
            account_holder_name='TEST',
        )
        card = Card.objects.create(
            account=account,
            card_holder_name='TEST',
            card_flag='MC',
            pin='1234'
        )
        payment = PaymentSDK(self.item)
        response = payment.card_credentials(
            card_number=card.card_number,
            validity=f'{card.validity.month}/{str(card.validity.year)[2:]}',
            cnpj='0000000000000',
            cvv=card.cvv,
            holder=card.card_holder_name
        )
        self.assertIsNone(response)


    def test_should_return_a_sum_of_all_items(self):
        self.item.append(
            {'id': 2, 'title': 'test', 'quantity': 2, 'unit_price': 10}
        )

        payment = PaymentSDK(self.item)
        self.assertEqual(
            payment.get_items_total_value(),
            Decimal('30.00')
        )


    def test_should_raise_if_the_transation_is_wrong(self):
        payment = PaymentSDK(self.item)
        with self.assertRaises(ValueError):
            payment.send_response('test')


    def test_should_send_the_response_if_the_transation_is_correct(self):
        for t in PaymentSDK.TRANSACTION:
            with self.subTest():
                payment = PaymentSDK(self.item)
                response = json.loads(payment.send_response(t))
                self.assertEqual(response['transaction'], t)


    def test_should_check_if_the_amount_key_was_created(self):
        payment = PaymentSDK(self.item)
        response = json.loads(payment.send_response('success'))
        self.assertIn('amount', response)


    def test_should_check_if_the_createdat_key_was_created(self):
        payment = PaymentSDK(self.item)
        response = json.loads(payment.send_response('success'))
        self.assertIn('created_at', response)


    def test_should_return_a_success_transaction(self):
        card = self.get_card('PROBATUS')
        validity = f'{card.validity.month}/{str(card.validity.year)[2:]}'
        payment = PaymentSDK(self.item)
        response = payment.payment(
            cpf=card.account.cpf, 
            card_number=card.card_number, 
            validity=validity, 
            cvv=card.cvv, 
            holder=card.card_holder_name
        )
        response_object = json.loads(response)

        self.assertEqual(response_object['transaction'], 'success')


    def test_should_return_a_failure_transaction(self):
        card = self.get_card('PROBATUS')
        validity = f'{card.validity.month}/{str(card.validity.year)[2:]}'
        payment = PaymentSDK(self.item)
        response = payment.payment(
            cpf=card.account.cpf, card_number=card.card_number, 
            validity=validity, cvv=card.cvv, holder='TEST'
        )
        response_object = json.loads(response)

        self.assertEqual(response_object['transaction'], 'failure')


    def test_should_return_a_pending_transaction(self):
        card = self.get_card('PENDENTE')
        validity = f'{card.validity.month}/{str(card.validity.year)[2:]}'
        payment = PaymentSDK(self.item)
        response = payment.payment(
            cpf=card.account.cpf, 
            card_number=card.card_number, 
            validity=validity, 
            cvv=card.cvv, 
            holder=card.card_holder_name
        )
        response_object = json.loads(response)

        self.assertEqual(response_object['transaction'], 'pending')

    
    def test_should_return_a_failure_transaction_if_balance_is_not_enough(self):
        card = self.get_card('REPROBI')
        validity = f'{card.validity.month}/{str(card.validity.year)[2:]}'
        payment = PaymentSDK(self.item)
        response = payment.payment(
            cpf=card.account.cpf, card_number=card.card_number, 
            validity=validity, cvv=card.cvv, holder=card.card_holder_name
        )
        response_object = json.loads(response)

        self.assertEqual(response_object['transaction'], 'failure')


    @patch('payment_emulation.payment.paymentSDK.PaymentSDK.set_seeds')
    def test_should_call_set_seeds_once(self, mock: M):
        PaymentSDK.get_seeds()
        self.assertEqual(mock.call_count, 3)

    def test_should_return_an_object_with_the_seeds(self):
        seeds = PaymentSDK.get_seeds()
        self.assertIn('PROBATUS', seeds)
        self.assertIn('REPROBI', seeds)
        self.assertIn('PENDENTE', seeds)
