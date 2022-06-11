import arrow
from rest_framework import serializers


class NotAuthorizedSerializer(serializers.Serializer):
    """Status 401 Response."""

    detail = serializers.CharField(default="Not authorized")


class AuthenticationFailedSerializer(serializers.Serializer):
    """Status 403 Response."""

    detail = serializers.CharField(default="Authorization header not found")


class NotFoundSerializer(serializers.Serializer):
    """Status 404 Response."""

    detail = serializers.CharField(default="Not found.")


class BadRequestSerializer(serializers.Serializer):
    """Status 400 Response."""

    field = serializers.ListField(default=["field error validation"])


class GatewayTimeoutSerializer(serializers.Serializer):
    """Status 504 Response."""

    detail = serializers.CharField(default="Gateway Timeout")


class HealthCheckResponseSerializer(serializers.Serializer):
    """Response Ok."""

    service = serializers.CharField(default="CustomerAPI (production)")
    version = serializers.CharField(default="1.0.0")
    status = serializers.CharField(default="OK")
    time = serializers.CharField(default=arrow.utcnow().isoformat())


class HealthCheckReadinessSerializer(HealthCheckResponseSerializer):
    database = serializers.CharField(default="OK (1)")


class AdminMixin:
    readonly_fields = [
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
        "deleted_at",
        "deleted_by",
        "deleted",
    ]


DEFAULT_RESPONSES = {
    401: AuthenticationFailedSerializer,
    403: NotAuthorizedSerializer,
    504: GatewayTimeoutSerializer,
}
