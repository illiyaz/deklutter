#!/bin/bash

echo "🐳 Docker Deployment Script"
echo "============================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found"
    echo "   Run: cp .env.example .env and configure it"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

echo "Building Docker image..."
docker build -t deklutter:latest .

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed"
    exit 1
fi

echo "✅ Docker image built successfully"
echo ""

echo "Starting services with docker-compose..."
docker-compose -f docker-compose.prod.yml up -d

if [ $? -ne 0 ]; then
    echo "❌ Failed to start services"
    exit 1
fi

echo ""
echo "✅ Services started successfully!"
echo ""
echo "Waiting for services to be ready..."
sleep 5

# Check health
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Application is healthy!"
    echo ""
    echo "🎉 Deployment complete!"
    echo ""
    echo "Access your application:"
    echo "  - API: http://localhost:8000"
    echo "  - Docs: http://localhost:8000/docs"
    echo "  - Health: http://localhost:8000/health"
    echo ""
    echo "View logs:"
    echo "  docker-compose -f docker-compose.prod.yml logs -f app"
    echo ""
    echo "Stop services:"
    echo "  docker-compose -f docker-compose.prod.yml down"
else
    echo "⚠️  Application may not be ready yet"
    echo "   Check logs: docker-compose -f docker-compose.prod.yml logs app"
fi
