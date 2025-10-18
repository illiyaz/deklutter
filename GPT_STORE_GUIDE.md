# 📱 Deklutter GPT Store App - Complete Guide

## 🎯 Overview

This guide will help you create and publish **Deklutter** as a Custom GPT in the ChatGPT GPT Store.

**What users will experience:**
1. Discover "Deklutter" in GPT Store
2. Start a conversation
3. Authorize Gmail access via OAuth
4. Get AI-powered inbox cleaning recommendations
5. Approve and execute cleanup

---

## 📋 Prerequisites

✅ You already have:
- Working API at https://deklutter-api.onrender.com
- OAuth configured with Google
- Privacy policy at `/privacy`
- Terms of service at `/terms`

---

## 🏗️ Step 1: Create OpenAPI Schema

Your API needs an OpenAPI schema for GPT Actions. I'll create this for you.

**File:** `openapi.yaml` (in your repo)

This describes your API endpoints for ChatGPT to understand.

---

## 🎨 Step 2: Create Custom GPT

### Go to ChatGPT GPT Builder

1. **Visit:** https://chat.openai.com/gpts/editor
2. **Click:** "Create a GPT"
3. **Choose:** "Configure" tab (not "Create")

### Basic Information

**Name:**
```
Deklutter
```

**Description:**
```
AI-powered Gmail inbox cleaner. Automatically identify and remove spam, newsletters, and promotional emails. Free up space and declutter your inbox in seconds.
```

**Instructions:** (See detailed instructions below)

**Conversation Starters:**
```
• Clean my inbox
• Scan for spam emails
• Show my inbox statistics
• Delete promotional emails
```

**Knowledge:** (Leave empty for now)

**Capabilities:**
- ✅ Web Browsing: OFF
- ✅ DALL·E Image Generation: OFF
- ✅ Code Interpreter: OFF

---

## 📝 Step 3: GPT Instructions

Copy this into the "Instructions" field:

```
You are Deklutter, an AI assistant that helps users clean their Gmail inbox by identifying and removing spam, newsletters, and promotional emails.

## Your Personality
- Friendly and helpful
- Privacy-conscious and transparent
- Efficient and action-oriented
- Clear about what you're doing

## Your Capabilities
1. Scan Gmail inbox for unwanted emails
2. Classify emails as: delete, review, or keep
3. Provide summaries and statistics
4. Execute cleanup with user approval

## Workflow

### First Time Users
1. Greet warmly and explain what you do
2. Ask for Gmail authorization
3. Use `initializeGmailOAuth` action
4. Guide them through OAuth flow
5. Once authorized, proceed to scan

### Scanning
1. Ask user preferences:
   - How many days back to scan (default: 30)
   - How many emails to analyze (default: 100)
2. Use `scanGmail` action
3. Present results clearly:
   - Total emails scanned
   - Safe to delete (spam/promotional)
   - Review recommended (uncertain)
   - Keep (important)
   - Space that can be freed

### Cleanup
1. Show what will be deleted
2. Ask for explicit confirmation
3. Use `applyCleanup` action
4. Confirm completion
5. Offer to scan again or adjust settings

## Important Rules
- ALWAYS get explicit user confirmation before deleting emails
- NEVER delete emails without showing what will be deleted first
- Be transparent about OAuth and data access
- Explain that deleted emails go to Trash (recoverable for 30 days)
- If user seems uncertain, recommend "review" mode first

## Error Handling
- If OAuth fails: Guide user to re-authorize
- If scan fails: Suggest checking Gmail permissions
- If API errors: Explain clearly and offer to retry

## Privacy & Security
- Emphasize that you only read email metadata (not content)
- Explain OAuth tokens are encrypted
- Mention users can revoke access anytime
- Link to privacy policy when asked

## Example Conversations

User: "Clean my inbox"
You: "I'd be happy to help clean your Gmail inbox! First, I need permission to access your Gmail. This will allow me to scan for spam and unwanted emails. I only read email metadata (sender, subject, date) - not the content of your emails. Ready to authorize?"

User: "Yes"
You: [Use initializeGmailOAuth action, provide authorization link]

After OAuth:
You: "✅ Connected! Now scanning your inbox... [Use scanGmail action]"

After scan:
You: "📊 Scan complete! Here's what I found:
- 127 emails scanned (last 30 days)
- 45 spam/promotional emails (safe to delete) - 3.2 MB
- 12 newsletters (review recommended) - 0.8 MB
- 70 important emails (keep)

Would you like me to delete the 45 spam emails? They'll be moved to Trash where you can recover them for 30 days if needed."

User: "Yes, delete them"
You: [Use applyCleanup action] "✅ Done! Deleted 45 emails and freed up 3.2 MB. Your inbox is cleaner! Want me to scan again or adjust the settings?"
```

---

## 🔌 Step 4: Configure Actions

### Add Action

1. Click **"Create new action"**
2. **Authentication:** OAuth
3. **Schema:** Import from URL or paste YAML

**Import URL:**
```
https://deklutter-api.onrender.com/openapi.json
```

Or paste the `openapi.yaml` content (I'll create this file next)

### OAuth Configuration

**Authentication Type:** OAuth

**Client ID:**
```
<Your Google OAuth Client ID>
```

**Client Secret:**
```
<Your Google OAuth Client Secret>
```

**Authorization URL:**
```
https://accounts.google.com/o/oauth2/auth
```

**Token URL:**
```
https://oauth2.googleapis.com/token
```

**Scope:**
```
https://www.googleapis.com/auth/gmail.readonly
```

**Token Exchange Method:** Default (POST)

---

## 🎨 Step 5: Branding (Optional but Recommended)

### Profile Picture
- Upload a logo (512x512 px recommended)
- Use an envelope/inbox icon
- Keep it simple and recognizable

### Color Scheme
- Primary: Blue (#2563eb)
- Accent: Green (#16a34a)

---

## 🧪 Step 6: Test Your GPT

### Test Conversation Flow

1. **Start conversation:**
   ```
   "Clean my inbox"
   ```

2. **Verify OAuth:**
   - Should provide authorization link
   - Should redirect correctly
   - Should confirm connection

3. **Test scan:**
   ```
   "Scan my inbox from the last 7 days"
   ```

4. **Test cleanup:**
   ```
   "Delete the spam emails"
   ```

5. **Test edge cases:**
   - "What do you do?"
   - "Is this safe?"
   - "Can I undo deletions?"
   - "Show my privacy policy"

---

## 📢 Step 7: Publish to GPT Store

### Before Publishing

**Checklist:**
- ✅ GPT works in testing
- ✅ OAuth flow completes successfully
- ✅ All actions work correctly
- ✅ Instructions are clear
- ✅ Privacy policy is accessible
- ✅ Terms of service is accessible
- ✅ Profile picture uploaded
- ✅ Description is compelling

### Publish Settings

**Visibility:**
- **Public** - Anyone can find and use
- **Unlisted** - Only people with link
- **Private** - Only you

**Category:**
```
Productivity
```

**Tags:**
```
gmail, email, productivity, automation, cleanup
```

### Publishing

1. Click **"Publish"** button
2. Choose **"Public"** (for GPT Store)
3. Review and accept terms
4. Click **"Confirm"**

**Your GPT will be reviewed by OpenAI (usually 1-2 days)**

---

## 📊 Step 8: Monitor & Iterate

### After Publishing

**Track:**
- User conversations
- Common questions
- Error patterns
- Feature requests

**Improve:**
- Update instructions based on user feedback
- Add more conversation starters
- Improve error messages
- Add new features to API

---

## 💰 Step 9: Monetization (Optional)

### GPT Store Revenue Share

**Requirements:**
- ChatGPT Plus subscription
- Builder profile verified
- Significant usage

**How it works:**
- OpenAI shares revenue based on usage
- Paid quarterly
- Based on user engagement time

### Alternative Monetization

**Freemium Model:**
- Free: 10 scans/month
- Pro: Unlimited scans ($5/month)
- Implement in your API with usage tracking

---

## 🎯 Success Metrics

**Track these:**
- Total users
- Active users (weekly/monthly)
- Scans performed
- Emails deleted
- User ratings
- Conversation completion rate

---

## 🚨 Common Issues & Solutions

### Issue: OAuth fails
**Solution:** Check redirect URI matches exactly in Google Console

### Issue: Actions not working
**Solution:** Verify OpenAPI schema is correct and API is accessible

### Issue: GPT gives wrong responses
**Solution:** Refine instructions, add more examples

### Issue: Users confused about privacy
**Solution:** Add more transparency in initial message

---

## 📚 Resources

- **GPT Editor:** https://chat.openai.com/gpts/editor
- **OpenAI Actions Guide:** https://platform.openai.com/docs/actions
- **Your API Docs:** https://deklutter-api.onrender.com/docs
- **Your Privacy Policy:** https://deklutter-api.onrender.com/privacy

---

## 🎊 Next Steps

1. ✅ Create OpenAPI schema
2. ✅ Configure Custom GPT
3. ✅ Add Actions
4. ✅ Configure OAuth
5. ✅ Test thoroughly
6. ✅ Publish to GPT Store
7. ✅ Share with users!

---

**Let's create the OpenAPI schema next!** 🚀
