```{.py3 hl_lines="9-19"}
{{ vars.full_inport }}

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
