
```{.py3 hl_lines="26-36"}
{{ vars.full_inport }}


items = [
    {'id': 2, 'title': 'shoe', 'quantity': 1, 'unit_price': 149.99},
    {'id': 3, 'title': 'sweater', 'quantity': 2, 'unit_price': 80},
]

redirect_urls = {
    'success': 'http://my_site/transation/success',
    'failure': 'http://my_site/transation/failure',
    'pending': 'http://my_site/transation/pending',
}

address = {
    'number': '456', 'street': 'Oak Street', 'city': 'Greenfield', 
    'state': 'CA', 'zip_code': '90210', 'country': 'USA'
}

payer = {
    'full_name': 'John Doe', 
    'email': 'johndoe@example.com', 
    'phone': '+1 (555) 123-4567'
}

sdk = PaymentSDK(items, redirect_urls, address, payer)

response = sdk.payment(
    cpf='47388464263', 
    card_number='4232303567390851', 
    validity='1/30', 
    cvv='394', 
    holder'PROBATUS'
)

print(response)

expected output:
>>> {
        "transaction": "success", 
        "items": [
            {"id": 2, "title": "shoe", "quantity": 1, "unit_price": 149.99}, 
            {"id": 3, "title": "sweater", "quantity": 2, "unit_price": 80}
        ], 
        "redirect_urls": {
            "success": "http://my_site/transation/success", 
            "failure": "http://my_site/transation/failure", 
            "pending": "http://my_site/transation/pending"
        }, 
        "address": {
            "number": "456", 
            "street": "Oak Street", 
            "city": "Greenfield", 
            "state": "CA", 
            "zip_code": "90210", 
            "country": "USA"
        }, 
        "payer": {
            "full_name": "John Doe", 
            "email": "johndoe@example.com", 
            "phone": "+1 (555) 123-4567"
        }, 
        "amount": 309.99, 
        "created_at": "2025-01-12T15:07:10.312132-03:00"
    }
```
