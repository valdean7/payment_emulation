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
