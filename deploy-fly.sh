#!/bin/bash
# Fly.io deployment script for FC Backend

echo "🚀 Starting Fly.io deployment for FC Backend..."

# Check if flyctl is installed
if ! command -v fly &> /dev/null; then
    echo "❌ Fly CLI not found. Please install it first:"
    echo "   Visit: https://fly.io/docs/hands-on/install-flyctl/"
    exit 1
fi

# Check if user is logged in
if ! fly auth whoami &> /dev/null; then
    echo "❌ Not logged in to Fly.io. Please run: fly auth login"
    exit 1
fi

echo "✅ Fly CLI found and authenticated"

# Set app name
APP_NAME="fc-backend"
echo "📱 App name: $APP_NAME"

# Check if app exists
if fly apps list | grep -q "$APP_NAME"; then
    echo "✅ App $APP_NAME already exists"
else
    echo "🆕 Creating new app $APP_NAME..."
    fly launch --no-deploy --name $APP_NAME --region ord
fi

# Set environment variables
echo "🔧 Setting environment variables..."
fly secrets set DEBUG=False --app $APP_NAME
fly secrets set SECRET_KEY=$(openssl rand -base64 32) --app $APP_NAME
fly secrets set ALLOWED_HOSTS="*.fly.dev,fgpremiumfunds.com" --app $APP_NAME

# Check if database exists
if ! fly postgres list | grep -q "fc-backend-db"; then
    echo "🗄️ Creating PostgreSQL database..."
    fly postgres create --name fc-backend-db --region ord
    fly postgres attach --app $APP_NAME fc-backend-db
else
    echo "✅ Database fc-backend-db already exists"
fi

# Deploy the application
echo "🚀 Deploying application..."
fly deploy --app $APP_NAME

# Show deployment status
echo "📊 Deployment status:"
fly status --app $APP_NAME

# Show app URL
echo "🌐 Your app is available at:"
echo "   https://$APP_NAME.fly.dev"

echo "✅ Deployment completed!"
echo ""
echo "🔗 Useful commands:"
echo "   fly logs --app $APP_NAME          # View logs"
echo "   fly ssh console --app $APP_NAME   # SSH into machine"
echo "   fly open --app $APP_NAME          # Open in browser"
