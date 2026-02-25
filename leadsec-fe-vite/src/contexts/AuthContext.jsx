import React, { createContext, useState, useEffect, useCallback } from 'react'
import { authAPI } from '../utils/api'

export const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Check if user is already logged in on app load
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await authAPI.me()
        if (response.data.user) {
          setUser(response.data.user)
        }
      } catch (err) {
        console.error('Auth check failed:', err)
        setUser(null)
      } finally {
        setLoading(false)
      }
    }

    checkAuth()
  }, [])

  const login = useCallback(async (username, password) => {
    try {
      setError(null)
      const response = await authAPI.login({ username, password })
      setUser(response.data.user)
      return response.data
    } catch (err) {
      const errorMessage = err.response?.data?.error || 'Login failed'
      setError(errorMessage)
      throw err
    }
  }, [])

  const logout = useCallback(async () => {
    try {
      await authAPI.logout()
      setUser(null)
      setError(null)
    } catch (err) {
      console.error('Logout failed:', err)
      // Still clear user on client side even if logout request fails
      setUser(null)
    }
  }, [])

  const value = {
    user,
    loading,
    error,
    login,
    logout,
    isAuthenticated: !!user
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}
