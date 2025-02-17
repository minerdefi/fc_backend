# Generated by Django 5.1 on 2025-02-13 18:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_remove_profile_profile_picture_profile_ada_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ADATransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('transaction_type', models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], max_length=10)),
                ('description', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ada_transactions', to='authentication.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_type', models.CharField(choices=[('USDT', 'USDT (TRC-20)'), ('BTC', 'BTC'), ('BCH', 'BCH'), ('ETH', 'ETH'), ('WIRE', 'Wire Transfer')], default='BTC', max_length=50)),
                ('deposit_type', models.CharField(choices=[('tax', 'Tax'), ('fund', 'Fund'), ('fees', 'Fees'), ('ada', 'ADA')], default='fund', max_length=50)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=20)),
                ('transaction_id', models.CharField(blank=True, max_length=100, null=True)),
                ('proof_of_payment', models.ImageField(blank=True, null=True, upload_to='deposits/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='EarningsTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('transaction_type', models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], max_length=10)),
                ('description', models.CharField(max_length=255)),
                ('source', models.CharField(choices=[('investment', 'Investment Return'), ('referral', 'Referral Bonus'), ('bonus', 'Bonus'), ('other', 'Other')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='earnings_transactions', to='authentication.profile')),
            ],
        ),
        migrations.CreateModel(
            name='TaxTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('transaction_type', models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], max_length=10)),
                ('description', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tax_transactions', to='authentication.profile')),
            ],
        ),
    ]
