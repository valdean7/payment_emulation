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
        
        """Generates an encrypted CVV based on the card number, expiration date
        and a secret key.

        Args:
            card_number: A sequence of digits.
            validity: A `date` of datetime  Ex: 2024-12-1.
            secret: A sequence of characters.

        Returns:
            A sequence of 3 digits.
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
    """Checks that the CVV provided matches the card number and expiration date.

    Args:
        card_number: a sequence of digits.
        validity: a date with the month and year Ex: 12/24.
        secret: a secret key chosen for encryption.
        cvv_to_verify: CVV provided for verification.

    Returns:
        A `bool`, True or False.
    """
    expected_cvv = generate_cvv(card_number, validity, secret)

    return cvv_to_verify == expected_cvv


def luhn_checksum(card_number: str) -> int:
    """Calculates the Luhn algorithm checksum to validate the card number.

    Args:
        card_number: A sequence of digits.

    Returns:
        Valid if it is zero, otherwise invalid.
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
    """Generates a valid card number based on the provided flag.
    The preconfigured flags are (Visa, Mastercard, Elo and Other).

    Args:
        flag: A name of a flag that is in the `prefixes` variable.

    Raises:
        ValueError: If the flag are not in the `prefixes`.

    Returns:
        A sequence of digits.
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
    """Generates a sequence of random numbers.

    Returns:
        A sequence of digits.
    """
    agency = f"{random.randint(1000, 9999)}{random.randint(0, 9)}"
    account = f"{random.randint(10000, 99999)}{random.randint(10, 99)}"
    account_number =  f"{agency}{account}"
    return account_number
