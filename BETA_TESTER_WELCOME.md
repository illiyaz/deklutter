# 🎉 Welcome to Deklutter Beta!

Thank you for being an early tester! Your feedback will help shape the future of Deklutter.

---

## 🚀 What is Deklutter?

**Deklutter** is an AI-powered tool that helps you clean your Gmail inbox automatically. It identifies spam, newsletters, and promotional emails that you can safely delete, freeing up storage space and decluttering your inbox.

---

## ✨ How to Get Started (2 minutes)

### **Step 1: Connect Your Gmail**
Visit: **https://api.deklutter.co/start**

- Click the link
- Sign in with your Gmail account
- Click "Allow" to grant permissions
- **Copy your JWT token** from the success page

### **Step 2: Try the API**
Go to: **https://api.deklutter.co/docs**

1. Click the **"Authorize"** button (green lock icon)
2. Select **"BearerAuth"**
3. Paste your JWT token
4. Click **"Authorize"** then **"Close"**

### **Step 3: Scan Your Inbox**
1. Find the `/gmail/scan` endpoint
2. Click **"Try it out"**
3. Set parameters:
   - `days_back`: 30 (scan last 30 days)
   - `limit`: 100 (scan up to 100 emails)
4. Click **"Execute"**
5. Wait 30-60 seconds for results

### **Step 4: Review Results**
You'll see:
- **Delete**: Emails safe to delete (spam, newsletters)
- **Review**: Emails that need your review (uncertain)
- **Keep**: Important emails to keep

Plus sample emails from each category!

---

## 🧪 What to Test

### **1. Accuracy**
- Are the "delete" emails actually spam/unwanted?
- Are there any false positives (important emails marked for deletion)?
- Are the "keep" emails truly important?

### **2. User Experience**
- Was the setup process easy?
- Are the instructions clear?
- Is the API response helpful?

### **3. Performance**
- How long did the scan take?
- Did you encounter any errors?
- Did the rate limiting affect you?

### **4. Features**
- What features are missing?
- What would make this more useful?
- Would you use this regularly?

---

## 📊 What We're Measuring

- **Accuracy**: % of correctly classified emails
- **User Satisfaction**: Would you recommend this?
- **Performance**: Scan time and reliability
- **Feature Requests**: What do you want to see next?

---

## 🐛 How to Report Issues

### **Found a Bug?**
Email: mohammad.illiyaz@gmail.com

Include:
- What you were trying to do
- What happened (error message, unexpected behavior)
- Screenshots if possible

### **Have Feedback?**
Email: mohammad.illiyaz@gmail.com

Tell us:
- What you liked
- What you didn't like
- What features you want
- Would you pay for this?

---

## 🔒 Privacy & Security

### **What We Collect:**
- Your email address (for authentication)
- Email metadata (sender domain, date, size)
- Classification decisions (delete/review/keep)

### **What We DON'T Collect:**
- ❌ Email subjects
- ❌ Email content/body
- ❌ Sender email addresses
- ❌ Recipient information

### **Your Data:**
- Stored securely with encryption
- Never shared with third parties
- You can delete it anytime via `/oauth/revoke`

Read full privacy policy: https://api.deklutter.co/privacy

---

## 🎁 Beta Tester Perks

As a thank you for testing:
- ✅ **Free lifetime access** to Pro features (when launched)
- ✅ **Priority support** via email
- ✅ **Early access** to new features
- ✅ **Your name** in our credits (if you want!)

---

## 📅 Testing Timeline

- **Week 1**: Test core features, report bugs
- **Week 2**: Test improvements, provide feedback
- **Week 3**: Final testing before public launch

---

## 🤝 Join the Community

- **GitHub**: https://github.com/illiyaz/deklutter
- **Email**: mohammad.illiyaz@gmail.com
- **API Docs**: https://api.deklutter.co/docs

---

## ❓ FAQ

### **Q: Is this safe?**
A: Yes! We only move emails to trash (recoverable for 30 days). We never permanently delete anything without your explicit confirmation.

### **Q: What permissions do you need?**
A: We need:
- Read your emails (to scan and classify)
- Modify your emails (to move to trash/label)
- See your email address (for authentication)

### **Q: Can I undo deletions?**
A: Yes! Emails are moved to trash, not permanently deleted. You can recover them from Gmail's trash folder for 30 days.

### **Q: How long does a scan take?**
A: Typically 30-60 seconds for 100 emails. Larger scans may take longer.

### **Q: Is there a limit?**
A: Currently:
- Max 5 scans per minute
- Max 10 cleanup operations per minute
- Max 1000 emails per scan

### **Q: Will this work with ChatGPT?**
A: Yes! We have a ChatGPT GPT integration. Ask for the link!

---

## 🚀 Next Steps

1. **Test the API** (today)
2. **Send feedback** (this week)
3. **Share with friends** (if you like it!)
4. **Stay tuned** for updates

---

**Thank you for helping us build Deklutter!** 🙏

Your feedback is invaluable. Let's declutter the digital world together! 🌟

---

**Questions?** Email mohammad.illiyaz@gmail.com anytime!
