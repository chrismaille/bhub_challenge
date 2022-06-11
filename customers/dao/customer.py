from dataclasses import dataclass

import arrow
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from loguru import logger

from customers.models.customer import Customer
from customers.models.customer_account import CustomerAccount
from customers.models.customer_address import CustomerAddress
from customers.serializers import (
    CustomerAccountSerializer,
    CustomerAddressSerializer,
    CustomerSerializer,
)


@dataclass
class CustomerDAO:
    user: User

    def create_customer(
        self,
        serializer: CustomerSerializer,
        payload: dict | None,
    ) -> Customer:
        logger.info(
            f"Creating customer for Tax Id: {serializer.validated_data['tax_id']}",
        )
        return serializer.save(
            created_by=self.user,
            payload=payload,
        )

    def mark_as_deleted(self, customer: Customer):
        logger.info(f"Mark customer {customer} as deleted.")
        customer.deleted_at = arrow.utcnow().datetime
        customer.deleted_by = self.user
        customer.deleted = True
        customer.save()

    def mark_as_blocked(self, customer: Customer, reason: str) -> Customer:
        logger.info(f"Mark customer {customer} as blocked.")
        customer.blocked_reason = reason
        customer.status = Customer.Status.BLOCKED
        customer.blocked_by = self.user
        customer.save()
        return customer

    def mark_address_as_deleted(self, customer_address: CustomerAddress):
        logger.info(f"Mark customer address {customer_address} as deleted.")
        customer_address.deleted_at = arrow.utcnow().datetime
        customer_address.deleted_by = self.user
        customer_address.deleted = True
        customer_address.save()

    def create_customer_address(
        self,
        serializer: CustomerAddressSerializer,
    ) -> CustomerAddress:
        logger.info(
            f"Save customer address with zipcode "
            f"{serializer.validated_data['address']['zip_code']}",
        )
        return serializer.save(
            created_by=self.user,
        )

    def create_customer_account(
        self,
        serializer: CustomerAccountSerializer,
    ) -> CustomerAccount:
        logger.info(
            f"Save customer account type {serializer.validated_data['payment_type']}",
        )
        return serializer.save(
            created_by=self.user,
        )

    def mark_account_as_deleted(self, customer_account: CustomerAccount):
        if customer_account.active:
            raise ValidationError(
                _(
                    "Customer Account is active. "
                    "Please mark another account as active before deleting.",
                ),
            )
        logger.info(f"Mark customer account {customer_account} as deleted.")
        customer_account.deleted_at = arrow.utcnow().datetime
        customer_account.deleted_by = self.user
        customer_account.deleted = True
        customer_account.save()

    def update_customer(self, serializer) -> Customer:
        logger.info(
            f"Update customer for TaxId {serializer.instance.tax_id}",
        )
        return serializer.save(
            updated_at=arrow.utcnow().datetime,
            updated_by=self.user,
        )

    def update_customer_address(self, serializer):
        logger.info(
            f"Update customer address for customer "
            f"{serializer.instance.customer.id}",
        )
        return serializer.save(
            updated_at=arrow.utcnow().datetime,
            updated_by=self.user,
        )

    def update_customer_account(self, serializer):
        logger.info(
            f"Save customer account for customer {serializer.instance.customer.id}",
        )
        return serializer.save(
            updated_at=arrow.utcnow().datetime,
            updated_by=self.user,
        )
