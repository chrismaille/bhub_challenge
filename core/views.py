import arrow
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
    throttle_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from core.serializers import (
    HealthCheckReadinessSerializer,
    HealthCheckResponseSerializer,
)
from core.settings import ENV, PROJECT_NAME
from core.tools.throttle import AnonThrottle


@require_http_methods(["GET", "OPTIONS"])
@extend_schema(
    summary=_("Container is responding?"),
    description=_("Returns a simple health check."),
    responses={200: HealthCheckResponseSerializer},
    tags=["health"],
)
@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def health_check(request: Request) -> Response:
    """
    Health-Check endpoint.
    Answers: Application is responding?
    Will check: Container is running.

    :returns: HealthCheck.
    """
    from core import __version__

    payload = {
        "service": f"{PROJECT_NAME} ({ENV})",
        "version": __version__,
        "status": "OK",
        "time": arrow.utcnow().isoformat(),
    }
    return Response(payload)


@require_http_methods(["GET", "OPTIONS"])
@extend_schema(
    summary=_("Application is Ready?"),
    description=_("Returns a readiness health check. Cannot be throttled."),
    responses={200: HealthCheckReadinessSerializer},
    tags=["health"],
)
@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([AnonThrottle])
def health_check_readiness(request: Request) -> Response:
    """
    Health-Check Liveness endpoint.
    Answers: Application is ready?
    Will check: Container is running and has database connection.

    :returns: HealthCheck.
    """
    from core import __version__

    user_count = User.objects.count()  # check database
    payload = {
        "service": f"{PROJECT_NAME} ({ENV})",
        "version": __version__,
        "status": "OK",
        "database": f"OK ({user_count})",
        "time": arrow.utcnow().isoformat(),
    }
    return Response(payload)
