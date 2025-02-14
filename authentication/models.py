from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from decimal import Decimal
from django.contrib.auth import get_user_model
from .utils import send_deposit_confirmation, send_withdrawal_approval

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="static/profile/")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    earnings = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    ADA = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    avail_balance = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    Tax_balance = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    deposit = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    transaction_pin = models.CharField(max_length=6, blank=True, null=True)
    pin_otp = models.CharField(max_length=6, blank=True, null=True)
    pin_otp_created = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

class ADATransaction(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='ada_transactions')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=[('credit', 'Credit'), ('debit', 'Debit')])
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.transaction_type == 'credit':
            self.profile.ADA += self.amount
        else:
            self.profile.ADA -= self.amount
        self.profile.save()
        super().save(*args, **kwargs)

class TaxTransaction(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='tax_transactions')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=[('credit', 'Credit'), ('debit', 'Debit')])
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.transaction_type == 'credit':
            self.profile.Tax_balance += self.amount
        else:
            self.profile.Tax_balance -= self.amount
        self.profile.save()
        super().save(*args, **kwargs)

class EarningsTransaction(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='earnings_transactions')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=[('credit', 'Credit'), ('debit', 'Debit')])
    description = models.CharField(max_length=255)
    source = models.CharField(max_length=50, choices=[
        ('investment', 'Investment Return'),
        ('referral', 'Referral Bonus'),
        ('bonus', 'Bonus'),
        ('other', 'Other')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new:  # Only on creation
            profile = self.profile
            prev_balance = profile.earnings
            
            if self.transaction_type == 'credit':
                profile.earnings += self.amount
            else:
                profile.earnings -= self.amount
            
            new_balance = profile.earnings
            
            # Create transaction history record
            TransactionHistory.objects.create(
                user=profile.user,
                transaction_type='earnings_update',
                amount=self.amount,
                previous_balance=prev_balance,
                new_balance=new_balance,
                status=self.transaction_type,  # 'credit' or 'debit'
                description=f"Earnings {self.transaction_type} - {self.get_source_display()}",
            )
            
            profile.save()
        super().save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} verification token"

class Deposit(models.Model):
    CRYPTO_CHOICES = (
        ('USDT', 'USDT (TRC-20)'),
        ('BTC', 'BTC'),
        ('BCH', 'BCH'),
        ('ETH', 'ETH'),
        ('WIRE', 'Wire Transfer'),
    )
    
    DEPOSIT_TYPE_CHOICES = (
        ('tax', 'Tax'),
        ('fund', 'Balance'),  # Changed display name to Balance
        ('ada', 'ADA'),
    )
    
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=50, choices=CRYPTO_CHOICES, default='BTC')
    deposit_type = models.CharField(max_length=50, choices=DEPOSIT_TYPE_CHOICES, default='fund')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    proof_of_payment = models.ImageField(upload_to='deposits/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_status = None
        
        if not is_new:
            old_status = Deposit.objects.get(pk=self.pk).status

        super().save(*args, **kwargs)

        # Create transaction record for new deposits regardless of status
        if is_new:
            TransactionHistory.objects.create(
                user=self.user,
                transaction_type='deposit',
                amount=self.amount,
                previous_balance=self.user.profile.balance,
                new_balance=self.user.profile.balance,
                status=self.status,
                description=f"Deposit via {self.get_payment_type_display()}",
                reference_id=self.transaction_id
            )

        # Send email and update balances when deposit is marked as completed
        if old_status != 'completed' and self.status == 'completed':
            send_deposit_confirmation(self.user, self)
            profile = self.user.profile
            
            # Record the transaction before updating balances
            if self.deposit_type == 'tax':
                prev_balance = profile.Tax_balance
                profile.Tax_balance += self.amount
                new_balance = profile.Tax_balance
                balance_type = 'Tax Balance'
            elif self.deposit_type == 'fund':
                prev_balance = profile.balance
                profile.balance += self.amount
                new_balance = profile.balance
                balance_type = 'Balance'
            elif self.deposit_type == 'ada':
                prev_balance = profile.ADA
                profile.ADA += self.amount
                new_balance = profile.ADA
                balance_type = 'ADA Balance'

            # Update the transaction history with completed status
            TransactionHistory.objects.filter(
                user=self.user,
                transaction_type='deposit',
                reference_id=self.transaction_id
            ).update(
                status='completed',
                previous_balance=prev_balance,
                new_balance=new_balance,
                description=f"Deposit to {balance_type} via {self.get_payment_type_display()}"
            )
            
            profile.save()

    def __str__(self):
        return f"{self.user.username}'s {self.get_deposit_type_display()} deposit of {self.amount} {self.payment_type}"

    class Meta:
        ordering = ['-created_at']

class Withdrawal(models.Model):
    CRYPTO_CHOICES = (
        ('USDT', 'USDT (TRC-20)'),
        ('BTC', 'BTC'),
        ('BCH', 'BCH'),
        ('ETH', 'ETH'),
        ('WIRE', 'Wire Transfer'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected')
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=CRYPTO_CHOICES)
    wallet_address = models.CharField(max_length=255)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_status = None
        
        if not is_new:
            old_status = Withdrawal.objects.get(pk=self.pk).status

        # Make sure amount is Decimal
        if isinstance(self.amount, float):
            self.amount = Decimal(str(self.amount))

        # First save to get the ID
        super().save(*args, **kwargs)

        # Handle status change to completed
        if old_status != 'completed' and self.status == 'completed':
            # Send email notification
            send_withdrawal_approval(self.user, self)

            # Update transaction history
            TransactionHistory.objects.filter(
                user=self.user,
                transaction_type='withdrawal',
                reference_id=self.transaction_id
            ).update(
                status='completed',
                description=f"Withdrawal completed via {self.get_payment_method_display()} to {self.wallet_address}"
            )

        # Only create transaction record on new withdrawals
        if is_new:
            profile = self.user.profile
            if profile.avail_balance >= self.amount:
                prev_balance = profile.avail_balance
                profile.avail_balance = prev_balance - self.amount
                new_balance = profile.avail_balance
                
                # Create transaction record
                TransactionHistory.objects.create(
                    user=self.user,
                    transaction_type='withdrawal',
                    amount=self.amount,
                    previous_balance=prev_balance,
                    new_balance=new_balance,
                    status='pending',
                    description=f"Withdrawal via {self.get_payment_method_display()}",
                    reference_id=self.transaction_id
                )
                
                profile.save()
            else:
                raise ValueError("Insufficient available balance")

    def __str__(self):
        return f"{self.user.username}'s withdrawal of {self.amount} {self.payment_method}"

    class Meta:
        ordering = ['-created_at']

class TransactionHistory(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('ada_update', 'ADA Update'),
        ('tax_update', 'Tax Update'),
        ('earnings_update', 'Earnings Update'),
        ('balance_update', 'Balance Update'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('rejected', 'Rejected'),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    previous_balance = models.DecimalField(max_digits=15, decimal_places=2)
    new_balance = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    description = models.CharField(max_length=255)
    reference_id = models.CharField(max_length=100, blank=True, null=True)  # For linking to specific transactions
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Transaction histories"

    def __str__(self):
        return f"{self.user.username}'s {self.transaction_type} of {self.amount}"

class WalletAddress(models.Model):
    CRYPTO_CHOICES = (
        ('USDT', 'USDT'),
        ('BTC', 'Bitcoin'),
        ('BCH', 'Bitcoin Cash'),
        ('ETH', 'Ethereum'),
        ('BNB', 'Binance Coin'),
        ('MATIC', 'Polygon'),
        ('SOL', 'Solana'),
    )

    NETWORK_CHOICES = (
        ('TRC20', 'TRON (TRC-20)'),
        ('ERC20', 'Ethereum (ERC-20)'),
        ('BEP20', 'BNB Smart Chain (BEP-20)'),
        ('BITCOIN', 'Bitcoin Network'),
        ('BCH', 'Bitcoin Cash Network'),
        ('POLYGON', 'Polygon Network'),
        ('SOLANA', 'Solana Network'),
    )

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Under Maintenance'),
    )

    cryptocurrency = models.CharField(max_length=20, choices=CRYPTO_CHOICES)
    network = models.CharField(max_length=20, choices=NETWORK_CHOICES)
    address = models.CharField(max_length=255)
    qr_code = models.ImageField(upload_to='wallet_qr_codes/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    memo = models.CharField(max_length=100, blank=True, null=True, help_text="For cryptocurrencies that require memo/tag")
    description = models.TextField(blank=True, help_text="Additional information or instructions")
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Wallet Address"
        verbose_name_plural = "Wallet Addresses"
        unique_together = ['cryptocurrency', 'network']
        ordering = ['cryptocurrency', 'network']

    def __str__(self):
        return f"{self.get_cryptocurrency_display()} ({self.get_network_display()})"

    def save(self, *args, **kwargs):
        if self.is_default:
            # Ensure only one default address per cryptocurrency
            WalletAddress.objects.filter(
                cryptocurrency=self.cryptocurrency,
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)


