# Testing Gmail Integration

This guide walks you through testing the Gmail integration in Deklutter.

## Prerequisites

### 1. Set up Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use existing)
3. Enable the **Gmail API**:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"

### 2. Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Configure consent screen if prompted:
   - User Type: External (for testing)
   - App name: Deklutter
   - User support email: your email
   - Developer contact: your email
4. Application type: **Web application**
5. Name: Deklutter Local Dev
6. Authorized redirect URIs:
   ```
   http://localhost:8000/auth/google/callback
   ```
7. Click "Create"
8. Copy the **Client ID** and **Client Secret**

### 3. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```bash
   DATABASE_URL=postgresql://deklutter_user:deklutter_password@localhost:5433/deklutter

   # Google OAuth
   GOOGLE_CLIENT_ID=your-actual-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-actual-client-secret
   GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback

   # Encryption key (generate a random 32+ character string)
   APP_SECRET=your-random-secret-key-at-least-32-chars
   ```

3. Generate a secure APP_SECRET:
   ```bash
   python3 -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

## Testing Methods

### Method 1: Using the Test Script (Recommended)

1. **Start the server:**
   ```bash
   make dev
   ```

2. **Run the test script:**
   ```bash
   python test_gmail.py
   ```

3. **Follow the interactive prompts:**
   - Choose option 4 for full flow
   - Browser will open for Google authorization
   - Authorize the app
   - Copy the `code` parameter from the callback URL
   - Paste it into the terminal
   - Script will complete OAuth and scan your Gmail

### Method 2: Using cURL

#### Step 1: Get OAuth URL
```bash
curl -X POST http://localhost:8000/auth/google/init \
  -H "X-User-Email: demo@user.test"
```

Response:
```json
{
  "auth_url": "https://accounts.google.com/o/oauth2/auth?..."
}
```

#### Step 2: Authorize in Browser
- Open the `auth_url` in your browser
- Sign in and authorize
- You'll be redirected to: `http://localhost:8000/auth/google/callback?code=...&state=...`
- Copy the `code` parameter value

#### Step 3: Exchange Code for Tokens
```bash
curl -X GET "http://localhost:8000/auth/google/callback?code=YOUR_CODE&state=user:demo@user.test" \
  -H "X-User-Email: demo@user.test"
```

Response:
```json
{
  "message": "Authorized. You can run a scan now."
}
```

#### Step 4: Scan Gmail
```bash
curl -X POST http://localhost:8000/gmail/scan \
  -H "X-User-Email: demo@user.test" \
  -H "Content-Type: application/json" \
  -d '{"days_back": 7, "limit": 10}'
```

### Method 3: Using API Docs (Swagger UI)

1. **Start the server:**
   ```bash
   make dev
   ```

2. **Open API docs:**
   ```bash
   make api
   # Or manually open: http://localhost:8000/docs
   ```

3. **Test endpoints:**
   - Click on `/auth/google/init` > "Try it out"
   - Add header: `X-User-Email: demo@user.test`
   - Execute and copy the auth URL
   - Complete OAuth flow in browser
   - Use `/auth/google/callback` with the code
   - Test `/gmail/scan` endpoint

## Troubleshooting

### Error: "redirect_uri_mismatch"
- Ensure the redirect URI in Google Console exactly matches: `http://localhost:8000/auth/google/callback`
- No trailing slash
- Must be `http` (not `https`) for local development

### Error: "invalid_client"
- Check that `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are correct
- Ensure there are no extra spaces or quotes in `.env`

### Error: "Access blocked: This app's request is invalid"
- Make sure Gmail API is enabled in Google Cloud Console
- Check that OAuth consent screen is configured

### Error: "Connection refused"
- Server is not running. Start it with: `make dev`
- Check that port 8000 is not in use

### Error: Database connection failed
- Ensure PostgreSQL is running: `make up`
- Check database credentials in `.env`

## Verifying OAuth Tokens in Database

Check if tokens were stored:
```bash
make db-shell
```

Then in PostgreSQL:
```sql
SELECT id, user_id, provider, scope, created_at 
FROM oauth_tokens 
ORDER BY id DESC 
LIMIT 5;
```

## Testing with Your Own Gmail

The app uses a dev authentication system (header-based). In production, you'd implement proper JWT/session auth.

For testing:
- The `X-User-Email` header simulates the logged-in user
- All OAuth tokens are associated with `user_id=1` (demo user)
- You can test with your real Gmail account safely (readonly scope)

## Next Steps

After successful OAuth:
1. Test the scan endpoint with different parameters
2. Review the decision logs in the database
3. Test the apply endpoint (if implemented)
4. Add test users to the database
5. Implement proper authentication

## Security Notes

⚠️ **Important for Production:**
- Never commit `.env` file with real credentials
- Use proper JWT/session authentication (not header-based)
- Implement rate limiting
- Add CSRF protection
- Use HTTPS for redirect URIs
- Rotate `APP_SECRET` regularly
- Consider using a secrets manager (AWS Secrets Manager, HashiCorp Vault, etc.)
