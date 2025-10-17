# 🔐 Authentication System Setup

## What Was Added

### 1. **JWT-Based Authentication**
- User signup and login with email/password
- JWT tokens for secure API access
- Password hashing with bcrypt
- Token expiration (7 days)

### 2. **New Dependencies**
```bash
python-jose[cryptography]==3.3.0  # JWT handling
passlib[bcrypt]==1.7.4            # Password hashing
python-multipart==0.0.9           # Form data handling
```

### 3. **New Files Created**
- `services/auth/utils.py` - JWT and password utilities
- `services/auth/routes.py` - Authentication endpoints
- `test_auth.py` - Test script for auth system

### 4. **Updated Files**
- `db/models.py` - Added `hashed_password` and `is_active` to User model
- `services/gateway/deps.py` - Real JWT authentication instead of hardcoded user
- `services/gateway/main.py` - Added auth routes
- `services/gateway/routes_gmail.py` - Auto-create users from OAuth
- `requirements.txt` - Added auth dependencies
- `.env.example` - Added JWT_SECRET_KEY

---

## 🚀 How to Use

### 1. **Restart the Server**
The server should auto-reload, but if not:
```bash
# Stop current server (Ctrl+C)
make dev
```

### 2. **Test Authentication**
```bash
python test_auth.py
```

This will:
- ✅ Create a test user
- ✅ Login with credentials
- ✅ Get user info with JWT token
- ✅ Access protected Gmail endpoint

### 3. **API Endpoints**

#### **Signup**
```bash
POST /auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}

Response:
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "created_at": "2025-10-17T..."
  }
}
```

#### **Login**
```bash
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=securepassword

Response: (same as signup)
```

#### **Get Current User**
```bash
GET /auth/me
Authorization: Bearer eyJ...

Response:
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2025-10-17T..."
}
```

#### **Protected Gmail Endpoints**
All Gmail endpoints now require authentication:
```bash
POST /auth/google/init
Authorization: Bearer eyJ...

POST /gmail/scan
Authorization: Bearer eyJ...
```

---

## 🔧 How It Works

### 1. **User Signup/Login**
- User provides email + password
- Password is hashed with bcrypt
- JWT token is generated with user ID and email
- Token expires in 7 days

### 2. **Accessing Protected Endpoints**
- Client sends JWT token in `Authorization: Bearer <token>` header
- Server decodes and validates token
- Extracts user ID and email
- Verifies user exists and is active
- Passes `CurrentUser` object to endpoint

### 3. **OAuth Flow with Authentication**
- User must be logged in to start OAuth
- OAuth callback auto-creates user if needed (for testing)
- OAuth tokens are linked to authenticated user
- Each user has their own Gmail tokens

---

## 🎯 Next Steps

### For OpenAI GPT Store:
1. **Deploy backend** to Render/Railway
2. **Configure OAuth** for GPT Actions
3. **Create Custom GPT** with Actions pointing to your API
4. **Test** with real users

### For Web App:
1. **Build React frontend** with login/signup forms
2. **Store JWT** in localStorage/cookies
3. **Add logout** functionality
4. **Build dashboard** to show scan results

---

## 🔒 Security Notes

- ✅ Passwords are hashed with bcrypt (never stored plain text)
- ✅ JWT tokens are signed and verified
- ✅ OAuth tokens are encrypted in database
- ⚠️ Change `JWT_SECRET_KEY` in production
- ⚠️ Use HTTPS in production
- ⚠️ Add rate limiting for auth endpoints

---

## 🐛 Troubleshooting

### "User not found or inactive"
- Token is valid but user was deleted/deactivated
- Login again to get new token

### "Could not validate credentials"
- Token is expired or invalid
- Login again to get new token

### "Email already registered"
- User already exists
- Use login endpoint instead

---

## 📝 Testing Checklist

- [x] User can signup with email/password
- [x] User can login with credentials
- [x] JWT token is generated
- [x] Protected endpoints require authentication
- [x] Invalid tokens are rejected
- [x] OAuth flow works with authenticated users
- [ ] Deploy to production
- [ ] Test with multiple users
- [ ] Add refresh token support (future)
