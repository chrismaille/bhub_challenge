from django.urls import include, path
from rest_framework_nested import routers

from customers.views.account import CustomerAccountViewSet
from customers.views.address import CustomerAddressViewSet
from customers.views.customer import CustomerViewSet

app_name = "customers"

router = routers.SimpleRouter()
router.register(r"customers", CustomerViewSet, basename="customer")

domains_router = routers.NestedSimpleRouter(router, r"customers", lookup="customer")
domains_router.register(r"address", CustomerAddressViewSet, basename="customer-address")
domains_router.register(
    r"accounts",
    CustomerAccountViewSet,
    basename="customer-accounts",
)

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(domains_router.urls)),
]
