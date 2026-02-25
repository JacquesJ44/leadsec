import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { jobcardAPI } from '../utils/api'
import useAuth from '../hooks/useAuth'
import './JobCardsList.css'

function JobCardsList() {
  const navigate = useNavigate()
  const auth = useAuth()
  const [jobcards, setJobcards] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(0)
  const [statusFilter, setStatusFilter] = useState('')

  useEffect(() => {
    fetchJobcards()
  }, [page, statusFilter])

  const fetchJobcards = async () => {
    setLoading(true)
    setError('')
    try {
      const params = {
        page,
        per_page: 10
      }
      if (statusFilter) {
        params.status = statusFilter
      }
      const response = await jobcardAPI.getAllJobcards(params)
      setJobcards(response.data.jobcards)
      setTotalPages(response.data.pages)
    } catch (err) {
      setError(err.response?.data?.error || 'Error fetching jobcards')
    } finally {
      setLoading(false)
    }
  }

  const handleStatusChange = (e) => {
    setStatusFilter(e.target.value)
    setPage(1)
  }

  const handleCreateNew = () => {
    navigate('/')
  }

  const handleViewJobcard = (id) => {
    navigate(`/jobcard/${id}`)
  }

  const handleLogout = async () => {
    try {
      await auth.logout()
      navigate('/login')
    } catch (err) {
      console.error('Logout error:', err)
    }
  }

  const getStatusBadge = (status) => {
    const statusClasses = {
      'pending': 'badge-warning',
      'approved': 'badge-success',
      'completed': 'badge-info'
    }
    return statusClasses[status] || 'badge-gray'
  }

  return (
    <div className="jobcards-list-container">
      <div className="list-header">
        <div>
          <h1>JobCards</h1>
          <p>Manage and view all submitted jobcards</p>
        </div>
        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          {auth.user && (
            <span style={{ color: 'white', fontSize: '14px' }}>
              Signed in as: <strong>{auth.user.username}</strong>
            </span>
          )}
          <button 
            className="btn btn-primary"
            onClick={handleCreateNew}
          >
            + Create New JobCard
          </button>
          <button 
            className="btn btn-secondary"
            onClick={handleLogout}
          >
            Sign Out
          </button>
        </div>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      <div className="filters">
        <div className="filter-group">
          <label htmlFor="status-filter">Filter by Status:</label>
          <select 
            id="status-filter"
            value={statusFilter}
            onChange={handleStatusChange}
            className="select select-bordered"
          >
            <option value="">All Statuses</option>
            <option value="pending">Pending</option>
            <option value="approved">Approved</option>
            <option value="completed">Completed</option>
          </select>
        </div>
      </div>

      {loading ? (
        <div className="loading">Loading jobcards...</div>
      ) : jobcards.length === 0 ? (
        <div className="empty-state">
          <p>No jobcards found</p>
          <button 
            className="btn btn-primary"
            onClick={handleCreateNew}
          >
            Create the first one
          </button>
        </div>
      ) : (
        <>
          <div className="table-container">
            <table className="jobcards-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Job Title</th>
                  <th>Client Name</th>
                  <th>Service Date</th>
                  <th>Status</th>
                  <th>Images</th>
                  <th>Created</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {jobcards.map(jobcard => (
                  <tr key={jobcard.id}>
                    <td>#{jobcard.id}</td>
                    <td>
                      <strong>{jobcard.job_title}</strong>
                    </td>
                    <td>{jobcard.client_name}</td>
                    <td>{new Date(jobcard.service_date).toLocaleDateString()}</td>
                    <td>
                      <span className={`badge ${getStatusBadge(jobcard.status)}`}>
                        {jobcard.status}
                      </span>
                    </td>
                    <td>
                      <span className="badge badge-sm">
                        {jobcard.images?.length || 0} images
                      </span>
                    </td>
                    <td>
                      {new Date(jobcard.created_at).toLocaleDateString()}
                    </td>
                    <td>
                      <button 
                        className="btn btn-sm btn-ghost"
                        onClick={() => handleViewJobcard(jobcard.id)}
                      >
                        View
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="pagination">
            <button 
              className="btn btn-sm"
              disabled={page === 1}
              onClick={() => setPage(page - 1)}
            >
              ← Previous
            </button>
            <span>Page {page} of {totalPages}</span>
            <button 
              className="btn btn-sm"
              disabled={page === totalPages}
              onClick={() => setPage(page + 1)}
            >
              Next →
            </button>
          </div>
        </>
      )}
    </div>
  )
}

export default JobCardsList
