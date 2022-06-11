import factory
from factory.django import DjangoModelFactory

from conftest import get_cell_phone_number, get_tax_id
from customers.models.customer import Customer


class CustomerFactory(DjangoModelFactory):

    id = factory.Faker("uuid4")
    tax_id = factory.LazyFunction(get_tax_id)
    first_name = factory.Faker("first_name", locale="pt_BR")
    last_name = factory.Faker("last_name", locale="pt_BR")
    email = factory.Faker("email", locale="pt_BR")
    cell_phone = factory.LazyFunction(get_cell_phone_number)
    personal_pronoums = factory.Faker(
        "random_elements",
        elements=["Ele, Seu", "Ela, Sua"],
        length=1,
    )
    declared_income = factory.Faker(
        "pydecimal",
        right_digits=2,
        min_value=1000,
        max_value=150000,
    )
    declared_income_currency = factory.Faker("currency_code")
    status = factory.Faker(
        "random_element",
        elements=[choice[0] for choice in Customer.Status.choices],
    )
    blocked_reason = factory.LazyAttribute(
        lambda o: factory.Faker("sentence")
        if o.status == Customer.Status.BLOCKED
        else None,
    )
    payload = factory.Faker("json")

    class Meta:
        model = Customer
        django_get_or_create = ("id",)
