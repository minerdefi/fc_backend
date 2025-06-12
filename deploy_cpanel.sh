#!/bin/bash
# cPanel Deployment Script
# Run this script after uploading your Django project to cPanel

echo "🚀 Starting cPanel Django Deployment..."

# Install requirements
echo "📦 Installing Python dependencies..."
pip install -r requirements_cpanel.txt

# Generate secret key if not exists
if [ ! -f .env ]; then
    echo "🔑 Generating Django secret key..."
    python generate_secret_key_cpanel.py
    echo "⚠️  Please create .env file with the generated secret key"
fi

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

echo "✅ Deployment script completed!"
echo ""
echo "Next steps:"
echo "1. Create .env file with your database and secret key settings"
echo "2. Update ALLOWED_HOSTS in settings.py with your domain"
echo "3. Configure your cPanel Python app to point to passenger_wsgi.py"
echo "4. Test your API endpoints"
echo ""
echo "🌐 Your Django API should be available at: https://yourdomain.com/api/"
