# Deklutter - TODO & Roadmap

**Last Updated:** Oct 19, 2025

---

## 🔥 IMMEDIATE (Tomorrow)

### Deploy & Test
- [ ] Deploy latest changes on Render
- [ ] Update GPT instructions in GPT Builder
- [ ] Test classification thoroughly:
  - [ ] Scan personal inbox
  - [ ] Verify samples are actually spam
  - [ ] Check for false positives
  - [ ] Test protected domains (banks, gov, healthcare)
  - [ ] Test important keywords (receipt, invoice, booking)
- [x] Set privacy policy URL: `https://api.deklutter.co/privacy`
- [ ] Share with 2-3 friends for beta testing
- [ ] Document issues and feedback

### Fix Issues Found
- [ ] Adjust classification rules based on testing
- [ ] Add/remove protected domains as needed
- [ ] Update important keywords list
- [ ] Fix any bugs discovered

---

## 📅 WEEK 1: Safety & Trust

### ✅ Completed (Oct 19, 2025)
- [x] Show sample emails before deletion
- [x] Add safety guardrails (protected domains, keywords)
- [x] Improve GPT conversation flow (action-oriented)
- [x] Prevent hallucination (fake features)
- [x] Privacy policy page
- [x] Better classification (trust Gmail categories 85%)
- [x] Expanded protected domains (Indian services)
- [x] Pagination & batch API (handle 10K+ emails)
- [x] Retry logic with exponential backoff
- [x] Circuit breaker pattern
- [x] Provider-agnostic configuration system
- [x] Comprehensive documentation (RESILIENCE.md, ADDING_NEW_PROVIDER.md)
- [x] Enhanced health check endpoint
- [x] Version endpoint
- [x] Condensed GPT instructions (8,556 → 3,568 chars)

### 🔄 In Progress
- [ ] Test classification thoroughly
- [ ] Fix false positives

---

## 📅 WEEK 2: Reliability

### 1. Fix OAuth State Management ✅ COMPLETED (Oct 19)
**Status:** ✅ Done  
**Why:** In-memory dict lost on restart, users re-auth after every deploy  
**Files:** `services/auth/gpt_oauth.py`, `db/models.py`

**Completed:**
- [x] Create `oauth_states` database table
- [x] Move `_oauth_states` dict to database
- [x] Add state expiration (30 min timeout)
- [x] Add cleanup job for expired states
- [x] Test OAuth flow with database

**Result:** OAuth states now survive server restarts! ✅

---

### 2. Add Batch Deletion (MEDIUM PRIORITY - 3 hours)
**Status:** 🔴 Not Started  
**Why:** Safer than deleting all at once, better UX  
**Files:** `services/gmail_connector/api.py`, `GPT_INSTRUCTIONS.md`

**Tasks:**
- [ ] Modify `apply_cleanup` to support batch size parameter
- [ ] Add progress tracking (deleted X/Y emails)
- [ ] Update GPT instructions to show progress
- [ ] Add "stop deletion" capability
- [ ] Test with large email batches
- [ ] Update OpenAPI schema

**Acceptance Criteria:**
- Deletes in batches of 10-20 emails
- Shows progress: "Deleted 10/45..."
- User can stop mid-deletion
- All or nothing rollback on error

---

### 3. Better Error Messages (MEDIUM PRIORITY - 2 hours)
**Status:** 🔴 Not Started  
**Why:** Generic errors confuse users  
**Files:** All API files, `GPT_INSTRUCTIONS.md`

**Tasks:**
- [ ] Map error codes to user-friendly messages
- [ ] Add retry logic for transient failures
- [ ] Provide actionable guidance in errors
- [ ] Update GPT instructions with error responses
- [ ] Test error scenarios

**Acceptance Criteria:**
- Errors explain what went wrong
- Errors suggest how to fix
- Transient errors auto-retry
- GPT displays helpful messages

---

## 📅 WEEK 3: Polish

### 1. Add Undo Feature (LOW PRIORITY - 4 hours)
**Status:** 🔴 Not Started  
**Why:** Safety net for mistakes  
**Files:** `services/gmail_connector/api.py`

**Tasks:**
- [ ] Track last deletion batch (message IDs)
- [ ] Add `undoCleanup` endpoint
- [ ] Gmail API: move from Trash back to Inbox
- [ ] Update GPT instructions
- [ ] Time limit: 5 minutes after deletion

---

### 2. Add Basic Analytics (LOW PRIORITY - 3 hours)
**Status:** 🔴 Not Started  
**Why:** Show users their inbox trends  
**Files:** New `services/analytics/` module

**Tasks:**
- [ ] Track scans over time
- [ ] Aggregate sender statistics
- [ ] Calculate space saved
- [ ] Top spam senders
- [ ] Add `/analytics` endpoint

---

## 📅 WEEK 4+: Expansion

### Security & Privacy Enhancements

#### 1. Email Encryption Service (LOW PRIORITY - 4 hours)
**Status:** 🔴 Not Started  
**Why:** Enhanced privacy for user emails (enterprise feature)  
**Files:** New `services/security/email_encryption.py`, `db/models.py`

**Tasks:**
- [ ] Create encryption/decryption service
- [ ] Add `email_hash` column (for lookup)
- [ ] Add `email_encrypted` column (AES-256)
- [ ] Update User model to use encrypted email
- [ ] Add migration script for existing users
- [ ] Update OAuth flow to work with encrypted emails
- [ ] Add key rotation mechanism
- [ ] Performance testing (encryption overhead)

**Acceptance Criteria:**
- User emails encrypted at rest
- OAuth lookup works via email_hash
- No performance degradation
- Backward compatible with existing data

**Notes:**
- Not critical for MVP
- Useful for enterprise customers
- Consider after 1,000+ users
- Alternative: Use separate UserEmail table

---

### Multi-Provider Support

**⚠️ IMPORTANT: When adding a new provider:**
1. ✅ Add configuration to `services/connectors/provider_config.py`
2. ✅ Run `./scripts/update_resilience_docs.sh` to generate docs
3. ✅ Update `RESILIENCE.md` with generated content
4. ✅ Test with provider-specific rate limits
5. ✅ Update `GPT_INSTRUCTIONS.md` if needed

**Providers to add:**
- [ ] Yahoo Mail integration
- [ ] Outlook/Microsoft 365 integration
- [ ] Google Drive cleanup
- [ ] Dropbox integration
- [ ] iCloud Mail & Drive

---

## 🏢 ENTERPRISE ROADMAP (6-12 months)

### Phase 1: Enterprise Workspace Integrations

#### 1. Confluence Cleanup & Intelligence (HIGH VALUE - 8 weeks)
**Status:** 🔴 Not Started  
**Why:** Enterprise teams have cluttered Confluence spaces with outdated docs  
**Market:** Every company using Atlassian ($50B+ market)

**Features:**
- [ ] Scan Confluence spaces for outdated/duplicate pages
- [ ] Identify stale documentation (not updated in 6+ months)
- [ ] Find duplicate content across spaces
- [ ] Suggest page archival/deletion
- [ ] AI-powered content summarization
- [ ] Auto-tag pages by topic/department
- [ ] Generate knowledge graph of related pages
- [ ] Identify broken links and outdated references

**Technical Requirements:**
- [ ] Confluence REST API integration
- [ ] OAuth 2.0 for Atlassian
- [ ] Content similarity detection (embeddings)
- [ ] Page version history analysis
- [ ] Workspace-level permissions

**Monetization:**
- $49/month per workspace (up to 100 users)
- $199/month for enterprise (unlimited users)

---

#### 2. Google Drive Intelligence (HIGH VALUE - 6 weeks)
**Status:** 🔴 Not Started  
**Why:** Average user has 1,000+ files, 70% unused  
**Market:** 3 billion Google Workspace users

**Features:**
- [ ] Scan Drive for duplicate files
- [ ] Identify large unused files (>100MB, not accessed in 6 months)
- [ ] Find orphaned files (not in any folder)
- [ ] Suggest folder organization
- [ ] Auto-categorize files by type/project
- [ ] Detect sensitive files (PII, credentials)
- [ ] Generate storage usage reports
- [ ] Smart file archival (move to cold storage)

**Technical Requirements:**
- [ ] Google Drive API v3
- [ ] File metadata analysis
- [ ] Content-based deduplication
- [ ] OCR for scanned documents
- [ ] ML-based categorization

**Monetization:**
- $9/month per user (personal)
- $29/month per user (business)

---

#### 3. SharePoint & OneDrive Cleanup (MEDIUM VALUE - 6 weeks)
**Status:** 🔴 Not Started  
**Why:** Microsoft 365 has 345M+ paid users  
**Market:** Enterprise-heavy, high willingness to pay

**Features:**
- [ ] Scan SharePoint sites for stale content
- [ ] Identify duplicate documents across sites
- [ ] Find large/unused files in OneDrive
- [ ] Suggest document retention policies
- [ ] Auto-archive old files
- [ ] Generate compliance reports
- [ ] Detect sensitive data (GDPR, HIPAA)
- [ ] Integration with Microsoft Teams

**Technical Requirements:**
- [ ] Microsoft Graph API
- [ ] Azure AD authentication
- [ ] SharePoint REST API
- [ ] OneDrive API
- [ ] Compliance API integration

**Monetization:**
- $99/month per organization (up to 50 users)
- $499/month for enterprise (unlimited)

---

#### 4. Slack Workspace Intelligence (MEDIUM VALUE - 4 weeks)
**Status:** 🔴 Not Started  
**Why:** Slack channels get cluttered, hard to find info  
**Market:** 20M+ daily active users

**Features:**
- [ ] Identify inactive channels (suggest archival)
- [ ] Find duplicate/similar channels
- [ ] Extract key decisions from conversations
- [ ] Auto-summarize long threads
- [ ] Generate searchable knowledge base from Slack
- [ ] Detect important messages (action items, decisions)
- [ ] Channel health metrics

**Technical Requirements:**
- [ ] Slack API integration
- [ ] Message history analysis
- [ ] NLP for key phrase extraction
- [ ] Sentiment analysis
- [ ] Channel activity tracking

**Monetization:**
- $19/month per workspace (up to 100 users)
- $99/month for enterprise

---

### Phase 2: Enterprise Authentication & Security

#### 1. Single Sign-On (SSO) (HIGH PRIORITY - 3 weeks)
**Status:** 🔴 Not Started  
**Why:** Enterprise requirement, non-negotiable  
**Protocols:** SAML 2.0, OAuth 2.0, OpenID Connect

**Providers to Support:**
- [ ] Okta
- [ ] Azure AD / Microsoft Entra
- [ ] Google Workspace SSO
- [ ] OneLogin
- [ ] Auth0
- [ ] JumpCloud
- [ ] Ping Identity

**Technical Requirements:**
- [ ] SAML 2.0 implementation
- [ ] SP-initiated and IdP-initiated flows
- [ ] JIT (Just-In-Time) user provisioning
- [ ] SCIM for user sync
- [ ] Multi-tenant architecture
- [ ] Domain verification
- [ ] SSO configuration UI for admins

**Files to Create:**
- `services/auth/sso/` - SSO handlers
- `services/auth/sso/saml.py` - SAML implementation
- `services/auth/sso/oidc.py` - OpenID Connect
- `services/auth/sso/scim.py` - User provisioning

---

#### 2. Role-Based Access Control (RBAC) (MEDIUM PRIORITY - 2 weeks)
**Status:** 🔴 Not Started  
**Why:** Enterprise teams need granular permissions

**Roles:**
- [ ] Super Admin (full access)
- [ ] Admin (workspace management)
- [ ] Manager (team oversight)
- [ ] User (basic access)
- [ ] Auditor (read-only)

**Permissions:**
- [ ] Workspace management
- [ ] User management
- [ ] Billing management
- [ ] Audit log access
- [ ] Integration management
- [ ] Policy configuration

**Technical Requirements:**
- [ ] Permission system in database
- [ ] Role hierarchy
- [ ] Permission checking middleware
- [ ] Audit logging for all actions
- [ ] Admin dashboard

---

#### 3. Audit Logging & Compliance (HIGH PRIORITY - 2 weeks)
**Status:** 🔴 Not Started  
**Why:** SOC 2, GDPR, HIPAA requirements

**Features:**
- [ ] Log all user actions
- [ ] Log all data access
- [ ] Log all deletions
- [ ] Immutable audit trail
- [ ] Compliance reports (GDPR, HIPAA)
- [ ] Data retention policies
- [ ] Export audit logs (CSV, JSON)
- [ ] Real-time alerts for suspicious activity

**Compliance Standards:**
- [ ] SOC 2 Type II
- [ ] GDPR (EU)
- [ ] HIPAA (Healthcare)
- [ ] CCPA (California)
- [ ] ISO 27001

---

### Phase 3: Enterprise Features

#### 1. Team Workspaces (2 weeks)
- [ ] Multi-user workspaces
- [ ] Shared integrations
- [ ] Team statistics
- [ ] Centralized billing

#### 2. Admin Dashboard (3 weeks)
- [ ] User management
- [ ] Usage analytics
- [ ] Cost tracking
- [ ] Integration status
- [ ] Audit logs viewer

#### 3. API for Enterprises (2 weeks)
- [ ] REST API for automation
- [ ] Webhooks for events
- [ ] API rate limiting
- [ ] API key management
- [ ] Developer documentation

#### 4. Custom Policies (2 weeks)
- [ ] Custom retention rules
- [ ] Auto-deletion policies
- [ ] Compliance policies
- [ ] Approval workflows

---

### Phase 4: AI & Intelligence Layer

#### 1. Smart Categorization (4 weeks)
- [ ] ML-based content classification
- [ ] Auto-tagging across all platforms
- [ ] Duplicate detection (semantic, not just exact)
- [ ] Content recommendations

#### 2. Natural Language Queries (3 weeks)
- [ ] "Find all marketing docs from Q1"
- [ ] "Show me files I haven't touched in 6 months"
- [ ] "What's taking up the most space?"

#### 3. Predictive Analytics (3 weeks)
- [ ] Predict storage growth
- [ ] Identify future bottlenecks
- [ ] Suggest proactive cleanup

---

## 💰 Enterprise Pricing Strategy

### Tier 1: Starter ($99/month)
- Up to 10 users
- 1 workspace integration
- Basic SSO
- Email support

### Tier 2: Business ($499/month)
- Up to 100 users
- 3 workspace integrations
- Full SSO (SAML, OIDC)
- Priority support
- Audit logs

### Tier 3: Enterprise (Custom)
- Unlimited users
- All integrations
- Custom SSO
- Dedicated support
- On-premise option
- SLA guarantee
- Custom compliance

---

## 🎯 Go-to-Market Strategy

### Target Customers:
1. **Mid-size companies (100-1,000 employees)**
   - Pain: Cluttered workspaces, wasted storage
   - Budget: $5K-50K/year for productivity tools

2. **Enterprise (1,000+ employees)**
   - Pain: Compliance, governance, cost optimization
   - Budget: $50K-500K/year

3. **Specific Verticals:**
   - Legal firms (document management)
   - Healthcare (HIPAA compliance)
   - Financial services (SOC 2, audit trails)
   - Tech companies (fast-growing, lots of data)

### Sales Channels:
- [ ] Direct sales (enterprise)
- [ ] Self-serve (SMB)
- [ ] Atlassian Marketplace (Confluence plugin)
- [ ] Google Workspace Marketplace
- [ ] Microsoft AppSource (SharePoint/Teams)

---

## 📊 Success Metrics

### Product Metrics:
- [ ] Number of enterprise customers
- [ ] Average contract value (ACV)
- [ ] Storage saved per customer
- [ ] Time saved per user (hours/month)
- [ ] Customer retention rate

### Technical Metrics:
- [ ] API uptime (99.9% SLA)
- [ ] Average scan time
- [ ] Accuracy of duplicate detection
- [ ] False positive rate (<5%)

---

## 🚧 Technical Challenges

### 1. Scale
- Handle millions of files per workspace
- Real-time scanning for large enterprises
- Distributed processing

### 2. Security
- Enterprise-grade encryption
- Zero-trust architecture
- Compliance certifications

### 3. Integration Complexity
- Each platform has different APIs
- Rate limits vary widely
- Permission models differ

### 4. AI/ML
- Accurate duplicate detection
- Semantic understanding of content
- Multi-language support

---

## 📅 Timeline

**Q1 2026:** Confluence + Google Drive  
**Q2 2026:** SharePoint + SSO  
**Q3 2026:** Slack + RBAC + Audit Logs  
**Q4 2026:** AI Layer + Enterprise Sales  

**Total Investment:** 6-9 months, 2-3 engineers

---

## 🐛 Known Issues

### High Priority
- [x] OAuth state management (in-memory, lost on restart) - ✅ FIXED Oct 19
- [x] No pagination (limited to 100 emails) - ✅ FIXED Oct 19 (now handles 1,000+)
- [ ] Generic error messages

### Medium Priority
- [x] No testing coverage - ✅ FIXED Oct 19 (35 unit tests for classifier)
- [ ] Activity logs not implemented
- [x] No rate limiting - ✅ FIXED Oct 19 (100ms between batches, circuit breaker)

### Low Priority
- [ ] Documentation incomplete
- [ ] No monitoring/alerting

---

## 💡 Feature Requests (From Users)

_Add user feedback here as it comes in_

- [ ] Daily email reminders (NOT IMPLEMENTED - hallucination risk)
- [ ] Automatic scheduled scans (NOT IMPLEMENTED)
- [ ] Activity logs (NOT IMPLEMENTED)

---

## 📊 Metrics to Track

### User Engagement
- [ ] Number of scans per user
- [ ] Number of emails deleted
- [ ] Space freed (MB/GB)
- [ ] User retention (7-day, 30-day)

### Technical
- [ ] API response times
- [ ] Error rates
- [ ] OAuth success rate
- [ ] Classification accuracy

---

## 🎯 Success Criteria

### Week 1
- ✅ Sample emails working
- [ ] No false positives in testing
- [ ] 3+ friends using successfully

### Week 2
- [ ] OAuth states persist across restarts
- [ ] Batch deletion working smoothly
- [ ] Error messages are helpful

### Week 3
- [ ] Undo feature working
- [ ] Basic analytics available
- [ ] 10+ active users

### Week 4+
- [ ] Yahoo Mail support
- [ ] 50+ active users
- [ ] Consider monetization

---

## 📝 Notes

- Keep GPT instructions under 8K characters
- Always test locally before deploying (when possible)
- Document all breaking changes
- Update IMPROVEMENTS.md when completing tasks
- Gather user feedback continuously

---

**Next Review:** After Week 1 testing (Oct 20, 2025)
