# Generated by Django 5.1 on 2025-02-14 15:59

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_remove_profile_reset_password_expire_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='total_deposits',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=15),
        ),
    ]
