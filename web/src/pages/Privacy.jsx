export default function Privacy() {
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Privacy Policy</h1>
        <p className="text-sm text-gray-600 mb-8">Last Updated: November 30, 2025</p>

        <div className="prose prose-lg max-w-none">
          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">1. Introduction</h2>
            <p className="text-gray-700 mb-4">
              Welcome to Deklutter ("we," "our," or "us"). We are committed to protecting your privacy and ensuring the security of your personal information. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our email cleaning service.
            </p>
            <p className="text-gray-700">
              By using Deklutter, you agree to the collection and use of information in accordance with this policy.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">2. Information We Collect</h2>
            
            <h3 className="text-xl font-semibold text-gray-800 mb-3">2.1 Information You Provide</h3>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li><strong>Email Address:</strong> When you sign up using Google OAuth</li>
              <li><strong>Profile Information:</strong> Name and profile picture from your Google account</li>
            </ul>

            <h3 className="text-xl font-semibold text-gray-800 mb-3">2.2 Information We Access</h3>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li><strong>Email Metadata:</strong> Subject lines, sender information, dates, and Gmail labels</li>
              <li><strong>Email Content:</strong> We analyze email content solely to categorize and identify spam/promotional emails</li>
              <li><strong>Gmail API Access:</strong> We use limited Gmail API scopes to read and modify (delete) emails with your explicit permission</li>
            </ul>

            <h3 className="text-xl font-semibold text-gray-800 mb-3">2.3 Automatically Collected Information</h3>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li><strong>Usage Data:</strong> Number of scans, emails deleted, and service usage patterns</li>
              <li><strong>Technical Data:</strong> IP address, browser type, and device information</li>
              <li><strong>Log Data:</strong> Error logs and performance metrics</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">3. How We Use Your Information</h2>
            <p className="text-gray-700 mb-4">We use your information for the following purposes:</p>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li><strong>Service Delivery:</strong> To scan your inbox and identify spam/promotional emails</li>
              <li><strong>Email Cleanup:</strong> To delete emails you explicitly approve for deletion</li>
              <li><strong>Authentication:</strong> To verify your identity and maintain your session</li>
              <li><strong>Service Improvement:</strong> To analyze usage patterns and improve our algorithms</li>
              <li><strong>Communication:</strong> To send service-related notifications (with your consent)</li>
              <li><strong>Security:</strong> To detect and prevent fraud, abuse, and security incidents</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">4. Data Storage and Security</h2>
            
            <h3 className="text-xl font-semibold text-gray-800 mb-3">4.1 What We Store</h3>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li><strong>User Profile:</strong> Email address, name, and Google user ID</li>
              <li><strong>OAuth Tokens:</strong> Encrypted access and refresh tokens for Gmail API access</li>
              <li><strong>Usage Statistics:</strong> Aggregated data about scans and deletions (no email content)</li>
            </ul>

            <h3 className="text-xl font-semibold text-gray-800 mb-3">4.2 What We DON'T Store</h3>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li><strong>Email Content:</strong> We do not store the content of your emails</li>
              <li><strong>Email Bodies:</strong> We do not retain email text after analysis</li>
              <li><strong>Attachments:</strong> We do not access or store email attachments</li>
              <li><strong>Passwords:</strong> We use OAuth; we never see or store your Gmail password</li>
            </ul>

            <h3 className="text-xl font-semibold text-gray-800 mb-3">4.3 Security Measures</h3>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li><strong>Encryption:</strong> All data is encrypted in transit (TLS/SSL) and at rest</li>
              <li><strong>Access Control:</strong> Strict access controls and authentication mechanisms</li>
              <li><strong>Regular Audits:</strong> Security audits and vulnerability assessments</li>
              <li><strong>Secure Infrastructure:</strong> Hosted on secure cloud infrastructure (Render.com)</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">5. Data Sharing and Disclosure</h2>
            <p className="text-gray-700 mb-4">
              <strong>We do NOT sell, rent, or share your personal information with third parties for marketing purposes.</strong>
            </p>
            
            <h3 className="text-xl font-semibold text-gray-800 mb-3">We may share information only in these limited cases:</h3>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li><strong>Service Providers:</strong> With trusted service providers (e.g., hosting, analytics) under strict confidentiality agreements</li>
              <li><strong>Legal Requirements:</strong> When required by law, court order, or government request</li>
              <li><strong>Safety and Security:</strong> To protect the rights, property, or safety of Deklutter, our users, or others</li>
              <li><strong>Business Transfers:</strong> In connection with a merger, acquisition, or sale of assets (with notice to you)</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">6. Your Rights and Choices</h2>
            <p className="text-gray-700 mb-4">You have the following rights regarding your data:</p>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li><strong>Access:</strong> Request a copy of your personal data</li>
              <li><strong>Correction:</strong> Request correction of inaccurate data</li>
              <li><strong>Deletion:</strong> Request deletion of your account and data</li>
              <li><strong>Revoke Access:</strong> Disconnect Gmail access at any time via Google Account settings</li>
              <li><strong>Data Portability:</strong> Request your data in a portable format</li>
              <li><strong>Opt-Out:</strong> Opt out of non-essential communications</li>
            </ul>
            <p className="text-gray-700">
              To exercise these rights, contact us at <a href="mailto:privacy@deklutter.co" className="text-blue-600 hover:underline">privacy@deklutter.co</a>
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">7. Data Retention</h2>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li><strong>Active Accounts:</strong> We retain your data while your account is active</li>
              <li><strong>Deleted Accounts:</strong> Data is permanently deleted within 30 days of account deletion</li>
              <li><strong>Legal Obligations:</strong> Some data may be retained longer if required by law</li>
              <li><strong>Anonymized Data:</strong> Aggregated, anonymized usage statistics may be retained indefinitely</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">8. Google API Services User Data Policy</h2>
            <p className="text-gray-700 mb-4">
              Deklutter's use and transfer of information received from Google APIs adheres to the{' '}
              <a href="https://developers.google.com/terms/api-services-user-data-policy" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                Google API Services User Data Policy
              </a>, including the Limited Use requirements.
            </p>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li>We only request the minimum Gmail API scopes necessary for our service</li>
              <li>We do not use Gmail data for advertising or marketing purposes</li>
              <li>We do not allow humans to read your emails (automated processing only)</li>
              <li>We do not transfer Gmail data to third parties (except as required for service operation)</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">9. Children's Privacy</h2>
            <p className="text-gray-700">
              Deklutter is not intended for users under 13 years of age. We do not knowingly collect personal information from children under 13. If you believe we have collected information from a child under 13, please contact us immediately.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">10. International Data Transfers</h2>
            <p className="text-gray-700">
              Your information may be transferred to and processed in countries other than your country of residence. We ensure appropriate safeguards are in place to protect your data in accordance with this Privacy Policy and applicable laws.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">11. Changes to This Privacy Policy</h2>
            <p className="text-gray-700 mb-4">
              We may update this Privacy Policy from time to time. We will notify you of any material changes by:
            </p>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li>Posting the new Privacy Policy on this page</li>
              <li>Updating the "Last Updated" date</li>
              <li>Sending you an email notification (for significant changes)</li>
            </ul>
            <p className="text-gray-700">
              Your continued use of Deklutter after changes constitutes acceptance of the updated policy.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">12. Contact Us</h2>
            <p className="text-gray-700 mb-4">
              If you have questions, concerns, or requests regarding this Privacy Policy or your data, please contact us:
            </p>
            <div className="bg-gray-100 p-4 rounded-lg">
              <p className="text-gray-700"><strong>Email:</strong> <a href="mailto:privacy@deklutter.co" className="text-blue-600 hover:underline">privacy@deklutter.co</a></p>
              <p className="text-gray-700"><strong>Support:</strong> <a href="mailto:support@deklutter.co" className="text-blue-600 hover:underline">support@deklutter.co</a></p>
              <p className="text-gray-700"><strong>Website:</strong> <a href="https://app.deklutter.co" className="text-blue-600 hover:underline">https://app.deklutter.co</a></p>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">13. Compliance</h2>
            <p className="text-gray-700 mb-4">We comply with:</p>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li><strong>GDPR:</strong> General Data Protection Regulation (EU)</li>
              <li><strong>CCPA:</strong> California Consumer Privacy Act (US)</li>
              <li><strong>Google API Services User Data Policy</strong></li>
              <li><strong>CAN-SPAM Act:</strong> For email communications</li>
            </ul>
          </section>
        </div>

        <div className="mt-12 pt-8 border-t border-gray-200">
          <p className="text-center text-gray-600">
            <a href="/" className="text-blue-600 hover:underline">← Back to Home</a>
            {' | '}
            <a href="/terms" className="text-blue-600 hover:underline">Terms of Service</a>
          </p>
        </div>
      </div>
    </div>
  )
}
