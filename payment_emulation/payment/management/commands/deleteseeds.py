from django.core.management import BaseCommand
from payment_emulation.payment.models import Account


SEEDS_NAME = ['PROBATUS', 'REPROBI', 'PENDENTE']


class Command(BaseCommand):
    help = 'Delete seeds in the `Account` and `Card` models.'


    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            '--name',
            default='all', 
            type=str, 
            help='Name of the seed: PROBATUS | REPROBI | PENDENTE'
        )


    def handle(self, *args, **options):
        name = options.get('name')

        if name != 'all':
            if seed := Account.objects.filter(
                account_holder_name=name.upper()).first():
                try:
                    seed.delete()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'The seed named `{name.upper()}` was successfully'
                            f' deleted.' 
                        )
                    )
                except Exception as error:
                    self.stdout.write(self.style.ERROR(error.args[0]))
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'The seed with the given name `{name}` was not found.'
                    )
                )
        else:
            deleted_seeds = []
            for seed in SEEDS_NAME:
                try:
                    seed_object = Account.objects.filter(
                        account_holder_name=seed).first()
                    if seed_object:
                        seed_object.delete()
                        deleted_seeds.append(seed)
                except Exception as error:
                    self.stdout.write(
                        self.style.ERROR(f'{seed}: {error.args[0]}')
                    )
            if deleted_seeds:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'{", ".join(map(lambda x: f"`{x}`", deleted_seeds))} '
                        f'seeds were successfully deleted.'
                    )
                )
