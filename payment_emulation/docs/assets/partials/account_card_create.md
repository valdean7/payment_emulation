```{.py3}
from payment_emulation.payment.models import Account, Card
from payment_emulation.pycpfcnpj.gen import cpf

account = Account(
    cpf=cpf(), 
    account_holder_name='Jhon Doe', 
    balance=10000
)

account.save()

card = Card(
    account=account, 
    card_holder_name='Jhon Doe', 
    card_flag='VISA', 
    pin='1234'
)

card.save()
```