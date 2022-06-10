from django.utils.translation import gettext_lazy as _
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework.permissions import BasePermission

from core import settings


class ApiKeyAuthenticationScheme(OpenApiAuthenticationExtension):
    """DRF Api-Key Authentication Scheme."""

    target_class = "rest_framework_api_key.permissions.HasAPIKey"
    name = "DRF ApiKey"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
        }


class UsingAppToken(BasePermission):
    """Using Token for API Operations."""

    message = _("Use this Permission with Device only.")

    def has_permission(self, request, view):
        authorization = request.headers.get("Authorization", "")
        return (
            authorization
            and authorization.replace("Api-Key ", "") == settings.SECRET_TOKEN
        )


class AppTokenAuthenticationScheme(OpenApiAuthenticationExtension):
    """App Token Authentication Scheme."""

    target_class = "core.tools.auth.UsingAppToken"
    name = "Using App Token"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
        }
