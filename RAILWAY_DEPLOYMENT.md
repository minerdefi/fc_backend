# Railway Deployment Guide for FG Premium Backend

## Prerequisites
1. Railway account (https://railway.app)
2. GitLab repository with your Django backend code
3. PostgreSQL database addon (recommended)

## Deployment Steps

### 1. Create New Railway Project
```bash
# Install Railway CLI (optional)
npm install -g @railway/cli

# Login to Railway
railway login
```

### 2. Connect GitLab Repository
1. Go to Railway Dashboard
2. Click "New Project"
3. Select "Deploy from GitLab repo"
4. Choose your repository: `https://gitlab.com/fg5654823/fg.git`
5. Select the main branch

### 3. Add PostgreSQL Database
1. In your Railway project dashboard
2. Click "New" → "Database" → "Add PostgreSQL"
3. Railway will automatically set the `DATABASE_URL` environment variable

### 4. Configure Environment Variables
Go to your service settings and add these variables:

```
DEBUG=False
SECRET_KEY=your-generated-secret-key-here
ALLOWED_HOSTS=.railway.app,.up.railway.app
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com,http://localhost:3000
```

### 5. Deploy
1. Railway will automatically detect your Django app
2. It will use the `railway.json` configuration
3. The build process will:
   - Install dependencies from `requirements.txt`
   - Run database migrations
   - Collect static files
   - Start the Gunicorn server

### 6. Post-Deployment
1. Check deployment logs for any errors
2. Test the health endpoint: `https://your-app.railway.app/api/health/`
3. Update your frontend's `NEXT_PUBLIC_API_URL` to point to your Railway URL

## Important Files for Railway

- `railway.json` - Railway configuration
- `requirements.txt` - Python dependencies
- `Procfile.railway` - Process definitions
- `railway-build.sh` - Build script
- `.env.railway` - Environment variables template

## Troubleshooting

### Common Issues:
1. **Build fails**: Check Python version compatibility
2. **Database connection**: Ensure PostgreSQL addon is added
3. **Static files**: Whitenoise is configured for static file serving
4. **CORS errors**: Update CORS_ALLOWED_ORIGINS with your frontend URL

### Useful Commands:
```bash
# View logs
railway logs

# Connect to database
railway connect

# Run migrations manually
railway run python manage.py migrate
```

## Production Checklist
- [ ] Environment variables set correctly
- [ ] PostgreSQL database added
- [ ] Frontend CORS origins configured
- [ ] Health endpoint responding
- [ ] Static files loading correctly
- [ ] Database migrations completed
