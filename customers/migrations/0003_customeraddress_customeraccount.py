# Generated by Django 4.0.5 on 2022-06-09 23:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customers', '0002_bank_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerAddress',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('active', models.BooleanField(default=True)),
                ('address_type', models.CharField(choices=[('BILLING', 'Billing'), ('DELIVERY', 'Delivery')], max_length=20)),
                ('address_number', models.CharField(max_length=255)),
                ('address_complement', models.CharField(max_length=255, null=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.address')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)ss_created_by', related_query_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)ss_deleted_by', related_query_name='%(app_label)s_%(class)s_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)ss_updated_by', related_query_name='%(app_label)s_%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Customer Address',
                'db_table': 'customer_address',
            },
        ),
        migrations.CreateModel(
            name='CustomerAccount',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('payment_type', models.CharField(choices=[('PIX', 'Pix'), ('CREDIT_CARD', 'Credit Card'), ('BANK_TRANSFER', 'Bank Transfer')], max_length=255)),
                ('active', models.BooleanField(default=False)),
                ('token_id', models.UUIDField(null=True)),
                ('bank_branch', models.CharField(max_length=255, null=True)),
                ('bank_account', models.CharField(max_length=255, null=True)),
                ('bank', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='customers.bank')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)ss_created_by', related_query_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)ss_deleted_by', related_query_name='%(app_label)s_%(class)s_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)ss_updated_by', related_query_name='%(app_label)s_%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Customer Account',
                'db_table': 'customer_account',
            },
        ),
    ]
