## Sobre os modelos Account e Card

### Modelo Account

O modelo `Account` é responsável por representar uma conta bancária. 
Ele armazena informações essenciais como a identificação do titular (através do CPF ou CNPJ), 
nome do titular, número da conta, saldo e status da conta (ativo, inativo ou bloqueado).

??? Quote "Source code in <code>payment_emulation\payment\models.py</code>" 
    
    ```{.python linenums="1"}
    from django.core.exceptions import ValidationError
    from django.contrib.auth import hashers
    from pycpfcnpj import cpf, cnpj
    from django.conf import settings
    from datetime import date, timedelta
    from payment_emulation.utils import generators
    from django.db import models
    import re


    class Account(models.Model):
        status_choices = [('AC', 'active'), ('IN', 'inactive'), ('BL', 'blocked')]

        cpf = models.CharField(
            max_length=11, blank=True,null=True, unique=True, verbose_name='CPF'
        )
        cnpj = models.CharField(
            max_length=14, blank=True,null=True, unique=True, verbose_name='CNPJ'
        )
        account_holder_name = models.CharField(max_length=100)
        account_number = models.CharField(
            max_length=20, unique=True, null=True, blank=True
        )
        balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
        status = models.CharField(
            max_length=2, choices=status_choices, default='AC'
        )
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)


        def __str__(self) -> str:
            return self.account_holder_name
        

        @classmethod
        def generate_account_number(cls) -> str:
            account_number =  generators.generate_account_number()

            if cls.objects.filter(account_number=account_number).exists():
                return cls.generate_account_number()
            return account_number
        

        def save(self, *args, **kwargs):
            self.full_clean()
            self.account_holder_name = self.account_holder_name.upper()

            if not self.account_number:
                self.account_number = self.generate_account_number()

            return super().save(*args, **kwargs)
        

        def clean(self):
            super().clean()
            if (self.cpf and self.cnpj) or (not self.cpf and not self.cnpj):
                raise ValidationError('Provide only CPF or CNPJ.')
            if self.cpf:
                if not cpf.validate(self.cpf):
                    raise ValidationError(
                        {'cpf': 'The `cpf` provided is not valid.'}
                    )
            if self.cnpj:
                if not cnpj.validate(self.cnpj):
                    raise ValidationError(
                        {'cnpj': 'The `cnpj` provided is not valid.'}
                    )
            
            if self.account_number:
                if not self.account_number.isdigit():
                    raise ValidationError(
                        {
                            'account_number': 
                            'The `account_number` must contain only numbers.'
                        }
                    )
            
            if not re.fullmatch(r'^[A-Za-z ]+$', self.account_holder_name):
                raise ValidationError(
                    {
                        'account_holder_name': 
                        'the `account_holder_name` must contain only letters.'
                    }
                )
    ```

### Campos do modelo Account

- **cpf**
    - Tipo: `CharField`
    - Máximo de caracteres: 11
    - Opções: `blank=True`, `null=True`, `unique=True`
    - Verbose name: "CPF"
    - Observação: 
        1. Não há valor padrão. 
        2. Deve ser informado ou o campo `cnpj` (mas não ambos).

- **cnpj**
    - Tipo: `CharField`
    - Máximo de caracteres: 14
    - Opções: `blank=True`, `null=True`, `unique=True`
    - Verbose name: "CNPJ"
    - Observação: 
        1. Não há valor padrão. 
        2. Assim como o `cpf`, deve ser informado de forma exclusiva.

- **account_holder_name**
    - Tipo: `CharField`
    - Máximo de caracteres: 100
    - Observação: 
        1. Não há valor padrão. 
        2. No método `#!python save()`, o valor é convertido para letras maiúsculas para padronização.

- **account_number**
    - Tipo: `CharField`
    - Máximo de caracteres: 20
    - Opções: `blank=True`, `null=True`, `unique=True`
    - Observação: 
        1. Caso não seja informado, o método `#!python save()` utiliza a função utilitária [`generate_account_number()`](utils/generators.md/#payment_emulation.utils.generators.generate_account_number){:target="_blank"} 
        para gerar um número de conta único automaticamente.

- **balance**
    - Tipo: `DecimalField`
    - Máximo de dígitos: 12
    - Casas decimais: 2
    - Valor padrão: `0.00`
    - Observação: 
        1. Se não for fornecido, o saldo inicia com o valor padrão de 0.00.

- **status**
    - Tipo: `CharField`
    - Máximo de caracteres: 2
    - Opções (choices):
        - `'AC'`: active
        - `'IN'`: inactive
        - `'BL'`: blocked
    - Valor padrão: `'AC'`
    - Observação: 
        1. Se não informado, o status será definido como "active" (`'AC'`).
    
- **created_at**
    - Tipo: `DateTimeField`
    - Opção: `auto_now_add=True`
    - Observação: 
        1. Atribui automaticamente a data e hora da criação do registro.

- **updated_at**
    - Tipo: `DateTimeField`
    - Opção: `auto_now=True`
    - Observação: 
        1. Atualiza automaticamente a data e hora sempre que o registro é salvo.

#### Comportamento do método `save()` (Account):



- Executa `#!python full_clean()` para validar os dados.
- Converte o `account_holder_name` para letras maiúsculas.
- Se o `account_number` não for informado, gera um número de conta único via função utilitária [`generate_account_number()`](utils/generators.md/#payment_emulation.utils.generators.generate_account_number){:target="_blank"}.


### Modelo Card

O modelo `Card` está vinculado a uma conta (`Account`) e representa um cartão bancário associado a essa conta. Ele gerencia informações como o titular do cartão, número do cartão, validade, código CVV, bandeira do cartão, status de ativação e o PIN.

??? Quote "Source code in <code>payment_emulation\payment\models.py</code>"
    ```{.python linenums="88"}
    class Card(models.Model):
        @staticmethod
        def create_validity():
            date_delta = date.today() + timedelta(days=5 * 365)
            return date_delta


        card_flags_choices = [
            ('VISA', 'Visa'),
            ('MC', 'MasterCard'),
            ('ELO', 'Elo'),
            ('OTHER', 'Other'),
        ]

        account = models.ForeignKey(Account, models.CASCADE)
        card_holder_name = models.CharField(max_length=50)
        card_number = models.CharField(
            max_length=16, unique=True, blank=True, null=True
        )
        validity = models.DateField(null=True, blank=True)
        cvv = models.CharField(
            max_length=4, verbose_name='CVV', blank=True, null=True
        )
        card_flag = models.CharField(max_length=5, choices=card_flags_choices)
        active = models.BooleanField(default=True)
        pin = models.CharField(max_length=255)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)


        def __str__(self) -> str:
            return self.card_holder_name


        @classmethod
        def generate_card_number(cls, flag: str) -> str:
            card_number = generators.generate_card_number(flag)

            if cls.objects.filter(card_number=card_number).exists():
                return cls.generate_card_number(flag)
            return card_number


        def save(self, *args, **kwargs):
            self.full_clean()
            self.card_holder_name = self.card_holder_name.upper()

            if not self.card_number:
                self.card_number = self.generate_card_number(
                    self.card_flag
                )

            if self.pin.isdigit():
                self.pin = hashers.make_password(self.pin)

            if not self.validity:
                self.validity = self.create_validity()

            if not self.cvv:
                self.cvv = generators.generate_cvv(
                    self.card_number, self.validity, settings.SECRET_KEY
                )
            
            return super().save(*args, **kwargs)


        def clean(self):
            super().clean()
            if not re.fullmatch(r'^[A-Za-z ]+$', self.card_holder_name):
                raise ValidationError(
                    {
                        'card_holder_name': 
                        'the `card_holder_name` must contain only letters.'
                    }
                )
            
            if self.pk is None:
                if not self.pin.isdigit():
                    raise ValidationError(
                        {
                            'pin': 
                            'The `pin` must contain only numbers.'
                        }
                    )
                if len(self.pin) < 4:
                    raise ValidationError(
                        {
                            'pin': 
                            'the `pin` must contain 4 or more characters.'
                        }
                    )
            
            if self.card_number:
                if not self.card_number.isdigit():
                    raise ValidationError(
                        {
                            'card_number': 
                            'The `card_number` must contain only numbers.'
                        }
                    )
            
            if self.cvv:
                if not self.cvv.isdigit():
                    raise ValidationError(
                        {
                            'cvv': 
                            'The `cvv` must contain only numbers.'
                        }
                    )



        def check_pin(self, pin: str):
            return hashers.check_password(pin, self.pin)

    ```

### Campos do modelo Card

- **account**
    - Tipo: `ForeignKey` para o modelo Account
    - Comportamento: 
        1. Relacionamento obrigatório com a conta (`Account`).
        2. Em caso de deleção da conta associada, o cartão também é removido (`on_delete=models.CASCADE`).

- **card_holder_name**
    - Tipo: `CharField`
    - Máximo de caracteres: 50
    - Observação: 
        1. Campo obrigatório. 
        2. No `#!python save()`, o nome do titular é convertido para letras maiúsculas.

- **card_number**
    - Tipo: `CharField`
    - Máximo de caracteres: 16
    - Opções: `blank=True`, `null=True`, `unique=True`
    - Observação: 
        1. Se não for informado, o método `#!python save()` utiliza a função utilitária [`generate_card_number(flag)`](utils/generators.md/#payment_emulation.utils.generators.generate_card_number){:target="_blank"} (onde `flag` é o valor de `card_flag`) para gerar um número de cartão válido e único.

- **validity**
    - Tipo: `DateField`
    - Opções: `blank=True`, `null=True`
    - Observação: 
        1. Caso não seja informado, o método `#!python save()` define sua validade utilizando o método estático `#!python create_validity()`, que retorna a data atual acrescida de 5 anos.

- **cvv**
    - Tipo: `CharField`
    - Máximo de caracteres: 4
    - Verbose name: "CVV"
    - Opções: `blank=True`, `null=True`
    - Observação: 
        1. Se não informado, durante o `#!python save()`, o CVV é gerado automaticamente via função utilitária [`generate_cvv()`](utils/generators.md/#payment_emulation.utils.generators.generate_cvv){:target="_blank"}, utilizando o `card_number`, a `validity` e uma chave secreta (`secret`).

- **card_flag**
    - Tipo: `CharField`
    - Máximo de caracteres: 5
    - Opções (choices):
        - `'VISA'`: Visa
        - `'MC'`: MasterCard
        - `'ELO'`: Elo
        - `'OTHER'`: Other
    - Observação: 
        1. Campo obrigatório, define a bandeira do cartão.
        2. Os cartões criados com a bandeira `'OTHER'` resultará em uma transação [`pending`](transactions.md/#resultado-das-transacoes){:target="_blank"}.

- **active**
    - Tipo: `BooleanField`
    - Valor padrão: `True`
    - Observação: 
        1. Indica se o cartão está ativo ou não.

- **pin**
    - Tipo: `CharField`
    - Máximo de caracteres: 255
    - Observação:
        1. Campo obrigatório.
        2. Durante a criação (quando o registro ainda não possui `pk`), o método `#!python clean()` valida que o `pin` contenha apenas dígitos e tenha, no mínimo, 4 caracteres.
        3. No `#!python save()`, se o `pin` for composto apenas de dígitos, ele é criptografado utilizando [`hashers.make_password()`](https://docs.djangoproject.com/en/5.1/topics/auth/passwords/#django.contrib.auth.hashers.make_password){:target="_blank"}.

- **created_at**
    - Tipo: `DateTimeField`
    - Opção: `auto_now_add=True`
    - Observação: 
        1. Armazena a data e hora de criação do registro automaticamente.

- **updated_at**
    - Tipo: `DateTimeField`
    - Opção: `auto_now=True`
    - Observação: 
        1. Atualiza automaticamente a data e hora sempre que o registro é salvo.

#### Comportamento do método `save()` (Card):

- Executa `#!python full_clean()` para validar os dados.
- Converte o `card_holder_name` para letras maiúsculas.
- Se o `card_number` não for informado, gera-o automaticamente via função utilitária [`generate_card_number()`](utils/generators.md/#payment_emulation.utils.generators.generate_card_number){:target="_blank"}.
- Se o `pin` for composto apenas por dígitos, o mesmo é criptografado.
- Se a `validity` não for informada, é a data atual mais 5 anos (via `#!python create_validity()`).
- Se o `cvv` não for informado, gera-o automaticamente utilizando a função utilitária [`generate_cvv()`](utils/generators.md/#payment_emulation.utils.generators.generate_cvv){:target="_blank"}.

## Como criar uma conta e cartão

A seguir veja um exemplo de como criar uma nova conta e cartão.  

{% include "assets/partials/account_card_create.md" %}