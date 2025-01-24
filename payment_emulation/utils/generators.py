import random
import hmac
import hashlib
from datetime import date


prefixes = {
        "VISA": ["4"],
        "MC": ["51", "52", "53", "54", "55", "2221", "2720"],
        "OTHER": ["00", "0000", "0001"],
        "ELO": [
            "4011", "4312", "4389", "4514", "4576", "5041", "5066", "5090",
            "6277", "6362"
        ]
    }


def generate_cvv(card_number: str, validity: date, secret: str) -> str:
    """Gera um CVV criptografado com base no número do cartão, data de validade 
        e uma chave secreta.

        Args:
            card_number: Uma sequência de dígitos.
            validity: Uma data do tipo `date`. Ex: 2024-12-1.
            secret: Uma sequência de caracteres.

        Returns:
            Uma sequência de 3 dígitos.
    """

    data = f"{card_number}-{validity.month}/{str(validity.year)[2:]}"

    hmac_generator = hmac.new(
        secret.encode(), data.encode(), hashlib.sha256
    )

    hash_hex = hmac_generator.hexdigest()

    cvv = ''.join(filter(str.isdigit, hash_hex))[:3]

    return cvv


def verify_cvv(card_number: str, validity: str, secret: str,
                cvv_to_verify: str) -> bool:
    """Verifica se o CVV fornecido corresponde ao número do cartão e à data de validade.

    Args:
        card_number: uma sequência de dígitos.
        validity: uma data com o mês e o ano. Ex: 12/24.
        secret: uma chave secreta escolhida para criptografia.
        cvv_to_verify: CVV fornecido para verificação.

    Returns:
        Um `bool`, True ou False.
    """
    expected_cvv = generate_cvv(card_number, validity, secret)

    return cvv_to_verify == expected_cvv


def luhn_checksum(card_number: str) -> int:
    """Calcula a soma de verificação do algoritmo de Luhn para validar o número do cartão.

    Args:
        card_number: Uma sequência de dígitos.

    Returns:
        Válido se for zero, caso contrário, inválido.
    """
    def digits_of(n):
        return [int(d) for d in str(n)]

    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10

def generate_card_number(flag: str) -> str:
    """Gera um número de cartão válido com base na flag fornecida.
    As flags preconfiguradas são (Visa, Mastercard, Elo e Other).

    Args:
        flag: O nome de uma flag que está na variável `prefixes`.

    Raises:
        ValueError: Se a flag não estiver nos `prefixes`.

    Returns:
        Uma sequência de dígitos.
    """

    if flag.upper() not in prefixes:
        raise ValueError(
            "Flag not supported."
        )

    prefix = random.choice(prefixes[flag])

    total_length = 16

    initial_number = prefix + ''.join(str(random.randint(0, 9)) for _ in range(total_length - len(prefix) - 1))

    for final_digit in range(10):
        full_number = initial_number + str(final_digit)
        if luhn_checksum(full_number) == 0:
            return full_number


def generate_account_number() -> str:
    """Gera uma sequência de números aleatórios.

    Returns:
        Uma sequência de dígitos.
    """
    agency = f"{random.randint(1000, 9999)}{random.randint(0, 9)}"
    account = f"{random.randint(10000, 99999)}{random.randint(10, 99)}"
    account_number =  f"{agency}{account}"
    return account_number
