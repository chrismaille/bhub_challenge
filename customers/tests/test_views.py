import pytest
from django.urls import reverse

from core import settings
from core.helpers.asyncio import async_
from customers.models.customer import Customer
from customers.tests.factories.customer import CustomerFactory

CONTENT_TYPE = "application/json"

pytestmark = [pytest.mark.django_db(transaction=True), pytest.mark.asyncio]


@pytest.mark.parametrize(
    "auth_token, test_payload, expected_status_code",
    [
        (settings.SECRET_TOKEN, pytest.lazy_fixture("customer_payload"), 201),
        ("I AM HECKERMAN", pytest.lazy_fixture("customer_payload"), 403),
        (settings.SECRET_TOKEN, pytest.lazy_fixture("bad_customer_payload"), 400),
    ],
)
async def test_create_customer_view(
    async_client,
    auth_token,
    admin_user,
    test_payload,
    expected_status_code,
):
    # Arrange
    headers = {"AUTHORIZATION": f"Api-Key {auth_token}"}

    # Act
    response = await async_client.post(
        reverse("customer-list"),
        content_type=CONTENT_TYPE,
        data=test_payload,
        **headers,
    )
    data = response.json()

    # Assert
    assert response.status_code == expected_status_code

    if response.status_code in [201]:
        assert "id" in data
    elif response.status_code in [400]:
        assert data == {"taxId": ["CPF number is not valid."]}
    else:
        assert "detail" in data


@pytest.mark.parametrize(
    "auth_token, test_payload, expected_status_code",
    [
        (settings.SECRET_TOKEN, pytest.lazy_fixture("customer_address_payload"), 201),
        ("I AM HECKERMAN", pytest.lazy_fixture("customer_address_payload"), 403),
        (
            settings.SECRET_TOKEN,
            pytest.lazy_fixture("bad_customer_address_payload"),
            400,
        ),
    ],
)
async def test_create_customer_address_view(
    async_client,
    auth_token,
    admin_user,
    test_payload,
    expected_status_code,
):
    # Arrange
    headers = {"AUTHORIZATION": f"Api-Key {auth_token}"}
    customer = await async_(CustomerFactory)(status=Customer.Status.ACTIVE)

    # Act
    response = await async_client.post(
        reverse("customer-address-list", kwargs={"customer_id": customer.id}),
        content_type=CONTENT_TYPE,
        data=test_payload,
        **headers,
    )
    data = response.json()

    # Assert
    assert response.status_code == expected_status_code

    if response.status_code in [201]:
        assert "id" in data
    elif response.status_code in [400]:
        assert data == {"address": {"zipCode": ["invalid brazilian zip code format"]}}
    else:
        assert "detail" in data


@pytest.mark.parametrize(
    "auth_token, test_payload, expected_status_code",
    [
        (settings.SECRET_TOKEN, pytest.lazy_fixture("customer_account_payload"), 201),
        ("I AM HECKERMAN", pytest.lazy_fixture("customer_account_payload"), 403),
        (
            settings.SECRET_TOKEN,
            pytest.lazy_fixture("bad_customer_account_payload"),
            400,
        ),
    ],
)
async def test_create_customer_account_view(
    async_client,
    auth_token,
    admin_user,
    test_payload,
    expected_status_code,
):
    # Arrange
    headers = {"AUTHORIZATION": f"Api-Key {auth_token}"}
    customer = await async_(CustomerFactory)(status=Customer.Status.ACTIVE)

    # Act
    response = await async_client.post(
        reverse("customer-accounts-list", kwargs={"customer_id": customer.id}),
        content_type=CONTENT_TYPE,
        data=test_payload,
        **headers,
    )
    data = response.json()

    # Assert
    assert response.status_code == expected_status_code

    if response.status_code in [201]:
        assert "id" in data
    elif response.status_code in [400]:
        assert data == {"paymentType": ["Este campo é obrigatório."]}
    else:
        assert "detail" in data
