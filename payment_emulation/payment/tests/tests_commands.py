from django.test import TestCase
from django.core.management import call_command
from io import StringIO
from payment.models import Account # type: ignore
import re
from decimal import Decimal


class TestCommand(TestCase):
    def setUp(self):
        def re_string(out: StringIO):
            stdout_string = re.sub(r'\x1b\[.*?m', '', out.getvalue())
            return stdout_string
        
        self.stdout_string = re_string


    def test_should_delete_all_seeds(self):
        out = StringIO()
        call_command('deleteseeds', stdout=out)
        self.assertEqual(
        '`PROBATUS`, `REPROBI`, `PENDENTE` seeds were successfully deleted.\n',
        self.stdout_string(out)
        )


    def test_should_delete_just_one_seed_with_flag_name(self):
        test_list = [
            (
                'probatus', 
                'The seed named `PROBATUS` was successfully deleted.\n'
            ),
            (
                'reprobi', 
                'The seed named `REPROBI` was successfully deleted.\n'
            ),
            (
                'pendente', 
                'The seed named `PENDENTE` was successfully deleted.\n'
            )
        ]

        for value, expect in test_list:
            with self.subTest(value=value, expect=expect):
                out = StringIO()
                call_command('deleteseeds', '--name', value, stdout=out)
                self.assertIn(expect, self.stdout_string(out))


    def test_should_not_delete_the_seed_if_the_name_gived_is_wrong(self):
        out = StringIO()
        name = 'test'
        call_command('deleteseeds', '--name', name, stdout=out)
        self.assertEqual(
        f'The seed with the given name `{name}` was not found.\n',
        self.stdout_string(out)
        )


    def test_should_not_delete_if_the_seed_do_not_exists(self):
        Account.objects.all().delete()
        out = StringIO()
        call_command('deleteseeds', stdout=out)
        self.assertEqual('', self.stdout_string(out))


    def test_should_create_seeds(self):
        Account.objects.all().delete()
        out = StringIO()
        call_command('createseeds', stdout=out)
        self.assertEqual(
        '`PROBATUS`, `REPROBI`, `PENDENTE` seeds were successfully created.\n',
        self.stdout_string(out)
        )


    def test_should_not_create_seeds_if_they_are_already_created(self):
        out = StringIO()
        call_command('createseeds', stdout=out)
        self.assertEqual('', self.stdout_string(out))


    def test_should_create_just_one_seed_if_the_other_exists(self):
        seeds = [
            ('PROBATUS', '`PROBATUS` seeds were successfully created.\n'),
            ('REPROBI', '`REPROBI` seeds were successfully created.\n'),
            ('PENDENTE', '`PENDENTE` seeds were successfully created.\n'),
        ]

        for value, expect in seeds:
            with self.subTest(value=value, expect=expect):
                Account.objects.get(account_holder_name=value).delete()
                out = StringIO()
                call_command('createseeds', stdout=out)
                self.assertEqual(expect, self.stdout_string(out))


    def test_should_set_the_balance_with_a_default_value(self):
        account = Account.objects.get(account_holder_name='PROBATUS')
        account.balance = Decimal(str(0))
        out = StringIO()
        call_command('setbalance', stdout=out)
        self.assertEqual(
            'The balance was set to 99999.\n', 
            self.stdout_string(out)
        )


    def test_should_set_the_balance_with_a_give_value(self):
        account = Account.objects.get(account_holder_name='PROBATUS')
        account.balance = Decimal(str(0))
        out = StringIO()
        call_command('setbalance', '-b', '1000', stdout=out)
        self.assertEqual(
            'The balance was set to 1000.\n', 
            self.stdout_string(out)
        )


    def test_should_not_set_the_balance_if_seed_do_not_exists(self):
            account = Account.objects.get(account_holder_name='PROBATUS')
            account.delete()
            out = StringIO()
            call_command('setbalance', stdout=out)
            self.assertEqual(
                'The `PROBATUS` seed was not created.\n', 
                self.stdout_string(out)
            )
