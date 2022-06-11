from uuid import UUID

from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from core.helpers.asyncio import async_
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
from customers.models.customer import Customer
from customers.serializers import (
    BlockUserSerializer,
    CustomerSerializer,
    EditCustomerSerializer,
)


class CustomerFilter(filters.FilterSet):
    class Meta:
        model = Customer
        fields = ["email", "tax_id"]


@extend_schema(
    summary=_("Customer Resource"),
    description=_("Manages Customer Endpoint."),
    tags=["customers"],
)
class CustomerViewSet(
    UserMixin,
    AsyncMixin,
    AsyncCreateModelMixin,
    AsyncRetrieveModelMixin,
    AsyncUpdateModelMixin,
    AsyncDestroyModelMixin,
    AsyncListModelMixin,
    viewsets.GenericViewSet,
):
    """Customer ViewSet.

    More info:
        * https://www.django-rest-framework.org/api-guide/viewsets/
        * https://github.com/encode/django-rest-framework/discussions/7774

    """

    lookup_field = "id"
    permission_classes = [UsingAppToken | IsAuthenticated]
    serializer_class = CustomerSerializer
    queryset = Customer.objects.filter(deleted=False).all()
    http_method_names = ["get", "post", "head", "put", "delete", "options"]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("email", "tax_id")

    @extend_schema(
        summary=_("List Bhub Customers."),
        description=_("Can filter by Email and TaxId."),
        responses={
            200: CustomerSerializer,
        }
        | DEFAULT_RESPONSES,
    )
    async def list(self, request, *args, **kwargs):
        return await super().list(request, *args, **kwargs)

    @extend_schema(
        summary=_("Create new customer."),
        description=_("TaxId must be unique per Customer."),
        responses={
            201: CustomerSerializer,
            400: BadRequestSerializer,
        }
        | DEFAULT_RESPONSES,
    )
    async def create(self, request, *args, **kwargs):
        return await super().create(request, *args, **kwargs)

    def perform_create(self, serializer: CustomerSerializer):
        user = self._get_user()
        dao = CustomerDAO(user)
        dao.create_customer(serializer, payload=self.request.data)

    @extend_schema(
        summary=_("Find Customer by Id."),
        description=_("Returns a single resource."),
        responses={
            200: CustomerSerializer,
            404: NotFoundSerializer,
        }
        | DEFAULT_RESPONSES,
    )
    async def retrieve(self, request, *args, **kwargs):
        return await super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary=_("Update Customer Data."),
        description=_("Update Customer."),
        request=EditCustomerSerializer,
        responses={
            200: CustomerSerializer,
            400: BadRequestSerializer,
            404: NotFoundSerializer,
        }
        | DEFAULT_RESPONSES,
    )
    async def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return await super().update(request, *args, **kwargs)

    def perform_update(self, serializer: CustomerSerializer):
        user = self._get_user()
        dao = CustomerDAO(user)
        dao.update_customer(serializer)

    @extend_schema(
        summary=_("Mark Customer as deleted."),
        description=_(
            "Deleted customers will not show in API. "
            "Please use Django Admin to edit them.",
        ),
        responses={
            204: OpenApiResponse(description=_("Empty Response")),
        }
        | DEFAULT_RESPONSES,
    )
    async def destroy(self, request, *args, **kwargs):
        return await super().destroy(request, *args, **kwargs)

    def perform_destroy(self, instance: Customer):
        user = self._get_user()
        dao = CustomerDAO(user)
        dao.mark_as_deleted(instance)

    @extend_schema(
        summary=_("Mark Customer as Blocked."),
        description=_("Inform Block Reason for Customer."),
        request=BlockUserSerializer,
        responses={
            200: CustomerSerializer,
            400: BadRequestSerializer,
            404: NotFoundSerializer,
        }
        | DEFAULT_RESPONSES,
    )
    @action(methods=["put"], detail=True)
    async def block(self, request: Request, id: UUID) -> Response:
        serializer = BlockUserSerializer(data=request.data)
        await async_(serializer.is_valid)(raise_exception=True)

        customer = await async_(self.perform_block)(
            customer_id=id,
            reason=serializer.validated_data["reason"],
        )
        return Response(self.get_serializer(customer).data)

    def perform_block(self, customer_id: UUID, reason: str) -> Customer:
        user = self._get_user()
        customer = get_object_or_404(Customer, pk=customer_id)

        dao = CustomerDAO(user)
        return dao.mark_as_blocked(
            customer=customer,
            reason=reason,
        )
