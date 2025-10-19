# Adding a New Email Provider to Deklutter

**Last Updated:** Oct 19, 2025

This document provides a step-by-step checklist for adding a new email provider (Yahoo, Outlook, etc.) to Deklutter.

---

## 📋 Pre-Implementation Checklist

Before you start coding, gather this information about the provider:

- [ ] **Provider Name:** (e.g., Yahoo Mail, Outlook, ProtonMail)
- [ ] **API Documentation URL:** 
- [ ] **OAuth 2.0 Support:** Yes/No
- [ ] **API Rate Limits:**
  - Daily quota: 
  - Per-second limit:
  - Batch request support: Yes/No (max batch size: ___)
- [ ] **Required Scopes/Permissions:**
  - Read emails: 
  - Delete/modify emails:
  - List folders/labels:
- [ ] **API Endpoints:**
  - List messages:
  - Get message details:
  - Delete/trash message:
  - Create label:
  - Batch endpoint (if available):

---

## 🔧 Implementation Steps

### **Step 1: Add Provider Configuration**

**File:** `services/connectors/provider_config.py`

Add a new entry to `PROVIDER_CONFIGS`:

```python
"yahoo": ProviderConfig(
    name="yahoo",
    display_name="Yahoo Mail",
    
    # Rate limiting (adjust based on API docs)
    max_emails_per_scan=500,
    batch_size=50,
    rate_limit_delay=0.2,
    
    # Retry configuration
    max_retries=3,
    retry_delay=3.0,
    retry_on_status_codes=[429, 500, 503],
    
    # Circuit breaker
    circuit_breaker_failure_threshold=3,
    circuit_breaker_timeout=120,
    circuit_breaker_success_threshold=3,
    
    # API quota info
    daily_quota="10,000 requests/day",
    quota_per_second="10 requests/second",
    notes="Yahoo Mail API has stricter rate limits."
)
```

**Test:**
```bash
python3 services/connectors/provider_config.py
# Should print provider configurations without errors
```

---

### **Step 2: Create OAuth Handler**

**File:** `services/auth/oauth/providers/{provider_name}.py`

Create a new OAuth provider class:

```python
from services.auth.oauth.base import OAuthProvider
import os
import requests

class YahooOAuthProvider(OAuthProvider):
    def __init__(self):
        super().__init__(
            provider_name="yahoo",
            client_id=os.getenv("YAHOO_CLIENT_ID"),
            client_secret=os.getenv("YAHOO_CLIENT_SECRET"),
            redirect_uri=os.getenv("YAHOO_REDIRECT_URI"),
            auth_url="https://api.login.yahoo.com/oauth2/request_auth",
            token_url="https://api.login.yahoo.com/oauth2/get_token",
            scopes=["mail-r", "mail-w"]  # Adjust based on provider
        )
    
    def get_authorization_url(self, state: str) -> str:
        # Implement provider-specific auth URL generation
        pass
    
    def exchange_code_for_token(self, code: str) -> dict:
        # Implement token exchange
        pass
    
    def refresh_token(self, refresh_token: str) -> dict:
        # Implement token refresh
        pass
    
    def revoke_token(self, token: str) -> bool:
        # Implement token revocation
        pass
```

**Checklist:**
- [ ] Implement all abstract methods
- [ ] Handle provider-specific OAuth quirks
- [ ] Add error handling
- [ ] Test token exchange flow
- [ ] Test token refresh flow

---

### **Step 3: Create Email Connector**

**File:** `services/connectors/{provider_name}/connector.py`

Create a connector that implements the standard interface:

```python
from services.connectors.base import EmailConnector
from services.connectors.provider_config import get_provider_config

class YahooConnector(EmailConnector):
    def __init__(self):
        self.config = get_provider_config("yahoo")
        self.circuit_breaker = get_circuit_breaker(
            "yahoo_api",
            failure_threshold=self.config.circuit_breaker_failure_threshold,
            timeout=self.config.circuit_breaker_timeout,
            success_threshold=self.config.circuit_breaker_success_threshold
        )
    
    def list_messages(self, user_id: int, days_back: int, limit: int) -> list:
        # Implement with retry logic and circuit breaker
        pass
    
    def get_message(self, user_id: int, message_id: str) -> dict:
        # Implement message fetching
        pass
    
    def delete_message(self, user_id: int, message_id: str) -> bool:
        # Implement deletion
        pass
    
    def create_label(self, user_id: int, label_name: str) -> str:
        # Implement label creation
        pass
```

**Checklist:**
- [ ] Use provider config for rate limits
- [ ] Implement retry logic with exponential backoff
- [ ] Integrate circuit breaker
- [ ] Add comprehensive logging
- [ ] Handle provider-specific errors
- [ ] Support batch requests (if available)

---

### **Step 4: Add API Routes**

**File:** `services/gateway/routes_{provider_name}.py`

Create API endpoints for the new provider:

```python
from fastapi import APIRouter, Depends
from services.connectors.yahoo.connector import YahooConnector

router = APIRouter()
connector = YahooConnector()

@router.post("/yahoo/scan")
def scan_yahoo(
    user: CurrentUser = Depends(get_current_user),
    days_back: int = 30,
    limit: int = 500,
    db: Session = Depends(get_db)
):
    # Implement scan endpoint
    pass

@router.post("/yahoo/apply")
def apply_yahoo_cleanup(
    user: CurrentUser = Depends(get_current_user),
    message_ids: list[str],
    mode: str,
    db: Session = Depends(get_db)
):
    # Implement cleanup endpoint
    pass
```

**Checklist:**
- [ ] Add scan endpoint
- [ ] Add cleanup endpoint
- [ ] Add OAuth endpoints
- [ ] Add revoke endpoint
- [ ] Include in main app (`services/gateway/main.py`)

---

### **Step 5: Update OpenAPI Schema**

**File:** `openapi.yaml`

Add new endpoints to the OpenAPI schema:

```yaml
/yahoo/scan:
  post:
    operationId: scanYahoo
    summary: Scan Yahoo Mail inbox
    description: Analyze Yahoo Mail inbox for spam and unwanted emails
    security:
      - DeklutterOAuth: []
    parameters:
      - name: days_back
        in: query
        schema:
          type: integer
          default: 30
    responses:
      '200':
        description: Scan results
        # ... (similar to Gmail)
```

**Checklist:**
- [ ] Add all new endpoints
- [ ] Match existing schema structure
- [ ] Include proper descriptions
- [ ] Add security requirements
- [ ] Test with OpenAPI validator

---

### **Step 6: Update GPT Instructions**

**File:** `GPT_INSTRUCTIONS.md`

Update instructions to support the new provider:

```markdown
## Your Capabilities (ONLY THESE - DO NOT PROMISE MORE)
1. Scan Gmail inbox for unwanted emails
2. Scan Yahoo Mail inbox for unwanted emails  ← ADD THIS
3. Classify emails as: delete, review, or keep
...

## Workflow

### First Time Users
When user says "clean my Yahoo inbox":  ← ADD THIS
- Warm greeting: "I'll help clean your Yahoo Mail inbox! ..."
```

**Checklist:**
- [ ] Add provider to capabilities list
- [ ] Add provider-specific workflow
- [ ] Update examples
- [ ] Keep under 8,000 character limit

---

### **Step 7: Update Classification Rules**

**File:** `services/classifier/policy.py`

Check if classification rules need provider-specific adjustments:

```python
# If Yahoo uses different label names
YAHOO_PROMO_LABELS = {"BULK", "SPAM"}  # Yahoo-specific

def _heuristic_yahoo(item):
    # Provider-specific classification if needed
    pass
```

**Checklist:**
- [ ] Check if provider uses different labels
- [ ] Adjust protected domains if needed
- [ ] Test classification accuracy
- [ ] Update important keywords if needed

---

### **Step 8: Environment Variables**

**File:** `.env` (and document in README)

Add required environment variables:

```bash
# Yahoo Mail OAuth
YAHOO_CLIENT_ID=your_client_id
YAHOO_CLIENT_SECRET=your_client_secret
YAHOO_REDIRECT_URI=https://deklutter-api.onrender.com/auth/yahoo/callback
```

**Checklist:**
- [ ] Add to `.env.example`
- [ ] Document in README.md
- [ ] Add to Render environment variables
- [ ] Test with actual credentials

---

### **Step 9: Update Documentation**

#### **9.1 Generate Resilience Docs**

```bash
./scripts/update_resilience_docs.sh
```

Copy the generated provider section to `RESILIENCE.md`

#### **9.2 Update README.md**

Add provider to supported list:

```markdown
## Supported Providers
- ✅ Gmail
- ✅ Yahoo Mail  ← ADD THIS
- 🔄 Outlook (coming soon)
```

#### **9.3 Update IMPROVEMENTS.md**

Mark provider as completed:

```markdown
- [x] Yahoo Mail integration (Oct 19, 2025)
```

**Checklist:**
- [ ] Update RESILIENCE.md
- [ ] Update README.md
- [ ] Update IMPROVEMENTS.md
- [ ] Update TODO.md

---

### **Step 10: Testing**

#### **10.1 Unit Tests**

Create test file: `tests/test_{provider_name}_connector.py`

```python
def test_yahoo_oauth_flow():
    # Test OAuth
    pass

def test_yahoo_scan():
    # Test scanning
    pass

def test_yahoo_cleanup():
    # Test cleanup
    pass

def test_yahoo_rate_limiting():
    # Test rate limits
    pass

def test_yahoo_circuit_breaker():
    # Test circuit breaker
    pass
```

#### **10.2 Integration Tests**

- [ ] Test OAuth flow end-to-end
- [ ] Test scanning with real account
- [ ] Test cleanup (use test emails)
- [ ] Test error handling
- [ ] Test rate limiting
- [ ] Test circuit breaker opens/closes

#### **10.3 Load Testing**

- [ ] Test with 1,000 emails
- [ ] Test with 10,000 emails
- [ ] Monitor API quota usage
- [ ] Verify rate limiting works
- [ ] Check circuit breaker behavior

**Checklist:**
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Run load tests
- [ ] Fix any issues found
- [ ] Document test results

---

### **Step 11: Privacy & Security**

#### **11.1 Update Privacy Policy**

**File:** `services/gateway/privacy_policy.py`

Add provider to privacy policy:

```python
<li><strong>Yahoo Mail API:</strong> To access your email metadata</li>
```

#### **11.2 Security Review**

- [ ] Tokens are encrypted (AES-256)
- [ ] No email content is stored
- [ ] OAuth scopes are minimal
- [ ] Revocation works properly
- [ ] No sensitive data in logs

**Checklist:**
- [ ] Update privacy policy
- [ ] Security review completed
- [ ] GDPR compliance verified
- [ ] Data retention policy updated

---

### **Step 12: Deployment**

#### **12.1 Pre-Deployment**

- [ ] All tests passing
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] Environment variables set in Render
- [ ] Provider OAuth app approved (if required)

#### **12.2 Deploy**

```bash
git add .
git commit -m "Add Yahoo Mail provider support"
git push
```

- [ ] Deploy to Render
- [ ] Verify deployment successful
- [ ] Check logs for errors

#### **12.3 Post-Deployment**

- [ ] Test OAuth flow in production
- [ ] Test scanning with real account
- [ ] Monitor error rates
- [ ] Monitor circuit breaker state
- [ ] Check API quota usage

**Checklist:**
- [ ] Deployed successfully
- [ ] Production testing completed
- [ ] Monitoring set up
- [ ] No critical errors

---

### **Step 13: User Communication**

#### **13.1 Update GPT**

- [ ] Update GPT instructions in GPT Builder
- [ ] Test GPT with new provider
- [ ] Verify GPT doesn't hallucinate features

#### **13.2 Announce**

- [ ] Update changelog
- [ ] Announce to beta users
- [ ] Update marketing materials (if any)
- [ ] Share on social media (if applicable)

**Checklist:**
- [ ] GPT updated
- [ ] Users notified
- [ ] Announcement made

---

## 📊 Provider Comparison Checklist

After implementation, verify these metrics:

| Metric | Gmail | Yahoo | Outlook | Notes |
|--------|-------|-------|---------|-------|
| Max emails/scan | 1000 | 500 | 1000 | |
| Batch size | 100 | 50 | 20 | |
| Rate limit delay | 0.1s | 0.2s | 0.15s | |
| Circuit breaker threshold | 5 | 3 | 5 | |
| OAuth working | ✅ | ⬜ | ⬜ | |
| Scan working | ✅ | ⬜ | ⬜ | |
| Cleanup working | ✅ | ⬜ | ⬜ | |
| Tests passing | ✅ | ⬜ | ⬜ | |

---

## 🚨 Common Pitfalls

### **1. Rate Limiting**
- ❌ Don't use Gmail's rate limits for Yahoo
- ✅ Always use provider-specific config

### **2. OAuth Scopes**
- ❌ Don't request more permissions than needed
- ✅ Use minimal scopes (read + modify only)

### **3. Error Handling**
- ❌ Don't assume all providers return same error codes
- ✅ Handle provider-specific errors

### **4. Batch Requests**
- ❌ Don't assume all providers support batching
- ✅ Check provider docs, fallback to sequential

### **5. Circuit Breaker**
- ❌ Don't share circuit breaker across providers
- ✅ Each provider gets its own circuit breaker

### **6. Documentation**
- ❌ Don't forget to update RESILIENCE.md
- ✅ Run `./scripts/update_resilience_docs.sh`

---

## ✅ Final Checklist

Before marking the provider as "done":

- [ ] All code implemented
- [ ] All tests passing
- [ ] Documentation updated (README, RESILIENCE, GPT_INSTRUCTIONS)
- [ ] Privacy policy updated
- [ ] Environment variables documented
- [ ] Deployed to production
- [ ] Production testing completed
- [ ] Monitoring in place
- [ ] Users notified
- [ ] No critical bugs

---

## 📚 Reference Files

When adding a provider, you'll touch these files:

1. `services/connectors/provider_config.py` - Provider configuration
2. `services/auth/oauth/providers/{provider}.py` - OAuth handler
3. `services/connectors/{provider}/connector.py` - Email connector
4. `services/gateway/routes_{provider}.py` - API routes
5. `openapi.yaml` - API schema
6. `GPT_INSTRUCTIONS.md` - GPT instructions
7. `RESILIENCE.md` - Resilience documentation
8. `README.md` - Main documentation
9. `.env` - Environment variables
10. `services/gateway/privacy_policy.py` - Privacy policy

---

## 🆘 Need Help?

- Check existing Gmail implementation as reference
- Review provider's API documentation
- Test in development environment first
- Ask for code review before deploying

---

**Good luck adding your new provider!** 🚀

Remember: When in doubt, check how Gmail does it and adapt for your provider's specifics.
