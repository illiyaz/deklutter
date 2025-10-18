"""
Privacy Policy endpoint for Deklutter
"""

PRIVACY_POLICY_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Deklutter - Privacy Policy</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }
        h1 { color: #2563eb; border-bottom: 2px solid #2563eb; padding-bottom: 10px; }
        h2 { color: #1e40af; margin-top: 30px; }
        .last-updated { color: #666; font-style: italic; }
        .highlight { background-color: #eff6ff; padding: 15px; border-left: 4px solid #2563eb; margin: 20px 0; }
        ul { padding-left: 25px; }
        li { margin-bottom: 8px; }
    </style>
</head>
<body>
    <h1>🧹 Deklutter - Privacy Policy</h1>
    <p class="last-updated">Last Updated: October 19, 2025</p>
    
    <div class="highlight">
        <strong>TL;DR:</strong> We only access email metadata (sender, subject, date, size) - never your email content. 
        All data is encrypted, and you can revoke access anytime.
    </div>

    <h2>1. Information We Collect</h2>
    <p>When you use Deklutter, we collect:</p>
    <ul>
        <li><strong>Email Metadata Only:</strong> Sender email address, subject line, date, and message size</li>
        <li><strong>Gmail Labels:</strong> Categories assigned by Gmail (e.g., Promotions, Social)</li>
        <li><strong>OAuth Tokens:</strong> Encrypted access tokens to connect to your Gmail account</li>
        <li><strong>Classification Decisions:</strong> Records of which emails were marked for deletion/review/keep</li>
    </ul>

    <h2>2. What We DO NOT Collect</h2>
    <ul>
        <li>❌ Email body content or message text</li>
        <li>❌ Email attachments or files</li>
        <li>❌ Contact lists or address books</li>
        <li>❌ Passwords or credentials (handled securely via OAuth)</li>
        <li>❌ Personal information beyond what's in email metadata</li>
    </ul>

    <h2>3. How We Use Your Information</h2>
    <p>We use the collected metadata to:</p>
    <ul>
        <li>Classify emails as spam, promotional, or important</li>
        <li>Show you statistics about your inbox (e.g., space used, email counts)</li>
        <li>Execute cleanup actions (delete/label emails) with your explicit approval</li>
        <li>Improve our classification algorithms</li>
    </ul>

    <h2>4. Data Security</h2>
    <ul>
        <li><strong>Encryption:</strong> All OAuth tokens are encrypted using AES-256 encryption</li>
        <li><strong>Token Expiration:</strong> Access tokens expire every hour and are auto-renewed</li>
        <li><strong>Secure Storage:</strong> Data is stored in encrypted databases with restricted access</li>
        <li><strong>HTTPS Only:</strong> All communications use secure HTTPS connections</li>
    </ul>

    <h2>5. Data Retention</h2>
    <ul>
        <li><strong>OAuth Tokens:</strong> Stored for 90 days or until you revoke access</li>
        <li><strong>Classification Logs:</strong> Retained for 90 days for analytics and debugging</li>
        <li><strong>Revocation:</strong> When you revoke access, all your data is immediately deleted</li>
    </ul>

    <h2>6. Third-Party Services</h2>
    <p>We integrate with:</p>
    <ul>
        <li><strong>Google Gmail API:</strong> To access your email metadata (subject to Google's Privacy Policy)</li>
        <li><strong>OpenAI ChatGPT:</strong> As the interface for interacting with Deklutter</li>
    </ul>
    <p>We do not share your data with any other third parties.</p>

    <h2>7. Your Rights</h2>
    <p>You have the right to:</p>
    <ul>
        <li><strong>Revoke Access:</strong> Say "revoke access" to the GPT to immediately delete all your data</li>
        <li><strong>Data Portability:</strong> Request a copy of your classification logs</li>
        <li><strong>Deletion:</strong> All data is deleted when you revoke access</li>
    </ul>

    <h2>8. Data Sharing</h2>
    <p><strong>We NEVER:</strong></p>
    <ul>
        <li>❌ Sell your data to third parties</li>
        <li>❌ Use your data for advertising</li>
        <li>❌ Share your email metadata with anyone</li>
        <li>❌ Send emails on your behalf</li>
    </ul>

    <h2>9. Children's Privacy</h2>
    <p>Deklutter is not intended for users under 13 years of age. We do not knowingly collect data from children.</p>

    <h2>10. Changes to This Policy</h2>
    <p>We may update this privacy policy from time to time. The "Last Updated" date at the top will reflect any changes. 
    Continued use of Deklutter after changes constitutes acceptance of the updated policy.</p>

    <h2>11. Contact Us</h2>
    <p>If you have questions about this privacy policy or your data, please contact us:</p>
    <ul>
        <li><strong>Email:</strong> privacy@deklutter.app (or your email)</li>
        <li><strong>GitHub:</strong> <a href="https://github.com/illiyaz/deklutter">github.com/illiyaz/deklutter</a></li>
    </ul>

    <h2>12. Compliance</h2>
    <ul>
        <li><strong>GDPR:</strong> We comply with EU General Data Protection Regulation</li>
        <li><strong>CCPA:</strong> We comply with California Consumer Privacy Act</li>
        <li><strong>Google API Services:</strong> We comply with Google API Services User Data Policy</li>
    </ul>

    <div class="highlight">
        <strong>🔒 Your Privacy Matters:</strong> Deklutter is built with privacy-first principles. 
        We only access what's necessary to help you clean your inbox, and you're always in control.
    </div>

    <hr style="margin-top: 40px; border: none; border-top: 1px solid #ddd;">
    <p style="text-align: center; color: #666; font-size: 14px;">
        © 2025 Deklutter. All rights reserved.
    </p>
</body>
</html>
"""
