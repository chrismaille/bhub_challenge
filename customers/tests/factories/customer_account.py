import factory
from factory.django import DjangoModelFactory

from customers.models.customer_account import CustomerAccount
from customers.tests.factories.bank import BankFactory
from customers.tests.factories.customer import CustomerFactory


class CustomerAccountFactory(DjangoModelFactory):

    id = factory.Faker("uuid4")
    customer = factory.SubFactory(CustomerFactory)
    bank = factory.SubFactory(BankFactory)
    payment_type = factory.Faker(
        "random_element",
        elements=[choice[0] for choice in CustomerAccount.PaymentType.choices],
    )
    token_id = factory.LazyAttribute(
        lambda o: factory.Faker("uuid4")
        if o.payment_type == CustomerAccount.PaymentType.CREDIT_CARD
        else None,
    )
    direct_transfer_id = factory.LazyAttribute(
        lambda o: factory.Faker("email")
        if o.payment_type == CustomerAccount.PaymentType.PIX
        else None,
    )
    bank_branch = factory.LazyAttribute(
        lambda o: factory.Faker("random_number", digits=4, fix_len=True)
        if o.payment_type == CustomerAccount.PaymentType.BANK_TRANSFER
        else None,
    )
    bank_account = factory.LazyAttribute(
        lambda o: factory.Faker("random_number", digits=8, fix_len=True)
        if o.payment_type == CustomerAccount.PaymentType.BANK_TRANSFER
        else None,
    )

    class Meta:
        model = CustomerAccount
        django_get_or_create = ("id",)
