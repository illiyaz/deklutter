import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Mail, Trash2, AlertCircle, Check, Loader2, LogOut, RefreshCw } from 'lucide-react'

const API_URL = import.meta.env.VITE_API_URL || 'https://api.deklutter.co'

export default function Dashboard() {
  const navigate = useNavigate()
  const [token, setToken] = useState(null)
  const [loading, setLoading] = useState(false)
  const [scanning, setScanning] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)
  const [daysBack, setDaysBack] = useState(30)

  useEffect(() => {
    const storedToken = localStorage.getItem('deklutter_token')
    if (!storedToken) {
      navigate('/')
    } else {
      setToken(storedToken)
    }
  }, [navigate])

  const handleScan = async () => {
    setScanning(true)
    setError(null)
    
    try {
      const response = await fetch(`${API_URL}/gmail/scan`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          days_back: daysBack,
          limit: 100
        })
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.message || 'Scan failed')
      }

      const data = await response.json()
      setResults(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setScanning(false)
    }
  }

  const handleCleanup = async () => {
    if (!results?.safe_to_delete || results.safe_to_delete.length === 0) {
      alert('No emails to delete')
      return
    }

    if (!confirm(`Are you sure you want to move ${results.safe_to_delete.length} emails to trash? You can recover them for 30 days.`)) {
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`${API_URL}/gmail/apply`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message_ids: results.safe_to_delete,
          mode: 'trash'
        })
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.message || 'Cleanup failed')
      }

      alert('✅ Cleanup complete! Emails moved to trash.')
      setResults(null) // Clear results after cleanup
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('deklutter_token')
    navigate('/')
  }

  if (!token) {
    return null
  }

  return (
    <div className="min-h-screen">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div className="flex items-center space-x-2">
            <Mail className="w-8 h-8 text-blue-600" />
            <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Deklutter
            </span>
          </div>
          <button onClick={handleLogout} className="flex items-center space-x-2 text-gray-600 hover:text-red-600 transition">
            <LogOut className="w-5 h-5" />
            <span>Logout</span>
          </button>
        </div>

        {/* Scan Section */}
        <div className="card max-w-2xl mx-auto mb-8">
          <h2 className="text-2xl font-bold mb-4">Scan Your Inbox</h2>
          <p className="text-gray-600 mb-6">
            Choose how many days back to scan. We'll analyze your emails and categorize them.
          </p>

          <div className="flex items-center space-x-4 mb-6">
            <label className="text-gray-700 font-medium">Scan last:</label>
            <select 
              value={daysBack} 
              onChange={(e) => setDaysBack(Number(e.target.value))}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value={7}>7 days</option>
              <option value={30}>30 days</option>
              <option value={90}>90 days</option>
              <option value={180}>6 months</option>
              <option value={365}>1 year</option>
            </select>
          </div>

          <button 
            onClick={handleScan} 
            disabled={scanning}
            className="btn-primary w-full flex items-center justify-center space-x-2"
          >
            {scanning ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Scanning...</span>
              </>
            ) : (
              <>
                <RefreshCw className="w-5 h-5" />
                <span>Scan Inbox</span>
              </>
            )}
          </button>
        </div>

        {/* Error */}
        {error && (
          <div className="card max-w-2xl mx-auto mb-8 bg-red-50 border-2 border-red-200">
            <div className="flex items-start space-x-3">
              <AlertCircle className="w-6 h-6 text-red-600 flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="font-semibold text-red-900 mb-1">Error</h3>
                <p className="text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Results */}
        {results && (
          <div className="max-w-4xl mx-auto space-y-6">
            {/* Summary */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="card bg-red-50 border-2 border-red-200">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-gray-700 font-medium">Delete</span>
                  <Trash2 className="w-5 h-5 text-red-600" />
                </div>
                <div className="text-3xl font-bold text-red-600">{results.summary.counts.delete}</div>
                <div className="text-sm text-gray-600 mt-1">
                  {results.summary.approx_size_mb?.toFixed(2)} MB
                </div>
              </div>

              <div className="card bg-yellow-50 border-2 border-yellow-200">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-gray-700 font-medium">Review</span>
                  <AlertCircle className="w-5 h-5 text-yellow-600" />
                </div>
                <div className="text-3xl font-bold text-yellow-600">{results.summary.counts.review}</div>
                <div className="text-sm text-gray-600 mt-1">Needs review</div>
              </div>

              <div className="card bg-green-50 border-2 border-green-200">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-gray-700 font-medium">Keep</span>
                  <Check className="w-5 h-5 text-green-600" />
                </div>
                <div className="text-3xl font-bold text-green-600">{results.summary.counts.keep}</div>
                <div className="text-sm text-gray-600 mt-1">Important</div>
              </div>
            </div>

            {/* Sample Emails */}
            {results.samples && (
              <div className="space-y-6">
                {/* Delete Samples */}
                {results.samples.delete && results.samples.delete.length > 0 && (
                  <div className="card">
                    <h3 className="text-xl font-bold mb-4 flex items-center space-x-2">
                      <Trash2 className="w-5 h-5 text-red-600" />
                      <span>Emails to Delete</span>
                    </h3>
                    <div className="space-y-3">
                      {results.samples.delete.slice(0, 5).map((email, idx) => (
                        <div key={idx} className="p-3 bg-red-50 rounded-lg border border-red-200">
                          <div className="font-medium text-gray-900">{email.subject}</div>
                          <div className="text-sm text-gray-600 mt-1">From: {email.from}</div>
                          <div className="text-xs text-gray-500 mt-1">{email.date} • {email.size_kb} KB</div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Review Samples */}
                {results.samples.review && results.samples.review.length > 0 && (
                  <div className="card">
                    <h3 className="text-xl font-bold mb-4 flex items-center space-x-2">
                      <AlertCircle className="w-5 h-5 text-yellow-600" />
                      <span>Emails to Review</span>
                    </h3>
                    <div className="space-y-3">
                      {results.samples.review.slice(0, 5).map((email, idx) => (
                        <div key={idx} className="p-3 bg-yellow-50 rounded-lg border border-yellow-200">
                          <div className="font-medium text-gray-900">{email.subject}</div>
                          <div className="text-sm text-gray-600 mt-1">From: {email.from}</div>
                          <div className="text-xs text-gray-500 mt-1">{email.date} • {email.size_kb} KB</div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Action Button */}
            {results.safe_to_delete && results.safe_to_delete.length > 0 && (
              <div className="card bg-gradient-to-r from-red-600 to-pink-600 text-white">
                <h3 className="text-2xl font-bold mb-2">Ready to Clean?</h3>
                <p className="mb-4 opacity-90">
                  Move {results.safe_to_delete.length} emails to trash and free up {results.summary.approx_size_mb?.toFixed(2)} MB
                </p>
                <button 
                  onClick={handleCleanup}
                  disabled={loading}
                  className="bg-white text-red-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-all duration-200 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
                >
                  {loading ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      <span>Cleaning...</span>
                    </>
                  ) : (
                    <>
                      <Trash2 className="w-5 h-5" />
                      <span>Clean Inbox</span>
                    </>
                  )}
                </button>
                <p className="text-sm mt-3 opacity-75">
                  ✓ Emails will be moved to trash (recoverable for 30 days)
                </p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
