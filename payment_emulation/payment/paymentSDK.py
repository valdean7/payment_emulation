from django.utils.timezone import now, localtime
from decimal import Decimal, ROUND_HALF_UP
from .models import Card
import json


class PaymentSDK():
    RESPONSE = {
        'transaction': None,
        'items': [],
        'redirect_urls': None,
        'address': None,
        'payer': None
    }

    TRANSACTION = ['success', 'failure', 'pending']


    def __init__(
        self, 
        items: list[dict[str, str | int | float]], 
        redirect_urls: dict | None = None,
        address: dict | None = None, 
        payer: dict | None = None,
        **extra
        ):
        """_summary_

        Args:
            items: A list containing one or more dict of items.
            redirect_urls: A dict containing redirect urls for each type of transaction.
            address: A dict containing the payer's address.
            payer: A dict containing the payer's data.
        """
        self._validate_items(items)
        self.items = items
        self.redirect_urls = redirect_urls
        self.address = address
        self.payer = payer
        self.extra = extra

        self._set_response()


    def card_credentials(self, cpf: str, card_number: str, 
        validity: str, cvv: str, holder: str) -> Card | None:
        """Will return a `Card` object if the credentials are 
        valid, otherwise `None`.

        Args:
            cpf: A valid CPF of the holder.
            card_number: A sequence of digits (max: 16).
            validity: A date with the month and year Ex: 12/24.
            cvv: A sequence of 3 digits.
            holder: the registered name of the holder.

        Returns:
            A `Card` object or `None`.  
        """
        error_count = 0

        card = Card.objects.filter(card_number=card_number.strip()).first()
        if card is None: return
        if not card.active: return
        if card.account.status == 'BL': return

        if card.account.cpf != cpf.strip(): 
            error_count +=1

        if card.cvv != cvv.strip(): error_count += 1

        if str(card.validity.year)[2:] != validity.strip().split('/')[1]: 
            error_count += 1

        if str(card.validity.month) != validity.strip().split('/')[0]: 
            error_count += 1

        if card.card_holder_name != holder.strip().upper(): error_count += 1

        if error_count == 0:
            return card
        else: return 


    def get_items_total_value(self) -> Decimal:
        """Takes all items, multiplies the quantity by the unit price, and
        returns a value in `Decimal`.

        Returns:
            A `Decimal` value.
        """
        value = 0
        for item in self.items:
            value += int(item['quantity']) * float(item['unit_price'])

        decimal_value = Decimal(str(value))
        total_value = decimal_value.quantize(
                Decimal('0.01'),
                rounding=ROUND_HALF_UP
            )

        return total_value


    def _validate_items(self, items: list[dict]) -> None:
        """Checks if the dictionaries contained in the list have the keys
        `quantity` and `unit_price`.

        Args:
            items: A list passed in the class initializer.

        Raises:
            KeyError: If the required keys `quantity` and `unit_price` are not passed.
        """
        missing_keys = []
        for item in items:
            if item.get('quantity') is None:
                missing_keys.append('quantity')

            if item.get('unit_price') is None:
                missing_keys.append('unit_price')

        if len(missing_keys) > 0:
            raise KeyError(
                f'The required {f'key' if len(missing_keys) == 1 else f'keys'}' 
                f' {', '.join(map(lambda x: f'`{x}`', missing_keys))} is'
                f' missing in the dict passed in the `items` parameter.'
            )


    def _set_response(self) -> None:
        """Defines the response with the parameters passed in the class
        initializer.
        """
        self.RESPONSE['items'] = self.items
        self.RESPONSE['redirect_urls'] = self.redirect_urls
        self.RESPONSE['payer'] = self.payer
        self.RESPONSE['address'] = self.address
        if self.extra:
            for ex in self.extra.items():
                self.RESPONSE[ex[0]] = ex[1]


    def send_response(self, transaction: str) -> str:
        """Sends a JSON response with data about the transaction.

        Args:
            transaction: The result of the transaction (success, failure, pending).

        Raises:
            ValueError: If the transaction is not success, failure or pending.

        Returns:
            A `JSON` string.
        """
        if transaction not in self.TRANSACTION:
            raise ValueError(f'The `{transaction}` is not valid value.')
        
        self.RESPONSE['transaction'] = transaction
        if transaction == 'success':
            self.RESPONSE['amount'] = float(self.get_items_total_value())
            self.RESPONSE['created_at'] = localtime(now()).isoformat()
        return json.dumps(self.RESPONSE)


    def payment(self, cpf: str, card_number: str, 
        validity: str, cvv: str, holder: str) -> str:
        """Receives card credentials and performs a transaction.

        Args:
            cpf: A valid CPF of the holder.
            card_number (str): A sequence of digits (max: 16).
            validity (str): A date with the month and year Ex: 12/24.
            cvv (str): A sequence of 3 digits.
            holder (str): The registered name of the holder.

        Returns:
            A `JSON` string.
        """
        card = self.card_credentials(cpf, card_number, validity, cvv, holder)
        
        if card is None:
            return self.send_response(self.TRANSACTION[1])
        
        if card.card_flag == 'OTHER':
            return self.send_response(self.TRANSACTION[2])
        
        card_account_balance = Decimal(str(card.account.balance))
        items_total_value = self.get_items_total_value()

        if card_account_balance < items_total_value:
            return self.send_response(self.TRANSACTION[1])
        
        try:
            new_balane = card_account_balance - items_total_value
            card.account.balance = new_balane
            card.account.save()
        except:
            return self.send_response(self.TRANSACTION[1])
        
        return self.send_response(self.TRANSACTION[0])


    @staticmethod
    def set_seeds(instance: Card) -> dict:
        """Receives an instance of the `Card` model and transforms the values
        into a dict.

        Args:
            instance: An instance of `Card` model.

        Returns:
            A `dict` with the instance values.
        """
        return {
                'account': {
                    'cpf': instance.account.cpf,
                    'account_holder_name': instance.account.account_holder_name,
                    'account_number': instance.account.account_number,
                    'balance': instance.account.balance,
                    'status': instance.account.get_status_display(),
                },
                'card': {
                    'card_holder_name': instance.card_holder_name,
                    'card_number': instance.card_number,
                    'validity': f'{instance.validity.month}/{
                        str(instance.validity.year)[2:]}',
                    'cvv': instance.cvv,
                    'card_flag': instance.card_flag,
                }
            }


    @classmethod
    def get_seeds(cls) -> dict:
        """Return the seeds if they are created. 

        Returns:
            A `dict` with the values of the seeds.
        """
        SEEDS = {}
        if probatus := Card.objects.filter(card_holder_name='PROBATUS').first():
            SEEDS['PROBATUS'] = cls.set_seeds(probatus)

        if reprobi := Card.objects.filter(card_holder_name='REPROBI').first():
            SEEDS['REPROBI'] = cls.set_seeds(reprobi)

        if pendente := Card.objects.filter(card_holder_name='PENDENTE').first():
            SEEDS['PENDENTE'] = cls.set_seeds(pendente)

        return SEEDS
