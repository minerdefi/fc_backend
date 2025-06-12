# PowerShell deployment script for Fly.io
# Usage: .\deploy-fly.ps1

Write-Host "🚀 Starting Fly.io deployment for FC Backend..." -ForegroundColor Green

# Check if flyctl is installed
if (-not (Get-Command fly -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Fly CLI not found. Please install it first:" -ForegroundColor Red
    Write-Host "   Visit: https://fly.io/docs/hands-on/install-flyctl/" -ForegroundColor Yellow
    exit 1
}

# Check if user is logged in
try {
    fly auth whoami | Out-Null
    Write-Host "✅ Fly CLI found and authenticated" -ForegroundColor Green
} catch {
    Write-Host "❌ Not logged in to Fly.io. Please run: fly auth login" -ForegroundColor Red
    exit 1
}

# Set app name
$APP_NAME = "fc-backend"
Write-Host "📱 App name: $APP_NAME" -ForegroundColor Cyan

# Check if app exists
try {
    $existingApps = fly apps list
    if ($existingApps -match $APP_NAME) {
        Write-Host "✅ App $APP_NAME already exists" -ForegroundColor Green
    } else {
        Write-Host "🆕 Creating new app $APP_NAME..." -ForegroundColor Yellow
        Write-Host "⚠️  Note: You need to add payment information to your Fly.io account first!" -ForegroundColor Yellow
        Write-Host "   Visit: https://fly.io/dashboard/billing" -ForegroundColor Cyan
        Write-Host "   Press Enter after adding payment info to continue..."
        Read-Host
    fly launch --no-deploy --name $APP_NAME --region ord
}

# Generate secret key
$SECRET_KEY = [System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes([System.Guid]::NewGuid().ToString()))

# Set environment variables
Write-Host "🔧 Setting environment variables..." -ForegroundColor Yellow
fly secrets set DEBUG=False --app $APP_NAME
fly secrets set SECRET_KEY=$SECRET_KEY --app $APP_NAME
fly secrets set ALLOWED_HOSTS="*.fly.dev,fgpremiumfunds.com" --app $APP_NAME

# Check if database exists
$existingDbs = fly postgres list
if ($existingDbs -match "fc-backend-db") {
    Write-Host "✅ Database fc-backend-db already exists" -ForegroundColor Green
} else {
    Write-Host "🗄️ Creating PostgreSQL database..." -ForegroundColor Yellow
    fly postgres create --name fc-backend-db --region ord
    fly postgres attach --app $APP_NAME fc-backend-db
}

# Deploy the application
Write-Host "🚀 Deploying application..." -ForegroundColor Green
fly deploy --app $APP_NAME

# Show deployment status
Write-Host "📊 Deployment status:" -ForegroundColor Cyan
fly status --app $APP_NAME

# Show app URL
Write-Host "🌐 Your app is available at:" -ForegroundColor Green
Write-Host "   https://$APP_NAME.fly.dev" -ForegroundColor Blue

Write-Host "✅ Deployment completed!" -ForegroundColor Green
Write-Host ""
Write-Host "🔗 Useful commands:" -ForegroundColor Cyan
Write-Host "   fly logs --app $APP_NAME          # View logs" -ForegroundColor Gray
Write-Host "   fly ssh console --app $APP_NAME   # SSH into machine" -ForegroundColor Gray
Write-Host "   fly open --app $APP_NAME          # Open in browser" -ForegroundColor Gray
