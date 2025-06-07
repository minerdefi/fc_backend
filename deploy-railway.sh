#!/usr/bin/env bash
# Railway deployment helper script

set -e

echo "🚀 Preparing FG Premium Backend for Railway Deployment..."

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Check for required files
required_files=("requirements.txt" "manage.py" "fc_backend/settings.py")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Error: Required file $file not found"
        exit 1
    fi
done

echo "✅ All required files present"

# Add all changes
echo "📝 Adding changes to git..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "Prepare for Railway deployment" || echo "No changes to commit"

# Push to GitLab
echo "📤 Pushing to GitLab..."
git push origin main

echo "🎉 Backend prepared for Railway deployment!"
echo ""
echo "Next steps:"
echo "1. Go to https://railway.app"
echo "2. Create new project from GitLab repo"
echo "3. Add PostgreSQL database"
echo "4. Configure environment variables"
echo "5. Deploy!"
echo ""
echo "📖 See RAILWAY_DEPLOYMENT.md for detailed instructions"
