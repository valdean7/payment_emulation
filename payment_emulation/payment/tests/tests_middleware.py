from django.test import TestCase, RequestFactory
from django.http import HttpResponse
from payment_emulation.payment.middleware import CredentialsMiddleware


class TestMiddleware(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = CredentialsMiddleware(lambda req: HttpResponse('ok!'))

    
    def test_should_return_an_empty_dict_if_request_metthod_are_get(self):
        request = self.factory.get('/')
        self.middleware(request)
        self.assertDictEqual(request.credentials, {})


    def test_should_return_an_empty_dict_if_allowed_keys_are_not_passed(self):
        request = self.factory.post('/', {'data':'test', 'test': True})
        self.middleware(request)
        self.assertDictEqual(request.credentials, {})


    def test_should_return_a_dict_with_key_if_one_allowed_key_are_passed(self):
        request = self.factory.post('/', {'holder':'test'})
        self.middleware(request)
        credentials_dict = {
            'card_number': '', 'cvv': '', 'holder': 'test', 'validity': ''
        }
        self.assertDictEqual(request.credentials, credentials_dict)


    def test_sould_return_a_dict_with_all_allowed_keys_and_cpf_key(self):
        data = {
            'card_number': '0000000', 'cvv': '000', 'holder': 'test',
            'validity': '00/00', 'cpf': '0000000'
        }
        request = self.factory.post('/', data)
        self.middleware(request)
        self.assertDictEqual(request.credentials, data)


    def test_sould_return_a_dict_with_all_allowed_keys_and_cnpj_key(self):
        data = {
            'card_number': '0000000', 'cvv': '000', 'holder': 'test',
            'validity': '00/00', 'cnpj': '0000000'
        }
        request = self.factory.post('/', data)
        self.middleware(request)
        self.assertDictEqual(request.credentials, data)


    def test_sould_return_a_dict_with_cpfcnpj_value_iquals_to_CPF(self):
        data = {
            'card_number': '0000000', 'cvv': '000', 'holder': 'test',
            'validity': '00/00', 'cpfcnpj': 'CPF', 'cpf': ''
        }
        request = self.factory.post('/', data)
        data.pop('cpfcnpj')
        self.middleware(request)
        self.assertDictEqual(request.credentials, data)


    def test_sould_return_a_dict_with_cpfcnpj_value_iquals_to_CNPJ(self):
        data = {
            'card_number': '0000000', 'cvv': '000', 'holder': 'test',
            'validity': '00/00', 'cpfcnpj': 'CNPJ', 'cnpj': ''
        }
        request = self.factory.post('/', data)
        data.pop('cpfcnpj')
        self.middleware(request)
        self.assertDictEqual(request.credentials, data)
