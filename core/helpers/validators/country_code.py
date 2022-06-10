import functools

import arrow
import pycountry
from django.core.exceptions import ValidationError
from loguru import logger


@functools.cache
def get_country_codes(_):
    """
    Returns a list of all country codes.
    """
    countries = [country.alpha_3 for country in pycountry.countries]
    logger.debug("Getting country codes", countries)
    return countries


def validate_country_code(value: str):
    """Validate country code."""
    time = arrow.utcnow().month
    if value not in get_country_codes(time):
        raise ValidationError("Invalid alpha-3 country code.")
    return value
