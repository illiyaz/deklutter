#!/bin/bash

echo "🚀 ngrok Setup Guide for Deklutter"
echo "=================================="
echo ""
echo "Step 1: Start ngrok in a NEW terminal window:"
echo "  ngrok http 8000"
echo ""
echo "Step 2: Copy the HTTPS URL from ngrok output"
echo "  Example: https://abc123.ngrok-free.app"
echo ""
echo "Step 3: Paste your ngrok URL here (press Enter when done):"
read -p "ngrok URL: " NGROK_URL

# Remove trailing slash if present
NGROK_URL=${NGROK_URL%/}

echo ""
echo "✅ Got URL: $NGROK_URL"
echo ""
echo "Step 4: Updating .env file..."

# Update .env file
if [ -f .env ]; then
    # Backup
    cp .env .env.backup
    
    # Update GOOGLE_REDIRECT_URI
    if grep -q "GOOGLE_REDIRECT_URI=" .env; then
        sed -i '' "s|GOOGLE_REDIRECT_URI=.*|GOOGLE_REDIRECT_URI=${NGROK_URL}/auth/google/callback|g" .env
        echo "✅ Updated GOOGLE_REDIRECT_URI in .env"
    else
        echo "GOOGLE_REDIRECT_URI=${NGROK_URL}/auth/google/callback" >> .env
        echo "✅ Added GOOGLE_REDIRECT_URI to .env"
    fi
else
    echo "❌ .env file not found!"
    exit 1
fi

echo ""
echo "📋 Now update Google Cloud Console:"
echo "=================================="
echo ""
echo "1. Go to: https://console.cloud.google.com/apis/credentials"
echo ""
echo "2. Click on your OAuth 2.0 Client ID"
echo ""
echo "3. Under 'Authorized redirect URIs', add:"
echo "   ${NGROK_URL}/auth/google/callback"
echo ""
echo "4. Click SAVE"
echo ""
echo "5. Go to: https://console.cloud.google.com/apis/credentials/consent"
echo ""
echo "6. Click EDIT APP, then fill in:"
echo "   - Application home page: ${NGROK_URL}"
echo "   - Privacy policy: ${NGROK_URL}/privacy"
echo "   - Terms of service: ${NGROK_URL}/terms"
echo ""
echo "7. Click SAVE AND CONTINUE through all steps"
echo ""
echo "8. Wait 2 minutes, then test:"
echo "   python test_gmail.py"
echo ""
echo "=================================="
echo "🛑 To stop ngrok later:"
echo "   - Go to the terminal running ngrok"
echo "   - Press Ctrl+C"
echo "=================================="
