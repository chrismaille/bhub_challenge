import factory
from factory.django import DjangoModelFactory

from conftest import get_zip_code
from customers.models.address import Address


class AddressFactory(DjangoModelFactory):
    id = factory.Faker("uuid4")
    street = factory.Faker("street_address", locale="pt_BR")
    district = factory.Faker("bairro", locale="pt_BR")
    city = factory.Faker("city", locale="pt_BR")
    state = factory.Faker("estado_sigla", locale="pt_BR")
    country = factory.Faker("country_code", locale="pt_BR")
    zip_code = factory.LazyFunction(get_zip_code)

    class Meta:
        model = Address
        django_get_or_create = ("id",)
