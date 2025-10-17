# Fix "Access blocked: Authorization Error"

## Step-by-Step Fix

### 1. Go to Google Cloud Console
https://console.cloud.google.com/

### 2. Select Your Project
- Click the project dropdown at the top
- Select your Deklutter project

### 3. Go to OAuth Consent Screen
- Left sidebar: **APIs & Services** → **OAuth consent screen**

### 4. Add Yourself as Test User
- Scroll to **Test users** section
- Click **+ ADD USERS**
- Enter the Gmail address you want to test with (the one you're authorizing)
- Click **SAVE**

### 5. Verify App Configuration
Click **EDIT APP** and check each step:

#### App Information
- ✅ App name: `Deklutter`
- ✅ User support email: Your email
- ✅ App logo: Optional for testing
- ✅ Developer contact: Your email

#### Scopes
- ✅ Click **ADD OR REMOVE SCOPES**
- ✅ Filter for "gmail"
- ✅ Check: `https://www.googleapis.com/auth/gmail.readonly`
- ✅ Click **UPDATE**
- ✅ Click **SAVE AND CONTINUE**

#### Test Users
- ✅ Your Gmail address should be listed
- ✅ If not, add it here

#### Summary
- ✅ Review and click **BACK TO DASHBOARD**

### 6. Wait a Moment
Sometimes changes take 1-2 minutes to propagate.

### 7. Try Again
```bash
python test_gmail.py
# Choose option 1 again
```

## Alternative: Use a Different Scope

If you're still having issues, try starting with a more basic scope:

### Update the OAuth Code Temporarily

Edit: `services/gmail_connector/oauth.py`

Change line 12 from:
```python
_SCOPES_READONLY = ["https://www.googleapis.com/auth/gmail.readonly"]
```

To:
```python
_SCOPES_READONLY = ["https://www.googleapis.com/auth/userinfo.email"]
```

This will just test OAuth without Gmail access. Once that works, add Gmail scopes back.

## Common Error Messages & Solutions

### "Access blocked: This app's request is invalid"
- **Cause**: OAuth consent screen not configured
- **Fix**: Complete all steps in OAuth consent screen

### "Access blocked: Authorization Error"
- **Cause**: You're not added as a test user
- **Fix**: Add your email to test users list

### "redirect_uri_mismatch"
- **Cause**: Redirect URI doesn't match
- **Fix**: Ensure it's exactly: `http://localhost:8000/auth/google/callback`

### "invalid_client"
- **Cause**: Wrong Client ID or Secret
- **Fix**: Re-copy credentials from Google Cloud Console

## Verify Your Setup

### Check Credentials Page
Go to: **APIs & Services** → **Credentials**

Your OAuth 2.0 Client should show:
- **Type**: Web application
- **Authorized redirect URIs**: `http://localhost:8000/auth/google/callback`

### Check Gmail API
Go to: **APIs & Services** → **Library**
- Search: "Gmail API"
- Status should be: **Enabled** (green checkmark)

## Still Not Working?

### Option 1: Create New OAuth Client
1. Go to **Credentials**
2. Delete the old OAuth client
3. Create a new one:
   - Type: Web application
   - Name: Deklutter Dev
   - Redirect URI: `http://localhost:8000/auth/google/callback`
4. Copy new Client ID and Secret to `.env`

### Option 2: Use Google's OAuth Playground
Test if your account can authorize at all:
1. Go to: https://developers.google.com/oauthplayground/
2. Click settings (gear icon)
3. Check "Use your own OAuth credentials"
4. Enter your Client ID and Secret
5. Try authorizing with Gmail scope
6. If this works, the issue is in your app code
7. If this fails, the issue is in Google Cloud setup

## Need More Help?

Check the full error message in the browser URL after the error. It usually contains:
```
?error=access_denied&error_description=...
```

The `error_description` will give you more details about what went wrong.
