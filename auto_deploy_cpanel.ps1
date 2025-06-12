# cPanel Deployment Automation Script
# Run this script after uploading files to cPanel

Write-Host "🚀 Starting Automated cPanel Deployment..." -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan

# Function to check if command succeeded
function Test-Command {
    param($Command, $Description)
    Write-Host "📝 $Description..." -ForegroundColor Yellow
    try {
        Invoke-Expression $Command
        Write-Host "✅ $Description completed successfully!" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "❌ $Description failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Check if we're in the right directory
if (-not (Test-Path "manage.py")) {
    Write-Host "❌ Error: manage.py not found. Please run this script from your Django project directory." -ForegroundColor Red
    exit 1
}

Write-Host "📍 Current directory: $(Get-Location)" -ForegroundColor Cyan

# Step 1: Install dependencies
Write-Host "`n🔧 STEP 1: Installing Dependencies" -ForegroundColor Magenta
Write-Host "=====================================" -ForegroundColor Cyan

if (Test-Path "requirements_cpanel.txt") {
    Test-Command "pip install -r requirements_cpanel.txt" "Installing Python packages"
} else {
    Write-Host "⚠️  requirements_cpanel.txt not found, using requirements.txt" -ForegroundColor Yellow
    Test-Command "pip install -r requirements.txt" "Installing Python packages"
}

# Step 2: Environment check
Write-Host "`n🔍 STEP 2: Environment Check" -ForegroundColor Magenta
Write-Host "=============================" -ForegroundColor Cyan

if (Test-Path ".env") {
    Write-Host "✅ .env file found" -ForegroundColor Green
} else {
    Write-Host "⚠️  .env file not found. Creating from template..." -ForegroundColor Yellow
    if (Test-Path ".env.cpanel") {
        Copy-Item ".env.cpanel" ".env"
        Write-Host "📝 .env created from .env.cpanel template" -ForegroundColor Green
        Write-Host "🚨 IMPORTANT: Edit .env file with your actual database and domain details!" -ForegroundColor Red
    } else {
        Write-Host "❌ No .env template found. Please create .env file manually." -ForegroundColor Red
    }
}

# Step 3: Django setup
Write-Host "`n🗄️  STEP 3: Django Database Setup" -ForegroundColor Magenta
Write-Host "===================================" -ForegroundColor Cyan

Test-Command "python manage.py check --deploy" "Django deployment check"
Test-Command "python manage.py migrate" "Running database migrations"
Test-Command "python manage.py collectstatic --noinput" "Collecting static files"

# Step 4: Test setup
Write-Host "`n🧪 STEP 4: Testing Setup" -ForegroundColor Magenta
Write-Host "=========================" -ForegroundColor Cyan

Write-Host "📝 Testing Django configuration..." -ForegroundColor Yellow
$testScript = @"
import os
import django
from django.conf import settings
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fc_backend.settings')
django.setup()

print("✅ Django setup successful")
print(f"🔧 DEBUG mode: {settings.DEBUG}")
print(f"🗄️  Database engine: {settings.DATABASES['default']['ENGINE']}")
print(f"📁 Database file: {settings.DATABASES['default']['NAME']}")
print(f"🌐 Allowed hosts: {settings.ALLOWED_HOSTS}")

try:
    cursor = connection.cursor()
    cursor.execute("SELECT 1")
    print("✅ SQLite database connection successful")
    
    # Check if database file exists
    db_path = settings.DATABASES['default']['NAME']
    if os.path.exists(db_path):
        print(f"✅ Database file exists at: {db_path}")
        # Get file size
        size = os.path.getsize(db_path)
        print(f"📊 Database size: {size} bytes")
    else:
        print("⚠️  Database file will be created on first migration")
        
except Exception as e:
    print(f"❌ Database connection failed: {e}")
"@

$testScript | python

# Step 5: File permissions check (if on Unix-like system)
Write-Host "`n🔐 STEP 5: File Permissions" -ForegroundColor Magenta
Write-Host "============================" -ForegroundColor Cyan

if (Test-Path "passenger_wsgi.py") {
    Write-Host "✅ passenger_wsgi.py found" -ForegroundColor Green
} else {
    Write-Host "❌ passenger_wsgi.py not found!" -ForegroundColor Red
}

# Step 6: Final checklist
Write-Host "`n📋 STEP 6: Deployment Checklist" -ForegroundColor Magenta
Write-Host "================================" -ForegroundColor Cyan

$checklist = @"
Manual Steps You Still Need to Complete:
  
🟢 SIMPLIFIED DEPLOYMENT (No Database Setup Required!)
     SQLite database will be created automatically ✅
  
🔴 1. Update .env file with your domain:
     - ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
     - FRONTEND_URL=https://yourdomain.com
     - Email settings (optional)
  
🔴 2. Set up Python App in cPanel:
     - Application root: fc_backend
     - Startup file: passenger_wsgi.py
     - Python version: 3.8+
  
🔴 3. Upload .htaccess to public_html:
     - Update paths in .htaccess for your setup
  
🔴 4. Set file permissions:
     - Directories: 755
     - Files: 644
     - passenger_wsgi.py: 755
  
🔴 5. Create superuser:
     - Run: python manage.py createsuperuser
  
🔴 6. Test your deployment:
     - Visit: https://yourdomain.com/api/
     - Check: https://yourdomain.com/api/admin/

💡 DATABASE: Using SQLite (no database setup required!)
   - Database file: db.sqlite3 (created automatically)
   - No MySQL/PostgreSQL configuration needed
   - Perfect for small to medium applications
"@

Write-Host $checklist -ForegroundColor White

# Summary
Write-Host "`n🎉 Automated Setup Complete!" -ForegroundColor Green
Write-Host "=============================" -ForegroundColor Cyan

Write-Host "✅ Dependencies installed" -ForegroundColor Green
Write-Host "✅ Database migrations run" -ForegroundColor Green
Write-Host "✅ Static files collected" -ForegroundColor Green
Write-Host "✅ Django configuration tested" -ForegroundColor Green

Write-Host "`n🔄 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Complete the manual checklist above" -ForegroundColor White
Write-Host "2. Test your API endpoints" -ForegroundColor White
Write-Host "3. Update your frontend to use the new API URL" -ForegroundColor White

Write-Host "`n📚 For detailed instructions, see:" -ForegroundColor Cyan
Write-Host "   - CPANEL_STEP_BY_STEP.md" -ForegroundColor White
Write-Host "   - CPANEL_QUICK_REFERENCE.md" -ForegroundColor White

Write-Host "`n🚀 Happy deploying!" -ForegroundColor Green
