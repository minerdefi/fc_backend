from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from decimal import Decimal

def send_verification_email(user, verification_token):
    verification_url = f"{settings.FRONTEND_URL}/verify-email?token={verification_token}"
    
    context = {
        'user': user,
        'verification_url': verification_url
    }
    
    html_message = render_to_string('authentication/verification_email.html', context)
      send_mail(
        subject='Verify your FG Premium Funds account',
        message=f'Please verify your email by clicking this link: {verification_url}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message
    )

def send_deposit_confirmation(user, deposit):
    context = {
        'user': user,
        'amount': Decimal(deposit.amount).quantize(Decimal('0.00')),
        'payment_type': deposit.get_payment_type_display(),
        'deposit_type': deposit.get_deposit_type_display(),
        'transaction_id': deposit.transaction_id or 'N/A',
        'date': deposit.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    html_message = render_to_string('authentication/deposit_confirmation_email.html', context)
      send_mail(
        subject='Deposit Confirmation - FG Premium Funds',
        message=f'Your deposit of ${deposit.amount} has been confirmed.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message
    )

def send_withdrawal_approval(user, withdrawal):
    context = {
        'user': user,
        'amount': Decimal(withdrawal.amount).quantize(Decimal('0.00')),
        'payment_method': withdrawal.get_payment_method_display(),
        'transaction_id': withdrawal.transaction_id or 'N/A',
        'wallet_address': withdrawal.wallet_address,
        'date': withdrawal.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    html_message = render_to_string('authentication/withdrawal_approval_email.html', context)
      send_mail(
        subject='Withdrawal Approved - FG Premium Funds',
        message=f'Your withdrawal of ${withdrawal.amount} has been approved.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message
    )
