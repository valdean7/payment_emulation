# Payment Emulation

[![codecov](https://codecov.io/gh/valdean7/payment_emulation/graph/badge.svg?token=IHKF7WUWDY)](https://codecov.io/gh/valdean7/payment_emulation) ![CI](https://github.com/valdean7/payment_emulation/actions/workflows/pipiline.yaml/badge.svg) ![docs](https://readthedocs.org/projects/payment-emulation/badge/?version=latest&style=default)

## Descrição

Payment Emulation é uma biblioteca desenvolvida para ser usada em projetos Django 
para emular pagamentos com cartões bancários. Ela é ideal para ser usada em seus 
projetos para implementar um método de pagamento.

## Requisitos
Payment Emulation requer o seguinte:

- Django (>=5.1)
- Python (>=3.10)

## Instalação

### 1. Instalar a biblioteca Payment Emulation:

```bash
pip install payment-emulation
```

### 2. Adicione em `INSTALLED_APPS`: 

```python
INSTALLED_APPS = [
    ...
    'payment_emulation.payment',
]
```

### 3. Realize as migrações:

```bash
python manage.py migrate
```

## Exemplo

Vamos dar uma olhada em um exemplo rápido de como usar a biblioteca Payment Emulation.

```python
from payment_emulation.payment.paymentSDK import PaymentSDK

items = [
    {'id': 1, 'title': 'T-shirt', 'quantity': 3, 'unit_price': 49.99},
    {'id': 2, 'title': 'shoe', 'quantity': 1, 'unit_price': 149.99},
    {'id': 3, 'title': 'sweater', 'quantity': 2, 'unit_price': 80},
]

sdk = PaymentSDK(items)

response = sdk.payment(
    cpf='45230544015',
    card_namber='4763871810133150',
    validity='12/29',
    cvv='342',
    holder='PROBATUS'
)

print(response)

expected output:
>>>{
        "transaction": "success", 
        "items": [
            {"id": 1, "title": "T-shirt", "quantity": 3, "unit_price": 49.99}, 
            {"id": 2, "title": "shoe", "quantity": 1, "unit_price": 149.99}, 
            {"id": 3, "title": "sweater", "quantity": 2, "unit_price": 80}
        ], 
        "redirect_urls": null, 
        "address": null, 
        "payer": null,
        "amount": 459.96, 
        "created_at": "2024-12-31T10:38:12.465986-03:00"
    }
```

## Documentação

Veja a documentação completa para obter mais detalhes de como usar este pacote clicando [nesse link.](https://payment-emulation.readthedocs.io/latest/)
