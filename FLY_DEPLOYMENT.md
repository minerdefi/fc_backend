# Fly.io Deployment Guide for FC Backend

## Prerequisites
1. Install the Fly CLI: https://fly.io/docs/hands-on/install-flyctl/
2. Sign up for a Fly.io account: https://fly.io/app/sign-up
3. Authenticate: `fly auth login`

## Deployment Steps

### 1. Initialize Fly App
```bash
cd c:\lets_see\fc_fullstack\fc_backend
fly launch --no-deploy
```

### 2. Set Environment Variables
```bash
fly secrets set DEBUG=False
fly secrets set SECRET_KEY=$(openssl rand -base64 32)
fly secrets set ALLOWED_HOSTS="*.fly.dev,fgpremiumfunds.com"
```

### 3. Create PostgreSQL Database
```bash
fly postgres create --name fc-backend-db --region ord
fly postgres attach --app fc-backend fc-backend-db
```

### 4. Deploy
```bash
fly deploy
```

### 5. Open Your App
```bash
fly open
```

## Environment Variables
Set these in Fly.io dashboard or via CLI:

- `DEBUG=False`
- `SECRET_KEY=<generated-secret-key>`
- `ALLOWED_HOSTS=*.fly.dev,fgpremiumfunds.com`
- `DATABASE_URL=<auto-set-by-postgres-attach>`

## Monitoring
- View logs: `fly logs`
- Check status: `fly status`
- Scale app: `fly scale count 2`

## Custom Domains
To add your custom domain:
```bash
fly certs create fgpremiumfunds.com
fly certs create api.fgpremiumfunds.com
```

## Troubleshooting
- Check health: `fly checks list`
- SSH into machine: `fly ssh console`
- Restart app: `fly apps restart fc-backend`
