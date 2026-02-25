import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import JobCardForm from './components/JobCardForm'
import JobCardsList from './components/JobCardsList'
import JobCardDetail from './components/JobCardDetail'
import Login from './components/Login'
import ProtectedRoute from './components/ProtectedRoute'
import './App.css'

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="app-container min-h-screen bg-gradient-to-br from-blue-600 to-purple-700 p-4 md:p-10">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/" element={<ProtectedRoute><JobCardForm /></ProtectedRoute>} />
            <Route path="/jobcards" element={<ProtectedRoute><JobCardsList /></ProtectedRoute>} />
            <Route path="/jobcard/:id" element={<ProtectedRoute><JobCardDetail /></ProtectedRoute>} />
            <Route path="*" element={<Navigate to="/jobcards" replace />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  )
}

export default App
