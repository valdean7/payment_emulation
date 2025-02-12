# Generated by Django 5.1.5 on 2025-01-17 00:47

from django.db import migrations
from django.apps.registry import Apps
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from datetime import timedelta
from django.utils.timezone import now
from django.conf import settings
from django.contrib.auth import hashers
from payment_emulation.utils import generators


SEEDS = [
    [
        {
            'cpf': '45230544015',
            'account_holder_name': 'PROBATUS',
            'balance': 99999,
        },
        {
            'card_holder_name': 'PROBATUS',
            'card_flag': 'VISA',
            'pin': '1234' 
        }
    ],
    [
        {
            'cpf': '52112067036',
            'account_holder_name': 'REPROBI',
            'balance': 0,
        },
        {
            'card_holder_name': 'REPROBI',
            'card_flag': 'ELO',
            'pin': '1234' 
        }
    ],
    [
        {
            'cpf': '98086977048',
            'account_holder_name': 'PENDENTE',
            'balance': 99999,
        },
        {
            'card_holder_name': 'PENDENTE',
            'card_flag': 'OTHER',
            'pin': '1234',
            
        }
    ],
]


def create_validity():
    row_data = now() + timedelta(days=5 *365)
    data = row_data.date()
    return data


def insert_seeds(apps: Apps, schema_editor: BaseDatabaseSchemaEditor):
    Account = apps.get_model('payment', 'Account')
    Card = apps.get_model('payment', 'Card')

    def generate_account_number() -> str:
        account_number =  generators.generate_account_number()

        if Account.objects.filter(account_number=account_number).exists():
            return generate_account_number() # pragma: no cover
        return account_number


    def generate_card_number(flag: str) -> str:
        card_number = generators.generate_card_number(flag)

        if Card.objects.filter(card_number=card_number).exists():
            return generate_card_number(flag) # pragma: no cover
        return card_number

    secret_key: str = settings.SECRET_KEY

    for seed in SEEDS:
        date = create_validity()
        random_number = generate_card_number(seed[1]['card_flag'])
        cvv = generators.generate_cvv(random_number, date,secret_key)

        account = Account.objects.create(
            cpf=seed[0]['cpf'],
            account_holder_name=seed[0]['account_holder_name'],
            account_number=generate_account_number(),
            balance=seed[0]['balance']
        )

        Card.objects.create(
            account=account,
            card_holder_name=seed[1]['card_holder_name'],
            card_number=random_number,
            card_flag=seed[1]['card_flag'],
            pin=hashers.make_password(seed[1]['pin']),
            validity=date,
            cvv=cvv
        )


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_seeds),
    ]
