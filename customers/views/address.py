from uuid import UUID

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
from core.views import UserMixin
from customers.dao.customer import CustomerDAO
from customers.models.customer_address import CustomerAddress
from customers.serializers import CustomerAddressSerializer


@extend_schema(
    summary=_("Customer Address Resource"),
    description=_("Manages Customer Address Endpoints."),
    tags=["address"],
    parameters=[
        OpenApiParameter(name="customer_id", location="path", type=UUID, required=True),
    ],
)
class CustomerAddressViewSet(
    UserMixin,
    AsyncMixin,
    AsyncCreateModelMixin,
    AsyncRetrieveModelMixin,
    AsyncUpdateModelMixin,
    AsyncDestroyModelMixin,
    AsyncListModelMixin,
    viewsets.GenericViewSet,
):
    """Customer Address ViewSet."""

    permission_classes = [UsingAppToken | IsAuthenticated]
    serializer_class = CustomerAddressSerializer
    http_method_names = ["get", "post", "head", "put", "delete", "options"]

    def get_queryset(self):
        return CustomerAddress.objects.filter(
            customer=self.kwargs["customer_id"],
            deleted=False,
        ).all()

    @extend_schema(
        summary=_("List Customer Addresses."),
        description=_("No filter available."),
        responses={
            200: CustomerAddressSerializer,
        }
        | DEFAULT_RESPONSES,
    )
    async def list(self, request, *args, **kwargs):
        return await super().list(request, *args, **kwargs)

    @extend_schema(
        summary=_("Create new customer address."),
        description=_(
            "Will not check for duplicates, but only one address is active at time.",
        ),
        responses={
            201: CustomerAddressSerializer,
            400: BadRequestSerializer,
        }
        | DEFAULT_RESPONSES,
    )
    async def create(self, request, *args, **kwargs):
        return await super().create(request, *args, **kwargs)

    def perform_create(self, serializer: CustomerAddressSerializer):
        user = self._get_user()
        dao = CustomerDAO(user)
        dao.create_customer_address(serializer)

    @extend_schema(
        summary=_("Find Customer Address by Customer Address Id."),
        description=_("Returns a single resource."),
        responses={
            200: CustomerAddressSerializer,
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
        summary=_("Update Customer Address."),
        description=_("Update Customer Address."),
        responses={
            200: CustomerAddressSerializer,
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

    def perform_update(self, serializer):
        user = self._get_user()
        dao = CustomerDAO(user)
        dao.update_customer_address(serializer)

    @extend_schema(
        summary=_("Mark Customer Address as deleted."),
        description=_(
            "Deleted customer addresses will not show in API. "
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

    def perform_destroy(self, instance: CustomerAddress):
        user = self._get_user()
        dao = CustomerDAO(user)
        dao.mark_address_as_deleted(instance)
