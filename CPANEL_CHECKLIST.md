# cPanel Django Deployment Checklist

## ✅ Pre-Deployment Checklist

### 1. cPanel Account Setup
- [ ] Verify Python support in cPanel (Python 3.8+ recommended)
- [ ] Check if SSH access is available
- [ ] Verify database options (MySQL/PostgreSQL)
- [ ] Confirm domain/subdomain configuration

### 2. Project Preparation
- [ ] Test Django project locally
- [ ] Ensure all dependencies are in requirements_cpanel.txt
- [ ] Create .env.cpanel file with your settings
- [ ] Generate new SECRET_KEY for production

### 3. Database Setup
- [ ] Create MySQL database in cPanel
- [ ] Create database user with full privileges
- [ ] Note database connection details
- [ ] Test database connection

## 🚀 Deployment Steps

### Step 1: File Upload
- [ ] Compress fc_backend folder to ZIP
- [ ] Upload ZIP to cPanel File Manager
- [ ] Extract files to application directory
- [ ] Set proper file permissions (755 for directories, 644 for files)

### Step 2: Python App Configuration
- [ ] Create Python App in cPanel
- [ ] Set Python version (3.8+)
- [ ] Set application root to fc_backend
- [ ] Set startup file to passenger_wsgi.py
- [ ] Configure application URL path

### Step 3: Environment Setup
- [ ] Create .env file from .env.cpanel template
- [ ] Set DEBUG=False
- [ ] Configure SECRET_KEY
- [ ] Set DATABASE_URL with cPanel database details
- [ ] Add your domain to ALLOWED_HOSTS
- [ ] Configure FRONTEND_URL

### Step 4: Dependencies Installation
- [ ] Access Python app environment
- [ ] Run: `pip install -r requirements_cpanel.txt`
- [ ] Verify all packages installed successfully

### Step 5: Database Migration
- [ ] Run: `python manage.py migrate`
- [ ] Run: `python manage.py collectstatic --noinput`
- [ ] Create superuser: `python manage.py createsuperuser`

### Step 6: Web Server Configuration
- [ ] Upload .htaccess to public_html (if serving from domain root)
- [ ] Configure URL rewriting rules
- [ ] Set up static file serving
- [ ] Configure CORS headers

## 🧪 Testing Checklist

### API Testing
- [ ] Test API root: `https://yourdomain.com/api/`
- [ ] Test admin panel: `https://yourdomain.com/api/admin/`
- [ ] Test authentication endpoints
- [ ] Test contact form submission
- [ ] Verify static files loading

### Frontend Integration
- [ ] Update frontend API_URL to point to cPanel
- [ ] Test CORS functionality
- [ ] Verify all API calls work from frontend
- [ ] Test file uploads (if applicable)

### Performance Testing
- [ ] Check page load times
- [ ] Test concurrent user handling
- [ ] Verify database performance
- [ ] Check error handling

## 🔧 Configuration Files Created

### Core Files
- [x] `passenger_wsgi.py` - WSGI entry point for cPanel
- [x] `.env.cpanel` - Environment variables template
- [x] `requirements_cpanel.txt` - Optimized dependencies
- [x] `.htaccess` - Web server configuration

### Deployment Scripts
- [x] `deploy_cpanel.sh` - Linux/Mac deployment script
- [x] `deploy_cpanel.ps1` - Windows PowerShell script
- [x] `generate_secret_key_cpanel.py` - Secret key generator

### Documentation
- [x] `CPANEL_DEPLOYMENT.md` - Complete deployment guide

## 🚨 Troubleshooting Checklist

### If You Get 500 Internal Server Error
- [ ] Check cPanel error logs
- [ ] Verify passenger_wsgi.py permissions (755)
- [ ] Check Python version compatibility
- [ ] Verify all dependencies installed
- [ ] Check .env file syntax

### If Database Connection Fails
- [ ] Verify DATABASE_URL format
- [ ] Check database user privileges
- [ ] Ensure database exists
- [ ] Test connection from cPanel phpMyAdmin

### If Static Files Don't Load
- [ ] Run `python manage.py collectstatic`
- [ ] Check .htaccess static file rules
- [ ] Verify staticfiles directory permissions
- [ ] Check STATIC_URL and STATIC_ROOT settings

### If CORS Issues Occur
- [ ] Update CORS_ALLOWED_ORIGINS with your domain
- [ ] Check .htaccess CORS headers
- [ ] Verify frontend URL configuration
- [ ] Test with browser developer tools

## 📱 Environment Variables Template

```bash
# Copy to .env file in your project root
DEBUG=False
SECRET_KEY=your-generated-secret-key-here
DATABASE_URL=mysql://cpanel_user:password@localhost/cpanel_database
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
FRONTEND_URL=https://yourdomain.com
EMAIL_HOST=mail.yourdomain.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your-email-password
```

## 📞 Support Resources

### cPanel Documentation
- Python App setup guide
- Database management
- File Manager usage
- Error log access

### Django Resources
- Django deployment checklist
- Database configuration
- Static files handling
- Security best practices

## ✅ Post-Deployment Tasks

### Security
- [ ] Enable SSL certificate
- [ ] Configure security headers
- [ ] Set up database backups
- [ ] Review Django security settings

### Monitoring
- [ ] Set up error monitoring
- [ ] Configure log rotation
- [ ] Monitor resource usage
- [ ] Set up uptime monitoring

### Performance
- [ ] Enable compression
- [ ] Configure caching
- [ ] Optimize database queries
- [ ] Review static file serving

## 🎉 Deployment Complete!

Once all items are checked, your Django backend should be successfully deployed on cPanel and ready to serve your frontend application.

**Final API URL**: `https://yourdomain.com/api/`
