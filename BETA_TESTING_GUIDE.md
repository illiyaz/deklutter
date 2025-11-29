# 🧪 Beta Testing Guide - Deklutter

**Welcome Beta Testers!** 🎉

Thank you for helping test Deklutter - an AI-powered Gmail cleanup tool.

---

## 🎯 What is Deklutter?

Deklutter automatically scans your Gmail inbox and identifies:
- 🗑️ **Spam & promotional emails** (safe to delete)
- 👀 **Receipts & confirmations** (review first)
- ✅ **Important emails** (keep)

**Privacy First:** We don't store email subjects or content. Only metadata like sender domain and size.

---

## 🚀 How to Test

### **Step 1: Connect Your Gmail**

Visit: https://api.deklutter.co/oauth/google/init?source=web

1. Click the link above
2. Copy the `auth_url` from the JSON response
3. Open that URL in your browser
4. Sign in with Google
5. Grant permissions (read & modify Gmail)
6. You'll be redirected back

**Note:** Use an **incognito/private window** to avoid cached sessions.

### **Step 2: Get Your JWT Token**

After OAuth, look at the URL in your browser. It should contain `?token=...`

Copy everything after `token=` - this is your JWT token.

**Example:**
```
http://localhost:3000/dashboard?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
                                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                      Copy this entire token
```

### **Step 3: Test API with Swagger**

1. Go to: https://api.deklutter.co/docs
2. Click **"Authorize"** button (top right)
3. Paste your JWT token
4. Click **"Authorize"**

Now you can test all endpoints!

### **Step 4: Scan Your Inbox**

In Swagger docs:
1. Find `/gmail/scan` endpoint
2. Click **"Try it out"**
3. Set parameters:
   - `days_back`: 7 (scan last 7 days)
   - `max_results`: 100
4. Click **"Execute"**
5. Wait 30-60 seconds
6. Check the response!

**What you'll see:**
- Total emails scanned
- How many to delete/review/keep
- Sample emails from each category
- Space that can be freed (MB)

---

## 📋 What to Test

### **1. OAuth Flow** ✅
- [ ] Can you connect your Gmail?
- [ ] Does the redirect work?
- [ ] Do you get a JWT token?

### **2. Email Scanning** ✅
- [ ] Does the scan complete?
- [ ] Are results accurate?
- [ ] Any false positives? (important emails marked as spam)
- [ ] Any false negatives? (spam marked as important)

### **3. Classification Quality** ✅
Check if these are classified correctly:
- [ ] **Spam:** Marketing emails, promotions
- [ ] **Review:** Receipts, order confirmations, newsletters you subscribed to
- [ ] **Keep:** Personal emails, work emails, important notifications

### **4. Edge Cases** ✅
- [ ] Empty inbox
- [ ] Very large inbox (1000+ emails)
- [ ] Emails in different languages
- [ ] Emails with attachments

### **5. Performance** ✅
- [ ] How long does scanning take?
- [ ] Does it timeout?
- [ ] Any errors?

---

## 🐛 How to Report Issues

### **What to Include:**

1. **What happened?** (Describe the issue)
2. **What did you expect?** (Expected behavior)
3. **Steps to reproduce** (How to recreate the issue)
4. **Screenshots** (If applicable)
5. **Error messages** (Copy exact error text)

### **Where to Report:**

Send to: [Your email or GitHub issues]

**Example Report:**
```
Issue: Scan timeout after 60 seconds

Expected: Scan should complete for 100 emails

Steps:
1. Connected Gmail with 5000+ emails
2. Tried to scan last 30 days
3. Got timeout error after 60 seconds

Error: "Request timeout - please try fewer days"

Screenshot: [attached]
```

---

## 📊 Feedback Form

After testing, please answer:

### **1. Overall Experience** (1-5 stars)
- How easy was it to set up?
- How accurate were the results?
- Would you use this regularly?

### **2. Classification Accuracy**
- Any important emails marked as spam? (List examples)
- Any spam emails marked as important? (List examples)
- Overall accuracy: ___ %

### **3. Performance**
- Scan time for 100 emails: ___ seconds
- Any timeouts or errors? Yes / No
- Speed: Too slow / Just right / Fast

### **4. Feature Requests**
- What features would you like to see?
- What's missing?
- What would make you use this daily?

### **5. Privacy Concerns**
- Do you feel comfortable giving Gmail access?
- Any privacy concerns?
- What would make you more comfortable?

---

## 🔐 Privacy & Security

### **What We Access:**
- ✅ Read your Gmail messages (to scan)
- ✅ Modify Gmail (to move emails to trash)
- ✅ Your email address (for authentication)

### **What We Store:**
- ✅ Your email address (hashed)
- ✅ Sender domains (e.g., "linkedin.com")
- ✅ Email metadata (date, size, labels)
- ❌ **NOT stored:** Email subjects, body content, attachments

### **What We Don't Do:**
- ❌ Send emails on your behalf
- ❌ Share your data with third parties
- ❌ Store email content
- ❌ Sell your data

**Full Privacy Policy:** https://api.deklutter.co/privacy

---

## 🎁 Beta Tester Perks

As a thank you for testing:
- 🎯 Early access to new features
- 💎 Free premium features (when launched)
- 🏆 Listed as beta tester (if you want)
- 📧 Direct line to the developer

---

## 🆘 Need Help?

### **Common Issues:**

**1. "Not authenticated" error**
- Solution: Make sure you copied the full JWT token
- Try authorizing again in Swagger docs

**2. "Redirect URI mismatch"**
- Solution: Use the exact URL provided
- Clear browser cache and try again

**3. Scan takes too long**
- Solution: Try fewer days (7 instead of 30)
- Reduce max_results (50 instead of 100)

**4. No results returned**
- Solution: Check if you have emails in the date range
- Try a different date range

### **Still Stuck?**

Contact: [Your contact info]

---

## 🙏 Thank You!

Your feedback is invaluable in making Deklutter better!

**Happy Testing!** 🚀

---

## 📝 Quick Links

- **API Docs:** https://api.deklutter.co/docs
- **Health Check:** https://api.deklutter.co/health
- **Privacy Policy:** https://api.deklutter.co/privacy
- **OAuth Init:** https://api.deklutter.co/oauth/google/init?source=web
