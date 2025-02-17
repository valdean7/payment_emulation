## CredentialsMiddleware

??? Quote "Source code in <code>payment_emulation\payment\middleware.py</code>"
    ```{.python linenums="1"}
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

    ```

O **CredentialsMiddleware** intercepta requisições HTTP para extrair, a partir de formulários, os dados de credenciais de pagamento. Ele foi desenvolvido especificamente para funcionar com o [modal de pagamento](payment_modal.md/#modal-do-formulario-de-pagamento). Sua principal função é criar, na instância de `request`, um atributo chamado `credentials` contendo um dicionário com os dados extraídos. Dessa forma, as credenciais ficam prontamente disponíveis para serem utilizadas, por exemplo, no método [`payment()`](payment/PaymentSDK.md/#payment_emulation.payment.paymentSDK.PaymentSDK.payment) do `PaymentSDK`.

### Como adicionar o middleware

Para que o middleware funcione corretamente, adicione-o ao final da lista de middlewares do seu projeto. Exemplo:

```{.python .copy}
MIDDLEWARE = [
    ...
    'payment_emulation.payment.middleware.CredentialsMiddleware',
]
```
### Exemplo de uso

No exemplo abaixo, o atributo `credentials` é utilizado em uma view para executar o pagamento:

```{.python .copy linenums="1" hl_lines="13"}
from django.shortcuts import render
from payment_emulation.payment.paymentSDK import PaymentSDK


def index(request):
    if request.method == 'POST':
        items = [
            {'quantity': 2, 'unit_price': 67.73, 'title': 'T-shirt'},
            {'quantity': 4, 'unit_price': 45.78, 'title': 'Shoes'},
        ]

        sdk = PaymentSDK(items)
        response = sdk.payment(**request.credentials)

        print(response)
        return render(request, 'index.html')
    else:
        return render(request, 'index.html')
```

```{.bash title="output:"}
{
    "transaction": "success", 
    "items": [
        {"quantity": 2, "unit_price": 67.73, "title": "T-shirt"}, 
        {"quantity": 4, "unit_price": 45.78, "title": "Shoes"}
    ], 
    "redirect_urls": null, 
    "address": null, 
    "payer": null, 
    "amount": 318.58, 
    "created_at": "2025-02-16T00:29:10.852211+00:00"
}
```

### Formulário genérico compatível com o middleware

Caso deseje implementar seu próprio formulário de pagamento e aproveitar a interceptação de dados realizada pelo middleware, certifique-se de utilizar os seguintes nomes para os campos de entrada:

- **card_number**: Número do cartão (os espaços serão removidos automaticamente).
- **holder**: Nome do titular do cartão.
- **validity**: Data de validade do cartão no formato `MM/AA`.
- **cvv**: Código de segurança (*valor de verificação do cartão*).
- **cpf**: CPF do titular (as pontuações `.`, `-` serão removidos automaticamente).
- **cnpj**: CNPJ do titular (as pontuações `.`, `-`, `/` serão removidos automaticamente).
- **cpfcnpj**: Campo (normalmente um select) para alternar entre `CPF` e `CNPJ`.

Utilize esses nomes de campos para que o middleware possa interceptar e processar corretamente as informações enviadas.