from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel


class Bank(BaseModel):
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name = _("Bank")
        db_table = "bank"
        ordering = ["created_at"]
