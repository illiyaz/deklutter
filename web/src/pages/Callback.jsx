import { useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { Loader2 } from 'lucide-react'

export default function Callback() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()

  useEffect(() => {
    const token = searchParams.get('token')
    
    if (token) {
      // Store token in localStorage
      localStorage.setItem('deklutter_token', token)
      
      // Redirect to dashboard
      navigate('/dashboard')
    } else {
      // No token, redirect to home
      navigate('/')
    }
  }, [searchParams, navigate])

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <Loader2 className="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
        <p className="text-gray-600">Connecting your Gmail...</p>
      </div>
    </div>
  )
}
