# Email Configuration Guide

## How Email Settings Work in This Project

### Current Configuration ✅

The project now uses **environment variables** for email configuration, which means:

1. **Settings.py** reads from environment variables (`.env` file)
2. **Fallback values** are provided for development
3. **Production values** come from your `.env` file

### Email Configuration Priority

```
Environment Variables (.env file) > Django Settings Fallbacks
```

## Configuration Files

### 1. Django Settings (`fc_backend/settings.py`)
```python
# Email settings (now reads from environment variables)
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '1025'))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'your-email@example.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'your-email-password')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@fgpremiumfunds.com')
CONTACT_FORM_EMAIL = os.environ.get('CONTACT_FORM_EMAIL', 'contact@fgpremiumfunds.com')
```

### 2. Environment Variables (`.env.cpanel`)
```bash
# Email settings for production (cPanel)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=mail.fgpremiumfunds.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@fgpremiumfunds.com
EMAIL_HOST_PASSWORD=your-actual-email-password
DEFAULT_FROM_EMAIL=noreply@fgpremiumfunds.com
CONTACT_FORM_EMAIL=contact@fgpremiumfunds.com
```

## Configuration for Different Environments

### Development (Local)
- **Default**: Console backend (prints emails to console)
- **Override**: Create `.env` file with your email settings

### Production (cPanel)
- **Required**: Create `.env` file with actual email credentials
- **Uses**: SMTP backend with your cPanel email settings

## cPanel Email Setup Steps

### 1. Create Email Accounts in cPanel
1. Go to cPanel → Email Accounts
2. Create these accounts:
   - `noreply@fgpremiumfunds.com` (for sending emails)
   - `contact@fgpremiumfunds.com` (for receiving contact forms)

### 2. Get Email Settings from cPanel
- **SMTP Server**: Usually `mail.yourdomain.com`
- **Port**: 587 (TLS) or 465 (SSL)
- **Authentication**: Required
- **Username**: Full email address
- **Password**: Email account password

### 3. Update .env File
```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=mail.fgpremiumfunds.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@fgpremiumfunds.com
EMAIL_HOST_PASSWORD=your-actual-password-here
DEFAULT_FROM_EMAIL=noreply@fgpremiumfunds.com
CONTACT_FORM_EMAIL=contact@fgpremiumfunds.com
```

## Email Backends Available

### 1. Console Backend (Development)
```bash
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```
- Prints emails to console/terminal
- Good for development and testing

### 2. SMTP Backend (Production)
```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
```
- Sends real emails via SMTP server
- Required for production

### 3. File Backend (Testing)
```bash
EMAIL_BACKEND=django.core.mail.backends.filebased.EmailBackend
EMAIL_FILE_PATH=tmp/app-messages  # Optional
```
- Saves emails to files
- Good for testing without sending real emails

## Testing Email Configuration

### 1. Django Shell Test
```python
python manage.py shell

# Test email sending
from django.core.mail import send_mail
from django.conf import settings

send_mail(
    'Test Subject',
    'Test message',
    settings.DEFAULT_FROM_EMAIL,
    ['test@example.com'],
    fail_silently=False,
)
```

### 2. Contact Form Test
- Visit your contact form
- Submit a test message
- Check if email is sent/received

## Troubleshooting

### Common Issues

1. **SMTP Authentication Failed**
   - Check email username/password
   - Verify email account exists in cPanel

2. **Connection Refused**
   - Check EMAIL_HOST (usually `mail.yourdomain.com`)
   - Check EMAIL_PORT (587 for TLS, 465 for SSL)

3. **TLS/SSL Issues**
   - Try `EMAIL_USE_TLS=True` with port 587
   - Try `EMAIL_USE_SSL=True` with port 465

### Debug Settings
Add to `.env` for debugging:
```bash
# Email debugging
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_TIMEOUT=30
```

## Current Status

✅ **Email configuration now uses environment variables**
✅ **Production settings ready for cPanel**
✅ **Development fallbacks in place**
✅ **Domain updated to fgpremiumfunds.com**
✅ **Missing ADMIN_EMAIL and FRONTEND_URL settings added**
✅ **Password reset HTML template created**
✅ **Admin notification HTML template created**
✅ **All email functions now use proper HTML templates**
✅ **Email testing utility created**

## Testing Your Email Setup

### Quick Test Script
Run the email testing utility:
```bash
python test_email_functionality.py
```

This will test:
- ✅ Email configuration loading
- ✅ Simple email sending
- ✅ HTML email sending
- ✅ Contact form notifications
- ✅ Email verification templates
- ✅ Password reset templates
- ✅ Admin notification templates

## Next Steps

1. **Create email accounts in cPanel**
2. **Update .env file with actual credentials**
3. **Run email testing utility: `python test_email_functionality.py`**
4. **Test email functionality end-to-end**
5. **Deploy to production**

## Email Accounts Needed for cPanel

Create these email accounts in your cPanel:
```bash
noreply@fgpremiumfunds.com    # For sending system emails
admin@fgpremiumfunds.com      # For receiving admin notifications
contact@fgpremiumfunds.com    # For receiving contact form submissions
```

## Complete Environment Variables List

```bash
# Email Configuration (add to .env file)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=mail.fgpremiumfunds.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@fgpremiumfunds.com
EMAIL_HOST_PASSWORD=your-actual-password
DEFAULT_FROM_EMAIL=noreply@fgpremiumfunds.com
CONTACT_FORM_EMAIL=contact@fgpremiumfunds.com
ADMIN_EMAIL=admin@fgpremiumfunds.com
FRONTEND_URL=https://fgpremiumfunds.com
```

The **environment variables (.env file)** now take priority over hardcoded settings, giving you full control over email configuration in different environments!
