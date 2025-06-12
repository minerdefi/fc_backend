# 🚀 Simple cPanel Deployment with SQLite

## ✅ Why SQLite for cPanel?

- **No Database Setup Required** - SQLite database file is created automatically
- **Simplified Deployment** - No need to create MySQL databases or configure connections
- **Perfect for Small to Medium Apps** - Handles thousands of concurrent users efficiently
- **Zero Configuration** - Works out of the box with your Django app
- **File-based** - Easy to backup and migrate

## 📋 Super Simple 6-Step Deployment

### Step 1: Prepare Your Files (2 minutes)
```powershell
# In your backend directory, create deployment package
powershell .\create_cpanel_package.ps1
```
This creates a ZIP file ready for upload.

### Step 2: Upload to cPanel (3 minutes)
1. Log into your cPanel
2. Go to **File Manager**
3. Upload the created ZIP file to your desired directory
4. **Extract** the ZIP file

### Step 3: Create Python App (2 minutes)
1. In cPanel, go to **"Setup Python App"**
2. Click **"Create Application"**
3. Set these values:
   - **Python Version**: 3.8+ (latest available)
   - **Application Root**: `fc_backend` (your extracted folder)
   - **Application URL**: `/api`
   - **Startup File**: `passenger_wsgi.py`
4. Click **"Create"**

### Step 4: Configure Environment (1 minute)
1. In your extracted `fc_backend` folder, copy `.env.cpanel` to `.env`
2. Edit `.env` file and change these lines:
   ```bash
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   FRONTEND_URL=https://yourdomain.com
   ```
   Replace `yourdomain.com` with your actual domain.

### Step 5: Install & Setup (2 minutes)
In your cPanel Python App terminal or SSH, run:
```bash
pip install -r requirements_cpanel.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### Step 6: Configure Web Access (1 minute)
1. Upload `.htaccess` file to your domain's `public_html` directory
2. Edit `.htaccess` and update paths to match your setup

## 🎉 That's It! Your API is Live!

**Your Django API will be available at:**
- **API Root**: `https://yourdomain.com/api/`
- **Admin Panel**: `https://yourdomain.com/api/admin/`

## 🔧 What Makes This So Simple?

### SQLite Benefits:
✅ **No database server setup**  
✅ **No connection strings to configure**  
✅ **No database user creation**  
✅ **No privileges to manage**  
✅ **Automatic database creation**  
✅ **Built into Python**  

### Files Created Automatically:
- `db.sqlite3` - Your database (created on first migration)
- `staticfiles/` - Static files (created by collectstatic)
- Log files for debugging

## 📊 SQLite Performance Notes

**Perfect for:**
- Personal projects
- Small business websites
- Portfolio sites
- Development/staging environments
- Apps with < 100,000 requests/day

**Considerations:**
- Single file database (easy backup)
- No concurrent writes (reads are unlimited)
- Great performance for read-heavy applications
- File-based - moves with your code

## 🔄 Upgrading to External Database Later

If you need to upgrade to MySQL/PostgreSQL later:

1. Set `USE_DATABASE_URL=true` in your `.env`
2. Add `DATABASE_URL=mysql://...` with your database details
3. Run migrations: `python manage.py migrate`
4. Your data will be migrated to the new database

## 🛠️ Quick Troubleshooting

### If API doesn't load:
- Check cPanel error logs
- Verify `passenger_wsgi.py` has 755 permissions
- Ensure `.htaccess` paths are correct

### If admin login fails:
- Run `python manage.py createsuperuser` again
- Check that migrations completed successfully

### If static files don't load:
- Run `python manage.py collectstatic --noinput`
- Check `.htaccess` static file rules

## 📱 Update Frontend

After deployment, update your frontend's API URL:
```bash
# In your frontend .env.local
NEXT_PUBLIC_API_URL=https://yourdomain.com/api
```

## 🎯 Total Deployment Time: ~11 Minutes

This is the **fastest way** to deploy Django on cPanel! No database complications, no complex configurations - just upload, configure, and go live! 🚀

---

**Need the detailed version?** See `CPANEL_STEP_BY_STEP.md` for comprehensive instructions.
