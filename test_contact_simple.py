#!/usr/bin/env python3

"""
Contact Form Test - Simple version
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fc_backend.settings')
django.setup()

from django.conf import settings
from django.test import Client
import json

def test_contact_form():
    """Test contact form submission"""
    print("🧪 Testing Contact Form...")
    
    # Print current settings
    print(f"Email Backend: {settings.EMAIL_BACKEND}")
    print(f"Contact Email: {getattr(settings, 'CONTACT_FORM_EMAIL', 'NOT SET')}")
    print(f"From Email: {getattr(settings, 'DEFAULT_FROM_EMAIL', 'NOT SET')}")
    
    # Test data
    test_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email_address': 'john.doe@example.com',
        'phone': '1234567890',
        'message': 'This is a test message.'
    }
    
    client = Client()
    
    try:
        # Test the contact form endpoint
        response = client.post(
            '/api/contact/submit/',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 201:
            print("✅ Contact form working!")
        else:
            print("❌ Contact form failed!")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    test_contact_form()
