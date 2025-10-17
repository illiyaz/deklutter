# 🚀 Deploy Deklutter - Quick Start

## ✅ Pre-Deployment Status

Your application is **production-ready**! Here's what's done:

- ✅ Code cleaned (no debug prints)
- ✅ Proper logging configured
- ✅ Authentication system working
- ✅ Gmail OAuth integration working
- ✅ Multi-user support implemented
- ✅ Dockerfile created
- ✅ Render configuration ready
- ✅ Documentation complete

---

## 🎯 Deploy in 3 Steps

### Step 1: Add JWT Secret (1 minute)

Run this command to generate and add secrets:

```bash
python scripts/generate_secrets.py
```

Copy the JWT_SECRET_KEY line and add it to your `.env` file.

### Step 2: Push to GitHub (2 minutes)

```bash
# Initialize git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Production ready - Deploy to Render"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/deklutter.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy to Render (5 minutes)

1. Go to https://render.com
2. Sign up with GitHub
3. Click **"New +"** → **"Blueprint"**
4. Select your `deklutter` repository
5. Render detects `render.yaml` automatically
6. Click **"Apply"**
7. Wait 3-5 minutes for deployment

---

## 🔧 Post-Deployment Configuration

### 1. Get Your Render URL

After deployment, Render gives you a URL like:
```
https://deklutter-api-xyz.onrender.com
```

### 2. Add Environment Variables in Render

Go to your service → Environment:

```bash
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=https://deklutter-api-xyz.onrender.com/auth/google/callback
```

### 3. Update Google Cloud Console

**OAuth Credentials:**
- Add redirect URI: `https://deklutter-api-xyz.onrender.com/auth/google/callback`

**OAuth Consent Screen:**
- Home page: `https://deklutter-api-xyz.onrender.com`
- Privacy: `https://deklutter-api-xyz.onrender.com/privacy`
- Terms: `https://deklutter-api-xyz.onrender.com/terms`
- Authorized domain: `onrender.com`

### 4. Restart Service

In Render dashboard:
- Click "Manual Deploy" → "Deploy latest commit"

---

## ✅ Verify Deployment

### Test Health Endpoint

```bash
curl https://your-app.onrender.com/health
# Should return: {"ok":true}
```

### Test API Docs

Visit: `https://your-app.onrender.com/docs`

### Test Authentication

```bash
# Signup
curl -X POST https://your-app.onrender.com/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'

# Should return access token
```

### Test Full Flow

1. Login and get token
2. Initialize OAuth
3. Authorize Gmail access
4. Scan emails
5. Apply cleanup

---

## 📊 What Gets Deployed

### Services Created by Render

1. **deklutter-api** (Web Service)
   - Your FastAPI application
   - Runs on free tier
   - Auto-sleeps after 15 min inactivity
   - Auto-wakes on request

2. **deklutter-db** (PostgreSQL)
   - 1GB free storage
   - Persistent data
   - Auto-backups

3. **deklutter-redis** (Redis)
   - 25MB free memory
   - For caching/sessions

### Costs

- **Free Tier**: $0/month
  - 750 hours/month web service
  - 1GB PostgreSQL
  - 25MB Redis
  - Sleeps after inactivity

- **Paid Tier**: $7/month (optional)
  - Always-on service
  - More resources
  - No sleep

---

## 🎯 Next Steps After Deployment

### 1. Create OpenAI GPT (Recommended)

Once deployed, you can create a Custom GPT:

1. Go to ChatGPT
2. Create new GPT
3. Configure Actions pointing to your Render URL
4. Add OAuth configuration
5. Test with real users

See `OPENAI_GPT_GUIDE.md` (coming next!)

### 2. Build Frontend (Optional)

- React dashboard
- Email preview
- Action buttons
- Better UX than chat

### 3. Monitor & Scale

- Set up error tracking (Sentry)
- Monitor logs in Render
- Upgrade to paid tier if needed

---

## 🐛 Troubleshooting

### Service Won't Start

**Check Render logs:**
- Go to service → Logs tab
- Look for errors

**Common issues:**
- Missing environment variables
- Database connection failed
- Wrong Python version

### OAuth Callback 404

**Issue:** Redirect URI mismatch

**Fix:**
1. Check exact URL in Render
2. Update Google Console
3. Update `GOOGLE_REDIRECT_URI` env var
4. Restart service

### Database Connection Error

**Fix:**
- Verify PostgreSQL service is running
- Check `DATABASE_URL` is auto-configured
- Wait for database to fully start (2-3 min)

---

## 📞 Support

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com
- **GitHub Issues**: Create an issue in your repo

---

## 🎊 You're Ready!

Your application is **production-ready** and **ready to deploy**!

**Total deployment time: ~10 minutes**

1. ⏱️ Add JWT secret (1 min)
2. ⏱️ Push to GitHub (2 min)
3. ⏱️ Deploy to Render (5 min)
4. ⏱️ Configure OAuth (2 min)

**Let's deploy!** 🚀
