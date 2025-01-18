from django.core.management import BaseCommand
from payment.models import Account # type: ignore
from decimal import Decimal


class Command(BaseCommand):
    help = 'Set the balance value of PROBATUS seed.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-b', 
            '--balance', 
            type=int, 
            default=99999,
            help='An int to set the balance value.'
        )
    

    def handle(self, *args, **options):
        balance_value = options.get('balance')

        account = Account.objects.filter(account_holder_name='PROBATUS')

        if account.exists():
            try:
                old_account = account.first()
                old_account.balance = Decimal(str(balance_value))
                old_account.save()
                self.stdout.write(self.style.SUCCESS(
                    f'The balance was set to {balance_value}.')
                )
            except Exception as error:
                self.stdout.write(self.style.ERROR(error.args[0]))
        else:
            self.stdout.write(
                self.style.WARNING('The `PROBATUS` seed was not created.')
            )
