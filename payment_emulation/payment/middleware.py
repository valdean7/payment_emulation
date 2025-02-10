from django.http import HttpRequest
from pycpfcnpj.compatible import clear_punctuation as cp


class CredentialsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request: HttpRequest):
        if request.method == 'POST':
            keys = ['validity', 'cvv', 'holder']

            values = {
                key: request.POST.get(key, "")
                for key in keys
            }

            card_number = request.POST.get('card_number')
            if card_number:
                values.update(card_number=card_number.replace(' ', ''))
            else:
                values.update(card_number="")

            if request.POST.get('cpfcnpj') == 'CPF':
                values.update(cpf=cp(request.POST.get('cpf', "")))
            elif request.POST.get('cpfcnpj') == 'CNPJ':
                values.update(cnpj=cp(request.POST.get('cnpj', "")))

            if not request.POST.get('cpfcnpj'):
                if request.POST.get('cpf'):
                    values['cpf'] = cp(request.POST.get('cpf', ""))

                elif request.POST.get('cnpj'):
                    values['cnpj'] = cp(request.POST.get('cnpj', ""))

            caunt = 0
            for _, value in values.items():
                if value != "":
                    caunt += 1
            if caunt > 0:
                request.credentials = values
            else:
                request.credentials = {}
        else:
            request.credentials = {}
            
        response = self.get_response(request)
        return response
