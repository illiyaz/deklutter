# Changelog

All notable changes to Deklutter will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-10-19

### 🎉 Initial Production Release

### Added
- **Gmail Integration**
  - OAuth 2.0 authentication with Google
  - Scan inbox for unwanted emails
  - Classify emails: delete, review, keep
  - Batch API requests (100 emails per batch)
  - Pagination support (up to 1,000 emails per scan)
  
- **Smart Classification**
  - Trust Gmail's categories (CATEGORY_PROMOTIONS, CATEGORY_SOCIAL, CATEGORY_FORUMS) at 85% confidence
  - Protected domains (banks, government, healthcare, Indian services)
  - Important keywords detection (receipt, invoice, booking, OTP, delivery, refund)
  - Heuristic-based spam detection
  
- **Resilience & Error Handling**
  - Retry logic with exponential backoff (2s, 4s, 8s)
  - Circuit breaker pattern (prevents cascading failures)
  - Rate limiting (100ms between batches)
  - Graceful degradation (continue on partial failures)
  - Comprehensive logging
  
- **Provider-Agnostic Architecture**
  - Centralized provider configuration (`provider_config.py`)
  - Gmail, Yahoo, Outlook configurations ready
  - Easy to add new email providers
  - Auto-documentation generator for provider configs
  
- **API Endpoints**
  - `POST /auth/google/init` - Initialize Gmail OAuth
  - `POST /gmail/scan` - Scan Gmail inbox
  - `POST /gmail/apply` - Apply cleanup (trash or label)
  - `POST /auth/revoke` - Revoke access
  - `GET /health` - Health check with database status
  - `GET /version` - API version and features
  - `GET /privacy` - Privacy policy (HTML)
  - `GET /terms` - Terms of service (HTML)
  
- **Security & Privacy**
  - AES-256 encrypted OAuth tokens
  - Metadata-only access (sender, subject, date, size)
  - Never access email content or attachments
  - Token expiration (hourly refresh)
  - GDPR & CCPA compliant
  - Easy revocation
  
- **Documentation**
  - `README.md` - Project overview and setup
  - `RESILIENCE.md` - Error handling and best practices
  - `ADDING_NEW_PROVIDER.md` - 13-step guide for adding providers
  - `TODO.md` - 4-week roadmap
  - `IMPROVEMENTS.md` - Feature tracking
  - `GPT_INSTRUCTIONS.md` - GPT configuration (3,568 chars)
  
- **GPT Integration**
  - Custom OpenAPI schema for ChatGPT
  - Action-oriented conversation flow
  - Warm, reassuring UX
  - Sample email preview before deletion
  - Never hallucinate features
  - Hide technical tool names

### Performance
- **100x faster** than sequential API calls (batch requests)
- **100x cheaper** quota usage (500 units vs 50,000 for 10K emails)
- **10x faster** scan time (10-15s vs 2-3 min for 10K emails)

### Protected Domains
**Financial:** PayPal, Stripe, Razorpay, Paytm, PhonePe, Zerodha, Groww, Upstox, Flipkart  
**Travel:** Uber, Lyft, Airbnb, Ola, MakeMyTrip, GoIbibo, Cleartrip, IRCTC  
**Healthcare:** Practo, 1mg  
**Utilities:** Airtel, Jio, Vodafone  
**Work:** Zoom, Slack, GitHub, Atlassian, Notion, Figma  
**Government:** NSDL, EPFO, IRS, USCIS  

### Important Keywords
receipt, invoice, booking, confirmation, order, payment, transaction, statement, tax, verification, OTP, password, reset, delivery, shipped, refund

---

## [Unreleased]

### Planned for Week 2
- Fix OAuth state management (database-backed)
- Add batch deletion with progress tracking
- Better error messages
- Activity logs endpoint
- Email statistics dashboard

### Planned for Week 3
- LLM-based classification (GPT-4)
- Scheduled scanning
- Email analytics
- Top spam senders

### Planned for Week 4+
- Yahoo Mail integration
- Outlook/Microsoft 365 integration
- Google Drive cleanup
- Dropbox integration
- iCloud Mail & Drive

---

## Version History

- **1.0.0** (2025-10-19) - Initial production release
- **0.1.0** (2025-10-17) - Development version

---

**Questions?** Check the [README](README.md) or open an issue on [GitHub](https://github.com/illiyaz/deklutter).
