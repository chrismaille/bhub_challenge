# Generated by Django 4.0.5 on 2022-06-10 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0004_alter_customer_cell_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='blocked_reason',
            field=models.TextField(blank=True, null=True),
        ),
    ]
