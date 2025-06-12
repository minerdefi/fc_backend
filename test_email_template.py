#!/usr/bin/env python
"""
Simple test script to verify email templates can be rendered correctly
Run this script to test email template rendering without sending actual emails
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

from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.conf import settings

def test_verification_email_template():
    """Test if the verification email template can be rendered"""
    print("🧪 Testing Email Template Rendering...")
    print("=" * 50)
    
    try:
        # Create a test user object
        test_user = User(
            username='testuser',
            email='test@example.com',
            first_name='John',
            last_name='Doe'
        )
        
        # Test data
        verification_url = f"{settings.FRONTEND_URL}/verify-email?token=test-token-123"
        
        context = {
            'user': test_user,
            'verification_url': verification_url
        }
        
        print(f"📧 Template Path: templates/authentication/verification_email.html")
        print(f"🌐 Frontend URL: {settings.FRONTEND_URL}")
        print(f"🔗 Verification URL: {verification_url}")
        print(f"👤 Test User: {test_user.first_name} {test_user.last_name} ({test_user.email})")
        print()
        
        # Try to render the template
        html_content = render_to_string('authentication/verification_email.html', context)
        
        print("✅ SUCCESS: Email template rendered successfully!")
        print(f"📄 Template length: {len(html_content)} characters")
        print()
        
        # Show a preview of the rendered content
        print("📋 Template Preview (first 500 characters):")
        print("-" * 50)
        print(html_content[:500] + "..." if len(html_content) > 500 else html_content)
        print("-" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Failed to render email template")
        print(f"🔍 Error details: {str(e)}")
        print(f"📁 Template directories: {settings.TEMPLATES[0]['DIRS']}")
        
        # Check if template file exists
        template_path = Path(settings.BASE_DIR) / 'templates' / 'authentication' / 'verification_email.html'
        print(f"📄 Template file exists: {template_path.exists()}")
        print(f"📍 Looking for template at: {template_path}")
        
        return False

def test_email_settings():
    """Test email configuration"""
    print("\n📧 Testing Email Configuration...")
    print("=" * 50)
    
    try:
        print(f"Email Backend: {settings.EMAIL_BACKEND}")
        print(f"Email Host: {settings.EMAIL_HOST}")
        print(f"Email Port: {settings.EMAIL_PORT}")
        print(f"Email Use TLS: {settings.EMAIL_USE_TLS}")
        print(f"Default From Email: {settings.DEFAULT_FROM_EMAIL}")
        print(f"Admin Email: {settings.ADMIN_EMAIL}")
        print(f"Contact Form Email: {settings.CONTACT_FORM_EMAIL}")
        print(f"Frontend URL: {settings.FRONTEND_URL}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Email configuration issue")
        print(f"🔍 Error details: {str(e)}")
        return False

if __name__ == '__main__':
    print("🧪 EMAIL TEMPLATE & CONFIGURATION TEST")
    print("=" * 60)
    
    # Test email settings
    settings_ok = test_email_settings()
    
    # Test template rendering
    template_ok = test_verification_email_template()
    
    print("\n📊 TEST RESULTS:")
    print("=" * 50)
    print(f"Email Settings: {'✅ PASS' if settings_ok else '❌ FAIL'}")
    print(f"Template Rendering: {'✅ PASS' if template_ok else '❌ FAIL'}")
    
    if settings_ok and template_ok:
        print("\n🎉 ALL TESTS PASSED! Email system should work correctly.")
    else:
        print("\n⚠️  SOME TESTS FAILED! Please fix the issues above.")
    
    print("\n💡 TIP: If templates fail, check that TEMPLATES['DIRS'] includes 'templates' directory")
    print("💡 TIP: If you're still getting errors, check Django error logs for more details")
