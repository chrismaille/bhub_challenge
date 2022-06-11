from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from validate_docbr import CPF


def validate_tax_id(value: str):
    """Validate CPF numbers."""
    cnpj = CPF()
    if not cnpj.validate(value):
        raise ValidationError(_("CPF number is not valid."))
    return value
