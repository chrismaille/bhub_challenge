from unittest.mock import Mock

import arrow
import pytest

from customers.dao.customer import CustomerDAO
from customers.models.customer import Customer

pytestmark = pytest.mark.django_db(transaction=True)


def test_create_customer(admin_user, customer_serializer, customer_payload):
    # Arrange
    customer_serializer.is_valid(raise_exception=True)

    # Act
    dao = CustomerDAO(admin_user)
    customer = dao.create_customer(customer_serializer, customer_payload)

    # Assert
    assert customer.created_by == admin_user


@pytest.mark.freeze_time("2022-06-10 12:00:01")
def test_mark_as_deleted(admin_user, active_customer):
    # Act
    dao = CustomerDAO(admin_user)
    dao.mark_as_deleted(active_customer)

    # Assert
    assert active_customer.deleted_by == admin_user
    assert active_customer.deleted is True
    assert active_customer.deleted_at == arrow.utcnow().datetime


@pytest.mark.freeze_time("2022-06-10 12:00:01")
def test_mark_as_blocked(admin_user, active_customer):
    # Arrange
    data = {"reason": "Test"}

    # Act
    dao = CustomerDAO(admin_user)
    customer = dao.mark_as_blocked(active_customer, data["reason"])

    # Assert
    assert customer.blocked_by == admin_user
    assert customer.blocked_reason == "Test"
    assert customer.status == Customer.Status.BLOCKED


@pytest.mark.freeze_time("2022-06-10 12:00:01")
def test_mark_address_as_deleted(admin_user, customer_delivery_address):
    # Act
    dao = CustomerDAO(admin_user)
    dao.mark_address_as_deleted(customer_delivery_address)

    # Assert
    assert customer_delivery_address.deleted_by == admin_user
    assert customer_delivery_address.deleted is True
    assert customer_delivery_address.deleted_at == arrow.utcnow().datetime


def test_create_customer_address(
    admin_user,
    customer_address_serializer,
    active_customer,
):
    # Arrange
    view_mock = Mock()
    view_mock.kwargs = {"customer_id": active_customer.id}
    customer_address_serializer.context["view"] = view_mock
    customer_address_serializer.is_valid(raise_exception=True)

    # Act
    dao = CustomerDAO(admin_user)
    customer_address = dao.create_customer_address(customer_address_serializer)

    # Assert
    assert customer_address.created_by == admin_user


def test_create_customer_account(
    admin_user,
    customer_account_serializer,
    active_customer,
):
    # Arrange
    view_mock = Mock()
    view_mock.kwargs = {"customer_id": active_customer.id}
    customer_account_serializer.context["view"] = view_mock
    customer_account_serializer.is_valid(raise_exception=True)

    # Act
    dao = CustomerDAO(admin_user)
    customer_account = dao.create_customer_account(customer_account_serializer)

    # Assert
    assert customer_account.created_by == admin_user


@pytest.mark.freeze_time("2022-06-10 12:00:01")
def test_mark_account_as_deleted(admin_user, customer_bank_transfer_account):
    # Act
    dao = CustomerDAO(admin_user)
    dao.mark_address_as_deleted(customer_bank_transfer_account)

    # Assert
    assert customer_bank_transfer_account.deleted_by == admin_user
    assert customer_bank_transfer_account.deleted is True
    assert customer_bank_transfer_account.deleted_at == arrow.utcnow().datetime
