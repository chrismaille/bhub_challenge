from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from core.helpers.validators.zip_code import validate_zip_code
from core.models import BaseModel


class Address(BaseModel):
    street = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = CountryField()
    zip_code = models.CharField(max_length=10, validators=[validate_zip_code])
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.street} - {self.district}/{self.city} ({self.country.name})"

    class Meta:
        verbose_name = _("Address")
        db_table = "address"
        ordering = ["created_at"]
