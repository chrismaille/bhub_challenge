import factory
from factory.django import DjangoModelFactory

from customers.models.customer_address import CustomerAddress
from customers.tests.factories.address import AddressFactory
from customers.tests.factories.customer import CustomerFactory


class CustomerAddressFactory(DjangoModelFactory):

    id = factory.Faker("uuid4")
    customer = factory.SubFactory(CustomerFactory)
    address = factory.SubFactory(AddressFactory)
    address_type = factory.Faker(
        "random_element",
        elements=[choice[0] for choice in CustomerAddress.AddressType.choices],
    )
    address_number = factory.Faker("building_number", locale="pt_BR")
    address_complement = factory.Faker("neighborhood", locale="pt_BR")

    class Meta:
        model = CustomerAddress
        django_get_or_create = ("id",)
