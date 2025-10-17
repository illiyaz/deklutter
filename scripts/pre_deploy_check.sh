#!/bin/bash

echo "🔍 Pre-Deployment Checklist"
echo "============================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found"
    echo "   Run: cp .env.example .env"
    exit 1
else
    echo "✅ .env file exists"
fi

# Check required env vars
echo ""
echo "Checking environment variables..."

check_env_var() {
    if grep -q "^$1=" .env && ! grep -q "^$1=.*change-me\|^$1=.*your-" .env; then
        echo "✅ $1 is set"
        return 0
    else
        echo "❌ $1 is not configured"
        return 1
    fi
}

ERRORS=0

check_env_var "GOOGLE_CLIENT_ID" || ((ERRORS++))
check_env_var "GOOGLE_CLIENT_SECRET" || ((ERRORS++))
check_env_var "GOOGLE_REDIRECT_URI" || ((ERRORS++))
check_env_var "JWT_SECRET_KEY" || ((ERRORS++))
check_env_var "APP_SECRET" || ((ERRORS++))

# Check if Docker is running
echo ""
echo "Checking Docker..."
if docker ps &> /dev/null; then
    echo "✅ Docker is running"
else
    echo "❌ Docker is not running"
    ((ERRORS++))
fi

# Check if services are up
echo ""
echo "Checking services..."
if docker ps | grep -q "infra-db-1"; then
    echo "✅ PostgreSQL is running"
else
    echo "❌ PostgreSQL is not running"
    echo "   Run: make infra"
    ((ERRORS++))
fi

if docker ps | grep -q "infra-redis-1"; then
    echo "✅ Redis is running"
else
    echo "❌ Redis is not running"
    echo "   Run: make infra"
    ((ERRORS++))
fi

# Check if venv exists
echo ""
echo "Checking Python environment..."
if [ -d ".venv" ]; then
    echo "✅ Virtual environment exists"
else
    echo "❌ Virtual environment not found"
    echo "   Run: python -m venv .venv"
    ((ERRORS++))
fi

# Check if requirements are installed
if [ -f ".venv/bin/python" ]; then
    if .venv/bin/python -c "import fastapi" 2>/dev/null; then
        echo "✅ Dependencies installed"
    else
        echo "❌ Dependencies not installed"
        echo "   Run: pip install -r requirements.txt"
        ((ERRORS++))
    fi
fi

# Check if server is running
echo ""
echo "Checking server..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Server is running"
else
    echo "⚠️  Server is not running"
    echo "   Run: make dev"
fi

# Summary
echo ""
echo "============================"
if [ $ERRORS -eq 0 ]; then
    echo "✅ All checks passed!"
    echo ""
    echo "Ready to deploy! Next steps:"
    echo "1. Push code to GitHub"
    echo "2. Create Render account"
    echo "3. Deploy using render.yaml"
    echo ""
    echo "See DEPLOYMENT_GUIDE.md for details"
else
    echo "❌ $ERRORS error(s) found"
    echo ""
    echo "Fix the errors above before deploying"
fi
echo "============================"
