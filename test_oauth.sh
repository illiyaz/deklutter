#!/bin/bash

# Temporary OAuth test script
# This sets the redirect URI to localhost for testing

echo "🔧 Setting up OAuth for local testing..."
echo ""
echo "Current GOOGLE_REDIRECT_URI:"
grep GOOGLE_REDIRECT_URI .env
echo ""
echo "⚠️  For local testing, you need to:"
echo "1. Go to Google Cloud Console: https://console.cloud.google.com/apis/credentials"
echo "2. Find your OAuth 2.0 Client ID: 830413157217-4lbcans9kh0m3idq589128e1tjnv2ru8"
echo "3. Add this redirect URI: http://localhost:8000/auth/google/callback"
echo "4. Click Save"
echo ""
echo "Then update your .env file:"
echo "GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback"
echo ""
echo "📝 Or use ngrok for testing:"
echo "   ngrok http 8000"
echo "   Then update GOOGLE_REDIRECT_URI to the ngrok URL"
