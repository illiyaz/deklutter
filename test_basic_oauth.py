#!/usr/bin/env python3
"""Test OAuth with minimal scopes to isolate the issue"""

import webbrowser
from urllib.parse import urlencode
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("GOOGLE_CLIENT_ID")
redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")

print("=" * 60)
print("🧪 Testing OAuth with MINIMAL scopes")
print("=" * 60)
print("\nThis test uses only 'openid' and 'email' scopes")
print("These don't require Gmail API or special permissions")
print("\nIf this works: The issue is with Gmail scope configuration")
print("If this fails: The issue is with basic OAuth setup")
print("=" * 60)

# Minimal scopes that should always work
params = {
    "response_type": "code",
    "client_id": client_id,
    "redirect_uri": redirect_uri,
    "scope": "openid email",  # Minimal scopes
    "state": "test_basic",
    "access_type": "offline",
    "prompt": "consent"
}

url = f"https://accounts.google.com/o/oauth2/auth?{urlencode(params)}"

print(f"\n📋 Test URL:\n{url}\n")
print("👉 Opening browser...")

webbrowser.open(url)

print("\n⚠️  What to look for:")
print("1. Does it show 'Choose an account' page? ✅")
print("2. After selecting account, does it show consent screen? ✅")
print("3. Does it redirect to your callback? ✅")
print("4. Or does it show 'Something went wrong'? ❌")
print("\n" + "=" * 60)
