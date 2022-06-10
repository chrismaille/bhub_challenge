from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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
        ordering = ["created_at"]

    def update_active_address(self):
        if self.active:
            CustomerAddress.objects.filter(
                active=True,
                address_type=self.address_type,
                customer=self.customer,
            ).exclude(id=self.id).update(active=False)


@receiver(post_save, sender=CustomerAddress)
def check_active_address(sender, instance: CustomerAddress, *args, **kwargs):
    instance.update_active_address()
