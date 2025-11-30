# Google OAuth Verification Checklist

## 📋 **Complete Checklist for Google OAuth App Verification**

Last Updated: November 30, 2025

---

## ✅ **1. Privacy Policy & Terms of Service** (COMPLETED)

### Requirements:
- [x] Privacy Policy page created (`/privacy`)
- [x] Terms of Service page created (`/terms`)
- [x] Both pages accessible without login
- [x] Both pages hosted on your domain

### URLs:
- **Privacy Policy:** https://app.deklutter.co/privacy
- **Terms of Service:** https://app.deklutter.co/terms

### What Google Checks:
- ✅ Clear explanation of data collection
- ✅ How user data is used
- ✅ Data retention policies
- ✅ User rights (access, deletion, export)
- ✅ Compliance with Google API Services User Data Policy
- ✅ Contact information

---

## 📧 **2. Official Email Setup** (PENDING)

### Current Status:
- ❌ Using personal email: `mohammad.illiyaz@gmail.com`
- ⚠️ Need professional domain email

### Required Email Addresses:

#### **Option A: Google Workspace (Recommended)**
Cost: $6/user/month

Setup:
1. Go to: https://workspace.google.com
2. Sign up with domain: `deklutter.co`
3. Create email addresses:
   - `support@deklutter.co` (primary contact)
   - `privacy@deklutter.co` (privacy inquiries)
   - `legal@deklutter.co` (legal/compliance)
   - `admin@deklutter.co` (admin account)

#### **Option B: Email Forwarding (Free, Quick)**
Setup with your domain registrar (Namecheap/GoDaddy):

1. **Email Forwarding Setup:**
   ```
   support@deklutter.co  → mohammad.illiyaz@gmail.com
   privacy@deklutter.co  → mohammad.illiyaz@gmail.com
   legal@deklutter.co    → mohammad.illiyaz@gmail.com
   ```

2. **How to Set Up (Namecheap):**
   - Go to Domain List → Manage → Email Forwarding
   - Add each forwarding rule
   - Verify via email confirmation

3. **Sending Emails:**
   - Use Gmail's "Send mail as" feature
   - Settings → Accounts → Add another email address
   - Add `support@deklutter.co` as sender

#### **Option C: Free Email Services**
- **Zoho Mail:** Free for up to 5 users
- **ProtonMail:** Free tier available
- **ImprovMX:** Free email forwarding

### **Recommended Setup:**
```
Primary: support@deklutter.co
Privacy: privacy@deklutter.co
Legal: legal@deklutter.co
```

---

## 🔐 **3. Google Cloud Console Setup**

### Current OAuth Client:
- **Client ID:** Already created
- **Client Secret:** Already configured
- **Redirect URI:** `https://api.deklutter.co/oauth/google/callback`

### Required Updates:

#### **A. OAuth Consent Screen**

1. **Go to:** https://console.cloud.google.com/apis/credentials/consent
2. **Update the following:**

```
App Name: Deklutter
User Support Email: support@deklutter.co  ⚠️ UPDATE THIS
Developer Contact: support@deklutter.co   ⚠️ UPDATE THIS

App Logo: (Upload 120x120 PNG)
App Domain: app.deklutter.co
Homepage: https://app.deklutter.co
Privacy Policy: https://app.deklutter.co/privacy
Terms of Service: https://app.deklutter.co/terms

Authorized Domains:
- deklutter.co
- app.deklutter.co
- api.deklutter.co
```

#### **B. OAuth Scopes**

Current scopes (verify these are minimal):
```
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/gmail.modify
https://www.googleapis.com/auth/userinfo.email
https://www.googleapis.com/auth/userinfo.profile
```

**Justification for each scope:**
- `gmail.readonly` - To scan and read email metadata
- `gmail.modify` - To move emails to trash
- `userinfo.email` - To identify the user
- `userinfo.profile` - To show user's name in dashboard

#### **C. Test Users (During Development)**

Add test users while in "Testing" mode:
- Your email
- 2-3 beta testers

---

## 📝 **4. Verification Submission Requirements**

### **A. App Information**

Prepare the following for Google's review:

1. **App Description (500 chars max):**
```
Deklutter is an AI-powered email cleaning service that helps users identify and delete spam, promotional, and unwanted emails from their Gmail inbox. Users can scan their inbox, review categorized results, and safely delete emails to free up storage space. All deletions are moved to trash (recoverable for 30 days).
```

2. **Why You Need Each Scope:**
```
gmail.readonly:
We need to read email metadata (subject, sender, date, labels) to identify spam and promotional emails. We analyze email content using heuristic rules to categorize emails as safe to delete, review, or keep.

gmail.modify:
We need to move emails to trash when users explicitly approve deletion. Emails are moved to Gmail's Trash folder (not permanently deleted) and can be recovered within 30 days.

userinfo.email & userinfo.profile:
We need to identify the user and display their name/email in the dashboard for a personalized experience.
```

3. **Video Demo (Required for Sensitive Scopes):**
   - Record a 2-3 minute video showing:
     - OAuth flow (sign in with Google)
     - Scanning inbox
     - Viewing categorized results
     - Deleting emails (showing they go to Trash)
     - Privacy policy and terms links
   - Upload to YouTube (unlisted)
   - Provide link in verification form

### **B. Domain Verification**

1. **Verify Domain Ownership:**
   - Go to: https://search.google.com/search-console
   - Add property: `app.deklutter.co`
   - Verify via DNS TXT record or HTML file upload

2. **Add to Google Cloud Console:**
   - Go to OAuth consent screen
   - Add verified domain: `deklutter.co`

### **C. Security Assessment**

Google may ask for:
- **CASA Tier 2 Assessment** (for sensitive scopes)
  - Cost: $15,000 - $75,000
  - Required for apps with >100,000 users
  - NOT required for early-stage apps

For now, you can:
- Start with "Testing" mode (up to 100 test users)
- Apply for verification when ready to scale
- Provide detailed security documentation

---

## 🎬 **5. Video Demo Script**

### **Recording Checklist:**

1. **Introduction (15 seconds):**
   - "Hi, this is Deklutter, an AI-powered Gmail cleaning service"
   - Show landing page: `https://app.deklutter.co`

2. **OAuth Flow (30 seconds):**
   - Click "Connect Gmail"
   - Show Google OAuth consent screen
   - Highlight scopes requested
   - Grant permission
   - Show redirect to dashboard

3. **Scanning Inbox (45 seconds):**
   - Click "Scan Inbox"
   - Show loading state
   - Display categorized results:
     - Safe to Delete (red)
     - Review (yellow)
     - Keep (green)
   - Show email samples

4. **Deleting Emails (30 seconds):**
   - Click "Clean Inbox"
   - Show confirmation dialog
   - Demonstrate deletion
   - Open Gmail → Trash to show emails are recoverable

5. **Privacy & Terms (15 seconds):**
   - Show footer links
   - Open Privacy Policy page
   - Open Terms of Service page

6. **Conclusion (15 seconds):**
   - "All data is encrypted and secure"
   - "Users can revoke access anytime"
   - Show contact email: `support@deklutter.co`

**Total Duration:** ~2.5 minutes

### **Recording Tools:**
- **Loom:** https://loom.com (free, easy)
- **OBS Studio:** Free, professional
- **QuickTime (Mac):** Built-in screen recording

---

## 📊 **6. Verification Timeline**

### **Testing Mode (Current):**
- ✅ Up to 100 test users
- ✅ No verification needed
- ✅ Fully functional
- ⚠️ Shows "unverified app" warning

### **Verification Process:**
1. **Submit Application:** 1-2 hours to prepare
2. **Google Review:** 3-6 weeks
3. **Possible Follow-up Questions:** 1-2 weeks
4. **Approval:** Instant once approved

### **What Happens After Approval:**
- ✅ "Verified" badge on OAuth screen
- ✅ No user limit
- ✅ Increased trust
- ✅ Better conversion rates

---

## 🚀 **7. Immediate Action Items**

### **Priority 1: Email Setup (Today)**
- [ ] Set up email forwarding for `support@deklutter.co`
- [ ] Set up email forwarding for `privacy@deklutter.co`
- [ ] Test sending emails from these addresses
- [ ] Update Privacy Policy with new email
- [ ] Update Terms of Service with new email

### **Priority 2: Google Cloud Console (Today)**
- [ ] Update OAuth consent screen with new emails
- [ ] Add app logo (create 120x120 PNG)
- [ ] Verify all URLs are correct
- [ ] Add authorized domains

### **Priority 3: Domain Verification (Tomorrow)**
- [ ] Verify domain in Google Search Console
- [ ] Add verified domain to OAuth consent screen

### **Priority 4: Video Demo (This Week)**
- [ ] Record demo video
- [ ] Upload to YouTube (unlisted)
- [ ] Test video quality and clarity

### **Priority 5: Verification Submission (Next Week)**
- [ ] Prepare scope justifications
- [ ] Fill out verification form
- [ ] Submit for review

---

## 📧 **8. ChatGPT GPT Submission**

### **Requirements:**
- [x] Privacy Policy URL
- [x] Terms of Service URL
- [ ] Official support email
- [ ] GPT description and instructions
- [ ] API endpoints documented

### **Submission Checklist:**
- [ ] Update GPT with new privacy/terms URLs
- [ ] Add support email to GPT description
- [ ] Test GPT thoroughly
- [ ] Submit for review in GPT Store

---

## 🔗 **9. Important Links**

### **Google OAuth:**
- OAuth Consent Screen: https://console.cloud.google.com/apis/credentials/consent
- Credentials: https://console.cloud.google.com/apis/credentials
- API Services User Data Policy: https://developers.google.com/terms/api-services-user-data-policy
- Verification Guide: https://support.google.com/cloud/answer/9110914

### **Domain Verification:**
- Google Search Console: https://search.google.com/search-console
- Webmaster Central: https://www.google.com/webmasters/verification/

### **Your URLs:**
- Web App: https://app.deklutter.co
- API: https://api.deklutter.co
- Privacy: https://app.deklutter.co/privacy
- Terms: https://app.deklutter.co/terms

---

## ✅ **10. Quick Start Guide**

### **Today (30 minutes):**
1. Set up email forwarding for `support@deklutter.co`
2. Update OAuth consent screen with new email
3. Deploy frontend changes (privacy/terms pages)

### **This Week (2-3 hours):**
1. Create app logo (120x120 PNG)
2. Record demo video
3. Verify domain ownership

### **Next Week (1-2 hours):**
1. Submit verification request
2. Monitor for Google's response
3. Address any follow-up questions

---

## 💡 **Pro Tips**

1. **Start with Testing Mode:**
   - You can have up to 100 test users without verification
   - Perfect for beta testing
   - No rush to verify immediately

2. **Email Setup:**
   - Email forwarding is fastest (5 minutes)
   - Google Workspace is most professional
   - Both work for verification

3. **Video Demo:**
   - Keep it under 3 minutes
   - Show actual functionality, not mockups
   - Highlight privacy and security

4. **Scope Justification:**
   - Be specific and honest
   - Explain why each scope is necessary
   - Show how you protect user data

5. **Response Time:**
   - Google usually responds in 2-4 weeks
   - Be patient and professional
   - Answer follow-up questions promptly

---

## 📞 **Need Help?**

If you get stuck:
1. Check Google's OAuth documentation
2. Search Stack Overflow
3. Contact Google Cloud Support
4. Ask in developer communities

---

**Good luck with verification!** 🚀
