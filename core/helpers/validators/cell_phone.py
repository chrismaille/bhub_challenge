import re

from django.core.exceptions import ValidationError

BRAZILIAN_CELL_PHONE_REGEX = r"\+(\d{2})(\d{2})\s([6-9]\d{4}\-\d{4})"


def validate_cell_phone(value: str):
    """Validate cellphone number."""
    if not re.match(BRAZILIAN_CELL_PHONE_REGEX, value):
        raise ValidationError("invalid brazilian cellphone format: +9999 99999-9999")
    return value
