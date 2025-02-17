# Generated by Django 5.1 on 2025-02-14 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_profile_pin_otp_profile_pin_otp_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='reset_password_expire',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='reset_password_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
