# Create cPanel Deployment Package
# This script creates a clean ZIP file ready for cPanel upload

Write-Host "📦 Creating cPanel Deployment Package..." -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan

# Check if we're in the right directory
if (-not (Test-Path "manage.py")) {
    Write-Host "❌ Error: manage.py not found. Please run this script from your Django project directory." -ForegroundColor Red
    exit 1
}

# Files and directories to exclude from the package
$excludePatterns = @(
    "*.pyc"
    "__pycache__"
    ".git*"
    ".env*"
    "db.sqlite3"
    "venv"
    "env"
    ".vscode"
    ".idea"
    "*.log"
    "node_modules"
    ".pytest_cache"
    "htmlcov"
    ".coverage"
    "*.zip"
)

# Create temporary directory
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$tempDir = "temp_cpanel_package_$timestamp"
$packageName = "fc_backend_cpanel_$timestamp.zip"

Write-Host "📁 Creating temporary directory: $tempDir" -ForegroundColor Yellow

try {
    # Create temp directory
    New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
    
    # Copy all files except excluded ones
    Write-Host "📋 Copying project files..." -ForegroundColor Yellow
    
    # Get all items to copy
    $allItems = Get-ChildItem -Path . -Recurse
    $itemsToCopy = @()
    
    foreach ($item in $allItems) {
        $shouldExclude = $false
        $relativePath = $item.FullName.Substring((Get-Location).Path.Length + 1)
        
        foreach ($pattern in $excludePatterns) {
            if ($relativePath -like $pattern -or $item.Name -like $pattern) {
                $shouldExclude = $true
                break
            }
        }
        
        if (-not $shouldExclude -and -not $relativePath.Contains("temp_cpanel_package")) {
            $itemsToCopy += $item
        }
    }
    
    # Copy files maintaining directory structure
    foreach ($item in $itemsToCopy) {
        $relativePath = $item.FullName.Substring((Get-Location).Path.Length + 1)
        $destPath = Join-Path $tempDir $relativePath
        
        if ($item.PSIsContainer) {
            New-Item -ItemType Directory -Path $destPath -Force | Out-Null
        } else {
            $destDir = Split-Path $destPath -Parent
            if ($destDir -and -not (Test-Path $destDir)) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }
            Copy-Item $item.FullName $destPath -Force
        }
    }
    
    # Create deployment instructions file
    $instructions = @"
🚀 cPanel Deployment Instructions

This package contains your Django project ready for cPanel deployment.

📋 Quick Setup Steps:
1. Upload this ZIP file to your cPanel File Manager
2. Extract to your Python app directory (usually fc_backend/)
3. Create MySQL database in cPanel
4. Create .env file with your database details
5. Set up Python app in cPanel pointing to passenger_wsgi.py
6. Run auto_deploy_cpanel.ps1 or follow manual steps in CPANEL_STEP_BY_STEP.md

📁 Package Contents:
- Django project files (excluding sensitive data)
- passenger_wsgi.py (cPanel WSGI entry point)
- .htaccess (web server configuration)
- requirements_cpanel.txt (dependencies)
- Deployment scripts and documentation
- Auto-deployment script

🔒 Security Notes:
- .env files are excluded (create manually with your details)
- Database files are excluded
- Git history is excluded
- Cache files are excluded

📚 Documentation:
- CPANEL_STEP_BY_STEP.md - Complete deployment guide
- CPANEL_QUICK_REFERENCE.md - Quick reference
- CPANEL_CHECKLIST.md - Deployment checklist

🆘 Support:
If you encounter issues, check the documentation files or contact your hosting provider.

Generated: $(Get-Date)
"@
    
    $instructions | Out-File -FilePath "$tempDir\DEPLOYMENT_INSTRUCTIONS.txt" -Encoding UTF8
    
    # Create the ZIP package
    Write-Host "🗜️  Creating ZIP package: $packageName" -ForegroundColor Yellow
    Compress-Archive -Path "$tempDir\*" -DestinationPath $packageName -Force
    
    # Clean up temp directory
    Remove-Item -Path $tempDir -Recurse -Force
    
    # Get package size
    $packageSize = (Get-Item $packageName).Length / 1MB
    
    Write-Host "`n✅ Package created successfully!" -ForegroundColor Green
    Write-Host "📦 Package name: $packageName" -ForegroundColor Cyan
    Write-Host "📏 Package size: $([math]::Round($packageSize, 2)) MB" -ForegroundColor Cyan
    
    Write-Host "`n📋 Package Contents:" -ForegroundColor Yellow
    Write-Host "- Django project files (clean, no sensitive data)" -ForegroundColor White
    Write-Host "- cPanel configuration files" -ForegroundColor White
    Write-Host "- Deployment scripts" -ForegroundColor White
    Write-Host "- Documentation and guides" -ForegroundColor White
    
    Write-Host "`n🚀 Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Upload $packageName to your cPanel File Manager" -ForegroundColor White
    Write-Host "2. Extract to your Python app directory" -ForegroundColor White
    Write-Host "3. Follow DEPLOYMENT_INSTRUCTIONS.txt" -ForegroundColor White
    
    Write-Host "`n🎯 Ready for cPanel deployment!" -ForegroundColor Green
    
} catch {
    Write-Host "❌ Error creating package: $($_.Exception.Message)" -ForegroundColor Red
    if (Test-Path $tempDir) {
        Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue
    }
    exit 1
}
