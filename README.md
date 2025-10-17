# 📧 Deklutter

AI-powered Gmail inbox cleaner that automatically identifies and removes spam, newsletters, and promotional emails.

## ✨ Features

- 🔐 **Secure OAuth 2.0** - Google authentication with encrypted token storage
- 🤖 **Smart Classification** - Heuristic-based email categorization
- 👤 **Multi-user Support** - JWT authentication for multiple users
- 📊 **Scan & Review** - Preview decisions before applying
- 🗑️ **Safe Deletion** - Move to trash (recoverable) or label for review
- 🚀 **REST API** - Full-featured API for integrations

## 🏗️ Tech Stack

- **Backend**: FastAPI (Python 3.13)
- **Database**: PostgreSQL
- **Cache**: Redis
- **Authentication**: JWT + OAuth 2.0
- **Gmail API**: Google API Python Client

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.13+
- Docker & Docker Compose
- Google Cloud Project with Gmail API enabled

### 2. Setup

```bash
# Clone repository
git clone <your-repo>
cd deklutter

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your credentials:
# - GOOGLE_CLIENT_ID
# - GOOGLE_CLIENT_SECRET
# - GOOGLE_REDIRECT_URI
# - JWT_SECRET_KEY
# - APP_SECRET
```

### 3. Start Infrastructure

```bash
# Start PostgreSQL and Redis
docker compose -f infra/docker-compose.yml up -d

# Or use make
make infra
```

### 4. Run Server

```bash
# Development mode
make dev

# Or manually
uvicorn services.gateway.main:app --reload --port 8000
```

### 5. Access API

- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📚 API Endpoints

### Authentication

```bash
# Signup
POST /auth/signup
{
  "email": "user@example.com",
  "password": "securepassword"
}

# Login
POST /auth/login
username=user@example.com&password=securepassword

# Get current user
GET /auth/me
Authorization: Bearer <token>
```

### Gmail Integration

```bash
# Initialize OAuth
POST /auth/google/init
Authorization: Bearer <token>

# Scan Gmail
POST /gmail/scan
Authorization: Bearer <token>
{
  "days_back": 365,
  "limit": 100
}

# Apply cleanup
POST /gmail/apply
Authorization: Bearer <token>
{
  "message_ids": ["msg_id_1", "msg_id_2"],
  "mode": "trash"  # or "label_only"
}
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | Yes |
| `GOOGLE_CLIENT_SECRET` | Google OAuth client secret | Yes |
| `GOOGLE_REDIRECT_URI` | OAuth callback URL | Yes |
| `JWT_SECRET_KEY` | Secret for JWT signing | Yes |
| `APP_SECRET` | Secret for token encryption | Yes |

### Google Cloud Setup

1. Create project at https://console.cloud.google.com
2. Enable Gmail API
3. Create OAuth 2.0 credentials
4. Add authorized redirect URI
5. Configure OAuth consent screen
6. Add test users (for testing mode)

See [AUTHENTICATION_SETUP.md](./AUTHENTICATION_SETUP.md) for detailed instructions.

## 🧪 Testing

```bash
# Test authentication
python test_auth.py

# Test Gmail integration
python test_gmail.py
```

## 📦 Deployment

### Using Docker

```bash
# Build image
docker build -t deklutter:latest .

# Run container
docker run -p 8000:8000 --env-file .env deklutter:latest
```

### Using Render/Railway

1. Connect your GitHub repository
2. Set environment variables
3. Deploy!

## 🛣️ Roadmap

- [ ] Deploy to production
- [ ] Create OpenAI GPT with Actions
- [ ] Build React frontend
- [ ] Add LLM-based classification
- [ ] Implement scheduled scanning
- [ ] Add mobile app support

## 📄 License

MIT

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

## 📧 Contact

For questions or support, contact: mohammad.illiyaz@gmail.com