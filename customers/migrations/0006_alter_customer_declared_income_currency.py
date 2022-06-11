# Generated by Django 4.0.5 on 2022-06-10 14:41

import core.helpers.validators.currency_code
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_alter_customer_blocked_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='declared_income_currency',
            field=models.CharField(max_length=3, validators=[core.helpers.validators.currency_code.validate_currency_code]),
        ),
    ]