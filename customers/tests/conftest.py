import pytest
from faker import Faker

from conftest import SAMPLE_BANK_DATA, get_cell_phone_number, get_zip_code
from customers.models.customer import Customer
from customers.models.customer_account import CustomerAccount
from customers.models.customer_address import CustomerAddress
from customers.serializers import (
    CustomerAccountSerializer,
    CustomerAddressSerializer,
    CustomerSerializer,
)
from customers.tests.factories.customer import CustomerFactory
from customers.tests.factories.customer_account import CustomerAccountFactory
from customers.tests.factories.customer_address import CustomerAddressFactory

# ********************************
# *                              *
# * Customer Fixtures            *
# *                              *
# ********************************


def get_customer_data() -> dict:
    faker = Faker("pt_BR")
    return {
        "tax_id": faker.cpf(),
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "gender": faker.random_element(
            elements=[choice[0] for choice in Customer.Gender.choices],
        ),
        "personal_pronoums": faker.random_elements(
            elements=["Ele, Seu", "Ela, Sua"],
            length=1,
        ),
        "declared_income": faker.pyfloat(
            right_digits=2,
            min_value=1000,
            max_value=150000,
        ),
        "declared_income_currency": "BRL",
        "email": faker.email(),
        "cell_phone": get_cell_phone_number(),
    }


@pytest.fixture
def customer_payload() -> dict:
    return get_customer_data()


@pytest.fixture
def bad_customer_payload() -> dict:
    bad_dog = get_customer_data()
    bad_dog["tax_id"] = "12345678901"
    return bad_dog


@pytest.fixture
def customer_serializer(customer_payload):
    return CustomerSerializer(data=customer_payload)


@pytest.fixture
def active_customer():
    return CustomerFactory(status=Customer.Status.ACTIVE, deleted=False)


# ********************************
# *                              *
# * Customer Address Fixtures    *
# *                              *
# ********************************


def get_address_data() -> dict:
    faker = Faker("pt_BR")
    return {
        "address": {
            "street": faker.street_name(),
            "district": faker.bairro(),
            "city": faker.city(),
            "state": faker.estado_sigla(),
            "country": faker.country_code(),
            "zip_code": get_zip_code(),
        },
        "address_type": faker.random_element(
            elements=[choice[0] for choice in CustomerAddress.AddressType.choices],
        ),
        "address_number": faker.building_number(),
        "address_complement": faker.neighborhood(),
    }


@pytest.fixture
def customer_address_payload() -> dict:
    return get_address_data()


@pytest.fixture
def bad_customer_address_payload() -> dict:
    bad_dog = get_address_data()
    bad_dog["address"]["zip_code"] = "12345678"
    return bad_dog


@pytest.fixture
def customer_address_serializer(customer_address_payload):
    return CustomerAddressSerializer(data=customer_address_payload)


@pytest.fixture
def customer_delivery_address():
    return CustomerAddressFactory(address_type=CustomerAddress.AddressType.DELIVERY)


# ********************************
# *                              *
# * Customer Account Fixtures    *
# *                              *
# ********************************


def get_account_data():
    faker = Faker("pt_BR")
    bank_code = faker.random_element(elements=SAMPLE_BANK_DATA.keys())
    payment_type = faker.random_element(
        elements=[choice[0] for choice in CustomerAccount.PaymentType.choices],
    )
    return {
        "bank": {"code": bank_code, "name": SAMPLE_BANK_DATA[bank_code]},
        "payment_type": payment_type,
        "token_id": faker.uuid4()
        if payment_type == CustomerAccount.PaymentType.CREDIT_CARD
        else None,
        "direct_transfer_id": faker.cpf()
        if payment_type == CustomerAccount.PaymentType.PIX
        else None,
        "bank_branch": faker.random_number(digits=4, fix_len=True)
        if payment_type == CustomerAccount.PaymentType.BANK_TRANSFER
        else None,
        "bank_account": f"{faker.random_number(digits=6, fix_len=True)}"
        f"-{faker.random_number(digits=1)}"
        if payment_type == CustomerAccount.PaymentType.BANK_TRANSFER
        else None,
    }


@pytest.fixture
def customer_account_payload() -> dict:
    return get_account_data()


@pytest.fixture
def bad_customer_account_payload() -> dict:
    bad_dog = get_account_data()
    del bad_dog["payment_type"]
    return bad_dog


@pytest.fixture
def customer_account_serializer(customer_account_payload):
    return CustomerAccountSerializer(data=customer_account_payload)


@pytest.fixture
def customer_bank_transfer_account():
    return CustomerAccountFactory(
        payment_type=CustomerAccount.PaymentType.BANK_TRANSFER,
    )
