from django.utils.timezone import now, localtime
from decimal import Decimal, ROUND_HALF_UP
from .models import Card
import json


class PaymentSDK():
    RESPONSE = {
        "transaction": None,
        "items": [],
        "redirect_urls": None,
        "address": None,
        "payer": None
    }

    TRANSACTION = ["success", "failure", "pending"]


    def __init__(
        self, 
        items: list[dict[str, str | int | float]], 
        redirect_urls: dict | None = None,
        address: dict | None = None, 
        payer: dict | None = None,
        **extra
        ):
        """Recebe um lista de produtos e outros dados adicionais para criar uma
        emulação de pagamento.

        Args:
            items: Uma lista contendo um ou mais dicionários de itens.
            redirect_urls: Um dicionário contendo URLs de redirecionamento para cada tipo de transação.
            address: Um dicionário contendo o endereço do pagador.
            payer: Um dicionário contendo os dados do pagador.
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
        """Retornará um objeto `Card` se as credenciais forem 
        válidas, caso contrário, `None`.

        Args:
            cpf: Um CPF válido do titular.
            card_number: Uma sequência de dígitos (máx.: 16).
            validity: Uma data com o mês e o ano. Ex: 12/24.
            cvv: Uma sequência de 3 dígitos.
            holder: O nome registrado do titular.

        Returns:
            Um objeto `Card` ou `None`.
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
        """Recebe todos os itens, multiplica a `quantity` pelo `unit_price` e 
        retorna um valor em `Decimal`.

        Returns:
            Um valor `Decimal`.
        """
        value = 0
        for item in self.items:
            value += int(item["quantity"]) * float(item["unit_price"])

        decimal_value = Decimal(str(value))
        total_value = decimal_value.quantize(
                Decimal('0.01'),
                rounding=ROUND_HALF_UP
            )

        return total_value


    def _validate_items(self, items: list[dict]) -> None:
        """Verifica se os dicionários contidos na lista possuem as chaves 
        `quantity` e `unit_price`.

        Args:
            items: Uma lista passada no inicializador da classe.

        Raises:
            KeyError: Se as chaves obrigatórias `quantity` e `unit_price` não forem informadas.
        """
        missing_keys = []
        for item in items:
            if item.get('quantity') is None:
                missing_keys.append('quantity')

            if item.get('unit_price') is None:
                missing_keys.append('unit_price')

        if len(missing_keys) > 0:
            raise KeyError(
                f'The required {"key" if len(missing_keys) == 1 else "keys"}' 
                f' {", ".join(map(lambda x: f"`{x}`", missing_keys))} is'
                f' missing in the dict passed in the `items` parameter.'
            )


    def _set_response(self) -> None:
        """Define a resposta com os parâmetros passados no inicializador da classe.
        """
        self.RESPONSE["items"] = self.items
        self.RESPONSE["redirect_urls"] = self.redirect_urls
        self.RESPONSE["payer"] = self.payer
        self.RESPONSE["address"] = self.address
        if self.extra:
            for ex in self.extra.items():
                self.RESPONSE[ex[0]] = ex[1]


    def send_response(self, transaction: str) -> str:
        """Envia uma resposta em JSON com dados sobre a transação.

        Args:
            transaction: O resultado da transação (success, failure, pending).

        Raises:
            ValueError: Se a transação não for success, failure ou pending.

        Returns:
            Uma string em `JSON`.
        """
        if transaction not in self.TRANSACTION:
            raise ValueError(f'The `{transaction}` is not valid value.')
        
        self.RESPONSE["transaction"] = transaction
        if transaction == "success":
            self.RESPONSE["amount"] = float(self.get_items_total_value())
            self.RESPONSE["created_at"] = localtime(now()).isoformat()
        return json.dumps(self.RESPONSE)


    def payment(self, cpf: str, card_number: str, 
        validity: str, cvv: str, holder: str) -> str:
        """Recebe as credenciais do cartão e realiza uma transação.

        Args:
            cpf: Um CPF válido do titular.
            card_number (str): Uma sequência de dígitos (máx.: 16).
            validity (str): Uma data com o mês e o ano. Ex: 12/24.
            cvv (str): Uma sequência de 3 dígitos.
            holder (str): O nome registrado do titular.

        Returns:
            Uma string em `JSON`.
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
        """Recebe uma instância do modelo `Card` e transforma os valores 
        em um dicionário.

        Args:
            instance: Uma instância do modelo `Card`.

        Returns:
            Um `dict` com os valores da instância.
        """
        month = instance.validity.month
        year = str(instance.validity.year)[2:]
        return {
                "account": {
                    "cpf": instance.account.cpf,
                    "account_holder_name": instance.account.account_holder_name,
                    "account_number": instance.account.account_number,
                    "balance": instance.account.balance,
                    "status": instance.account.get_status_display(),
                },
                "card": {
                    "card_holder_name": instance.card_holder_name,
                    "card_number": instance.card_number,
                    "validity": f'{month}/{year}',
                    "cvv": instance.cvv,
                    "card_flag": instance.card_flag,
                }
            }


    @classmethod
    def get_seeds(cls) -> dict:
        """Retorna as seeds caso elas estejam criadas. 

        Returns:
            Um `dict` com os valores das seeds.
        """
        SEEDS = {}
        if probatus := Card.objects.filter(card_holder_name='PROBATUS').first():
            SEEDS["PROBATUS"] = cls.set_seeds(probatus)

        if reprobi := Card.objects.filter(card_holder_name='REPROBI').first():
            SEEDS["REPROBI"] = cls.set_seeds(reprobi)

        if pendente := Card.objects.filter(card_holder_name='PENDENTE').first():
            SEEDS["PENDENTE"] = cls.set_seeds(pendente)

        return SEEDS
