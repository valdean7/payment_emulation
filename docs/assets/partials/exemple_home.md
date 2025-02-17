```{.python linenums="1" hl_lines="9-21" .copy}
{{ vars.full_inport }}


items = [
    {'id': 1, 'title': 'T-shirt', 'quantity': 3, 'unit_price': 49.99},
    {'id': 2, 'title': 'shoe', 'quantity': 1, 'unit_price': 149.99},
    {'id': 3, 'title': 'sweater', 'quantity': 2, 'unit_price': 80},
]

seeds = PaymentSDK.get_seeds()
probatus_seed = seeds['PROBATUS']
card = probatus_seed['card']

sdk = PaymentSDK(items)

response = sdk.payment(
    cpf=probatus_seed['account']['cpf'],
    card_namber=card['card_number'],
    validity=card['validity'],
    cvv=card['cvv'],
    holder=card['card_holder_name']
)

print(response)

```

```{.bash title="output:"}
{
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
