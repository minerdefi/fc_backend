# 📋 cPanel Deployment Quick Reference

## 🔑 Essential Information You'll Need

### Database Details (Fill in during setup):
```
Database Name: ________________________
Database User: ________________________  
Database Password: ____________________
Database Host: localhost
```

### Domain Information:
```
Your Domain: ___________________________
Frontend URL: __________________________
Email Host: ____________________________
```

### Generated Secret Key:
```
SECRET_KEY=FtzJBTb4fsqa=j=bc3=7xJNT4YFD!(iVD@yu^M0Yd@470*du5-
```

---

## ⚡ Quick Commands Reference

### Python Environment Setup:
```bash
# Install dependencies
pip install -r requirements_cpanel.txt

# Database setup
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser

# Test database
python manage.py shell
```

### File Permissions:
```
Directories: 755
Files: 644
passenger_wsgi.py: 755
```

---

## 🧪 Testing URLs

After deployment, test these URLs:
- [ ] `https://yourdomain.com/api/` - API Root
- [ ] `https://yourdomain.com/api/admin/` - Admin Panel
- [ ] `https://yourdomain.com/api/auth/` - Authentication
- [ ] `https://yourdomain.com/api/contact/` - Contact Form

---

## 🚨 Troubleshooting Quick Fixes

### 500 Error:
1. Check cPanel Error Logs
2. Verify file permissions
3. Check .env file syntax

### Database Issues:
1. Test: `python manage.py dbshell`
2. Verify DATABASE_URL in .env
3. Check database user privileges

### Static Files:
1. Run: `python manage.py collectstatic --clear --noinput`
2. Check .htaccess paths
3. Verify file permissions

---

## 📞 Emergency Contacts

- **Hosting Provider Support:** ________________
- **Domain Registrar:** _______________________
- **DNS Provider:** ___________________________

---

**🎯 Success Criteria:**
- API returns data at `/api/`
- Admin panel accessible
- No 500 errors in logs
- Frontend can connect to API
