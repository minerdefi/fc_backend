#!/usr/bin/env python
"""
Contact Form Email Debug Script
Run this script to test and debug contact form email functionality
"""

import os
import sys
import django
from pathlib import Path

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fc_backend.settings')
django.setup()

from django.conf import settings
from django.core.mail import send_mail
from contact.serializers import ContactSubmissionSerializer
from contact.models import ContactSubmission
import json

def test_contact_form_serializer():
    """Test contact form serializer validation"""
    print("🧪 Testing Contact Form Serializer...")
    print("=" * 50)
    
    # Test data
    test_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email_address': 'john.doe@example.com',
        'phone': '1234567890',
        'message': 'This is a test message from the contact form.'
    }
    
    try:
        serializer = ContactSubmissionSerializer(data=test_data)
        if serializer.is_valid():
            print("✅ Serializer validation: PASSED")
            print(f"📋 Validated data: {serializer.validated_data}")
            
            # Try to save the submission
            submission = serializer.save()
            print(f"💾 Submission saved: ID {submission.id}")
            
            # Clean up
            submission.delete()
            print("🗑️ Test submission deleted")
            
            return True, submission
        else:
            print("❌ Serializer validation: FAILED")
            print(f"🔍 Errors: {serializer.errors}")
            return False, None
            
    except Exception as e:
        print(f"❌ Serializer error: {str(e)}")
        return False, None

def test_email_settings():
    """Test email configuration"""
    print("\n📧 Testing Email Settings...")
    print("=" * 50)
    
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print(f"CONTACT_FORM_EMAIL: {settings.CONTACT_FORM_EMAIL}")
    
    # Check if using console backend
    if settings.EMAIL_BACKEND == 'django.core.mail.backends.console.EmailBackend':
        print("⚠️  Using console backend - emails will be printed to console")
        return True
    elif settings.EMAIL_BACKEND == 'django.core.mail.backends.smtp.EmailBackend':
        print("📤 Using SMTP backend - emails will be sent via SMTP")
        return True
    else:
        print(f"❓ Unknown email backend: {settings.EMAIL_BACKEND}")
        return False

def test_contact_email_sending():
    """Test contact form email sending"""
    print("\n📨 Testing Contact Form Email...")
    print("=" * 50)
    
    try:
        # Test email content
        subject = 'Test Contact Form Submission'
        message = """
        Test contact form submission:
        
        Name: John Doe
        Email: john.doe@example.com
        Phone: 1234567890
        
        Message:
        This is a test message to verify email functionality.
        """
        
        print(f"📧 From: {settings.DEFAULT_FROM_EMAIL}")
        print(f"📧 To: {settings.CONTACT_FORM_EMAIL}")
        print(f"📧 Subject: {subject}")
        
        # Send test email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_FORM_EMAIL],
            fail_silently=False,
        )
        
        print("✅ Email sent successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Email sending failed: {str(e)}")
        print(f"🔍 Error type: {type(e).__name__}")
        
        # Common error scenarios
        if "SMTP" in str(e):
            print("💡 SMTP Error - Check email host, port, credentials")
        elif "Authentication" in str(e):
            print("💡 Authentication Error - Check email username/password")
        elif "Connection" in str(e):
            print("💡 Connection Error - Check email host and port")
            
        return False

def test_contact_view_simulation():
    """Simulate the contact form view"""
    print("\n🎭 Simulating Contact Form View...")
    print("=" * 50)
    
    # Simulate request data
    request_data = {
        'first_name': 'Test',
        'last_name': 'User', 
        'email_address': 'test@example.com',
        'phone': '1234567890',
        'message': 'This is a test contact form submission.'
    }
    
    try:
        # Test serializer
        serializer = ContactSubmissionSerializer(data=request_data)
        if serializer.is_valid():
            submission = serializer.save()
            print(f"✅ Contact submission created: {submission}")
            
            # Test email sending
            subject = f'New Contact Form Submission from {submission.first_name} {submission.last_name}'
            message = f"""
            New contact form submission received:
            
            Name: {submission.first_name} {submission.last_name}
            Email: {submission.email_address}
            Phone: {submission.phone}
            
            Message:
            {submission.message}
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_FORM_EMAIL],
                fail_silently=False,
            )
            
            print("✅ Contact form email sent successfully!")
            
            # Clean up
            submission.delete()
            
            return True
        else:
            print(f"❌ Serializer errors: {serializer.errors}")
            return False
            
    except Exception as e:
        print(f"❌ Contact form simulation failed: {str(e)}")
        return False

def check_common_issues():
    """Check for common contact form issues"""
    print("\n🔍 Checking Common Issues...")
    print("=" * 50)
    
    issues = []
    
    # Check if contact app is in INSTALLED_APPS
    if 'contact' not in settings.INSTALLED_APPS:
        issues.append("❌ Contact app not in INSTALLED_APPS")
    else:
        print("✅ Contact app is in INSTALLED_APPS")
    
    # Check email backend
    if settings.EMAIL_BACKEND == 'django.core.mail.backends.dummy.EmailBackend':
        issues.append("❌ Using dummy email backend - emails won't be sent")
    
    # Check required email settings
    if not settings.DEFAULT_FROM_EMAIL or settings.DEFAULT_FROM_EMAIL == 'your-email@example.com':
        issues.append("❌ DEFAULT_FROM_EMAIL not properly configured")
    else:
        print("✅ DEFAULT_FROM_EMAIL is configured")
        
    if not settings.CONTACT_FORM_EMAIL or settings.CONTACT_FORM_EMAIL == 'contact@example.com':
        issues.append("❌ CONTACT_FORM_EMAIL not properly configured")
    else:
        print("✅ CONTACT_FORM_EMAIL is configured")
    
    # Check database table exists
    try:
        ContactSubmission.objects.count()
        print("✅ ContactSubmission model/table exists")
    except Exception as e:
        issues.append(f"❌ ContactSubmission table issue: {str(e)}")
    
    if issues:
        print("\n⚠️  Issues Found:")
        for issue in issues:
            print(f"   {issue}")
    else:
        print("\n✅ No common issues detected")
    
    return len(issues) == 0

if __name__ == '__main__':
    print("🔍 CONTACT FORM EMAIL DEBUG")
    print("=" * 60)
    
    # Run all tests
    print("Running comprehensive contact form tests...\n")
    
    # Test 1: Email settings
    email_ok = test_email_settings()
    
    # Test 2: Serializer
    serializer_ok, test_submission = test_contact_form_serializer()
    
    # Test 3: Email sending
    email_send_ok = test_contact_email_sending()
    
    # Test 4: View simulation
    view_ok = test_contact_view_simulation()
    
    # Test 5: Common issues
    no_issues = check_common_issues()
    
    # Summary
    print("\n📊 TEST RESULTS:")
    print("=" * 50)
    print(f"Email Settings: {'✅ PASS' if email_ok else '❌ FAIL'}")
    print(f"Serializer: {'✅ PASS' if serializer_ok else '❌ FAIL'}")
    print(f"Email Sending: {'✅ PASS' if email_send_ok else '❌ FAIL'}")
    print(f"View Simulation: {'✅ PASS' if view_ok else '❌ FAIL'}")
    print(f"No Common Issues: {'✅ PASS' if no_issues else '❌ FAIL'}")
    
    all_passed = all([email_ok, serializer_ok, email_send_ok, view_ok, no_issues])
    
    print(f"\n🎯 OVERALL STATUS: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    if all_passed:
        print("\n🎉 Contact form should work correctly!")
        print("💡 If you're still seeing errors on frontend, check:")
        print("   - Network connectivity to backend")
        print("   - CORS settings")
        print("   - Frontend API URL configuration")
    else:
        print("\n⚠️  Please fix the failing tests above")
        print("💡 Common fixes:")
        print("   - Set up proper email credentials in .env file")
        print("   - Ensure email backend is configured correctly")
        print("   - Check Django logs for detailed error messages")
