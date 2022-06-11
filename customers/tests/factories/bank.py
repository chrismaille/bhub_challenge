import factory
from factory.django import DjangoModelFactory

from conftest import SAMPLE_BANK_DATA
from customers.models.bank import Bank


class BankFactory(DjangoModelFactory):
    id = factory.Faker("uuid4")
    code = factory.Faker("random_element", elements=SAMPLE_BANK_DATA.keys())
    name = factory.LazyAttribute(lambda o: SAMPLE_BANK_DATA[o.code])

    class Meta:
        model = Bank
        django_get_or_create = ("id",)
