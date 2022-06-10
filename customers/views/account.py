from uuid import UUID

from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.serializers import DEFAULT_RESPONSES, BadRequestSerializer, NotFoundSerializer
from core.tools.auth import UsingAppToken
from core.tools.drf import (
    AsyncCreateModelMixin,
    AsyncDestroyModelMixin,
    AsyncListModelMixin,
    AsyncMixin,
    AsyncRetrieveModelMixin,
    AsyncUpdateModelMixin,
)
from customers.dao.customer import CustomerDAO
from customers.models.customer_account import CustomerAccount
from customers.serializers import CustomerAccountSerializer


@extend_schema(
    summary=_("Customer Account Resource"),
    description=_("Manages Customer Accounts Endpoints."),
    tags=["payment methods"],
    parameters=[
        OpenApiParameter(name="customer_id", location="path", type=UUID, required=True),
    ],
)
class CustomerAccountViewSet(
    AsyncMixin,
    AsyncCreateModelMixin,
    AsyncRetrieveModelMixin,
    AsyncUpdateModelMixin,
    AsyncDestroyModelMixin,
    AsyncListModelMixin,
    viewsets.GenericViewSet,
):
    """Customer Account ViewSet."""

    permission_classes = [UsingAppToken | IsAuthenticated]
    serializer_class = CustomerAccountSerializer
    http_method_names = ["get", "post", "head", "put", "delete", "options"]

    def get_queryset(self):
        return CustomerAccount.objects.filter(
            customer=self.kwargs["customer_id"],
            deleted=False,
        ).all()

    def _get_user(self) -> User:
        return self.request.user or User.objects.filter(is_superuser=True).first()

    @extend_schema(
        summary=_("List Customer Accounts."),
        description=_("No filter available."),
        responses={
            200: CustomerAccountSerializer,
        }
        | DEFAULT_RESPONSES,
    )
    async def list(self, request, *args, **kwargs):
        return await super().list(request, *args, **kwargs)

    @extend_schema(
        summary=_("Create new customer account."),
        description=_(
            "Will not check for duplicates, but only one account is active at time.",
        ),
        responses={
            201: CustomerAccountSerializer,
            400: BadRequestSerializer,
        }
        | DEFAULT_RESPONSES,
    )
    async def create(self, request, *args, **kwargs):
        return await super().create(request, *args, **kwargs)

    def perform_create(self, serializer: CustomerAccountSerializer):
        user = self._get_user()
        dao = CustomerDAO(user)
        dao.create_customer_account(serializer)

    @extend_schema(
        summary=_("Find Customer Account by Customer Account Id."),
        description=_("Returns a single resource."),
        responses={
            200: CustomerAccountSerializer,
            404: NotFoundSerializer,
        }
        | DEFAULT_RESPONSES,
        parameters=[
            OpenApiParameter(name="id", location="path", type=UUID, required=True),
        ],
    )
    async def retrieve(self, request, *args, **kwargs):
        return await super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary=_("Update Customer Account."),
        description=_("Update Customer Account."),
        responses={
            200: CustomerAccountSerializer,
            400: BadRequestSerializer,
            404: NotFoundSerializer,
        }
        | DEFAULT_RESPONSES,
        parameters=[
            OpenApiParameter(name="id", location="path", type=UUID, required=True),
        ],
    )
    async def update(self, request, *args, **kwargs):
        return await super().update(request, *args, **kwargs)

    @extend_schema(
        summary=_("Mark Customer Account as deleted."),
        description=_(
            "Deleted customer accounts will not show in API. "
            "Please use Django Admin to edit them.",
        ),
        responses={
            204: OpenApiResponse(description=_("Empty Response")),
        }
        | DEFAULT_RESPONSES,
        parameters=[
            OpenApiParameter(name="id", location="path", type=UUID, required=True),
        ],
    )
    async def destroy(self, request, *args, **kwargs):
        return await super().destroy(request, *args, **kwargs)

    def perform_destroy(self, instance: CustomerAccount):
        user = self._get_user()
        dao = CustomerDAO(user)
        dao.mark_account_as_deleted(instance)
