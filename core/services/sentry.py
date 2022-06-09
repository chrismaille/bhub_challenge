import os

import sentry_sdk
import toml
from loguru import logger
from sentry_sdk.integrations.boto3 import Boto3Integration
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration

from core import __version__


def configure_sentry():
    """Configuring Sentry SDK.

    Do not use Stela on this module, to allow Sentry load before it

    As per https://docs.sentry.io/platforms/python/guides/django/
    """
    pyproject_data = toml.load("pyproject.toml")
    environment = os.getenv("ENV")
    sentry_dsn = os.getenv(
        "PROJECT_SENTRY_DSN",
        pyproject_data["environment"]
        .get(environment, {})
        .get("project", {})
        .get("sentry_dsn", pyproject_data["environment"]["project"].get("sentry_dsn")),
    )
    project_type = os.getenv(
        "PROJECT_SERVICE_TYPE",
        pyproject_data["environment"]
        .get(environment, {})
        .get("project", {})
        .get(
            "service_type",
            pyproject_data["environment"]["project"].get("service_type"),
        ),
    )

    if sentry_dsn and sentry_dsn != "":
        integrations = [DjangoIntegration]
        if project_type in ["api", "worker"]:
            integrations += [Boto3Integration]
        if project_type in ["worker", "beat", "flower"]:
            integrations += [CeleryIntegration]
        sentry_sdk.init(
            dsn=sentry_dsn,
            integrations=[integration() for integration in integrations],
            environment=environment,
            release=__version__,
        )
        logger.info(f"Sentry Initialized. Environment is: {environment}")
