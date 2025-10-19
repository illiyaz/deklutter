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
- [ ] Set privacy policy URL: `https://deklutter-api.onrender.com/privacy`
- [ ] Share with 2-3 friends for beta testing
- [ ] Document issues and feedback

### Fix Issues Found
- [ ] Adjust classification rules based on testing
- [ ] Add/remove protected domains as needed
- [ ] Update important keywords list
- [ ] Fix any bugs discovered

---

## 📅 WEEK 1: Safety & Trust

### ✅ Completed
- [x] Show sample emails before deletion (Oct 19)
- [x] Add safety guardrails (protected domains, keywords)
- [x] Improve GPT conversation flow (action-oriented)
- [x] Prevent hallucination (fake features)
- [x] Privacy policy page

### 🔄 In Progress
- [ ] Test classification thoroughly
- [ ] Fix false positives

---

## 📅 WEEK 2: Reliability

### 1. Fix OAuth State Management (HIGH PRIORITY - 4 hours)
**Status:** 🔴 Not Started  
**Why:** In-memory dict lost on restart, users re-auth after every deploy  
**Files:** `services/auth/gpt_oauth.py`

**Tasks:**
- [ ] Create `oauth_states` database table
- [ ] Move `_oauth_states` dict to database
- [ ] Add state expiration (30 min timeout)
- [ ] Add cleanup job for expired states
- [ ] Test OAuth flow with database
- [ ] Deploy and verify persistence

**Acceptance Criteria:**
- OAuth states survive server restarts
- Old states are cleaned up automatically
- No re-auth needed after deploys

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

## 🐛 Known Issues

### High Priority
- [ ] OAuth state management (in-memory, lost on restart)
- [ ] No pagination (limited to 100 emails)
- [ ] Generic error messages

### Medium Priority
- [ ] No testing coverage
- [ ] Activity logs not implemented
- [ ] No rate limiting

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
