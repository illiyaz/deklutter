# Deployment Guide - api.deklutter.co

**Last Updated:** Oct 19, 2025

This guide walks you through deploying Deklutter to production with your custom domain.

---

## 📋 Pre-Deployment Checklist

- [ ] Domain purchased: `deklutter.co` ✅
- [ ] Render account created
- [ ] Google Cloud Console project created
- [ ] Database ready (PostgreSQL on Render)
- [ ] Environment variables prepared

---

## 🌐 Step 1: DNS Configuration

### **In Your Domain Registrar (Namecheap/GoDaddy/etc.):**

Add these DNS records:

```
Type: CNAME
Name: api
Value: deklutter-api.onrender.com (or your Render app URL)
TTL: Automatic (or 3600)
```

**Alternative (if Render gives you an IP):**
```
Type: A
Name: api
Value: [IP from Render]
TTL: Automatic
```

**Note:** DNS propagation can take 5-60 minutes.

---

## 🚀 Step 2: Render Setup

### **2.1 Create Web Service:**

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository: `illiyaz/deklutter`
4. Configure:
   - **Name:** `deklutter-api`
   - **Region:** Choose closest to your users
   - **Branch:** `main`
   - **Root Directory:** `.` (leave empty)
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn services.gateway.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** Free (or Starter for production)

### **2.2 Add Custom Domain:**

1. In your Render service, go to **Settings** → **Custom Domain**
2. Click **"Add Custom Domain"**
3. Enter: `api.deklutter.co`
4. Render will show you a CNAME value
5. Add that CNAME to your DNS (see Step 1)
6. Wait for verification (5-60 minutes)

### **2.3 Enable Auto-Deploy:**

1. Go to **Settings** → **Build & Deploy**
2. Enable **"Auto-Deploy"** for `main` branch
3. Every push to `main` will auto-deploy ✅

---

## 🔐 Step 3: Environment Variables

### **In Render Dashboard → Environment:**

Add these environment variables:

```bash
# Database (Render provides this automatically)
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# API URL
API_URL=https://api.deklutter.co

# Google OAuth
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=https://api.deklutter.co/auth/google/callback

# GPT OAuth
GPT_CLIENT_ID=deklutter-gpt
GPT_CLIENT_SECRET=[generate with: python3 -c "import secrets; print(secrets.token_urlsafe(32))"]

# Security Keys
APP_SECRET=[generate with: python3 -c "import secrets; print(secrets.token_urlsafe(32))"]
JWT_SECRET_KEY=[generate with: python3 -c "import secrets; print(secrets.token_urlsafe(32))"]

# Python version
PYTHON_VERSION=3.13.0
```

**Generate secure secrets:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 🔑 Step 4: Google Cloud Console Setup

### **4.1 Update OAuth Redirect URIs:**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Go to **APIs & Services** → **Credentials**
4. Click on your OAuth 2.0 Client ID
5. Under **Authorized redirect URIs**, add:
   ```
   https://api.deklutter.co/auth/google/callback
   https://api.deklutter.co/auth/gpt/oauth/callback
   ```
6. Click **Save**

### **4.2 Update Authorized JavaScript Origins (if needed):**

Add:
```
https://api.deklutter.co
```

---

## 🤖 Step 5: ChatGPT GPT Configuration

### **5.1 Update GPT Actions:**

1. Go to [ChatGPT GPT Builder](https://chat.openai.com/gpts/editor)
2. Open your Deklutter GPT
3. Go to **Actions** → **Schema**
4. Update the server URL in your OpenAPI schema:
   ```yaml
   servers:
     - url: https://api.deklutter.co
   ```
5. Click **Update**

### **5.2 Update OAuth Settings:**

In GPT Actions → Authentication:
- **Authorization URL:** `https://api.deklutter.co/auth/gpt/oauth/authorize`
- **Token URL:** `https://api.deklutter.co/auth/gpt/oauth/token`
- **Client ID:** `deklutter-gpt`
- **Client Secret:** [same as GPT_CLIENT_SECRET in Render]
- **Scope:** (leave empty)

### **5.3 Update Instructions:**

Copy the contents of `GPT_INSTRUCTIONS.md` to the GPT's instructions field.

---

## ✅ Step 6: Verify Deployment

### **6.1 Check Health:**

```bash
curl https://api.deklutter.co/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "services": {
    "database": "healthy",
    "api": "healthy"
  }
}
```

### **6.2 Check Version:**

```bash
curl https://api.deklutter.co/version
```

### **6.3 Check Privacy Policy:**

Visit: https://api.deklutter.co/privacy

### **6.4 Check OpenAPI Docs:**

Visit: https://api.deklutter.co/docs

---

## 🧪 Step 7: Test OAuth Flow

### **7.1 Test Google OAuth:**

1. Open ChatGPT
2. Start conversation with your Deklutter GPT
3. Say: "Scan my inbox"
4. Click the authorization link
5. Authorize with Google
6. Verify you're redirected back to ChatGPT
7. Check that scan works

### **7.2 Test End-to-End:**

1. Scan inbox
2. Review results
3. Delete some emails
4. Verify emails moved to trash in Gmail
5. Check stats endpoint

---

## 🐛 Troubleshooting

### **DNS not resolving:**
- Wait 5-60 minutes for propagation
- Check DNS with: `nslookup api.deklutter.co`
- Verify CNAME points to Render

### **OAuth redirect mismatch:**
- Verify redirect URI in Google Console matches exactly
- Check Render environment variable: `GOOGLE_REDIRECT_URI`
- Clear browser cache

### **Database connection error:**
- Check `DATABASE_URL` in Render environment
- Verify PostgreSQL service is running
- Check database logs in Render

### **500 Internal Server Error:**
- Check Render logs: Dashboard → Logs
- Look for Python errors
- Verify all environment variables are set

### **GPT can't connect:**
- Verify OpenAPI schema server URL
- Check GPT OAuth settings
- Test API directly with curl first

---

## 📊 Monitoring

### **Render Dashboard:**
- Monitor CPU/Memory usage
- Check logs for errors
- Set up alerts

### **Health Check:**
Set up a cron job to ping health endpoint:
```bash
*/5 * * * * curl https://api.deklutter.co/health
```

### **Error Tracking:**
Check Render logs regularly:
```bash
# In Render Dashboard → Logs
# Filter by: ERROR, WARNING
```

---

## 🔄 Continuous Deployment

Every push to `main` branch automatically deploys:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

Render will:
1. Pull latest code
2. Install dependencies
3. Run migrations (if any)
4. Deploy new version
5. Health check
6. Switch traffic

**Deployment time:** ~2-5 minutes

---

## 🎯 Post-Deployment Tasks

- [ ] Test OAuth flow end-to-end
- [ ] Scan your own inbox
- [ ] Check privacy policy page
- [ ] Verify stats endpoints work
- [ ] Share with 2-3 friends for beta testing
- [ ] Monitor logs for errors
- [ ] Set up uptime monitoring (UptimeRobot, etc.)

---

## 📝 Maintenance

### **Weekly:**
- Check Render logs for errors
- Monitor database size
- Review user feedback

### **Monthly:**
- Update dependencies: `pip list --outdated`
- Review and rotate secrets
- Check for security updates

### **Quarterly:**
- Database cleanup (expired OAuth states)
- Performance optimization
- Feature updates

---

## 🆘 Rollback

If deployment fails:

1. Go to Render Dashboard → Deploys
2. Find last successful deploy
3. Click **"Redeploy"**
4. Or revert git commit:
   ```bash
   git revert HEAD
   git push origin main
   ```

---

## 📞 Support

- **Render Support:** https://render.com/docs
- **Google OAuth:** https://developers.google.com/identity/protocols/oauth2
- **Issues:** https://github.com/illiyaz/deklutter/issues

---

**Good luck with your deployment!** 🚀
