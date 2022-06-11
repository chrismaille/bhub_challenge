# Register your models here.
from django.contrib import admin

from core.serializers import AdminMixin
from customers.models.address import Address
from customers.models.bank import Bank
from customers.models.customer import Customer
from customers.models.customer_account import CustomerAccount
from customers.models.customer_address import CustomerAddress


@admin.register(Customer)
class CustomerAdmin(AdminMixin, admin.ModelAdmin):
    list_display = ("id", "full_name", "email", "created_at", "status")
    search_fields = [
        "id",
        "tax_id",
        "email",
    ]
    list_filter = ["deleted"]
    readonly_fields = AdminMixin.readonly_fields + ["payload"]


@admin.register(Address)
class AddressAdmin(AdminMixin, admin.ModelAdmin):
    list_display = ("id", "street", "district", "city", "country")
    search_fields = [
        "zip_code",
    ]


@admin.register(Bank)
class BankAdmin(AdminMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "code",
    )
    search_fields = [
        "code",
    ]


@admin.register(CustomerAddress)
class CustomerAddressAdmin(AdminMixin, admin.ModelAdmin):
    list_display = (
        "customer",
        "address",
        "address_type",
        "address_number",
        "address_complement",
    )
    search_fields = [
        "address__zip_code",
    ]


@admin.register(CustomerAccount)
class CustomerAccountAdmin(AdminMixin, admin.ModelAdmin):
    def tax_id(self, obj: CustomerAccount):
        return obj.customer.tax_id

    list_display = ("tax_id", "payment_type", "active")
    search_fields = [
        "customer__tax_id",
    ]
