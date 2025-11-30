export default function Terms() {
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Terms of Service</h1>
        <p className="text-sm text-gray-600 mb-8">Last Updated: November 30, 2025</p>

        <div className="prose prose-lg max-w-none">
          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">1. Acceptance of Terms</h2>
            <p className="text-gray-700 mb-4">
              Welcome to Deklutter! By accessing or using our service, you agree to be bound by these Terms of Service ("Terms"). If you do not agree to these Terms, please do not use our service.
            </p>
            <p className="text-gray-700">
              These Terms constitute a legally binding agreement between you and Deklutter ("we," "us," or "our").
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">2. Description of Service</h2>
            <p className="text-gray-700 mb-4">
              Deklutter is an AI-powered email cleaning service that helps you:
            </p>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li>Scan your Gmail inbox for spam and promotional emails</li>
              <li>Identify emails safe to delete based on heuristic analysis</li>
              <li>Delete unwanted emails with your explicit approval</li>
              <li>Free up storage space in your email account</li>
            </ul>
            <p className="text-gray-700">
              The service is provided "as is" and we reserve the right to modify, suspend, or discontinue any aspect of the service at any time.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">3. User Accounts and Registration</h2>
            
            <h3 className="text-xl font-semibold text-gray-800 mb-3">3.1 Account Creation</h3>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li>You must have a valid Gmail account to use Deklutter</li>
              <li>You must be at least 13 years old to use our service</li>
              <li>You must provide accurate and complete information</li>
              <li>You are responsible for maintaining the security of your account</li>
            </ul>

            <h3 className="text-xl font-semibold text-gray-800 mb-3">3.2 Account Security</h3>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li>You are responsible for all activities under your account</li>
              <li>You must notify us immediately of any unauthorized access</li>
              <li>We are not liable for losses due to unauthorized use of your account</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">4. Gmail API Access and Permissions</h2>
            
            <h3 className="text-xl font-semibold text-gray-800 mb-3">4.1 OAuth Authorization</h3>
            <p className="text-gray-700 mb-4">
              By connecting your Gmail account, you authorize Deklutter to:
            </p>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li>Read email metadata (subject, sender, date, labels)</li>
              <li>Read email content for classification purposes</li>
              <li>Move emails to trash (only with your explicit approval)</li>
            </ul>

            <h3 className="text-xl font-semibold text-gray-800 mb-3">4.2 Scope of Access</h3>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li>We only request the minimum necessary Gmail API scopes</li>
              <li>We do not access emails marked as important or from protected domains</li>
              <li>We do not read email attachments</li>
              <li>You can revoke access at any time via Google Account settings</li>
            </ul>

            <h3 className="text-xl font-semibold text-gray-800 mb-3">4.3 Revoking Access</h3>
            <p className="text-gray-700">
              You may revoke Deklutter's access to your Gmail account at any time by visiting your{' '}
              <a href="https://myaccount.google.com/permissions" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                Google Account Permissions
              </a>.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">5. User Responsibilities</h2>
            
            <h3 className="text-xl font-semibold text-gray-800 mb-3">5.1 Acceptable Use</h3>
            <p className="text-gray-700 mb-4">You agree to:</p>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li>Use the service only for lawful purposes</li>
              <li>Review emails before approving deletion</li>
              <li>Not attempt to circumvent security measures</li>
              <li>Not abuse or overload our systems</li>
              <li>Not reverse engineer or copy our technology</li>
            </ul>

            <h3 className="text-xl font-semibold text-gray-800 mb-3">5.2 Prohibited Activities</h3>
            <p className="text-gray-700 mb-4">You must NOT:</p>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li>Use the service for illegal activities</li>
              <li>Attempt to gain unauthorized access to other users' accounts</li>
              <li>Transmit viruses, malware, or harmful code</li>
              <li>Scrape or harvest data from the service</li>
              <li>Impersonate others or provide false information</li>
              <li>Interfere with the proper functioning of the service</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">6. Email Deletion and Recovery</h2>
            
            <h3 className="text-xl font-semibold text-gray-800 mb-3">6.1 Deletion Process</h3>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li>Emails are moved to Gmail's Trash folder, not permanently deleted</li>
              <li>You can recover deleted emails from Trash within 30 days</li>
              <li>After 30 days, Gmail automatically permanently deletes emails from Trash</li>
              <li>We do not have the ability to recover permanently deleted emails</li>
            </ul>

            <h3 className="text-xl font-semibold text-gray-800 mb-3">6.2 User Responsibility</h3>
            <p className="text-gray-700 mb-4">
              <strong>You are solely responsible for:</strong>
            </p>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li>Reviewing emails before approving deletion</li>
              <li>Maintaining backups of important emails</li>
              <li>Any consequences of deleted emails</li>
            </ul>
            <p className="text-gray-700 font-semibold">
              ⚠️ We are not liable for any loss of data resulting from email deletion, even if caused by our service.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">7. Intellectual Property</h2>
            
            <h3 className="text-xl font-semibold text-gray-800 mb-3">7.1 Our Rights</h3>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li>Deklutter owns all rights to the service, including software, algorithms, and branding</li>
              <li>Our trademarks, logos, and service marks are protected</li>
              <li>You may not use our intellectual property without written permission</li>
            </ul>

            <h3 className="text-xl font-semibold text-gray-800 mb-3">7.2 Your Rights</h3>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li>You retain all rights to your email data</li>
              <li>We do not claim ownership of your emails or content</li>
              <li>You grant us a limited license to process your data as described in our Privacy Policy</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">8. Disclaimers and Limitations of Liability</h2>
            
            <h3 className="text-xl font-semibold text-gray-800 mb-3">8.1 Service Disclaimer</h3>
            <p className="text-gray-700 mb-4">
              THE SERVICE IS PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO:
            </p>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li>Accuracy of email classification</li>
              <li>Uninterrupted or error-free operation</li>
              <li>Fitness for a particular purpose</li>
              <li>Non-infringement</li>
            </ul>

            <h3 className="text-xl font-semibold text-gray-800 mb-3">8.2 Limitation of Liability</h3>
            <p className="text-gray-700 mb-4">
              TO THE MAXIMUM EXTENT PERMITTED BY LAW, DEKLUTTER SHALL NOT BE LIABLE FOR:
            </p>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li>Loss of data, including deleted emails</li>
              <li>Loss of profits or business opportunities</li>
              <li>Indirect, incidental, or consequential damages</li>
              <li>Damages exceeding the amount you paid us in the past 12 months (if any)</li>
            </ul>

            <h3 className="text-xl font-semibold text-gray-800 mb-3">8.3 Classification Accuracy</h3>
            <p className="text-gray-700">
              While we strive for accuracy, our email classification is not perfect. We are not responsible for:
            </p>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li>False positives (important emails marked as spam)</li>
              <li>False negatives (spam not detected)</li>
              <li>Any consequences of classification errors</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">9. Indemnification</h2>
            <p className="text-gray-700">
              You agree to indemnify, defend, and hold harmless Deklutter and its officers, directors, employees, and agents from any claims, damages, losses, liabilities, and expenses (including legal fees) arising from:
            </p>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li>Your use of the service</li>
              <li>Your violation of these Terms</li>
              <li>Your violation of any third-party rights</li>
              <li>Any content you submit or delete through the service</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">10. Termination</h2>
            
            <h3 className="text-xl font-semibold text-gray-800 mb-3">10.1 By You</h3>
            <p className="text-gray-700 mb-4">
              You may terminate your account at any time by:
            </p>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li>Revoking Gmail access via Google Account settings</li>
              <li>Contacting us to delete your account</li>
            </ul>

            <h3 className="text-xl font-semibold text-gray-800 mb-3">10.2 By Us</h3>
            <p className="text-gray-700 mb-4">
              We may suspend or terminate your account if:
            </p>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li>You violate these Terms</li>
              <li>You engage in fraudulent or illegal activity</li>
              <li>You abuse or overload our systems</li>
              <li>Required by law or court order</li>
            </ul>

            <h3 className="text-xl font-semibold text-gray-800 mb-3">10.3 Effect of Termination</h3>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li>Your access to the service will be revoked</li>
              <li>Your data will be deleted within 30 days</li>
              <li>Provisions that should survive termination will remain in effect</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">11. Changes to Terms</h2>
            <p className="text-gray-700 mb-4">
              We may update these Terms from time to time. We will notify you of material changes by:
            </p>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li>Posting the updated Terms on our website</li>
              <li>Updating the "Last Updated" date</li>
              <li>Sending you an email notification (for significant changes)</li>
            </ul>
            <p className="text-gray-700">
              Your continued use of the service after changes constitutes acceptance of the updated Terms.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">12. Governing Law and Dispute Resolution</h2>
            
            <h3 className="text-xl font-semibold text-gray-800 mb-3">12.1 Governing Law</h3>
            <p className="text-gray-700 mb-4">
              These Terms are governed by the laws of [Your Jurisdiction], without regard to conflict of law principles.
            </p>

            <h3 className="text-xl font-semibold text-gray-800 mb-3">12.2 Dispute Resolution</h3>
            <p className="text-gray-700 mb-4">
              Any disputes arising from these Terms or the service shall be resolved through:
            </p>
            <ul className="list-disc pl-6 mb-4 text-gray-700">
              <li>Good faith negotiation</li>
              <li>Mediation (if negotiation fails)</li>
              <li>Binding arbitration (if mediation fails)</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">13. Miscellaneous</h2>
            
            <h3 className="text-xl font-semibold text-gray-800 mb-3">13.1 Entire Agreement</h3>
            <p className="text-gray-700 mb-4">
              These Terms, together with our Privacy Policy, constitute the entire agreement between you and Deklutter.
            </p>

            <h3 className="text-xl font-semibold text-gray-800 mb-3">13.2 Severability</h3>
            <p className="text-gray-700 mb-4">
              If any provision of these Terms is found to be invalid or unenforceable, the remaining provisions will remain in full force and effect.
            </p>

            <h3 className="text-xl font-semibold text-gray-800 mb-3">13.3 Waiver</h3>
            <p className="text-gray-700 mb-4">
              Our failure to enforce any right or provision of these Terms does not constitute a waiver of that right or provision.
            </p>

            <h3 className="text-xl font-semibold text-gray-800 mb-3">13.4 Assignment</h3>
            <p className="text-gray-700 mb-4">
              You may not assign or transfer these Terms without our written consent. We may assign these Terms without restriction.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">14. Contact Information</h2>
            <p className="text-gray-700 mb-4">
              For questions about these Terms, please contact us:
            </p>
            <div className="bg-gray-100 p-4 rounded-lg">
              <p className="text-gray-700"><strong>Email:</strong> <a href="mailto:legal@deklutter.co" className="text-blue-600 hover:underline">legal@deklutter.co</a></p>
              <p className="text-gray-700"><strong>Support:</strong> <a href="mailto:support@deklutter.co" className="text-blue-600 hover:underline">support@deklutter.co</a></p>
              <p className="text-gray-700"><strong>Website:</strong> <a href="https://app.deklutter.co" className="text-blue-600 hover:underline">https://app.deklutter.co</a></p>
            </div>
          </section>
        </div>

        <div className="mt-12 pt-8 border-t border-gray-200">
          <p className="text-center text-gray-600">
            <a href="/" className="text-blue-600 hover:underline">← Back to Home</a>
            {' | '}
            <a href="/privacy" className="text-blue-600 hover:underline">Privacy Policy</a>
          </p>
        </div>
      </div>
    </div>
  )
}
