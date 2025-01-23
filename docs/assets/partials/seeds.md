```{.py3}
{{ vars.full_inport }}

response = PaymentSDK.get_seeds()
print(response['PROBATUS'])

expected output:
>>> {
        'account': {
            'cpf': '45230544015', 'account_holder_name': 'PROBATUS',
            'account_number': '830991818343', 'balance': Decimal('99999.00'), 
            'status': 'active'
        }, 
        'card': {
            'card_holder_name': 'PROBATUS', 'card_number': '4763871810133150',
            'validity': '12/29', 'cvv': '342', 'card_flag': 'VISA
        }
    }
```
