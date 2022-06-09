from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.helpers.validate_tax_id import validate_tax_id
from core.models import BaseModel


class Customer(BaseModel):
    class Gender(models.TextChoices):
        MALE = "MALE"
        FEMALE = "FEMALE"
        OTHER = "OTHER"

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE"
        BLOCKED = "BLOCKED"
        DELETED = "DELETED"

    # Personal Data
    tax_id = models.CharField(max_length=20, validators=[validate_tax_id], unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=20, choices=Gender.choices)
    personal_pronoums = ArrayField(models.CharField(max_length=10, blank=True))

    # Income Info
    declared_income = models.DecimalField(max_digits=20, decimal_places=2)
    declared_income_currency = models.CharField(max_length=3)

    # Contact Info
    email = models.EmailField(unique=True)
    cell_phone = models.CharField(max_length=20)

    # Domain data
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    blocked_reason = models.TextField(null=True)
    payload = models.JSONField(null=True)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _("Customer")
        db_table = "customer"
