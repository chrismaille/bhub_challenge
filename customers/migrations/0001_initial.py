# Generated by Django 4.0.5 on 2022-06-09 22:18

import uuid

import django.contrib.postgres.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import core.helpers.validators.tax_id


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(null=True)),
                ("deleted_at", models.DateTimeField(null=True)),
                (
                    "tax_id",
                    models.CharField(
                        max_length=20,
                        unique=True,
                        validators=[core.helpers.validators.tax_id.validate_tax_id],
                    ),
                ),
                ("first_name", models.CharField(max_length=255)),
                ("last_name", models.CharField(max_length=255)),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("MALE", "Male"),
                            ("FEMALE", "Female"),
                            ("OTHER", "Other"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "personal_pronoums",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(blank=True, max_length=10),
                        size=None,
                    ),
                ),
                (
                    "declared_income",
                    models.DecimalField(decimal_places=2, max_digits=20),
                ),
                ("declared_income_currency", models.CharField(max_length=3)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("cell_phone", models.CharField(max_length=20)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("ACTIVE", "Active"),
                            ("BLOCKED", "Blocked"),
                            ("DELETED", "Deleted"),
                        ],
                        default="ACTIVE",
                        max_length=20,
                    ),
                ),
                ("blocked_reason", models.TextField(null=True)),
                ("payload", models.JSONField(null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="%(app_label)s_%(class)ss_created_by",
                        related_query_name="%(app_label)s_%(class)s_created_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="%(app_label)s_%(class)ss_deleted_by",
                        related_query_name="%(app_label)s_%(class)s_deleted_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="%(app_label)s_%(class)ss_updated_by",
                        related_query_name="%(app_label)s_%(class)s_updated_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Customer",
                "db_table": "customer",
            },
        ),
    ]
