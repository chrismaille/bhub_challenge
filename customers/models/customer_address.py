from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel
from customers.models.address import Address
from customers.models.customer import Customer


class CustomerAddress(BaseModel):
    class AddressType(models.TextChoices):
        BILLING = "BILLING"
        DELIVERY = "DELIVERY"

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    address_type = models.CharField(max_length=20, choices=AddressType.choices)
    address_number = models.CharField(max_length=255)
    address_complement = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name = _("Customer Address")
        db_table = "customer_address"
