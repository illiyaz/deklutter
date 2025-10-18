# 🌐 Custom Domain Setup Guide

## Why Use a Custom Domain?

**Instead of:**
```
❌ deklutter-api.onrender.com
❌ deklutter-api.us-east-1.elasticbeanstalk.com  
❌ deklutter-api.run.app
```

**Use:**
```
✅ api.deklutter.com
```

### Benefits:
- ✅ **Platform Independence** - Switch from Render → AWS → GCP without changing URLs
- ✅ **No GPT Updates** - GPT schema stays the same
- ✅ **Professional Branding** - Better for users
- ✅ **SSL Control** - Manage your own certificates
- ✅ **Future-Proof** - Easy migrations

---

## Step 1: Buy a Domain

### Recommended Registrars:
- **Namecheap** - $10/year - https://www.namecheap.com
- **Google Domains** - $12/year - https://domains.google
- **Cloudflare** - $9/year - https://www.cloudflare.com/products/registrar

### Domain to Buy:
```
deklutter.com  (or .io, .app, .ai)
```

**Cost:** ~$10-15/year

---

## Step 2: Configure DNS

### For Render (Current):

**In your domain registrar (Namecheap/Google Domains):**

1. Go to DNS settings
2. Add CNAME record:
   ```
   Type: CNAME
   Host: api
   Value: deklutter-api.onrender.com
   TTL: Automatic
   ```

3. Save changes (propagation takes 5-60 minutes)

### For AWS (Future):

```
Type: CNAME
Host: api
Value: your-alb.us-east-1.elb.amazonaws.com
```

### For GCP (Future):

```
Type: A
Host: api
Value: 35.x.x.x (your GCP IP)
```

---

## Step 3: Configure SSL

### Option A: Automatic (Recommended)

**Render:**
1. Go to Render Dashboard
2. Select your service
3. Settings → Custom Domain
4. Add: `api.deklutter.com`
5. Render auto-provisions SSL (Let's Encrypt)
6. Done! ✅

**AWS:**
- Use AWS Certificate Manager (ACM)
- Free SSL certificates
- Auto-renewal

**GCP:**
- Use Google-managed SSL
- Free and automatic

### Option B: Cloudflare (Advanced)

1. Add domain to Cloudflare
2. Point nameservers to Cloudflare
3. Cloudflare provides:
   - Free SSL
   - CDN
   - DDoS protection
   - Analytics

---

## Step 4: Update Your Code

### Update openapi.yaml:

```yaml
servers:
  - url: https://api.deklutter.com  # ← Change this line
    description: Production server
```

### Commit and Deploy:

```bash
git add openapi.yaml
git commit -m "Update to custom domain"
git push
```

**That's it!** ✅

---

## Step 5: Test

```bash
# Test health endpoint
curl https://api.deklutter.com/health

# Should return:
{"ok":true}

# Test OpenAPI
curl https://api.deklutter.com/openapi.json
```

---

## Migration Scenarios

### Scenario 1: Render → AWS

**Before:**
```
URL: https://deklutter-api.onrender.com
DNS: api → deklutter-api.onrender.com
```

**After:**
```
URL: https://api.deklutter.com (same!)
DNS: api → your-alb.us-east-1.elb.amazonaws.com (updated)
```

**Changes needed:**
1. Update DNS CNAME (5 minutes)
2. Wait for propagation (5-60 minutes)
3. Done! ✅

**GPT:** No changes needed!

### Scenario 2: AWS → GCP

**Before:**
```
URL: https://api.deklutter.com
DNS: api → your-alb.us-east-1.elb.amazonaws.com
```

**After:**
```
URL: https://api.deklutter.com (same!)
DNS: api → 35.x.x.x (updated)
```

**Changes needed:**
1. Update DNS A record (5 minutes)
2. Wait for propagation
3. Done! ✅

**GPT:** No changes needed!

---

## Cost Breakdown

### Minimal Setup:
```
Domain: $10/year (Namecheap)
SSL: Free (Let's Encrypt via Render/AWS/GCP)
DNS: Free (included with domain)

Total: $10/year
```

### Professional Setup (with Cloudflare):
```
Domain: $9/year (Cloudflare Registrar)
SSL: Free (Cloudflare)
CDN: Free (Cloudflare)
DDoS Protection: Free (Cloudflare)

Total: $9/year
```

---

## Environment Variables

### Update these on Render:

```bash
# Add to Render Dashboard → Environment
API_URL=https://api.deklutter.com
WEBAPP_URL=https://deklutter.com  # (future)
```

### Update Google OAuth:

1. Go to Google Cloud Console
2. APIs & Services → Credentials
3. Edit OAuth 2.0 Client
4. Add redirect URI:
   ```
   https://api.deklutter.com/auth/google/callback
   https://api.deklutter.com/oauth/google/callback
   ```
5. Save

---

## Subdomain Strategy

### Recommended Structure:

```
deklutter.com           → Main website (future)
api.deklutter.com       → API (current)
app.deklutter.com       → Web app (future)
docs.deklutter.com      → Documentation (future)
blog.deklutter.com      → Blog (future)
```

### DNS Configuration:

```
Type: A
Host: @
Value: 76.76.21.21 (GitHub Pages or Vercel)

Type: CNAME
Host: api
Value: deklutter-api.onrender.com

Type: CNAME
Host: app
Value: deklutter-app.vercel.app

Type: CNAME
Host: docs
Value: deklutter.github.io

Type: CNAME
Host: blog
Value: deklutter.ghost.io
```

---

## Troubleshooting

### Issue: DNS not propagating

**Check:**
```bash
# Check DNS
dig api.deklutter.com

# Check from different locations
https://www.whatsmydns.net
```

**Wait:** 5-60 minutes for full propagation

### Issue: SSL certificate error

**Render:**
- Wait 5-10 minutes after adding custom domain
- Render auto-provisions SSL

**Fix:**
- Remove and re-add custom domain in Render

### Issue: 404 errors

**Check:**
- DNS points to correct server
- Server is running
- Firewall allows HTTPS (port 443)

---

## Timeline

### Day 1: Setup
- Buy domain (5 minutes)
- Configure DNS (5 minutes)
- Add to Render (2 minutes)
- Wait for SSL (10 minutes)
- Update code (5 minutes)
- Test (5 minutes)

**Total: ~30 minutes + DNS propagation**

### Day 2: Verify
- Check all endpoints work
- Update documentation
- Update GPT (if needed)

---

## Checklist

Before going live with custom domain:

- [ ] Domain purchased
- [ ] DNS configured (CNAME record)
- [ ] Added to Render/AWS/GCP
- [ ] SSL certificate active
- [ ] `openapi.yaml` updated
- [ ] Code deployed
- [ ] Health endpoint working
- [ ] Google OAuth redirect URIs updated
- [ ] Environment variables updated
- [ ] GPT tested (if already published)
- [ ] Documentation updated

---

## Future: Multi-Region Setup

### With Custom Domain:

```
api.deklutter.com → Cloudflare (global CDN)
  ↓
  ├─→ us-east-1 (AWS)
  ├─→ eu-west-1 (AWS)
  └─→ asia-southeast-1 (AWS)
```

**Benefits:**
- Global low latency
- High availability
- Auto-failover
- Same URL everywhere

**Cost:** ~$50/month (AWS)

---

## Recommended: Start Simple

### Phase 1 (Now):
```
api.deklutter.com → Render
```
**Cost:** $10/year

### Phase 2 (Month 3):
```
api.deklutter.com → Cloudflare → Render
```
**Cost:** $9/year

### Phase 3 (Month 6):
```
api.deklutter.com → Cloudflare → AWS (multi-region)
```
**Cost:** ~$50/month

---

## Summary

**Why:** Platform independence, professionalism, future-proofing
**Cost:** $10/year
**Time:** 30 minutes setup
**Benefit:** Never update GPT schema when changing platforms

**Recommended:** Set up custom domain before publishing GPT to avoid future updates.

---

**Questions?** Email: mohammad.illiyaz@gmail.com
