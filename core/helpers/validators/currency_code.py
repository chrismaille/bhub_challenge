from django.core.exceptions import ValidationError
from iso4217 import Currency


def validate_currency_code(value: str):
    if value not in [currency.code for currency in Currency]:
        raise ValidationError("Invalid currency code.")
    return value
