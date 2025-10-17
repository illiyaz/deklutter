# 🚀 Deployment Guide - Render

## Prerequisites

1. **GitHub Account** - Your code must be in a GitHub repository
2. **Render Account** - Sign up at https://render.com (free)
3. **Google Cloud Project** - With OAuth credentials configured

---

## Step 1: Prepare Your Repository

### 1.1 Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Production ready"

# Create GitHub repo and push
git remote add origin https://github.com/YOUR_USERNAME/deklutter.git
git branch -M main
git push -u origin main
```

### 1.2 Verify Files

Make sure these files are in your repo:
- ✅ `Dockerfile`
- ✅ `render.yaml`
- ✅ `.dockerignore`
- ✅ `requirements.txt`
- ✅ All `services/` code
- ✅ All `db/` code

---

## Step 2: Deploy to Render

### 2.1 Create Render Account

1. Go to https://render.com
2. Sign up with GitHub
3. Authorize Render to access your repositories

### 2.2 Create New Blueprint

1. Click **"New +"** → **"Blueprint"**
2. Connect your GitHub repository
3. Render will detect `render.yaml` automatically
4. Click **"Apply"**

### 2.3 Configure Environment Variables

Render will create 3 services:
- `deklutter-api` (Web Service)
- `deklutter-db` (PostgreSQL)
- `deklutter-redis` (Redis)

For the **deklutter-api** service, add these environment variables:

#### Required Variables

| Variable | Value | How to Get |
|----------|-------|------------|
| `GOOGLE_CLIENT_ID` | Your client ID | From Google Cloud Console |
| `GOOGLE_CLIENT_SECRET` | Your client secret | From Google Cloud Console |
| `GOOGLE_REDIRECT_URI` | `https://your-app.onrender.com/auth/google/callback` | Will be generated after deployment |

#### Auto-Generated (Don't Change)
- `DATABASE_URL` - Auto-configured from PostgreSQL
- `REDIS_URL` - Auto-configured from Redis
- `JWT_SECRET_KEY` - Auto-generated secure key
- `APP_SECRET` - Auto-generated secure key

### 2.4 Update Google OAuth Redirect URI

1. After deployment, Render gives you a URL like: `https://deklutter-api-xyz.onrender.com`
2. Go to Google Cloud Console → Credentials
3. Edit your OAuth 2.0 Client
4. Add redirect URI: `https://deklutter-api-xyz.onrender.com/auth/google/callback`
5. Update `GOOGLE_REDIRECT_URI` in Render environment variables
6. Restart the service

---

## Step 3: Verify Deployment

### 3.1 Check Health

```bash
curl https://your-app.onrender.com/health
# Should return: {"ok":true}
```

### 3.2 Check API Docs

Visit: `https://your-app.onrender.com/docs`

### 3.3 Test Authentication

```bash
# Signup
curl -X POST https://your-app.onrender.com/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"securepassword"}'

# Should return access token
```

---

## Step 4: Update OAuth Consent Screen

### 4.1 Update URLs in Google Console

Go to OAuth Consent Screen and update:

- **Application home page**: `https://your-app.onrender.com`
- **Privacy policy**: `https://your-app.onrender.com/privacy`
- **Terms of service**: `https://your-app.onrender.com/terms`
- **Authorized domains**: `onrender.com`

### 4.2 Add Production Redirect URI

In Credentials → OAuth 2.0 Client:

```
https://your-app.onrender.com/auth/google/callback
```

---

## Step 5: Test Full Flow

### 5.1 Test Authentication

```bash
# Get token
TOKEN=$(curl -s -X POST https://your-app.onrender.com/auth/login \
  -d "username=test@example.com&password=securepassword" | jq -r .access_token)

echo $TOKEN
```

### 5.2 Test OAuth Init

```bash
curl -X POST https://your-app.onrender.com/auth/google/init \
  -H "Authorization: Bearer $TOKEN"

# Returns OAuth URL - open in browser
```

### 5.3 Test Gmail Scan

```bash
curl -X POST https://your-app.onrender.com/gmail/scan \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"days_back":7,"limit":50}'
```

---

## Alternative: Manual Deployment

If you prefer not to use `render.yaml`:

### Option A: Web Service Only

1. **New Web Service**
   - Connect GitHub repo
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn services.gateway.main:app --host 0.0.0.0 --port $PORT`

2. **Add PostgreSQL**
   - New PostgreSQL database
   - Copy connection string
   - Add as `DATABASE_URL` env var

3. **Add Redis**
   - New Redis instance
   - Copy connection string
   - Add as `REDIS_URL` env var

### Option B: Docker Deployment

1. **New Web Service**
   - Connect GitHub repo
   - Environment: Docker
   - Dockerfile path: `./Dockerfile`

---

## Troubleshooting

### Service Won't Start

**Check logs in Render dashboard:**
```bash
# Common issues:
- Missing environment variables
- Database connection failed
- Port binding error
```

**Solution:**
- Verify all env vars are set
- Check DATABASE_URL format
- Ensure using `$PORT` in start command

### OAuth Callback 404

**Issue:** Redirect URI mismatch

**Solution:**
1. Check exact URL in Render dashboard
2. Update Google Cloud Console redirect URI
3. Update `GOOGLE_REDIRECT_URI` env var
4. Restart service

### Database Connection Error

**Issue:** PostgreSQL not accessible

**Solution:**
1. Verify PostgreSQL service is running
2. Check `DATABASE_URL` is set correctly
3. Ensure internal connection is enabled

---

## Production Checklist

- [ ] Code pushed to GitHub
- [ ] Render services deployed
- [ ] Environment variables configured
- [ ] Google OAuth redirect URI updated
- [ ] Health endpoint returns 200
- [ ] API docs accessible
- [ ] Authentication working
- [ ] Gmail OAuth flow working
- [ ] Email scanning working

---

## Monitoring & Logs

### View Logs

In Render dashboard:
1. Go to your service
2. Click "Logs" tab
3. See real-time logs

### Set Up Alerts

1. Go to service settings
2. Enable "Health Check Path": `/health`
3. Set up email notifications

---

## Scaling (Future)

### Free Tier Limits
- **Web Service**: Spins down after 15 min inactivity
- **Database**: 1GB storage
- **Redis**: 25MB memory

### Upgrade Options
- **Starter ($7/mo)**: Always on, more resources
- **Standard ($25/mo)**: Auto-scaling, more storage
- **Pro ($85/mo)**: High availability, dedicated resources

---

## Next Steps

1. ✅ Deploy to Render
2. ⏭️ Create OpenAI GPT with Actions
3. ⏭️ Build React frontend
4. ⏭️ Set up monitoring (Sentry, Datadog)
5. ⏭️ Add custom domain

---

## Support

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com
- **Your Email**: mohammad.illiyaz@gmail.com

**Good luck with deployment!** 🚀
