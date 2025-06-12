#!/usr/bin/env python
"""
Email Testing Utility for FG Premium Funds
Run this script to test all email functionality
"""

import os
import sys
import django
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fc_backend.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from authentication.models import Deposit, EmailVerification
from decimal import Decimal

def test_email_configuration():
    """Test basic email configuration"""
    print("🔧 Testing Email Configuration...")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print(f"CONTACT_FORM_EMAIL: {settings.CONTACT_FORM_EMAIL}")
    print(f"ADMIN_EMAIL: {settings.ADMIN_EMAIL}")
    print(f"FRONTEND_URL: {settings.FRONTEND_URL}")
    print("✅ Configuration loaded successfully!\n")

def test_simple_email():
    """Test sending a simple email"""
    print("📧 Testing Simple Email...")
    try:
        send_mail(
            'Test Email from FG Premium Funds',
            'This is a test email to verify email functionality.',
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        print("✅ Simple email sent successfully!\n")
        return True
    except Exception as e:
        print(f"❌ Simple email failed: {e}\n")
        return False

def test_html_email():
    """Test sending HTML email"""
    print("🎨 Testing HTML Email...")
    try:
        html_content = """
        <html>
        <body>
            <h2 style="color: #308e87;">Test HTML Email</h2>
            <p>This is a test HTML email from FG Premium Funds.</p>
            <p>If you can see this formatted text, HTML emails are working!</p>
        </body>
        </html>
        """
        
        send_mail(
            'HTML Test Email from FG Premium Funds',
            'This is the plain text version.',
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            html_message=html_content,
            fail_silently=False,
        )
        print("✅ HTML email sent successfully!\n")
        return True
    except Exception as e:
        print(f"❌ HTML email failed: {e}\n")
        return False

def test_contact_form_email():
    """Test contact form email notification"""
    print("📝 Testing Contact Form Email...")
    try:
        subject = 'Test Contact Form Submission'
        message = """
        Test contact form submission:
        
        Name: Test User
        Email: test@example.com
        Phone: +1234567890
        
        Message:
        This is a test contact form submission to verify email functionality.
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_FORM_EMAIL],
            fail_silently=False,
        )
        print("✅ Contact form email sent successfully!\n")
        return True
    except Exception as e:
        print(f"❌ Contact form email failed: {e}\n")
        return False

def test_verification_email_template():
    """Test email verification template"""
    print("🔐 Testing Email Verification Template...")
    try:
        # Create a test context
        context = {
            'user': {
                'first_name': 'Test',
                'username': 'testuser',
                'email': 'test@example.com'
            },
            'verification_url': f"{settings.FRONTEND_URL}/verify-email?token=test-token-123"
        }
        
        html_message = render_to_string('authentication/verification_email.html', context)
        
        send_mail(
            'Test Email Verification - FG Premium Funds',
            f'Verification URL: {context["verification_url"]}',
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            html_message=html_message,
            fail_silently=False,
        )
        print("✅ Email verification template sent successfully!\n")
        return True
    except Exception as e:
        print(f"❌ Email verification template failed: {e}\n")
        return False

def test_password_reset_template():
    """Test password reset email template"""
    print("🔑 Testing Password Reset Template...")
    try:
        # Create a test context
        context = {
            'user': {
                'first_name': 'Test',
                'username': 'testuser',
                'email': 'test@example.com'
            },
            'reset_url': f"{settings.FRONTEND_URL}/reset-password?token=test-reset-token-123"
        }
        
        html_message = render_to_string('authentication/password_reset_email.html', context)
        
        send_mail(
            'Test Password Reset - FG Premium Funds',
            f'Reset URL: {context["reset_url"]}',
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            html_message=html_message,
            fail_silently=False,
        )
        print("✅ Password reset template sent successfully!\n")
        return True
    except Exception as e:
        print(f"❌ Password reset template failed: {e}\n")
        return False

def test_admin_notification_template():
    """Test admin notification email template"""
    print("👨‍💼 Testing Admin Notification Template...")
    try:
        # Create a test context
        context = {
            'notification_type': 'Test Notification',
            'subject': 'This is a test admin notification',
            'user': {
                'first_name': 'Test',
                'last_name': 'User',
                'username': 'testuser',
                'email': 'test@example.com'
            },
            'amount': '1000.00',
            'payment_type': 'Credit Card',
            'transaction_id': 'TEST-123456',
            'timestamp': '2025-06-12 10:30:00',
            'action_required': 'This is a test notification - no action required.',
            'admin_email': settings.ADMIN_EMAIL
        }
        
        html_message = render_to_string('authentication/admin_notification_email.html', context)
        
        send_mail(
            'Test Admin Notification - FG Premium Funds',
            'This is a test admin notification email.',
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            html_message=html_message,
            fail_silently=False,
        )
        print("✅ Admin notification template sent successfully!\n")
        return True
    except Exception as e:
        print(f"❌ Admin notification template failed: {e}\n")
        return False

def run_all_tests():
    """Run all email tests"""
    print("🚀 Starting Email Functionality Tests\n")
    print("=" * 50)
    
    # Test configuration
    test_email_configuration()
    
    # Run tests
    tests = [
        ("Simple Email", test_simple_email),
        ("HTML Email", test_html_email),
        ("Contact Form Email", test_contact_form_email),
        ("Email Verification Template", test_verification_email_template),
        ("Password Reset Template", test_password_reset_template),
        ("Admin Notification Template", test_admin_notification_template),
    ]
    
    results = {}
    for test_name, test_func in tests:
        results[test_name] = test_func()
    
    # Summary
    print("=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All email tests passed! Email system is working correctly.")
    else:
        print("⚠️  Some email tests failed. Check your email configuration.")
        print("\nTroubleshooting tips:")
        print("1. Verify your .env file has correct email settings")
        print("2. Check if your email server is accessible")
        print("3. Verify email credentials are correct")
        print("4. Check Django logs for detailed error messages")

if __name__ == '__main__':
    run_all_tests()
