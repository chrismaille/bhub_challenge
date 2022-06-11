import pytest
from faker import Faker

SAMPLE_BANK_DATA = {341: "ITAU", 237: "BRADESCO"}


def get_zip_code() -> str:
    faker = Faker("pt_BR")
    zip_code = faker.postcode(formatted=True)
    if "-" not in zip_code:
        return get_zip_code()
    return zip_code


def get_cell_phone_number() -> str:
    faker = Faker("pt_BR")
    number = faker.msisdn()
    return f"+{number[:4]} {number[4:9]}-{number[9:]}"


def get_tax_id() -> str:
    faker = Faker("pt_BR")
    return faker.cpf()


@pytest.fixture(scope="session", autouse=True)
def faker_session_locale():
    return ["pt_BR"]
