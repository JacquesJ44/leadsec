import React, { useState } from 'react'
import { useNavigate, Navigate } from 'react-router-dom'
import useAuth from '../hooks/useAuth'
import './JobCardForm.css'

function Login() {
  const navigate = useNavigate()
  const auth = useAuth()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  // If already authenticated, redirect to jobcards
  if (auth.isAuthenticated) {
    return <Navigate to="/jobcards" replace />
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await auth.login(username, password)
      navigate('/jobcards')
    } catch (err) {
      setError(err.response?.data?.error || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="jobcard-form-container">
      <div className="form-header">
        <div>
          <h1>Sign in</h1>
          <p>Please sign in to continue</p>
        </div>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      <form onSubmit={handleSubmit} className="jobcard-form">
        <div className="form-group">
          <label>Username</label>
          <input value={username} onChange={e => setUsername(e.target.value)} required />
        </div>

        <div className="form-group">
          <label>Password</label>
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} required />
        </div>

        <div className="form-actions">
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Signing in...' : 'Sign in'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default Login
