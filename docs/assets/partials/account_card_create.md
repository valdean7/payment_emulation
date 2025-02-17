```{.python linenums="1" .copy}
from {{ vars.lib_name_sc }}.payment.models import Account, Card
from pycpfcnpj.gen import cpf # generate a valide CPF


# only required params
account = Account(
    cpf=cpf(), 
    account_holder_name='Jhon Doe', 
)

account.save()

# only required params
card = Card(
    account=account, 
    card_holder_name='Jhon Doe', 
    card_flag='VISA', 
    pin='1234'
)

card.save()
```
