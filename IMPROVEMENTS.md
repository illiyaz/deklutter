# Deklutter - Improvements & Feature Roadmap

**Last Updated:** Oct 19, 2025

This document tracks all planned improvements, feature requests, and technical debt for Deklutter.

---

## 🚨 High Priority - Safety & Accuracy

### Email Classification Improvements

#### **1. Show Sample Emails Before Deletion**
- **Status:** 🔴 Not Started
- **Priority:** High
- **Description:** Before deleting, show user 3-5 sample emails from the "safe to delete" category
- **Why:** Builds trust, lets user verify accuracy
- **Implementation:**
  - Modify `scanGmail` response to include sample email metadata
  - Update GPT instructions to display samples
  - Add "Show more samples" option

#### **2. AI-Powered Classification (LLM Edge Cases)**
- **Status:** 🟡 Stubbed (code exists but commented out)
- **Priority:** High
- **Description:** Use LLM to classify edge cases that heuristics can't handle
- **Why:** More accurate than simple rules
- **Implementation:**
  - Uncomment `judge_edge_cases()` in `services/classifier/policy.py`
  - Integrate OpenAI API or local LLM
  - Add confidence scoring
  - Handle API rate limits
- **File:** `services/classifier/llm_adapter.py`

#### **3. User Feedback Loop**
- **Status:** 🔴 Not Started
- **Priority:** Medium
- **Description:** Learn from user's keep/delete decisions
- **Why:** Personalized classification over time
- **Implementation:**
  - Track user corrections (kept emails marked as delete, etc.)
  - Store sender preferences per user
  - Adjust classification weights based on feedback
  - Add "This was wrong" feedback button

#### **4. Sender Whitelist/Blacklist**
- **Status:** 🔴 Not Started
- **Priority:** Medium
- **Description:** Let users manually mark senders as always keep/delete
- **Why:** User control over classification
- **Implementation:**
  - Add `sender_preferences` table (user_id, sender_hash, preference)
  - Check whitelist before classification
  - GPT command: "Always keep emails from X"

---

## 🎯 User Experience Improvements

### Better Interaction Flow

#### **5. Batch Deletion (Progressive)**
- **Status:** 🔴 Not Started
- **Priority:** Medium
- **Description:** Delete in smaller batches (10-20 emails) instead of all at once
- **Why:** Less risky, easier to verify
- **Implementation:**
  - Add pagination to delete operation
  - Show progress: "Deleted 10/45 emails..."
  - Allow user to stop mid-deletion

#### **6. Preview Mode**
- **Status:** 🔴 Not Started
- **Priority:** Medium
- **Description:** Show detailed list of emails to be deleted with subjects/senders
- **Why:** Transparency before action
- **Implementation:**
  - Add `getEmailDetails` endpoint
  - Return sender, subject, date for each email ID
  - Format as table in GPT response

#### **7. Undo Feature**
- **Status:** 🔴 Not Started
- **Priority:** Low
- **Description:** Quick restore from trash within GPT
- **Why:** Safety net for mistakes
- **Implementation:**
  - Add `undoCleanup` endpoint
  - Track last deletion batch
  - Gmail API: move from Trash back to Inbox

#### **8. Better Progress Indicators**
- **Status:** 🔴 Not Started
- **Priority:** Low
- **Description:** Show real-time progress during scan/delete
- **Why:** Better UX for large operations
- **Implementation:**
  - Add streaming responses
  - Show "Scanned 50/100 emails..."
  - Estimated time remaining

---

## 📊 Analytics & Insights

#### **9. Inbox Analytics Dashboard**
- **Status:** 🔴 Not Started
- **Priority:** Low
- **Description:** Show trends, top senders, space usage over time
- **Why:** Insights into email habits
- **Implementation:**
  - Track scans over time
  - Aggregate sender statistics
  - Show charts: "You receive 20 newsletters/week"

#### **10. Space Savings Tracker**
- **Status:** 🔴 Not Started
- **Priority:** Low
- **Description:** Show total space freed, emails deleted over time
- **Why:** Gamification, satisfaction
- **Implementation:**
  - Store cumulative stats per user
  - Show badges: "Freed 1GB!", "Deleted 1000 emails!"

---

## 🔧 Technical Improvements

### Performance & Scalability

#### **11. Pagination for Large Inboxes**
- **Status:** 🔴 Not Started
- **Priority:** High
- **Description:** Currently limited to 100 emails, need pagination
- **Why:** Users with 1000s of emails can't scan all
- **Implementation:**
  - Add `pageToken` support from Gmail API
  - Scan in chunks of 100
  - Aggregate results

#### **12. Background Processing**
- **Status:** 🔴 Not Started
- **Priority:** Medium
- **Description:** Move scan/delete to background jobs
- **Why:** Faster response, handle large operations
- **Implementation:**
  - Add Celery or similar task queue
  - Return job ID immediately
  - Poll for completion

#### **13. Caching & Rate Limiting**
- **Status:** 🔴 Not Started
- **Priority:** Medium
- **Description:** Cache scan results, rate limit API calls
- **Why:** Avoid hitting Gmail API limits
- **Implementation:**
  - Redis cache for recent scans
  - Rate limit per user (e.g., 10 scans/hour)
  - Show cached results if recent

#### **14. Database Optimization**
- **Status:** 🔴 Not Started
- **Priority:** Low
- **Description:** Add indexes, optimize queries
- **Why:** Faster as data grows
- **Implementation:**
  - Index on `user_id`, `message_id`, `sender_hash`
  - Add database migrations
  - Query optimization

---

## 🔐 Security & Privacy

#### **15. Token Rotation & Refresh**
- **Status:** 🟢 Implemented (basic)
- **Priority:** Medium
- **Improvements Needed:**
  - Auto-refresh before expiry
  - Handle refresh token expiration gracefully
  - Notify user when re-auth needed

#### **16. Audit Logging**
- **Status:** 🟡 Partial (MailDecisionLog exists)
- **Priority:** Medium
- **Description:** Comprehensive audit trail of all actions
- **Why:** Security, compliance, debugging
- **Implementation:**
  - Log all API calls (scan, delete, revoke)
  - Store IP, timestamp, action
  - User-accessible audit log

#### **17. Data Retention Policy**
- **Status:** 🔴 Not Started
- **Priority:** Low
- **Description:** Auto-delete old logs, expired tokens
- **Why:** Privacy, GDPR compliance
- **Implementation:**
  - Cron job to clean old data
  - Delete logs older than 90 days
  - Delete revoked tokens after 30 days

---

## 🌐 Multi-Provider Support

#### **18. Yahoo Mail Integration**
- **Status:** 🔴 Not Started
- **Priority:** High (Roadmap)
- **Description:** Support Yahoo Mail OAuth and scanning
- **Implementation:**
  - Add Yahoo OAuth provider
  - Yahoo Mail API integration
  - Unified interface

#### **19. Outlook/Microsoft 365**
- **Status:** 🔴 Not Started
- **Priority:** High (Roadmap)
- **Description:** Support Outlook.com and Microsoft 365
- **Implementation:**
  - Microsoft Graph API
  - Azure AD OAuth
  - Unified interface

#### **20. Google Drive Cleanup**
- **Status:** 🔴 Not Started
- **Priority:** Medium (Roadmap)
- **Description:** Scan and clean Google Drive duplicates
- **Implementation:**
  - Google Drive API
  - File deduplication algorithm
  - Preview before delete

#### **21. Dropbox Integration**
- **Status:** 🔴 Not Started
- **Priority:** Medium (Roadmap)
- **Description:** Clean Dropbox duplicates and old files

#### **22. iCloud Mail & Drive**
- **Status:** 🔴 Not Started
- **Priority:** Low (Roadmap)
- **Description:** Support Apple ecosystem

---

## 🤖 AI & Intelligence

#### **23. Smart Scheduling**
- **Status:** 🔴 Not Started
- **Priority:** Low
- **Description:** Auto-scan and suggest cleanups weekly/monthly
- **Why:** Proactive inbox management
- **Implementation:**
  - User preferences for schedule
  - Email/notification when cleanup ready
  - One-click approve

#### **24. Email Pattern Recognition**
- **Status:** 🔴 Not Started
- **Priority:** Low
- **Description:** Learn user's email patterns (work hours, important senders)
- **Why:** Better classification
- **Implementation:**
  - Analyze email timestamps
  - Identify frequent senders
  - Adjust importance scoring

#### **25. Natural Language Commands**
- **Status:** 🔴 Not Started
- **Priority:** Low
- **Description:** "Delete all emails from X older than 6 months"
- **Why:** Power user features
- **Implementation:**
  - Parse natural language queries
  - Build custom filters
  - Execute with confirmation

---

## 📱 Platform Expansion

#### **26. Web Dashboard**
- **Status:** 🔴 Not Started
- **Priority:** Medium
- **Description:** Standalone web app (not just GPT)
- **Why:** Reach non-ChatGPT users
- **Implementation:**
  - React frontend
  - Same backend API
  - OAuth flow for web

#### **27. Mobile App**
- **Status:** 🔴 Not Started
- **Priority:** Low
- **Description:** iOS/Android native apps
- **Why:** Mobile-first users

#### **28. Browser Extension**
- **Status:** 🔴 Not Started
- **Priority:** Low
- **Description:** Chrome/Firefox extension for Gmail
- **Why:** In-context cleanup

---

## 🐛 Known Issues & Tech Debt

#### **29. OAuth State Management**
- **Status:** 🟡 In Progress
- **Priority:** High
- **Issue:** Currently using in-memory dict for OAuth states (lost on restart)
- **Fix:** Move to Redis or database
- **File:** `services/auth/gpt_oauth.py`

#### **30. Error Handling**
- **Status:** 🔴 Needs Improvement
- **Priority:** Medium
- **Issue:** Generic error messages, not user-friendly
- **Fix:** Better error messages, retry logic, user guidance

#### **31. Testing Coverage**
- **Status:** 🔴 Minimal
- **Priority:** Medium
- **Issue:** No automated tests
- **Fix:** Add pytest, unit tests, integration tests

#### **32. Documentation**
- **Status:** 🟡 Partial
- **Priority:** Low
- **Issue:** Missing API docs, deployment guides
- **Fix:** Add OpenAPI docs, README improvements

---

## 📝 Notes

### Classification Safety Improvements (Completed ✅)
- ✅ Added protected domains (banks, gov, healthcare)
- ✅ Added important keywords (receipt, invoice, booking)
- ✅ INBOX protection (don't auto-delete main inbox emails)
- ✅ Lower confidence scores (70% instead of 90%)
- ✅ Updated GPT instructions for transparency

### OAuth Flow (Completed ✅)
- ✅ GPT OAuth integration working
- ✅ Google OAuth callback handling
- ✅ Token storage and encryption
- ✅ Revoke access endpoint

---

## How to Use This File

1. **Adding New Items:**
   - Add under appropriate section
   - Include: Status, Priority, Description, Why, Implementation notes

2. **Status Indicators:**
   - 🔴 Not Started
   - 🟡 In Progress / Partial
   - 🟢 Completed
   - ⏸️ On Hold

3. **Priority Levels:**
   - **High:** Critical for core functionality or safety
   - **Medium:** Important but not blocking
   - **Low:** Nice to have, future enhancement

4. **Before Starting Work:**
   - Update status to 🟡 In Progress
   - Add your name/date
   - Link to GitHub issue if applicable

5. **After Completion:**
   - Update status to 🟢 Completed
   - Add completion date
   - Move to "Completed" section at bottom if desired

---

## Contributing

When adding improvements:
- Be specific about the problem and solution
- Include implementation details
- Consider security and privacy implications
- Think about user experience
- Estimate effort (S/M/L/XL)

---

**Questions or suggestions?** Add them here or create a GitHub issue!
