import uuid

from django.contrib.auth.models import User
from django.db import models

RELATED_QUERY_NAME_STRING = "%(app_label)s_%(class)s_{}"
RELATED_NAME_STRING = "%(app_label)s_%(class)ss_{}"


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name=RELATED_NAME_STRING.format("created_by"),
        related_query_name=RELATED_QUERY_NAME_STRING.format("created_by"),
    )
    updated_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name=RELATED_NAME_STRING.format("updated_by"),
        related_query_name=RELATED_QUERY_NAME_STRING.format("updated_by"),
    )
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)
    deleted_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name=RELATED_NAME_STRING.format("deleted_by"),
        related_query_name=RELATED_QUERY_NAME_STRING.format("deleted_by"),
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        abstract = True
