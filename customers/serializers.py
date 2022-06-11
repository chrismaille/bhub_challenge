from django.shortcuts import get_object_or_404
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from customers.models.address import Address
from customers.models.bank import Bank
from customers.models.customer import Customer
from customers.models.customer_account import CustomerAccount
from customers.models.customer_address import CustomerAddress


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = [
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "deleted_by",
            "payload",
            "deleted",
            "blocked_by",
        ]
        extra_kwargs = {
            "status": {"read_only": True},
            "id": {"read_only": True},
            "blocked_reason": {"read_only": True},
        }


class BlockUserSerializer(serializers.Serializer):
    reason = serializers.CharField(required=True)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        read_only_fields = ["id", "active"]
        exclude = [
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "deleted_by",
            "deleted",
        ]


class CustomerAddressSerializer(WritableNestedModelSerializer):
    address = AddressSerializer()

    def validate(self, data: dict):
        customer_id = self.context["view"].kwargs["customer_id"]
        data["customer"] = get_object_or_404(Customer, id=customer_id)
        return data

    class Meta:
        model = CustomerAddress
        read_only_fields = ["id", "active"]
        exclude = [
            "customer",
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "deleted_by",
            "deleted",
        ]


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        read_only_fields = ["id", "active"]
        exclude = [
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "deleted_by",
            "deleted",
        ]


class CustomerAccountSerializer(WritableNestedModelSerializer):
    bank = BankSerializer()

    def validate(self, data: dict):
        customer_id = self.context["view"].kwargs["customer_id"]
        data["customer"] = get_object_or_404(Customer, id=customer_id)

        # Check for CreditCard
        if data["payment_type"] == CustomerAccount.PaymentType.CREDIT_CARD:
            if not data["token_id"]:
                raise serializers.ValidationError(
                    "Payment Token is required for creditcard method.",
                )

        # Check for PIX
        if data["payment_type"] == CustomerAccount.PaymentType.PIX:
            if not data["direct_transfer_id"]:
                raise serializers.ValidationError(
                    "PIX Identifier is required for PIX method.",
                )

        # Check for Bank Transfer
        if data["payment_type"] == CustomerAccount.PaymentType.BANK_TRANSFER:
            if not data["bank"] or not data["bank_branch"] or not data["bank_account"]:
                raise serializers.ValidationError(
                    "Bank Info is required for bank transfer method.",
                )

        return data

    class Meta:
        model = CustomerAccount
        read_only_fields = ["id", "active"]
        exclude = [
            "customer",
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "deleted_by",
            "deleted",
        ]
