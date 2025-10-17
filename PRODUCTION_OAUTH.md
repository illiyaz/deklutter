# Production OAuth Setup for ChatGPT Plugin

## Overview

For a ChatGPT plugin, you need to set up OAuth so that users can easily connect their Gmail without any manual credential setup.

## Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   ChatGPT   │─────▶│  Your API    │─────▶│   Google    │
│   Plugin    │      │  (Deklutter) │      │   OAuth     │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  PostgreSQL  │
                     │ (User Tokens)│
                     └──────────────┘
```

## Step 1: Google Cloud Setup (Production)

### 1.1 Create Production Project
1. Go to https://console.cloud.google.com/
2. Create project: "Deklutter Production"
3. Enable Gmail API

### 1.2 Configure OAuth Consent Screen
1. **Publishing status**: Choose "In Production" (requires verification)
2. **App information**:
   - App name: `Deklutter`
   - App logo: Upload your logo
   - App domain: `https://yourdomain.com`
   - Authorized domains: Add your domain
3. **Scopes**: Add these Gmail scopes:
   - `https://www.googleapis.com/auth/gmail.readonly` (read emails)
   - `https://www.googleapis.com/auth/gmail.modify` (delete/label emails)
4. **Test users**: Add your email for testing

### 1.3 App Verification (Required for Production)
Google requires verification if you request sensitive scopes:
- Submit your app for verification
- Provide privacy policy URL
- Provide terms of service URL
- Explain why you need Gmail access
- May take 1-2 weeks for approval

### 1.4 Create OAuth Credentials
1. **Application type**: Web application
2. **Name**: Deklutter Production
3. **Authorized redirect URIs**:
   ```
   https://yourdomain.com/auth/google/callback
   https://chat.openai.com/aip/{your-plugin-id}/oauth/callback
   ```
4. Save Client ID and Client Secret

## Step 2: ChatGPT Plugin Configuration

### 2.1 Plugin Manifest (`ai-plugin.json`)
```json
{
  "schema_version": "v1",
  "name_for_human": "Deklutter",
  "name_for_model": "deklutter",
  "description_for_human": "Clean up your Gmail inbox by identifying and removing spam emails.",
  "description_for_model": "Help users analyze their Gmail inbox and identify spam/unwanted emails for deletion.",
  "auth": {
    "type": "oauth",
    "client_url": "https://accounts.google.com/o/oauth2/v2/auth",
    "scope": "https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/gmail.modify",
    "authorization_url": "https://yourdomain.com/auth/google/callback",
    "authorization_content_type": "application/json",
    "verification_tokens": {
      "openai": "your-openai-verification-token"
    }
  },
  "api": {
    "type": "openapi",
    "url": "https://yourdomain.com/openapi.json"
  },
  "logo_url": "https://yourdomain.com/logo.png",
  "contact_email": "support@yourdomain.com",
  "legal_info_url": "https://yourdomain.com/legal"
}
```

### 2.2 OpenAPI Spec Updates
Your API needs to support OAuth token in headers:
```yaml
security:
  - OAuth2: []
securitySchemes:
  OAuth2:
    type: oauth2
    flows:
      authorizationCode:
        authorizationUrl: https://accounts.google.com/o/oauth2/v2/auth
        tokenUrl: https://oauth2.googleapis.com/token
        scopes:
          gmail.readonly: Read Gmail messages
          gmail.modify: Modify Gmail messages
```

## Step 3: Backend Changes

### 3.1 Update Environment Variables
```bash
# Production
GOOGLE_CLIENT_ID=your-production-client-id
GOOGLE_CLIENT_SECRET=your-production-secret
GOOGLE_REDIRECT_URI=https://yourdomain.com/auth/google/callback

# For ChatGPT plugin
CHATGPT_REDIRECT_URI=https://chat.openai.com/aip/{plugin-id}/oauth/callback
```

### 3.2 Update OAuth Flow
The current code needs modification to handle ChatGPT's OAuth flow:

```python
# services/gateway/routes_gmail.py
@router.get("/auth/google/callback")
def auth_google_callback(
    code: str, 
    state: str | None = None,
    redirect_uri: str | None = None  # ChatGPT sends this
):
    # Determine if this is from ChatGPT or direct user
    is_chatgpt = redirect_uri and "chat.openai.com" in redirect_uri
    
    # Exchange code for tokens
    tokens = exchange_code_for_tokens(code, redirect_uri)
    
    if is_chatgpt:
        # Return tokens to ChatGPT
        return {
            "access_token": tokens.access_token,
            "token_type": "Bearer",
            "expires_in": 3600
        }
    else:
        # Regular web flow - redirect to success page
        return RedirectResponse(url="/auth/success")
```

## Step 4: User Flow

### For ChatGPT Plugin Users:
1. User installs Deklutter plugin from ChatGPT store
2. User asks: "Clean up my Gmail inbox"
3. ChatGPT prompts: "Deklutter needs access to your Gmail"
4. User clicks "Connect"
5. Redirected to Google OAuth (using YOUR credentials)
6. User authorizes YOUR app
7. Tokens stored in YOUR database
8. User can now use the plugin

**User never sees or handles credentials!** ✅

## Step 5: Security Considerations

### 5.1 Token Storage
- Encrypt all tokens using Fernet (already implemented)
- Use strong APP_SECRET (32+ characters)
- Rotate encryption keys periodically

### 5.2 Token Refresh
Implement automatic token refresh:
```python
def refresh_access_token(user_id: int):
    token = db.query(OAuthToken).filter_by(user_id=user_id).first()
    if token.expiry < datetime.utcnow():
        # Refresh token
        creds = Credentials(
            token=None,
            refresh_token=decrypt(token.refresh_token),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=os.getenv("GOOGLE_CLIENT_ID"),
            client_secret=os.getenv("GOOGLE_CLIENT_SECRET")
        )
        creds.refresh(Request())
        # Update token in DB
        token.access_token = encrypt(creds.token)
        token.expiry = creds.expiry
        db.commit()
```

### 5.3 Rate Limiting
- Implement per-user rate limits
- Respect Gmail API quotas
- Cache frequently accessed data

### 5.4 Data Privacy
- Only store necessary data
- Provide user data deletion endpoint
- Clear privacy policy
- GDPR compliance if serving EU users

## Step 6: Required Legal Documents

### 6.1 Privacy Policy (Required)
Must include:
- What data you collect (Gmail messages metadata)
- How you use it (spam detection)
- How you store it (encrypted in database)
- How users can delete their data
- Third-party services (Google, OpenAI)

### 6.2 Terms of Service (Required)
Must include:
- Service description
- User responsibilities
- Limitations of liability
- Account termination conditions

### 6.3 Data Deletion
Provide endpoint for users to revoke access:
```python
@router.post("/auth/revoke")
def revoke_access(user: CurrentUser):
    # Delete tokens from database
    db.query(OAuthToken).filter_by(user_id=user.id).delete()
    db.commit()
    
    # Optionally revoke with Google
    # requests.post("https://oauth2.googleapis.com/revoke", ...)
    
    return {"message": "Access revoked"}
```

## Step 7: Testing

### 7.1 Local Testing
Use ngrok to test OAuth flow locally:
```bash
ngrok http 8000
# Use ngrok URL as redirect URI for testing
```

### 7.2 ChatGPT Plugin Testing
1. Submit plugin for review
2. Test in ChatGPT plugin developer mode
3. Verify OAuth flow works end-to-end

## Step 8: Deployment Checklist

- [ ] Google Cloud project created
- [ ] Gmail API enabled
- [ ] OAuth consent screen configured
- [ ] App submitted for verification
- [ ] Production credentials generated
- [ ] Privacy policy published
- [ ] Terms of service published
- [ ] SSL certificate installed (HTTPS required)
- [ ] Environment variables set on production server
- [ ] Database backups configured
- [ ] Monitoring and logging set up
- [ ] Rate limiting implemented
- [ ] Error handling tested
- [ ] ChatGPT plugin manifest created
- [ ] OpenAPI spec updated
- [ ] Plugin submitted to ChatGPT store

## Cost Considerations

### Google Cloud
- Gmail API: Free up to 1 billion quota units/day
- Typical usage: ~5-10 units per email scanned
- Should be free for most use cases

### Infrastructure
- Server hosting: $5-50/month (depends on scale)
- Database: Included or $10-20/month
- Domain: $10-15/year
- SSL certificate: Free (Let's Encrypt)

## Support Resources

- [Google OAuth 2.0 Guide](https://developers.google.com/identity/protocols/oauth2)
- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [ChatGPT Plugin Documentation](https://platform.openai.com/docs/plugins)
- [OAuth 2.0 Security Best Practices](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)
