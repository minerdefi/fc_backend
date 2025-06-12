#!/usr/bin/env python3

"""
Test script to verify email verification flow
Tests both the email generation and verification endpoint
"""

import os
import sys
import django
from django.conf import settings

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fc_backend.settings')
django.setup()

from django.contrib.auth.models import User
from authentication.models import EmailVerification
from authentication.utils import send_verification_email
from django.test import Client
import json

def test_verification_flow():
    """Test the complete verification flow"""
    print("🔍 Testing Email Verification Flow...")
    print("="*50)
    
    # Test settings
    print(f"✅ FRONTEND_URL: {settings.FRONTEND_URL}")
    print(f"✅ EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"✅ DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print()
    
    # Check if we have a test user
    try:
        user = User.objects.filter(email='test@example.com').first()
        if not user:
            print("Creating test user...")
            user = User.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='testpass123',
                first_name='Test',
                last_name='User'
            )
        
        print(f"✅ Test user: {user.username} ({user.email})")
        
        # Create or get email verification
        verification, created = EmailVerification.objects.get_or_create(
            user=user,
            defaults={'is_verified': False}
        )
        
        if not created:
            # Reset verification for testing
            verification.is_verified = False
            verification.save()
        
        print(f"✅ Verification token: {verification.token}")
        print(f"✅ Verification URL: {settings.FRONTEND_URL}/verify-email?token={verification.token}")
        print()
        
        # Test the verification endpoint
        client = Client()
        
        # Test with valid token
        print("🧪 Testing verification endpoint with valid token...")
        response = client.get(f'/auth/verify-email/?token={verification.token}')
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Check if verification was updated
        verification.refresh_from_db()
        print(f"✅ Verification status: {'Verified' if verification.is_verified else 'Not verified'}")
        print()
        
        # Test with invalid token
        print("🧪 Testing verification endpoint with invalid token...")
        response = client.get('/auth/verify-email/?token=invalid-token-123')
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
        
        # Test with missing token
        print("🧪 Testing verification endpoint with missing token...")
        response = client.get('/auth/verify-email/')
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
        
        # Test email sending (if not console backend)
        if settings.EMAIL_BACKEND != 'django.core.mail.backends.console.EmailBackend':
            print("🧪 Testing email sending...")
            try:
                # Reset verification for email test
                verification.is_verified = False
                verification.save()
                
                send_verification_email(user, verification.token)
                print("✅ Verification email sent successfully!")
            except Exception as e:
                print(f"❌ Email sending failed: {str(e)}")
        else:
            print("📧 Email backend is console - check console output for email content")
        
    except Exception as e:
        print(f"❌ Error in verification flow test: {str(e)}")
        import traceback
        traceback.print_exc()

def test_frontend_api_call():
    """Test the API call as frontend would make it"""
    print("\n" + "="*50)
    print("🌐 Testing Frontend API Call...")
    print("="*50)
    
    client = Client()
    
    # Simulate how frontend calls the API
    try:
        user = User.objects.filter(email='test@example.com').first()
        if user:
            verification = EmailVerification.objects.filter(user=user).first()
            if verification:
                # Reset for testing
                verification.is_verified = False
                verification.save()
                
                # Test API call with proper headers (simulating frontend)
                response = client.get(
                    f'/auth/verify-email/?token={verification.token}',
                    HTTP_ACCEPT='application/json',
                    HTTP_CONTENT_TYPE='application/json'
                )
                
                print(f"Status: {response.status_code}")
                print(f"Headers: {dict(response.items())}")
                print(f"Content: {response.content.decode()}")
                
                if response.status_code == 200:
                    print("✅ API call successful!")
                else:
                    print("❌ API call failed!")
                    
    except Exception as e:
        print(f"❌ Frontend API test failed: {str(e)}")

if __name__ == '__main__':
    test_verification_flow()
    test_frontend_api_call()
    print("\n🎉 Verification flow testing complete!")
