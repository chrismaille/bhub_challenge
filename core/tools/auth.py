import rest_framework.exceptions
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from genesis.models import Device
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission

from core import settings
from core.exceptions.device_blocked import DeviceBlocked


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
    """Using App Embedded Token for Device Operations."""

    message = _("Use this Permission with Device only.")

    def has_permission(self, request, view):
        authorization = request.headers.get("Authorization", "")
        return (
            authorization
            and authorization.replace("Api-Key ", "") == settings.SECRET_TOKEN
        )

    def has_object_permission(self, request, view, obj):
        from genesis.models import Device

        if type(obj).__name__ != Device.__name__:
            raise rest_framework.exceptions.PermissionDenied()
        return True


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


class DeviceNotBlocked(BasePermission):
    """Check for Blocked Devices."""

    def has_permission(self, request, view):
        device_id = request.data.get("device_id")
        if not device_id:
            return True
        device = Device.objects.filter(device_id=device_id).first()
        return not device or device.status != Device.Status.BLOCKED

    def has_object_permission(self, request, view, obj):
        from genesis.models import Device

        if isinstance(obj, Device) and obj.status == Device.Status.BLOCKED:
            raise DeviceBlocked()
        return True


class DeviceAuthentication(BaseAuthentication):
    def authenticate(self, request) -> tuple[None, Device] | None:
        try:
            api_key = request.headers.get("Authorization", "").replace("Api-Key ", "")
            if not api_key:
                return None
            device = Device.objects.get(
                ~Q(state=Device.Status.BLOCKED),
                api_key=api_key,
            )
            return None, device
        except Device.DoesNotExist:
            raise rest_framework.exceptions.AuthenticationFailed()


class DeviceAuthenticationScheme(OpenApiAuthenticationExtension):
    """Device Authentication Scheme."""

    target_class = "core.tools.auth.DeviceAuthentication"
    name = "Device Auth using Api-Key"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
        }
