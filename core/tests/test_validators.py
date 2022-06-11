import pytest
from django.core.exceptions import ValidationError

from core.helpers.validators.cell_phone import validate_cell_phone
from core.helpers.validators.currency_code import validate_currency_code
from core.helpers.validators.tax_id import validate_tax_id
from core.helpers.validators.zip_code import validate_zip_code


@pytest.mark.parametrize(
    "value, will_raise",
    [("11 4545-4545", True), ("94545-4545", True), ("+5511 91234-5678", False)],
)
def test_validate_cell_phone(value, will_raise):
    # Act / Assert
    if will_raise:
        with pytest.raises(ValidationError):
            validate_cell_phone(value)
    else:
        assert validate_cell_phone(value) == value


@pytest.mark.parametrize(
    "value, will_raise",
    [("R$", True), ("REAL", True), ("brl", True), ("BRL", False)],
)
def test_validate_currency_code(value, will_raise):
    # Act / Assert
    if will_raise:
        with pytest.raises(ValidationError):
            validate_currency_code(value)
    else:
        assert validate_currency_code(value) == value


@pytest.mark.parametrize(
    "value, will_raise",
    [
        ("67732967063", True),
        ("94.836.134/0001-90", True),
        ("138.715.290-44", False),
        ("67732967062", False),
    ],
    ids=["CPF with bad digit", "CNPJ", "Good formatted CPF", "Good CPF"],
)
def test_validate_tax_id(value, will_raise):
    # Act / Assert
    if will_raise:
        with pytest.raises(ValidationError):
            validate_tax_id(value)
    else:
        assert validate_tax_id(value) == value


@pytest.mark.parametrize(
    "value, will_raise",
    [("06700000", True), ("06700 000", True), ("06700-000", False)],
)
def test_validate_zip_code(value, will_raise):
    # Act / Assert
    if will_raise:
        with pytest.raises(ValidationError):
            validate_zip_code(value)
    else:
        assert validate_zip_code(value) == value
