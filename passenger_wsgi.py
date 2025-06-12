import os
import sys
from pathlib import Path

# Add your project directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fc_backend.settings')

# Import Django application
from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler

# Get the WSGI application
application = get_wsgi_application()

# Wrap with static files handler for development/shared hosting
# In production with proper web server, this is not needed
if os.environ.get('DEBUG', 'False') == 'True':
    application = StaticFilesHandler(application)
