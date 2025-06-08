# PythonAnywhere Deployment Guide for FG Premium Backend

## Prerequisites
1. Create a PythonAnywhere account (free tier available)
2. Have your Django project ready (which you do!)

## Step-by-Step Deployment

### 1. Upload Your Code
1. Log into your PythonAnywhere dashboard
2. Open a Bash console
3. Clone your repository:
   ```bash
   git clone https://github.com/minerdefi/fc_backend.git
   cd fc_backend
   ```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python3.10 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Database
```bash
# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### 4. Configure Web App
1. Go to PythonAnywhere Dashboard → Web
2. Click "Add a new web app"
3. Choose "Manual configuration" → Python 3.10
4. Configure the following:

**Source code:** `/home/yourusername/fc_backend`
**Working directory:** `/home/yourusername/fc_backend`

**Virtualenv:** `/home/yourusername/fc_backend/venv`

**WSGI configuration file:** Edit the auto-generated file and replace with:
```python
import os
import sys

# Add your project directory to Python path
path = '/home/yourusername/fc_backend'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fc_backend.settings')
os.environ.setdefault('DEBUG', 'False')
os.environ.setdefault('SECRET_KEY', 'your-secret-key-here')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 5. Configure Static Files
In the Web app configuration, add:
- **URL:** `/static/`
- **Directory:** `/home/yourusername/fc_backend/staticfiles/`

- **URL:** `/media/`
- **Directory:** `/home/yourusername/fc_backend/media/`

### 6. Environment Variables
Create a `.env` file in your project root by copying the template:
```bash
# Copy the template file
cp .env.pythonanywhere .env

# Edit the .env file with your actual values
nano .env
```

Update these key values in your `.env` file:
```bash
DEBUG=False
SECRET_KEY=your-very-secure-secret-key-generate-new-one
ALLOWED_HOSTS=yourusername.pythonanywhere.com,localhost,127.0.0.1
FRONTEND_URL=https://your-frontend-domain.com
```

**Important:** Generate a new SECRET_KEY for production using:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 7. Update Settings for PythonAnywhere
Your Django settings should include:
```python
ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1', 
    '.pythonanywhere.com',
    'yourusername.pythonanywhere.com',  # Replace with your actual username
    'fgpremiumfunds.com'
]

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://fgpremiumfunds.com",
    "https://wondrous-crumble-ab82ec.netlify.app",
    # Add your frontend URL here
]
```

### 8. Test Your Deployment
1. Click "Reload" in your web app configuration
2. Visit `https://yourusername.pythonanywhere.com`
3. Test your API endpoints:
   - `https://yourusername.pythonanywhere.com/api/health/`
   - `https://yourusername.pythonanywhere.com/admin/`

## Important Notes

### Database
- Free accounts use SQLite (which is already configured)
- For MySQL, upgrade to paid account and update DATABASE_URL

### Domain
- Free accounts get: `yourusername.pythonanywhere.com`
- Custom domains require paid accounts

### Debugging
- Check error logs in Web tab → Error log
- Use `print()` statements for debugging (they appear in error log)
- Console access available for troubleshooting

### File Structure on PythonAnywhere
```
/home/yourusername/
├── fc_backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── db.sqlite3
│   ├── fc_backend/
│   │   ├── settings.py
│   │   ├── wsgi.py
│   │   └── ...
│   ├── api/
│   ├── authentication/
│   ├── contact/
│   ├── staticfiles/
│   ├── media/
│   └── venv/
```

## Post-Deployment Checklist
- [ ] Web app loads without errors
- [ ] API endpoints respond correctly
- [ ] Static files serve properly
- [ ] Admin panel accessible
- [ ] CORS configured for frontend
- [ ] Environment variables set
- [ ] Database migrations applied

## Frontend Integration
After deployment, update your frontend `.env.local`:
```
NEXT_PUBLIC_API_URL=https://yourusername.pythonanywhere.com
```

## Maintenance
- To update code: `git pull` in the console, then reload web app
- To install new packages: activate venv, `pip install package`, then reload
- Monitor usage in Dashboard to avoid hitting free tier limits

Your Django backend will be available at: `https://yourusername.pythonanywhere.com`
