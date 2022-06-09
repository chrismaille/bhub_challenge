import os

from django.apps import AppConfig
from loguru import logger

from core import settings


class CustomersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "customers"

    @staticmethod
    def create_local_super_user():
        from django.contrib.auth.models import User

        super_user_exists = User.objects.filter(is_superuser=True).exists()
        if settings.ENV in ["local"] and not super_user_exists:
            logger.warning("Creating local super user.")
            super_user = User.objects.create_superuser(
                username=os.getenv("DJANGO_SUPERUSER_USERNAME", "admin"),
                email=os.getenv(
                    "DJANGO_SUPERUSER_EMAIL",
                    f"tech@{settings.EMAIL_ALLOWABLE_DOMAIN}",
                ),
                password=os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin"),
            )
            logger.info(f"Created superuser: {super_user.username}")
