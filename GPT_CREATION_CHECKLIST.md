# ✅ GPT Store Creation Checklist

Follow these steps to create and publish your Deklutter GPT.

---

## 📋 Pre-Launch Checklist

### ✅ Prerequisites (Already Done!)
- [x] API deployed to Render
- [x] OAuth configured
- [x] OpenAPI schema created
- [x] Privacy policy accessible
- [x] Terms of service accessible
- [x] Multi-provider architecture ready

---

## 🎨 Step 1: Create the GPT (15 minutes)

### 1.1 Go to GPT Builder
**URL:** https://chat.openai.com/gpts/editor

**Requirements:**
- ChatGPT Plus subscription ($20/month)
- Verified OpenAI account

### 1.2 Click "Create"
- Choose **"Configure"** tab (not "Create")
- This gives you full control

---

## 📝 Step 2: Basic Configuration (10 minutes)

### 2.1 Name
```
Deklutter
```

### 2.2 Description
```
AI-powered digital decluttering assistant. Clean your Gmail inbox by automatically identifying and removing spam, newsletters, and promotional emails. More providers (Yahoo, Outlook, Drive, Dropbox) coming soon!
```

### 2.3 Instructions
**Copy from:** `GPT_STORE_GUIDE.md` (lines 35-120)

Or use this condensed version:

```
You are Deklutter, an AI assistant that helps users clean their digital life, starting with Gmail.

## Your Personality
- Friendly and helpful
- Privacy-conscious and transparent
- Efficient and action-oriented

## Your Capabilities
1. Scan Gmail inbox for unwanted emails
2. Classify emails as: delete, review, or keep
3. Provide summaries and statistics
4. Execute cleanup with user approval

## Workflow

### First Time Users
1. Greet warmly: "Hi! I can help clean your Gmail inbox by identifying spam and unwanted emails. Ready to get started?"
2. Explain: "I'll need permission to access your Gmail. I only read email metadata (sender, subject, date) - not the content."
3. Use `initializeGmailOAuth` action to get authorization URL
4. Guide them through OAuth: "Please click this link to authorize: [URL]"
5. Once authorized, proceed to scan

### Scanning
1. Ask preferences: "How many days back should I scan? (default: 30 days)"
2. Use `scanGmail` action with user's preferences
3. Present results clearly:
   "📊 Scan complete!
   - Total emails: X
   - Spam/promotional (safe to delete): Y emails, Z MB
   - Important emails (keep): W emails
   
   Would you like me to delete the spam emails? They'll be moved to Trash where you can recover them for 30 days."

### Cleanup
1. ALWAYS get explicit confirmation before deleting
2. Show what will be deleted
3. Use `applyCleanup` action
4. Confirm completion: "✅ Done! Deleted X emails and freed up Y MB."
5. Offer next steps: "Want to scan again or adjust settings?"

## Important Rules
- NEVER delete emails without explicit user confirmation
- ALWAYS show what will be deleted first
- Be transparent about OAuth and data access
- Explain deleted emails go to Trash (recoverable for 30 days)
- If user seems uncertain, recommend "review" mode

## Future Vision
Mention when relevant: "Currently I support Gmail. Soon I'll be able to clean Yahoo Mail, Outlook, Google Drive, Dropbox, and more!"

## Error Handling
- If OAuth fails: "It looks like authorization didn't complete. Let's try again."
- If scan fails: "I couldn't scan your inbox. Please make sure you've authorized Gmail access."
- If API errors: Explain clearly and offer to retry
```

### 2.4 Conversation Starters
```
• Clean my Gmail inbox
• Scan for spam emails
• Show my inbox statistics
• Delete promotional emails
```

### 2.5 Knowledge
**Leave empty** (not needed for now)

### 2.6 Capabilities
- ❌ Web Browsing: OFF
- ❌ DALL·E: OFF
- ❌ Code Interpreter: OFF

---

## 🔌 Step 3: Configure Actions (20 minutes)

### 3.1 Click "Create new action"

### 3.2 Import Schema

**Option A: Import from URL (Recommended)**
```
https://deklutter-api.onrender.com/openapi.json
```

**Option B: Copy/Paste**
- Open `openapi.yaml` in your repo
- Copy entire contents
- Paste into schema field

### 3.3 Configure Authentication

**Authentication Type:** OAuth

**Client ID:**
```
<Your Google OAuth Client ID from .env file>
```

**Client Secret:**
```
<Your Google OAuth Client Secret from .env file>
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

**Token Exchange Method:** Default (POST request)

### 3.4 Save Action

Click "Save" - GPT will validate the schema

---

## 🎨 Step 4: Branding (10 minutes)

### 4.1 Profile Picture

**Option A: Use Emoji**
- Click profile picture area
- Choose 📧 or 🧹 emoji

**Option B: Upload Logo**
- Create 512x512 px image
- Simple icon (envelope, broom, sparkles)
- Upload via profile picture area

### 4.2 Preview

Check how it looks in the preview pane on the right

---

## 🧪 Step 5: Test Your GPT (15 minutes)

### 5.1 Test in Preview

In the right panel, try:

**Test 1: Introduction**
```
User: "What can you do?"
```
Expected: GPT explains its capabilities

**Test 2: OAuth Flow**
```
User: "Clean my inbox"
```
Expected: GPT asks for authorization and provides OAuth URL

**Test 3: Authorization**
- Click the OAuth URL
- Authorize Gmail access
- Return to chat

**Test 4: Scan**
```
User: "Scan my inbox"
```
Expected: GPT scans and shows results

**Test 5: Cleanup**
```
User: "Delete the spam emails"
```
Expected: GPT confirms and executes

### 5.2 Test Edge Cases

```
User: "Is this safe?"
User: "Can I undo deletions?"
User: "What data do you access?"
```

Expected: GPT answers appropriately

---

## 📢 Step 6: Publish to GPT Store (5 minutes)

### 6.1 Click "Publish" Button

### 6.2 Choose Visibility

**Options:**
- **Public** - Anyone can find in GPT Store ✅ (Recommended)
- **Unlisted** - Only people with link
- **Private** - Only you

**Choose:** Public

### 6.3 Select Category

**Category:** Productivity

**Tags:** 
```
gmail, email, productivity, automation, cleanup, organization
```

### 6.4 Confirm Publishing

- Review terms
- Click "Confirm"

**Note:** OpenAI will review your GPT (usually 1-2 days)

---

## ⏰ Step 7: Wait for Approval (1-2 days)

### What Happens
- OpenAI reviews your GPT
- Checks for policy compliance
- Tests basic functionality
- Approves or requests changes

### You'll Receive
- Email notification when approved
- GPT goes live in store
- Public URL to share

---

## 🎉 Step 8: Post-Launch (Ongoing)

### 8.1 Share Your GPT

**Get your GPT URL:**
```
https://chat.openai.com/g/g-[YOUR-GPT-ID]-deklutter
```

**Share on:**
- Twitter/X
- LinkedIn
- Reddit (r/ChatGPT, r/productivity)
- Product Hunt
- Hacker News

### 8.2 Monitor Usage

**Track:**
- Number of users
- Common questions
- Error patterns
- Feature requests

### 8.3 Iterate

**Based on feedback:**
- Update instructions
- Improve error messages
- Add conversation starters
- Refine responses

---

## 📊 Success Metrics

### Week 1
- Target: 10 users
- Target: 100 emails scanned

### Month 1
- Target: 100 users
- Target: 10,000 emails scanned
- Target: 4+ star rating

### Month 3
- Target: 1,000 users
- Target: 100,000 emails scanned
- Target: Featured in GPT Store

---

## 🐛 Troubleshooting

### Issue: OAuth doesn't work
**Fix:** 
- Check redirect URI in Google Console
- Verify client ID/secret are correct
- Test OAuth flow manually

### Issue: Actions fail
**Fix:**
- Check API is accessible
- Verify OpenAPI schema is correct
- Test endpoints with curl

### Issue: GPT gives wrong responses
**Fix:**
- Refine instructions
- Add more examples
- Test with different phrasings

### Issue: GPT rejected by OpenAI
**Fix:**
- Review OpenAI policies
- Ensure privacy policy is clear
- Remove any prohibited content

---

## 📚 Resources

- **GPT Editor:** https://chat.openai.com/gpts/editor
- **OpenAI Actions Docs:** https://platform.openai.com/docs/actions
- **Your API:** https://deklutter-api.onrender.com
- **API Docs:** https://deklutter-api.onrender.com/docs
- **Privacy Policy:** https://deklutter-api.onrender.com/privacy

---

## ✅ Final Checklist

Before publishing, verify:

- [ ] GPT name is "Deklutter"
- [ ] Description mentions Gmail and future providers
- [ ] Instructions are clear and comprehensive
- [ ] Conversation starters are helpful
- [ ] Actions are configured correctly
- [ ] OAuth works in testing
- [ ] Profile picture looks good
- [ ] Privacy policy is accessible
- [ ] Terms of service is accessible
- [ ] Tested with real Gmail account
- [ ] All edge cases handled

---

## 🎯 Next Steps After Publishing

1. **Week 1:** Monitor and fix issues
2. **Week 2:** Add Yahoo Mail connector
3. **Week 3:** Add Outlook connector
4. **Week 4:** Update GPT to support multiple providers
5. **Month 2:** Build React dashboard
6. **Month 3:** Launch mobile app

---

## 🚀 Ready to Create!

**Estimated Time:** 1-2 hours total

**Start here:** https://chat.openai.com/gpts/editor

**Good luck!** 🎉
