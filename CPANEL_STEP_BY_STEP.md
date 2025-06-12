# 🚀 Step-by-Step cPanel Deployment Guide

## ✅ Pre-Deployment Requirements

### 1. cPanel Account Requirements
- [ ] **cPanel hosting account** with Python 3.8+ support
- [ ] **SSH access** (recommended but optional)
- [ ] **MySQL database** capability
- [ ] **Domain or subdomain** configured
- [ ] **SSL certificate** (recommended)

### 2. Local Project Preparation
- [ ] Django project tested locally ✅ (Already done)
- [ ] All cPanel config files created ✅ (Already done)
- [ ] Secret key generated ✅ (Already done)

---

## 🏗️ STEP 1: cPanel Account Setup

### 1.1 Create MySQL Database
1. **Login to cPanel**
2. **Go to "MySQL Databases"**
3. **Create Database:**
   - Database Name: `your_cpanel_username_fc_backend`
   - Example: `johnsmith_fc_backend`
4. **Create Database User:**
   - Username: `your_cpanel_username_fcuser`
   - Password: Generate strong password (save it!)
5. **Add User to Database:**
   - Select user and database
   - Grant **ALL PRIVILEGES**
6. **Note Down Database Details:**
   ```
   Database: your_cpanel_username_fc_backend
   Username: your_cpanel_username_fcuser
   Password: [your_generated_password]
   Host: localhost
   ```

### 1.2 Set Up Python App
1. **Go to "Setup Python App" or "Python App"**
2. **Create New Application:**
   - **Python Version:** 3.8+ (choose latest available)
   - **Application Root:** `fc_backend` (or `public_html/fc_backend`)
   - **Application URL:** Leave blank for root, or `/api` for subdirectory
   - **Application Startup File:** `passenger_wsgi.py`
3. **Click "Create"**
4. **Note the Python Path** shown (you'll need this)

---

## 📦 STEP 2: Upload Project Files

### 2.1 Prepare Project for Upload
1. **Open PowerShell in your project directory:**
   ```powershell
   cd c:\lets_see\fc_fullstack\fc_backend
   ```

2. **Create deployment ZIP file:**
   ```powershell
   # Exclude sensitive files and create clean ZIP
   Compress-Archive -Path * -DestinationPath fc_backend_cpanel.zip -Exclude "db.sqlite3", ".env*", "__pycache__", "*.pyc", ".git*", "venv", "env"
   ```

### 2.2 Upload to cPanel
1. **Login to cPanel File Manager**
2. **Navigate to your application root directory**
   - Usually: `public_html/fc_backend` or just `fc_backend`
3. **Upload `fc_backend_cpanel.zip`**
4. **Right-click ZIP file → Extract**
5. **Delete the ZIP file after extraction**

### 2.3 Set File Permissions
1. **Select all directories → Set to 755**
2. **Select all files → Set to 644**
3. **Set `passenger_wsgi.py` → 755**
4. **Set `deploy_cpanel.sh` → 755** (if using SSH)

---

## ⚙️ STEP 3: Configure Environment

### 3.1 Create Production Environment File
1. **In File Manager, create new file: `.env`**
2. **Copy content from `.env.cpanel` and update:**

```bash
# Production Environment Configuration
DEBUG=False
SECRET_KEY=FtzJBTb4fsqa=j=bc3=7xJNT4YFD@yu^M0Yd@470*du5-

# Database (replace with YOUR details)
DATABASE_URL=mysql://your_cpanel_username_fcuser:YOUR_DB_PASSWORD@localhost/your_cpanel_username_fc_backend

# Domains (replace with YOUR domain)
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
FRONTEND_URL=https://yourdomain.com

# Email (configure with your cPanel email)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=mail.yourdomain.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your_email_password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
CONTACT_FORM_EMAIL=contact@yourdomain.com
```

### 3.2 Update Database Configuration
**Replace these placeholders with your actual values:**
- `your_cpanel_username_fcuser` → Your database username
- `YOUR_DB_PASSWORD` → Your database password  
- `your_cpanel_username_fc_backend` → Your database name
- `yourdomain.com` → Your actual domain

---

## 🔧 STEP 4: Install Dependencies

### 4.1 Access Python Environment
**Option A: Using cPanel Python App Interface**
1. Go to "Setup Python App"
2. Click on your app
3. Click "Open Terminal" or "Enter to the virtual environment"

**Option B: Using SSH (if available)**
```bash
ssh your_username@yourdomain.com
cd fc_backend
source fc_backend/bin/activate  # Path may vary
```

### 4.2 Install Requirements
```bash
pip install -r requirements_cpanel.txt
```

### 4.3 Verify Installation
```bash
pip list | grep -i django
# Should show Django and other packages
```

---

## 🗄️ STEP 5: Database Setup

### 5.1 Run Database Migrations
```bash
python manage.py migrate
```

### 5.2 Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 5.3 Create Superuser
```bash
python manage.py createsuperuser
```
- Enter username, email, and password for admin access

### 5.4 Test Database Connection
```bash
python manage.py shell
```
```python
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT 1")
print("Database connection successful!")
exit()
```

---

## 🌐 STEP 6: Configure Web Server

### 6.1 Set Up URL Routing
1. **Copy `.htaccess` to your domain's `public_html` directory**
2. **Edit `.htaccess` and update paths:**

```apache
# Update these paths to match your setup
RewriteRule ^static/(.*)$ /fc_backend/staticfiles/$1 [L]
RewriteRule ^media/(.*)$ /fc_backend/media/$1 [L]
RewriteRule ^api/(.*)$ /fc_backend/passenger_wsgi.py/$1 [L]
```

### 6.2 Update Domain References
**In `.htaccess`, replace `yourdomain.com` with your actual domain:**
```apache
SetEnvIf Origin "^https?://(.*\.)?YOURDOMAIN\.com(:[0-9]+)?$" CORS_ORIGIN=$0
```

---

## 🧪 STEP 7: Testing & Verification

### 7.1 Test API Endpoints
1. **API Root:** `https://yourdomain.com/api/`
   - Should return Django REST framework browseable API
2. **Admin Panel:** `https://yourdomain.com/api/admin/`
   - Should show Django admin login
3. **Health Check:** `https://yourdomain.com/api/health/` (if you have one)

### 7.2 Test Database Operations
1. **Login to admin panel**
2. **Try creating a test user or contact entry**
3. **Verify data persists**

### 7.3 Test CORS (if you have frontend)
1. **Open browser developer tools**
2. **Make API request from your frontend**
3. **Check for CORS errors in console**

---

## 🔍 STEP 8: Troubleshooting Common Issues

### 8.1 500 Internal Server Error
**Check cPanel Error Logs:**
1. Go to "Error Logs" in cPanel
2. Look for Python/Django errors
3. Common fixes:
   - Check file permissions
   - Verify `.env` file syntax
   - Ensure all dependencies installed

### 8.2 Database Connection Issues
```bash
# Test database connection manually
python manage.py dbshell
# If this fails, check DATABASE_URL in .env
```

### 8.3 Static Files Not Loading
```bash
# Re-collect static files
python manage.py collectstatic --clear --noinput
```

### 8.4 ImportError or Module Not Found
```bash
# Reinstall requirements
pip install -r requirements_cpanel.txt --force-reinstall
```

---

## 📱 STEP 9: Frontend Integration

### 9.1 Update Frontend Configuration
**In your frontend project, update API URL:**
```javascript
// .env.local or .env.production
NEXT_PUBLIC_API_URL=https://yourdomain.com/api
```

### 9.2 Test Frontend-Backend Communication
1. **Deploy your frontend** (Netlify, Vercel, etc.)
2. **Test API calls from frontend**
3. **Verify authentication works**
4. **Test file uploads** (if applicable)

---

## 🛡️ STEP 10: Security & Production Setup

### 10.1 Enable SSL (if not already)
1. **Go to "SSL/TLS" in cPanel**
2. **Enable "Force HTTPS Redirect"**
3. **Update Django settings if needed:**
   ```python
   SECURE_SSL_REDIRECT = True
   ```

### 10.2 Set Up Backups
1. **Database backup:** Use cPanel backup tools
2. **File backup:** Regular file system backups
3. **Test restore process**

### 10.3 Monitor Performance
1. **Check resource usage** in cPanel
2. **Monitor error logs regularly**
3. **Set up uptime monitoring**

---

## ✅ DEPLOYMENT COMPLETE!

### 🎉 Your Django API is now live at:
- **API Root:** `https://yourdomain.com/api/`
- **Admin Panel:** `https://yourdomain.com/api/admin/`

### 📋 Final Checklist:
- [ ] Database created and configured
- [ ] Python app set up in cPanel
- [ ] Project files uploaded and extracted
- [ ] Environment variables configured
- [ ] Dependencies installed
- [ ] Database migrated
- [ ] Static files collected
- [ ] Superuser created
- [ ] URL routing configured
- [ ] API endpoints tested
- [ ] Frontend integrated (if applicable)
- [ ] SSL enabled
- [ ] Backups configured

### 🔄 Next Steps:
1. **Update your frontend** to use the new API URL
2. **Test all functionality** thoroughly
3. **Set up monitoring** and alerts
4. **Document your deployment** for future reference

---

## 📞 Support & Resources

### If you encounter issues:
1. **Check cPanel error logs** first
2. **Review this checklist** step by step
3. **Test each component** individually
4. **Contact your hosting provider** for cPanel-specific issues

### Useful cPanel Paths:
- **Application Root:** Usually `/home/username/fc_backend/`
- **Public HTML:** `/home/username/public_html/`
- **Python Path:** Shown in Python App interface
- **Error Logs:** Available in cPanel Error Logs section

**🎊 Congratulations! Your Django backend is now successfully deployed on cPanel!**
