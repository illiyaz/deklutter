# Email Setup Guide - Quick Start

## 🎯 **Goal: Set up professional emails for Deklutter**

Required emails:
- `support@deklutter.co`
- `privacy@deklutter.co`
- `legal@deklutter.co`

---

## ⚡ **Option 1: Email Forwarding (FREE - 5 minutes)**

### **Step 1: Set Up Forwarding (Namecheap)**

1. **Login to Namecheap:**
   - Go to: https://www.namecheap.com
   - Sign in to your account

2. **Navigate to Email Forwarding:**
   - Dashboard → Domain List
   - Click "Manage" next to `deklutter.co`
   - Click "Email Forwarding" tab

3. **Add Forwarding Rules:**
   ```
   support@deklutter.co  → mohammad.illiyaz@gmail.com
   privacy@deklutter.co  → mohammad.illiyaz@gmail.com
   legal@deklutter.co    → mohammad.illiyaz@gmail.com
   ```

4. **Verify:**
   - Check your Gmail for verification emails
   - Click verification links

### **Step 2: Send Emails FROM @deklutter.co**

1. **Open Gmail Settings:**
   - Go to: https://mail.google.com/mail/u/0/#settings/accounts
   - Click "Accounts and Import"

2. **Add Send-As Address:**
   - Click "Add another email address"
   - Name: `Deklutter Support`
   - Email: `support@deklutter.co`
   - Uncheck "Treat as an alias"
   - Click "Next Step"

3. **Verify Ownership:**
   - Choose "Send through Gmail" (easier)
   - Click "Send Verification"
   - Check your Gmail for verification code
   - Enter code and verify

4. **Repeat for other emails:**
   - Add `privacy@deklutter.co`
   - Add `legal@deklutter.co`

5. **Set Default:**
   - Make `support@deklutter.co` the default sender
   - Or choose which email to use when composing

### **Step 3: Test**

Send a test email from `support@deklutter.co` to yourself:
- Compose new email
- Click "From" dropdown
- Select `support@deklutter.co`
- Send to your personal email
- Verify it arrives with correct sender

---

## 💼 **Option 2: Google Workspace (PAID - $6/month)**

### **Pros:**
- ✅ Professional email hosting
- ✅ 30GB storage per user
- ✅ Better deliverability
- ✅ Custom email signatures
- ✅ Mobile app support

### **Setup:**

1. **Sign Up:**
   - Go to: https://workspace.google.com
   - Click "Get Started"
   - Enter business name: `Deklutter`
   - Number of employees: `1-9`

2. **Verify Domain:**
   - Add domain: `deklutter.co`
   - Verify via TXT record (they'll provide instructions)

3. **Create Users:**
   ```
   support@deklutter.co
   privacy@deklutter.co
   legal@deklutter.co
   ```

4. **Set Up Email Client:**
   - Use Gmail interface: https://mail.google.com
   - Or configure in Outlook/Apple Mail

### **Cost:**
- **Business Starter:** $6/user/month
- **Total:** $18/month for 3 emails
- **Alternative:** Use aliases (1 user, multiple aliases) = $6/month

---

## 🆓 **Option 3: Zoho Mail (FREE)**

### **Pros:**
- ✅ Free for up to 5 users
- ✅ 5GB storage per user
- ✅ Professional email hosting
- ✅ No ads

### **Setup:**

1. **Sign Up:**
   - Go to: https://www.zoho.com/mail/
   - Click "Sign Up Now"
   - Choose "Free Plan"

2. **Add Domain:**
   - Enter: `deklutter.co`
   - Verify via TXT record

3. **Create Email Accounts:**
   ```
   support@deklutter.co
   privacy@deklutter.co
   legal@deklutter.co
   ```

4. **Access Email:**
   - Web: https://mail.zoho.com
   - Mobile: Download Zoho Mail app
   - Desktop: Configure IMAP/SMTP

---

## 📋 **Recommended Setup (Fastest)**

### **For Immediate Use:**
1. **Use Email Forwarding** (Option 1)
   - Takes 5 minutes
   - Completely free
   - Works for Google OAuth verification

### **For Long-term:**
2. **Upgrade to Google Workspace** (Option 2)
   - More professional
   - Better deliverability
   - Integrated with Google services

---

## ✅ **After Setup - Update These Files:**

### **1. Privacy Policy**
Update contact email in:
- `/web/src/pages/Privacy.jsx`
- Change `privacy@deklutter.co` (already done ✅)

### **2. Terms of Service**
Update contact email in:
- `/web/src/pages/Terms.jsx`
- Change `legal@deklutter.co` (already done ✅)

### **3. Google OAuth Consent Screen**
Update in Google Cloud Console:
- User support email: `support@deklutter.co`
- Developer contact: `support@deklutter.co`

### **4. Landing Page**
Update contact link:
- `/web/src/pages/LandingPage.jsx`
- Change `mailto:support@deklutter.co` (already done ✅)

---

## 🧪 **Testing Checklist**

After setup, test the following:

- [ ] Send email TO `support@deklutter.co` → Should arrive in Gmail
- [ ] Send email FROM `support@deklutter.co` → Should send successfully
- [ ] Reply to an email using `support@deklutter.co`
- [ ] Check spam folder (shouldn't be there)
- [ ] Test on mobile device

---

## 🚨 **Common Issues**

### **Issue: Emails not forwarding**
- Check spam folder
- Verify forwarding rules are active
- Wait 5-10 minutes for DNS propagation

### **Issue: Can't send from @deklutter.co**
- Make sure you verified the email in Gmail
- Check "Send mail as" settings
- Try "Send through Gmail" option

### **Issue: Emails going to spam**
- Add SPF record to DNS
- Add DKIM record to DNS
- Use Google Workspace for better deliverability

---

## 📞 **Need Help?**

- **Namecheap Support:** https://www.namecheap.com/support/
- **Google Workspace Support:** https://support.google.com/a/
- **Zoho Support:** https://help.zoho.com/portal/en/home

---

## ⏱️ **Time Estimates**

| Option | Setup Time | Cost | Difficulty |
|--------|------------|------|------------|
| Email Forwarding | 5 min | Free | Easy |
| Google Workspace | 30 min | $6-18/mo | Medium |
| Zoho Mail | 20 min | Free | Medium |

---

**Recommendation:** Start with **Email Forwarding** (5 minutes, free) to get verified quickly. Upgrade to Google Workspace later if needed.

Good luck! 🚀
