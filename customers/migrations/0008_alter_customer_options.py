# Generated by Django 4.0.5 on 2022-06-10 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0007_address_deleted_bank_deleted_customer_deleted_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['created_at'], 'verbose_name': 'Customer'},
        ),
    ]
