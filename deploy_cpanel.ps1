# cPanel Deployment Script for Windows
# Run this script in PowerShell after uploading your Django project to cPanel

Write-Host "🚀 Starting cPanel Django Deployment..." -ForegroundColor Green

# Install requirements
Write-Host "📦 Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements_cpanel.txt

# Generate secret key if not exists
if (-not (Test-Path .env)) {
    Write-Host "🔑 Generating Django secret key..." -ForegroundColor Yellow
    python generate_secret_key_cpanel.py
    Write-Host "⚠️  Please create .env file with the generated secret key" -ForegroundColor Red
}

# Collect static files
Write-Host "📁 Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput

# Run migrations
Write-Host "🗄️  Running database migrations..." -ForegroundColor Yellow
python manage.py migrate

Write-Host "✅ Deployment script completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Create .env file with your database and secret key settings"
Write-Host "2. Update ALLOWED_HOSTS in settings.py with your domain"
Write-Host "3. Configure your cPanel Python app to point to passenger_wsgi.py"
Write-Host "4. Test your API endpoints"
Write-Host ""
Write-Host "🌐 Your Django API should be available at: https://yourdomain.com/api/" -ForegroundColor Green
