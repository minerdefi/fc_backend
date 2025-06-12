# Django Backend Deployment Guide for cPanel

This guide will help you deploy your Django backend to a cPanel shared hosting environment.

## Prerequisites

1. **cPanel hosting account** with Python support (most modern cPanel hosts support Python 3.8+)
2. **SSH access** (optional but recommended)
3. **MySQL/PostgreSQL database** (available through cPanel)

## Step 1: Prepare Your cPanel Environment

### 1.1 Create Python App in cPanel
1. Log into your cPanel
2. Go to "Setup Python App" or "Python App" section
3. Create a new Python application:
   - **Python Version**: 3.8+ (latest available)
   - **Application Root**: `fc_backend`
   - **Application URL**: `/api` (or your preferred path)
   - **Application startup file**: `passenger_wsgi.py`
4. Click "Create"

### 1.2 Create Database
1. In cPanel, go to "MySQL Databases"
2. Create a new database: `your_username_fc_backend`
3. Create a database user with all privileges
4. Note down the database details

## Step 2: Upload Your Django Project

### 2.1 Upload Files
1. Compress your `fc_backend` folder into a ZIP file
2. Upload via cPanel File Manager to your application root directory
3. Extract the files

### 2.2 Install Dependencies
1. Access your Python app environment (through cPanel or SSH)
2. Install requirements:
```bash
pip install -r requirements.txt
```

## Step 3: Configure Your Django Application

### 3.1 Environment Variables
Create a `.env` file in your project root with the following:

```bash
DEBUG=False
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=mysql://username:password@localhost/database_name
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
FRONTEND_URL=https://yourdomain.com
```

### 3.2 Update Settings
Your `settings.py` is already configured to work with cPanel. Make sure these settings are correct:
- `DEBUG=False` for production
- `ALLOWED_HOSTS` includes your domain
- Database configuration uses environment variables

## Step 4: Create Required Files

The following files have been created for you:

1. **passenger_wsgi.py** - WSGI application entry point for cPanel
2. **.htaccess** - URL rewriting rules
3. **requirements_cpanel.txt** - Dependencies optimized for shared hosting
4. **.env.cpanel** - Environment variables template

## Step 5: Database Migration

1. Run migrations through SSH or cPanel Python app terminal:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

## Step 6: Configure Static Files

1. Your static files will be served from the `staticfiles` directory
2. Make sure your `.htaccess` file is configured to serve static files
3. Update your frontend to point to the correct static file URLs

## Step 7: Testing

1. Test your API endpoints: `https://yourdomain.com/api/`
2. Check Django admin: `https://yourdomain.com/api/admin/`
3. Verify CORS settings work with your frontend

## Troubleshooting

### Common Issues:

1. **500 Internal Server Error**
   - Check error logs in cPanel
   - Verify all dependencies are installed
   - Check file permissions

2. **Database Connection Issues**
   - Verify database credentials in `.env`
   - Check if database exists and user has privileges

3. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check `.htaccess` configuration
   - Verify file permissions

4. **CORS Issues**
   - Update `CORS_ALLOWED_ORIGINS` in settings.py
   - Add your frontend domain

### File Permissions
Set these permissions via cPanel File Manager:
- **Directories**: 755
- **Files**: 644
- **passenger_wsgi.py**: 755

## Environment Variables Reference

```bash
# Required
SECRET_KEY=your-django-secret-key
DEBUG=False
DATABASE_URL=mysql://user:pass@localhost/dbname

# Optional
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
FRONTEND_URL=https://yourdomain.com
EMAIL_HOST=mail.yourdomain.com
EMAIL_PORT=587
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your-email-password
```

## Support

If you encounter issues:
1. Check cPanel error logs
2. Contact your hosting provider for Python app support
3. Verify all environment variables are set correctly

## Next Steps

After successful deployment:
1. Update your frontend API URLs to point to your cPanel deployment
2. Test all API endpoints
3. Set up SSL certificate if not already configured
4. Configure email settings for contact forms
