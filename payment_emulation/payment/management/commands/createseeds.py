from django.core.management import BaseCommand
from payment.models import Account, Card # type: ignore
from pycpfcnpj.gen import cpf
from utils import generators # type: ignore
from django.contrib.auth import hashers
from django.utils.timezone import now
from datetime import timedelta
from django.conf import settings


SEEDS = [
    [
        {
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


def generate_cpf() -> str:
    generated_cpf = cpf()
    if Account.objects.filter(cpf=generated_cpf).exists():
        return generate_cpf()
    else:
        return generated_cpf


def generate_account_number() -> str:
    account_number =  generators.generate_account_number()

    if Account.objects.filter(account_number=account_number).exists():
        return generate_account_number()
    return account_number


def generate_card_number(flag: str) -> str:
        card_number = generators.generate_card_number(flag)

        if Card.objects.filter(card_number=card_number).exists():
            return generate_card_number(flag)
        return card_number


def create_validity():
        row_data = now() + timedelta(days=5 * 365)
        data = row_data.date()
        return data


class Command(BaseCommand):
    help = 'Creates seeds in the `Account` and `Card` models.'


    def handle(self, *args, **options):
        created_seeds = []
        for seed in SEEDS:
            a_h_n = seed[0]['account_holder_name']
            if not Account.objects.filter(account_holder_name=a_h_n).exists():
                try:
                    account = Account(
                        cpf=generate_cpf(),
                        account_holder_name=a_h_n,
                        account_number=generate_account_number(),
                        balance=seed[0]['balance']
                    )
                    account.save()

                    secret_key: str = settings.SECRET_KEY
                    date = create_validity()
                    random_number = generate_card_number(
                        seed[1]['card_flag'])
                    cvv = generators.generate_cvv(
                        random_number, date, secret_key
                    )

                    card = Card(
                        account=account,
                        card_holder_name=seed[1]['card_holder_name'],
                        card_number=random_number,
                        card_flag=seed[1]['card_flag'],
                        pin=hashers.make_password(seed[1]['pin']),
                        validity=date,
                        cvv=cvv
                    )
                    card.save()
                    created_seeds.append(a_h_n)
                except Exception as error:
                    self.stdout.write(
                        self.style.ERROR(f'{a_h_n}: {error.args[0]}')
                    )

        if created_seeds:
            self.stdout.write(
                self.style.SUCCESS(
                    f'{", ".join(map(lambda x: f'`{x}`', created_seeds))} '
                    'seeds were successfully created.'
                    )
            )
