import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import useAuth from '../hooks/useAuth'
import { jobcardAPI } from '../utils/api'
import './JobCardDetail.css'

function JobCardDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const auth = useAuth()
  const [jobcard, setJobcard] = useState(null)
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState(false)
  const [error, setError] = useState('')
  const [successMessage, setSuccessMessage] = useState('')
  const [updatedData, setUpdatedData] = useState({})
  const [uploadedImages, setUploadedImages] = useState([])
  const [selectedFiles, setSelectedFiles] = useState([])

  useEffect(() => {
    fetchJobcard()
  }, [id])

  const fetchJobcard = async () => {
    setLoading(true)
    setError('')
    try {
      const response = await jobcardAPI.getJobcard(id)
      setJobcard(response.data)
      setUpdatedData(response.data)
      setUploadedImages(response.data.images || [])
    } catch (err) {
      setError(err.response?.data?.error || 'Error fetching jobcard')
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setUpdatedData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleStatusChange = (e) => {
    setUpdatedData(prev => ({
      ...prev,
      status: e.target.value
    }))
  }

  const handleSaveChanges = async () => {
    try {
      setError('')
      const updatePayload = {
        job_title: updatedData.job_title,
        job_description: updatedData.job_description,
        status: updatedData.status,
        notes: updatedData.notes,
        labor_hours: updatedData.labor_hours ? parseFloat(updatedData.labor_hours) : null,
        cost_estimate: updatedData.cost_estimate ? parseFloat(updatedData.cost_estimate) : null
      }

      await jobcardAPI.updateJobcard(id, updatePayload)
      setJobcard(updatedData)
      setEditing(false)
      setSuccessMessage('Jobcard updated successfully!')
      setTimeout(() => setSuccessMessage(''), 3000)
    } catch (err) {
      setError(err.response?.data?.error || 'Error updating jobcard')
    }
  }

  const handleCancel = () => {
    setUpdatedData(jobcard)
    setEditing(false)
  }

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files)
    const validFiles = files.filter(file => file.type.startsWith('image/'))
    setSelectedFiles(prev => [...prev, ...validFiles])
  }

  const removeSelectedFile = (index) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index))
  }

  const handleUploadImages = async () => {
    if (selectedFiles.length === 0) return

    try {
      setError('')
      const formData = new FormData()
      selectedFiles.forEach(file => {
        formData.append('files', file)
      })

      const response = await jobcardAPI.uploadImages(id, formData)
      setUploadedImages(response.data.images)
      setSelectedFiles([])
      setSuccessMessage('Images uploaded successfully!')
      setTimeout(() => setSuccessMessage(''), 3000)
    } catch (err) {
      setError(`Error uploading images: ${err.response?.data?.error || err.message}`)
    }
  }

  const handleDeleteImage = async (imageId) => {
    if (!window.confirm('Are you sure you want to delete this image?')) return

    try {
      setError('')
      await jobcardAPI.deleteImage(imageId)
      setUploadedImages(prev => prev.filter(img => img.id !== imageId))
      setSuccessMessage('Image deleted successfully!')
      setTimeout(() => setSuccessMessage(''), 3000)
    } catch (err) {
      setError(err.response?.data?.error || 'Error deleting image')
    }
  }

  const handleToggleSendToClient = async (image) => {
    try {
      setError('')
      await jobcardAPI.updateImage(image.id, { send_to_client: !image.send_to_client })
      setUploadedImages(prev =>
        prev.map(img =>
          img.id === image.id ? { ...img, send_to_client: !img.send_to_client } : img
        )
      )
    } catch (err) {
      setError(err.response?.data?.error || 'Error updating image preference')
    }
  }

  const handleDownloadPDF = async () => {
    try {
      const response = await jobcardAPI.downloadPDF(id)
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `jobcard_${id}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.parentNode.removeChild(link)
    } catch (err) {
      setError('Error downloading PDF')
    }
  }

  const handleSendToClient = async () => {
    try {
      setError('')
      setLoading(true)
      await jobcardAPI.sendToClient(id)
      setSuccessMessage(`Jobcard sent to ${jobcard.client_email}!`)
      setTimeout(() => setSuccessMessage(''), 3000)
    } catch (err) {
      setError(err.response?.data?.error || 'Error sending jobcard to client')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="loading-container">Loading jobcard...</div>
  }

  if (!jobcard) {
    return (
      <div className="error-container">
        <p>Jobcard not found</p>
        <button className="btn btn-primary" onClick={() => navigate('/jobcards')}>
          Back to List
        </button>
      </div>
    )
  }

  const handleLogout = async () => {
    try {
      await auth.logout()
      navigate('/login')
    } catch (err) {
      console.error('Logout error:', err)
    }
  }

  return (
    <div className="jobcard-detail-container">
      <div className="detail-header">
        <div>
          <h1>JobCard #{jobcard.id}</h1>
          <p className="subtitle">{jobcard.job_title}</p>
        </div>
        <div className="header-actions">
          {auth.user && (
            <span style={{ color: '#6b7280', fontSize: '13px' }}>
              Signed in as: <strong>{auth.user.username}</strong>
            </span>
          )}
          <div>
            <button className="btn btn-secondary" onClick={() => navigate('/jobcards')}>
              ← Back to List
            </button>
            <button className="btn btn-secondary" onClick={handleLogout}>
              Sign Out
            </button>
          </div>
          <div>
            <button className="btn btn-info" onClick={handleDownloadPDF}>
              📥 Download PDF
            </button>
            <button className="btn btn-success" onClick={handleSendToClient}>
              ✉️ Send to Client
            </button>
            {!editing && (
              <button className="btn btn-primary" onClick={() => setEditing(true)}>
                ✏️ Edit
              </button>
            )}
          </div>
        </div>
      </div>

      <div className="detail-content">
        {/* Job Information */}
        <section className="detail-section">
          <h2>Job Information</h2>
          <div className="info-grid">
            <div className="info-item">
              <label>Job Title</label>
              {editing ? (
                <input
                  type="text"
                  name="job_title"
                  value={updatedData.job_title}
                  onChange={handleInputChange}
                  className="input input-bordered"
                />
              ) : (
                <p>{jobcard.job_title}</p>
              )}
            </div>

            <div className="info-item">
              <label>Status</label>
              {editing ? (
                <select
                  value={updatedData.status}
                  onChange={handleStatusChange}
                  className="select select-bordered"
                >
                  <option value="pending">Pending</option>
                  <option value="approved">Approved</option>
                  <option value="completed">Completed</option>
                </select>
              ) : (
                <span className={`badge badge-${jobcard.status}`}>{jobcard.status}</span>
              )}
            </div>

            <div className="info-item full-width">
              <label>Job Description</label>
              {editing ? (
                <textarea
                  name="job_description"
                  value={updatedData.job_description || ''}
                  onChange={handleInputChange}
                  className="textarea textarea-bordered"
                  rows="3"
                />
              ) : (
                <p>{jobcard.job_description || 'N/A'}</p>
              )}
            </div>

            <div className="info-item">
              <label>Service Date</label>
              <p>{new Date(jobcard.service_date).toLocaleDateString()}</p>
            </div>

            <div className="info-item">
              <label>Labor Hours</label>
              {editing ? (
                <input
                  type="number"
                  name="labor_hours"
                  value={updatedData.labor_hours || ''}
                  onChange={handleInputChange}
                  className="input input-bordered"
                  step="0.5"
                />
              ) : (
                <p>{jobcard.labor_hours || 'N/A'}</p>
              )}
            </div>

            <div className="info-item">
              <label>Cost Estimate</label>
              {editing ? (
                <input
                  type="number"
                  name="cost_estimate"
                  value={updatedData.cost_estimate || ''}
                  onChange={handleInputChange}
                  className="input input-bordered"
                  step="0.01"
                />
              ) : (
                <p>${jobcard.cost_estimate || 'N/A'}</p>
              )}
            </div>
          </div>

          <div className="info-item full-width">
            <label>Notes</label>
            {editing ? (
              <textarea
                name="notes"
                value={updatedData.notes || ''}
                onChange={handleInputChange}
                className="textarea textarea-bordered"
                rows="3"
              />
            ) : (
              <p>{jobcard.notes || 'No notes'}</p>
            )}
          </div>
        </section>

        {/* Client Information */}
        <section className="detail-section">
          <h2>Client Information</h2>
          <div className="info-grid">
            <div className="info-item">
              <label>Client Name</label>
              <p>{jobcard.client_name}</p>
            </div>

            <div className="info-item">
              <label>Client Email</label>
              <p>{jobcard.client_email}</p>
            </div>

            <div className="info-item">
              <label>Client Phone</label>
              <p>{jobcard.client_phone || 'N/A'}</p>
            </div>

            <div className="info-item full-width">
              <label>Service Location</label>
              <p>{jobcard.service_location}</p>
            </div>
          </div>
        </section>

        {/* Service Details */}
        <section className="detail-section">
          <h2>Service Details</h2>
          <div className="info-grid">
            <div className="info-item">
              <label>Technician Name</label>
              <p>{jobcard.technician_name}</p>
            </div>

            <div className="info-item">
              <label>Materials Used</label>
              <p>{jobcard.materials_used || 'N/A'}</p>
            </div>
          </div>
        </section>

        {/* Images Section */}
        <section className="detail-section">
          <h2>Invoice & Reference Images</h2>

          {uploadedImages.length > 0 && (
            <div className="images-section">
              <h3>Uploaded Images ({uploadedImages.length})</h3>
              <div className="image-grid">
                {uploadedImages.map(image => (
                  <div key={image.id} className="image-item">
                    <img src={`data:image/png;base64,${image.image_data}`} alt={image.filename} />
                    <p className="image-filename">{image.filename}</p>
                    <div className="image-checkbox">
                      <label>
                        <input
                          type="checkbox"
                          checked={image.send_to_client}
                          onChange={() => handleToggleSendToClient(image)}
                        />
                        <span>Send to client</span>
                      </label>
                    </div>
                    <button
                      className="btn btn-sm btn-error"
                      onClick={() => handleDeleteImage(image.id)}
                    >
                      Delete
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="upload-section">
            <h3>Add New Images</h3>
            <div className="form-group">
              <input
                type="file"
                multiple
                accept="image/*"
                onChange={handleFileSelect}
                className="file-input file-input-bordered"
              />
            </div>

            {selectedFiles.length > 0 && (
              <div className="selected-files">
                <h4>Files to Upload ({selectedFiles.length})</h4>
                <div className="file-list">
                  {selectedFiles.map((file, index) => (
                    <div key={index} className="file-item">
                      <span>{file.name}</span>
                      <button
                        type="button"
                        className="btn btn-sm btn-ghost"
                        onClick={() => removeSelectedFile(index)}
                      >
                        ✕
                      </button>
                    </div>
                  ))}
                </div>
                <button
                  className="btn btn-primary"
                  onClick={handleUploadImages}
                >
                  Upload {selectedFiles.length} Image(s)
                </button>
              </div>
            )}
          </div>
        </section>
        
        {error && <div className="alert alert-error">{error}</div>}
        {successMessage && <div className="alert alert-success">{successMessage}</div>}

        {/* Action Buttons */}
        {editing && (
          <div className="action-buttons">
            <button className="btn btn-ghost" onClick={handleCancel}>
              Cancel
            </button>
            <button className="btn btn-primary" onClick={handleSaveChanges}>
              Save Changes
            </button>
          </div>
        )}
      </div>

      {/* Metadata */}
      <div className="metadata">
        <p>Created: {new Date(jobcard.created_at).toLocaleString()}</p>
        <p>Last Updated: {new Date(jobcard.updated_at).toLocaleString()}</p>
      </div>
    </div>
  )
}

export default JobCardDetail
