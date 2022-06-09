from asgiref.sync import async_to_sync
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel
from customers.models.bank import Bank
from customers.models.customer import Customer


class CustomerAccount(BaseModel):
    class PaymentType(models.TextChoices):
        PIX = "PIX"
        CREDIT_CARD = "CREDIT_CARD"
        BANK_TRANSFER = "BANK_TRANSFER"

    payment_type = models.CharField(max_length=255, choices=PaymentType.choices)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    # CreditCard/PIX Info

    # We cannot save CreditCard data in the database,
    # unless we are PCI-compliant,
    # so we will save the Unique Token from our
    # PCI-compliant payment gateway
    token_id = models.UUIDField(null=True)

    # Bank Transfer info

    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, null=True)
    bank_branch = models.CharField(max_length=255, null=True)
    bank_account = models.CharField(max_length=255, null=True)

    def update_active_method(self):
        if self.active:
            self.objects.filter(active=True, customer=self.customer).exclude(
                id=self.id,
            ).update(active=False)

    class Meta:
        verbose_name = _("Customer Account")
        db_table = "customer_account"


@receiver(post_save, sender=CustomerAccount)
def check_active_payment_method(sender, instance: CustomerAccount, *args, **kwargs):
    async_to_sync(instance.update_active_method)()
