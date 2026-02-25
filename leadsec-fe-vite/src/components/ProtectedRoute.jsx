import React, { useContext } from 'react'
import { Navigate } from 'react-router-dom'
import { AuthContext } from '../contexts/AuthContext'

/**
 * ProtectedRoute component that requires authentication
 * If user is not authenticated, redirects to login
 */
function ProtectedRoute({ children }) {
  const auth = useContext(AuthContext)

  // Loading state - show nothing while checking authentication
  if (auth.loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-white">Loading...</div>
      </div>
    )
  }

  // Not authenticated - redirect to login
  if (!auth.isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  // Authenticated - render the component
  return children
}

export default ProtectedRoute
