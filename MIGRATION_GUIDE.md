# 🔄 Cloud Migration Guide

## Overview

Your Deklutter app is **100% portable** and can run on any cloud platform. Here's how to migrate from Render to AWS, GCP, or Azure.

---

## ✅ Why It's Easy to Migrate

### 1. **Dockerized Application**
- ✅ Single `Dockerfile` works everywhere
- ✅ No platform-specific code
- ✅ Consistent environment across clouds

### 2. **Standard Database**
- ✅ PostgreSQL (industry standard)
- ✅ Standard connection string
- ✅ Available on all clouds

### 3. **Environment Variables**
- ✅ 12-factor app methodology
- ✅ No hardcoded configs
- ✅ Easy to reconfigure

### 4. **No Vendor Lock-in**
- ❌ No Render-specific APIs
- ❌ No proprietary services
- ✅ Pure open-source stack

---

## 🚀 Migration Options

### Option 1: Render (Current - Free)

**Pros:**
- ✅ Free tier
- ✅ Easy setup (render.yaml)
- ✅ Auto-configured database
- ✅ Good for MVP/testing

**Cons:**
- ⚠️ Sleeps after 15 min inactivity
- ⚠️ Limited resources on free tier
- ⚠️ US-only regions

**Cost:** $0 (free) or $7/month (starter)

---

### Option 2: AWS (Production Scale)

**Services:**
```
├── ECS/Fargate (Docker containers)
├── RDS PostgreSQL (managed database)
├── ElastiCache Redis (managed cache)
├── ALB (load balancer)
└── Route 53 (DNS)
```

**Pros:**
- ✅ Most mature cloud
- ✅ Best scaling options
- ✅ Global regions
- ✅ Enterprise-grade

**Cons:**
- ⚠️ More complex setup
- ⚠️ Higher cost
- ⚠️ Steeper learning curve

**Cost:** ~$30-50/month (small scale)

**Migration Steps:**

1. **Push Docker image to ECR**
   ```bash
   aws ecr create-repository --repository-name deklutter
   docker build -t deklutter .
   docker tag deklutter:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/deklutter:latest
   docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/deklutter:latest
   ```

2. **Create RDS PostgreSQL**
   ```bash
   aws rds create-db-instance \
     --db-instance-identifier deklutter-db \
     --db-instance-class db.t3.micro \
     --engine postgres \
     --master-username deklutter_user \
     --master-user-password <secure-password> \
     --allocated-storage 20
   ```

3. **Create ECS Service**
   ```bash
   # Create task definition (JSON)
   # Create ECS service
   # Configure environment variables
   ```

4. **Update environment variables**
   ```bash
   DATABASE_URL=postgresql://user:pass@rds-endpoint:5432/deklutter
   REDIS_URL=redis://elasticache-endpoint:6379
   ```

---

### Option 3: GCP (Modern & Simple)

**Services:**
```
├── Cloud Run (serverless containers)
├── Cloud SQL PostgreSQL
├── Memorystore Redis
└── Cloud Load Balancing
```

**Pros:**
- ✅ Serverless (auto-scale to zero)
- ✅ Simple deployment
- ✅ Good pricing
- ✅ Fast global network

**Cons:**
- ⚠️ Smaller ecosystem than AWS
- ⚠️ Fewer regions

**Cost:** ~$20-30/month (small scale)

**Migration Steps:**

1. **Push to Container Registry**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/deklutter
   ```

2. **Create Cloud SQL**
   ```bash
   gcloud sql instances create deklutter-db \
     --database-version=POSTGRES_16 \
     --tier=db-f1-micro \
     --region=us-central1
   ```

3. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy deklutter \
     --image gcr.io/PROJECT_ID/deklutter \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars DATABASE_URL=$DB_URL,REDIS_URL=$REDIS_URL
   ```

---

### Option 4: Azure (Enterprise)

**Services:**
```
├── Container Apps (serverless containers)
├── Azure Database for PostgreSQL
├── Azure Cache for Redis
└── Application Gateway
```

**Pros:**
- ✅ Good for enterprises
- ✅ Strong Microsoft integration
- ✅ Hybrid cloud options

**Cons:**
- ⚠️ More expensive
- ⚠️ Complex pricing

**Cost:** ~$40-60/month (small scale)

---

## 🐳 Docker Deployment (Any Platform)

Your app is fully Dockerized and can run anywhere that supports Docker:

### Build & Run Locally

```bash
# Build image
docker build -t deklutter:latest .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL=$DATABASE_URL \
  -e REDIS_URL=$REDIS_URL \
  -e GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID \
  -e GOOGLE_CLIENT_SECRET=$GOOGLE_CLIENT_SECRET \
  -e JWT_SECRET_KEY=$JWT_SECRET_KEY \
  deklutter:latest
```

### Docker Compose (Full Stack)

I can create a `docker-compose.yml` for you:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/deklutter
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=deklutter_user
      - POSTGRES_PASSWORD=deklutter_password
      - POSTGRES_DB=deklutter
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

---

## 📊 Cost Comparison

| Platform | Free Tier | Small Scale | Medium Scale | Notes |
|----------|-----------|-------------|--------------|-------|
| **Render** | ✅ $0 | $7/mo | $25/mo | Best for MVP |
| **Railway** | ✅ $5 credit | $10/mo | $30/mo | Similar to Render |
| **GCP Cloud Run** | ✅ Free quota | $20/mo | $50/mo | Serverless |
| **AWS ECS** | ❌ No free | $30/mo | $100/mo | Most scalable |
| **Azure** | ❌ No free | $40/mo | $120/mo | Enterprise |
| **DigitalOcean** | ❌ No free | $12/mo | $40/mo | Simple |

---

## 🎯 Recommended Migration Path

### Phase 1: Start with Render (Now)
- ✅ Free tier
- ✅ Quick deployment
- ✅ Test with real users
- ✅ Validate product-market fit

### Phase 2: Scale on Render ($7/mo)
- When you get consistent traffic
- Remove sleep behavior
- More resources

### Phase 3: Migrate to GCP Cloud Run
- When you need global scale
- Better performance
- Auto-scaling
- Still cost-effective

### Phase 4: Move to AWS (If Needed)
- When you need enterprise features
- Complex infrastructure
- Multiple regions
- High availability

---

## 🔧 Migration Checklist

When migrating to any platform:

- [ ] Export database (pg_dump)
- [ ] Push Docker image to new registry
- [ ] Create database on new platform
- [ ] Import data (pg_restore)
- [ ] Update environment variables
- [ ] Update Google OAuth redirect URI
- [ ] Test all endpoints
- [ ] Update DNS (if using custom domain)
- [ ] Monitor for 24 hours
- [ ] Decommission old platform

---

## 🚨 Important Notes

### Database Migration
```bash
# Export from Render
pg_dump $OLD_DATABASE_URL > backup.sql

# Import to new platform
psql $NEW_DATABASE_URL < backup.sql
```

### Zero-Downtime Migration
1. Deploy to new platform
2. Test thoroughly
3. Update DNS to point to new platform
4. Monitor both platforms for 24h
5. Decommission old platform

### OAuth Redirect URIs
Remember to update Google Cloud Console with new URLs:
```
Old: https://deklutter-api-xyz.onrender.com/auth/google/callback
New: https://your-new-domain.com/auth/google/callback
```

---

## 📚 Platform-Specific Guides

### AWS Deployment
See: `docs/aws-deployment.md` (can create if needed)

### GCP Deployment
See: `docs/gcp-deployment.md` (can create if needed)

### Azure Deployment
See: `docs/azure-deployment.md` (can create if needed)

---

## 🎊 Summary

Your app is **100% portable** because:

1. ✅ **Dockerized** - Runs anywhere with Docker
2. ✅ **Standard database** - PostgreSQL works everywhere
3. ✅ **Environment variables** - Easy to reconfigure
4. ✅ **No vendor lock-in** - Pure open-source stack

**Start with Render (free), migrate later when needed!**

Migration time: **~2-4 hours** depending on platform complexity.
