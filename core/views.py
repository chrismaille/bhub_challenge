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

from core.serializers import HealthCheckResponseSerializer
from core.settings import ENV, PROJECT_NAME
from core.tools.throttle import AnonThrottle


@require_http_methods(["GET", "OPTIONS"])
@extend_schema(
    summary=_("Health Check endpoint"),
    description=_("Return simple health check."),
    responses={200: HealthCheckResponseSerializer},
    tags=["health"],
)
@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([AnonThrottle])
def health_check(request: Request) -> Response:
    """Return health check.

    All text here is available when accessing /api/health in DRF Browser.

    :param request: Django Rest Framework Request object
    :return: Response
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
