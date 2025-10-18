# Using SSH Tunnel for OAuth Testing

Since Google doesn't accept localhost URLs, we need a public URL that tunnels to localhost.

## Option 1: localhost.run (Easiest - No Installation)

### Step 1: Start your server
```bash
make dev
```

### Step 2: In a NEW terminal, create tunnel
```bash
ssh -R 80:localhost:8000 nokey@localhost.run
```

You'll see output like:
```
Connect to http://abc123.localhost.run or https://abc123.localhost.run
```

### Step 3: Update Google OAuth Console
Use the HTTPS URL:
- Application home page: `https://abc123.localhost.run`
- Privacy policy: `https://abc123.localhost.run/privacy`
- Terms of service: `https://abc123.localhost.run/terms`
- Authorized redirect URI: `https://abc123.localhost.run/auth/google/callback`

### Step 4: Update .env
```bash
GOOGLE_REDIRECT_URI=https://abc123.localhost.run/auth/google/callback
```

### Step 5: Restart server and test

**Note:** The URL changes each time you restart the tunnel.

## Option 2: Just Leave Fields Empty (Simplest)

For testing mode, Google allows empty privacy/terms fields:

1. Go to OAuth consent screen
2. Leave these EMPTY:
   - Application home page
   - Privacy policy link
   - Terms of service link
   - Authorized domains
3. Only fill required fields:
   - App name: Deklutter
   - User support email
   - Developer contact email
4. Save

This should work for testing mode!

## Option 3: Install ngrok (Best for Long-term Development)

```bash
brew install ngrok
ngrok http 8000
```

Then use the ngrok URL in Google Console.


# (.venv) (base) LENOVO@MacBook-Pro deklutter % ngrok config add-authtoken 34COVgGKEIJsUveHAEBahu5bBdt_7iRt9gqXP81XpzKwv5eEa
# Authtoken saved to configuration file: /Users/LENOVO/Library/Application Support/ngrok/ngrok.yml