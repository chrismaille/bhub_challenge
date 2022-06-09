import os

from django.apps import AppConfig
from django.db import ProgrammingError
from loguru import logger

from core import settings


class CustomersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "customers"

    def ready(self):
        try:
            self.update_site_domain()
            self.create_local_super_user()
        except ProgrammingError:
            logger.debug("Error while bootstrapping server. Database was migrated?")

    @staticmethod
    def update_site_domain():
        from django.contrib.sites.models import Site

        current_site = Site.objects.get_current()
        logger.info(f"Site domain is: {current_site.domain}")
        if current_site.domain != settings.CURRENT_SITE_DOMAIN:
            current_site.domain = settings.CURRENT_SITE_DOMAIN
            current_site.name = settings.CURRENT_SITE_DOMAIN
            logger.warning(
                f"Site domain has been changed to: {settings.CURRENT_SITE_DOMAIN}.",
            )
            current_site.save()

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
                    f"tech@{settings.GOOGLE_SSO_ALLOWABLE_DOMAINS[0]}",
                ),
                password=os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin"),
            )
            logger.info(f"Created superuser: {super_user.username}")
