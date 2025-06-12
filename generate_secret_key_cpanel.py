#!/usr/bin/env python
"""
Django secret key generator for cPanel deployment.
Run this script to generate a secure secret key for your Django application.
"""

import secrets
import string

def generate_secret_key(length=50):
    """Generate a Django secret key."""
    characters = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    secret_key = ''.join(secrets.choice(characters) for _ in range(length))
    return secret_key

if __name__ == '__main__':
    key = generate_secret_key()
    print("Generated Django Secret Key:")
    print(f"SECRET_KEY={key}")
    print("\nAdd this to your .env file or cPanel environment variables.")
