# Generated by Django 4.0.5 on 2022-06-10 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0006_alter_customer_declared_income_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bank',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customer',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customeraccount',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customeraddress',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customer',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Active'), ('BLOCKED', 'Blocked')], default='ACTIVE', max_length=20),
        ),
    ]
