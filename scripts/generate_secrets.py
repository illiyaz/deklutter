#!/usr/bin/env python3
"""Generate secure secrets for production"""

import secrets

print("🔐 Generating Secure Secrets")
print("=" * 60)
print()
print("Add these to your .env file:")
print()
print(f"JWT_SECRET_KEY={secrets.token_urlsafe(32)}")
print(f"APP_SECRET={secrets.token_urlsafe(32)}")
print()
print("=" * 60)
print()
print("Or run this command:")
print()
print("cat >> .env << EOF")
print(f"JWT_SECRET_KEY={secrets.token_urlsafe(32)}")
print(f"APP_SECRET={secrets.token_urlsafe(32)}")
print("EOF")
print()
