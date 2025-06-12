# Fly.io Deployment Guide for FC Backend

## Prerequisites

1. **Fly CLI**: ✅ Already installed
2. **Authentication**: ✅ Already logged in as snick4714@gmail.com
3. **Payment Info**: ⚠️  **REQUIRED** - Add credit card to continue

## Step 1: Add Payment Information

Before proceeding, you need to add payment information to your Fly.io account:

1. Visit: https://fly.io/dashboard/snick4714-gmail-com/billing
2. Add a credit card or buy credits
3. Note: Fly.io offers $5 free credits monthly for hobby apps

## Step 2: Create the Application

Once payment is added, run:

```bash
fly apps create fc-backend
```

## Step 3: Set Up PostgreSQL Database

```bash
# Create PostgreSQL database
fly postgres create --name fc-backend-db --region ord

# Attach database to app
fly postgres attach --app fc-backend fc-backend-db
```

## Step 4: Set Environment Variables

```bash
# Set production environment variables
fly secrets set DEBUG=False
fly secrets set SECRET_KEY="your-super-secret-key-here"
fly secrets set CORS_ALLOWED_ORIGINS="https://your-frontend-domain.vercel.app"

# Add API keys (replace with your actual keys)
fly secrets set COINGECKO_API_KEY="your-coingecko-api-key"
fly secrets set MORALIS_API_KEY="your-moralis-api-key"
fly secrets set INFURA_PROJECT_ID="your-infura-project-id"
fly secrets set ALCHEMY_API_KEY="your-alchemy-api-key"

# Blockchain RPC URLs
fly secrets set ETHEREUM_RPC_URL="https://mainnet.infura.io/v3/your-project-id"
fly secrets set POLYGON_RPC_URL="https://polygon-mainnet.infura.io/v3/your-project-id"
fly secrets set BSC_RPC_URL="https://bsc-dataseed.binance.org/"

# Contract addresses (update with your deployed contracts)
fly secrets set TOKEN_CONTRACT_ADDRESS="0x..."
fly secrets set STAKING_CONTRACT_ADDRESS="0x..."
fly secrets set INVESTMENT_CONTRACT_ADDRESS="0x..."
```

## Step 5: Deploy the Application

```bash
# Deploy to Fly.io
fly deploy
```

## Step 6: Monitor Deployment

```bash
# Check app status
fly status

# View logs
fly logs

# Check health
fly checks list
```

## Step 7: Access Your Application

Your backend will be available at: `https://fc-backend.fly.dev`

Test the health endpoint: `https://fc-backend.fly.dev/api/health/`

## Troubleshooting

### Common Issues:

1. **Payment Required**: Add credit card at https://fly.io/dashboard/billing
2. **Build Failures**: Check logs with `fly logs`
3. **Database Connection**: Ensure PostgreSQL is attached
4. **Environment Variables**: Verify with `fly secrets list`

### Useful Commands:

```bash
# SSH into the app
fly ssh console

# Scale the app
fly scale count 1

# Restart the app
fly apps restart fc-backend

# View app info
fly info

# Connect to database
fly postgres connect -a fc-backend-db
```

## Next Steps After Deployment

1. **Update Frontend**: Change `NEXT_PUBLIC_API_URL` to `https://fc-backend.fly.dev`
2. **Deploy Frontend**: Deploy to Vercel or Netlify
3. **Test Integration**: Verify frontend can communicate with backend
4. **Set up Monitoring**: Configure alerts and monitoring
5. **SSL Certificate**: Verify HTTPS is working
6. **Custom Domain**: (Optional) Add custom domain

## Environment Variables Reference

The following environment variables are configured:

- `DEBUG=False` - Production mode
- `SECRET_KEY` - Django secret key
- `DATABASE_URL` - PostgreSQL connection (auto-configured)
- `CORS_ALLOWED_ORIGINS` - Frontend domains
- API keys for external services
- Blockchain RPC URLs
- Smart contract addresses

## Cost Estimation

- **App**: ~$1.94/month (shared-cpu-1x, 256MB)
- **PostgreSQL**: ~$1.94/month (shared-cpu-1x, 256MB)
- **Total**: ~$4/month (within free $5 credits)

## Security Notes

1. All secrets are encrypted at rest
2. HTTPS is enforced by default
3. Database connections are secure
4. Environment variables are not exposed in logs
