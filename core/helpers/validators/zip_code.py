import re

from django.core.exceptions import ValidationError

BRAZILIAN_ZIP_CODE_REGEX = r"(\d{5})-(\d{3})"


def validate_zip_code(value: str):
    """Validate zip code."""
    if not re.match(BRAZILIAN_ZIP_CODE_REGEX, value):
        raise ValidationError("invalid brazilian zip code format")
    return value
