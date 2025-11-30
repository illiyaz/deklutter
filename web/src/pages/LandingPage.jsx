import { Mail, Trash2, Sparkles, Shield, Zap, Check } from 'lucide-react'

const API_URL = import.meta.env.VITE_API_URL || 'https://api.deklutter.co'

export default function LandingPage() {
  const handleGetStarted = async () => {
    try {
      const response = await fetch(`${API_URL}/oauth/google/init?source=web`, {
        method: 'POST'
      })
      const data = await response.json()
      window.location.href = data.auth_url
    } catch (error) {
      console.error('Failed to initiate OAuth:', error)
      alert('Failed to connect. Please try again.')
    }
  }

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <nav className="flex justify-between items-center mb-16">
          <div className="flex items-center space-x-2">
            <Mail className="w-8 h-8 text-blue-600" />
            <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Deklutter
            </span>
          </div>
          <div className="flex space-x-4">
            <a href="#features" className="text-gray-600 hover:text-blue-600 transition">Features</a>
            <a href="#how-it-works" className="text-gray-600 hover:text-blue-600 transition">How It Works</a>
            <a href={`${API_URL}/docs`} target="_blank" rel="noopener noreferrer" className="text-gray-600 hover:text-blue-600 transition">API Docs</a>
          </div>
        </nav>

        {/* Hero */}
        <div className="text-center max-w-4xl mx-auto mb-20">
          <div className="inline-flex items-center space-x-2 bg-blue-100 text-blue-700 px-4 py-2 rounded-full mb-6">
            <Sparkles className="w-4 h-4" />
            <span className="text-sm font-semibold">AI-Powered Email Cleaning</span>
          </div>
          
          <h1 className="text-6xl font-bold mb-6 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
            Clean Your Gmail Inbox in Minutes
          </h1>
          
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Automatically identify and remove spam, newsletters, and promotional emails. 
            Free up storage space and declutter your inbox with AI.
          </p>
          
          <div className="flex justify-center space-x-4">
            <button onClick={handleGetStarted} className="btn-primary flex items-center space-x-2">
              <Mail className="w-5 h-5" />
              <span>Connect Gmail</span>
            </button>
            <a href="#how-it-works" className="btn-secondary">
              Learn More
            </a>
          </div>
          
          <p className="text-sm text-gray-500 mt-4">
            ✓ Free to use  ✓ No credit card required  ✓ Privacy-first
          </p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto mb-20">
          <div className="card text-center">
            <div className="text-4xl font-bold text-blue-600 mb-2">10K+</div>
            <div className="text-gray-600">Emails Cleaned</div>
          </div>
          <div className="card text-center">
            <div className="text-4xl font-bold text-purple-600 mb-2">2GB</div>
            <div className="text-gray-600">Space Freed</div>
          </div>
          <div className="card text-center">
            <div className="text-4xl font-bold text-pink-600 mb-2">95%</div>
            <div className="text-gray-600">Accuracy Rate</div>
          </div>
        </div>

        {/* Features */}
        <div id="features" className="mb-20">
          <h2 className="text-4xl font-bold text-center mb-12">Why Choose Deklutter?</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="card">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <Sparkles className="w-6 h-6 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">AI-Powered</h3>
              <p className="text-gray-600">
                Smart classification using advanced AI to identify spam, newsletters, and promotional emails with 95% accuracy.
              </p>
            </div>

            <div className="card">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                <Shield className="w-6 h-6 text-purple-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Privacy-First</h3>
              <p className="text-gray-600">
                We never store email content or subjects. Only metadata is used for classification. Your privacy is our priority.
              </p>
            </div>

            <div className="card">
              <div className="w-12 h-12 bg-pink-100 rounded-lg flex items-center justify-center mb-4">
                <Zap className="w-6 h-6 text-pink-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Lightning Fast</h3>
              <p className="text-gray-600">
                Scan hundreds of emails in seconds. Clean your inbox in minutes, not hours. Get instant results.
              </p>
            </div>
          </div>
        </div>

        {/* How It Works */}
        <div id="how-it-works" className="mb-20">
          <h2 className="text-4xl font-bold text-center mb-12">How It Works</h2>
          
          <div className="max-w-3xl mx-auto space-y-8">
            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0 w-10 h-10 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
                1
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-2">Connect Your Gmail</h3>
                <p className="text-gray-600">
                  Click "Connect Gmail" and authorize Deklutter to access your inbox. We only request minimal permissions needed for cleaning.
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0 w-10 h-10 bg-purple-600 text-white rounded-full flex items-center justify-center font-bold">
                2
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-2">AI Scans Your Inbox</h3>
                <p className="text-gray-600">
                  Our AI analyzes your emails and classifies them into three categories: Delete (spam), Review (uncertain), and Keep (important).
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0 w-10 h-10 bg-pink-600 text-white rounded-full flex items-center justify-center font-bold">
                3
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-2">Review & Clean</h3>
                <p className="text-gray-600">
                  Review the results, see sample emails, and click "Clean" to move unwanted emails to trash. You can recover them for 30 days.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* CTA */}
        <div className="card max-w-3xl mx-auto text-center bg-gradient-to-r from-blue-600 to-purple-600 text-white">
          <h2 className="text-3xl font-bold mb-4">Ready to Declutter?</h2>
          <p className="text-lg mb-6 opacity-90">
            Join thousands of users who have already cleaned their inboxes
          </p>
          <button onClick={handleGetStarted} className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-all duration-200 shadow-lg">
            Get Started Free
          </button>
        </div>

        {/* Footer */}
        <footer className="mt-20 pt-8 border-t border-gray-200 text-center text-gray-600">
          <div className="flex justify-center space-x-6 mb-4">
            <a href="/privacy" className="hover:text-blue-600 transition">Privacy Policy</a>
            <a href="/terms" className="hover:text-blue-600 transition">Terms of Service</a>
            <a href="mailto:support@deklutter.co" className="hover:text-blue-600 transition">Contact</a>
            <a href="https://github.com/illiyaz/deklutter" target="_blank" rel="noopener noreferrer" className="hover:text-blue-600 transition">GitHub</a>
          </div>
          <p className="text-sm">© 2025 Deklutter. All rights reserved.</p>
        </footer>
      </div>
    </div>
  )
}
