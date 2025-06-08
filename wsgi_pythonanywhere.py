# WSGI config for PythonAnywhere deployment
# This file should be placed in your PythonAnywhere web app configuration

import os
import sys

# Add your project directory to Python path
path = '/home/yourusername/fc_backend'  # Update with your actual username
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables for production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fc_backend.settings')
os.environ.setdefault('DEBUG', 'False')
os.environ.setdefault('SECRET_KEY', 'your-secret-key-here')  # Generate a secure key

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
