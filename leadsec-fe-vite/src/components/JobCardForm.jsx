import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import SignaturePad from './SignaturePad'
import useAuth from '../hooks/useAuth'
import { jobcardAPI } from '../utils/api'
import './JobCardForm.css'

function JobCardForm() {
  const navigate = useNavigate()
  const auth = useAuth()
  const [formData, setFormData] = useState({
    job_title: '',
    job_description: '',
    client_name: '',
    client_email: '',
    client_phone: '',
    service_location: '',
    technician_name: '',
    service_date: '',
    labor_hours: '',
    materials_used: '',
    cost_estimate: '',
    notes: ''
  })

  const [signature, setSignature] = useState(null)
  const [loading, setLoading] = useState(false)
  const [successMessage, setSuccessMessage] = useState('')
  const [errorMessage, setErrorMessage] = useState('')
  const [selectedFiles, setSelectedFiles] = useState([])
  const [uploadedImages, setUploadedImages] = useState([])
  const [jobcardId, setJobcardId] = useState(null)

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSignatureCapture = (signatureData) => {
    setSignature(signatureData)
  }

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files)
    const validFiles = files.filter(file => file.type.startsWith('image/'))
    
    if (files.length !== validFiles.length) {
      setErrorMessage('Some files are not images. Only image files are allowed.')
    }
    
    setSelectedFiles(prev => [...prev, ...validFiles])
  }

  const removeSelectedFile = (index) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index))
  }

  const removeUploadedImage = (imageId) => {
    setUploadedImages(prev => prev.filter(img => img.id !== imageId))
  }

  const toggleImageSendToClient = (imageId) => {
    setUploadedImages(prev => 
      prev.map(img => 
        img.id === imageId ? { ...img, send_to_client: !img.send_to_client } : img
      )
    )
  }

  const uploadImages = async (jcardId) => {
    if (selectedFiles.length === 0) return true

    try {
      setLoading(true)
      const formDataToSend = new FormData()
      selectedFiles.forEach(file => {
        formDataToSend.append('files', file)
      })

      const response = await jobcardAPI.uploadImages(jcardId, formDataToSend)
      setUploadedImages(response.data.images)
      setSelectedFiles([])
      setSuccessMessage(`${response.data.images.length} image(s) uploaded successfully`)
      return true
    } catch (error) {
      console.error('Error uploading images:', error.response?.data || error.message)
      setErrorMessage(`Error uploading images: ${error.response?.data?.error || error.message}`)
      return false
    } finally {
      setLoading(false)
    }
  }

  const saveImagePreferences = async () => {
    const updates = uploadedImages.filter(img => img.send_to_client)
    
    try {
      for (const image of uploadedImages) {
        await jobcardAPI.updateImage(image.id, { send_to_client: image.send_to_client })
      }
      setSuccessMessage('Image preferences saved!')
      return true
    } catch (error) {
      console.error('Error saving image preferences:', error)
      setErrorMessage('Error saving image preferences.')
      return false
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setErrorMessage('')
    setSuccessMessage('')

    // Validate required fields
    if (!formData.job_title || !formData.client_name || !formData.client_email || 
        !formData.service_location || !formData.technician_name || !formData.service_date) {
      setErrorMessage('Please fill in all required fields')
      return
    }

    if (!signature) {
      setErrorMessage('Client signature is required')
      return
    }

    setLoading(true)

    try {
      const submitData = {
        ...formData,
        client_signature: signature,
        labor_hours: formData.labor_hours ? parseFloat(formData.labor_hours) : null,
        cost_estimate: formData.cost_estimate ? parseFloat(formData.cost_estimate) : null
      }

      const response = await jobcardAPI.createJobcard(submitData)
      const newJobcardId = response.data.jobcard.id
      setJobcardId(newJobcardId)
      
      // Upload images if any are selected
      if (selectedFiles.length > 0) {
        await uploadImages(newJobcardId)
      }
      
      setSuccessMessage(`JobCard #${newJobcardId} submitted successfully!`)
      
      // Reset form
      setFormData({
        job_title: '',
        job_description: '',
        client_name: '',
        client_email: '',
        client_phone: '',
        service_location: '',
        technician_name: '',
        service_date: '',
        labor_hours: '',
        materials_used: '',
        cost_estimate: '',
        notes: ''
      })
      setSignature(null)
      setSelectedFiles([])
      setUploadedImages([])

      // Navigate to jobcard detail after 2 seconds
      setTimeout(() => {
        navigate(`/jobcard/${newJobcardId}`)
      }, 2000)
    } catch (error) {
      console.error('Error submitting jobcard:', error)
      setErrorMessage(error.response?.data?.error || 'Error submitting jobcard. Please try again.')
    } finally {
      setLoading(false)
    }
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
    <div className="jobcard-form-container">
      <div className="form-header">
        <div>
          <h1>JobCard Form</h1>
          <p>Complete this form on-site and have it signed by the client</p>
        </div>
        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          {auth.user && (
            <span style={{ color: 'white', fontSize: '14px' }}>
              Signed in as: <strong>{auth.user.username}</strong>
            </span>
          )}
          <button 
            type="button"
            className="btn btn-secondary"
            onClick={() => navigate('/jobcards')}
          >
            📋 View All JobCards
          </button>
          <button 
            type="button"
            className="btn btn-secondary"
            onClick={handleLogout}
          >
            Sign Out
          </button>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="jobcard-form">
        {/* Job Information Section */}
        <fieldset className="form-section">
          <legend>Job Information</legend>
          
          <div className="form-group">
            <label htmlFor="job_title">
              Job Title <span className="required">*</span>
            </label>
            <input
              type="text"
              id="job_title"
              name="job_title"
              value={formData.job_title}
              onChange={handleInputChange}
              placeholder="e.g., Plumbing Installation"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="job_description">Job Description</label>
            <textarea
              id="job_description"
              name="job_description"
              value={formData.job_description}
              onChange={handleInputChange}
              placeholder="Detailed description of the work performed"
              rows="4"
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="service_date">
                Service Date <span className="required">*</span>
              </label>
              <input
                type="date"
                id="service_date"
                name="service_date"
                value={formData.service_date}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="labor_hours">Labor Hours</label>
              <input
                type="number"
                id="labor_hours"
                name="labor_hours"
                value={formData.labor_hours}
                onChange={handleInputChange}
                placeholder="0.0"
                step="0.5"
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="service_location">
              Service Location <span className="required">*</span>
            </label>
            <textarea
              id="service_location"
              name="service_location"
              value={formData.service_location}
              onChange={handleInputChange}
              placeholder="Full address of service location"
              rows="3"
              required
            />
          </div>
        </fieldset>

        {/* Client Information Section */}
        <fieldset className="form-section">
          <legend>Client Information</legend>
          
          <div className="form-group">
            <label htmlFor="client_name">
              Client Name <span className="required">*</span>
            </label>
            <input
              type="text"
              id="client_name"
              name="client_name"
              value={formData.client_name}
              onChange={handleInputChange}
              placeholder="Full name"
              required
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="client_email">
                Client Email <span className="required">*</span>
              </label>
              <input
                type="email"
                id="client_email"
                name="client_email"
                value={formData.client_email}
                onChange={handleInputChange}
                placeholder="client@example.com"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="client_phone">Client Phone</label>
              <input
                type="tel"
                id="client_phone"
                name="client_phone"
                value={formData.client_phone}
                onChange={handleInputChange}
                placeholder="(555) 123-4567"
              />
            </div>
          </div>
        </fieldset>

        {/* Service Details Section */}
        <fieldset className="form-section">
          <legend>Service Details</legend>
          
          <div className="form-group">
            <label htmlFor="technician_name">
              Technician Name <span className="required">*</span>
            </label>
            <input
              type="text"
              id="technician_name"
              name="technician_name"
              value={formData.technician_name}
              onChange={handleInputChange}
              placeholder="Your name"
              required
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="materials_used">Materials Used</label>
              <textarea
                id="materials_used"
                name="materials_used"
                value={formData.materials_used}
                onChange={handleInputChange}
                placeholder="List of materials used"
                rows="3"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="cost_estimate">Cost Estimate</label>
              <input
                type="number"
                id="cost_estimate"
                name="cost_estimate"
                value={formData.cost_estimate}
                onChange={handleInputChange}
                placeholder="0.00"
                step="0.01"
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="notes">Additional Notes</label>
            <textarea
              id="notes"
              name="notes"
              value={formData.notes}
              onChange={handleInputChange}
              placeholder="Any additional notes or observations"
              rows="4"
            />
          </div>
        </fieldset>

        {/* Invoice Images Section */}
        <fieldset className="form-section">
          <legend>Supplier Invoice & Reference Images</legend>
          <p className="form-section-hint">Upload photos of supplier invoices or other reference documents. You can choose which images to send to the client.</p>
          
          <div className="form-group">
            <label htmlFor="invoice_images">
              Select Images
            </label>
            <input
              type="file"
              id="invoice_images"
              multiple
              accept="image/*"
              onChange={handleFileSelect}
              className="file-input"
            />
            <p className="form-help-text">You can select multiple image files at once</p>
          </div>

          {selectedFiles.length > 0 && (
            <div className="images-section">
              <h4>Selected Images for Upload ({selectedFiles.length})</h4>
              <div className="image-grid">
                {selectedFiles.map((file, index) => (
                  <div key={index} className="image-preview-item selected">
                    <img src={URL.createObjectURL(file)} alt={`Selected ${index + 1}`} />
                    <p className="image-filename">{file.name}</p>
                    <button
                      type="button"
                      className="btn btn-small btn-danger"
                      onClick={() => removeSelectedFile(index)}
                    >
                      Remove
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {uploadedImages.length > 0 && (
            <div className="images-section">
              <h4>Uploaded Images ({uploadedImages.length})</h4>
              <p className="form-help-text">Check the box for images you want to include in the client email</p>
              <div className="image-grid">
                {uploadedImages.map((image) => (
                  <div key={image.id} className="image-preview-item uploaded">
                    <img src={`data:image/png;base64,${image.image_data}`} alt={image.filename} />
                    <p className="image-filename">{image.filename}</p>
                    <label className="image-checkbox">
                      <input
                        type="checkbox"
                        checked={image.send_to_client}
                        onChange={() => toggleImageSendToClient(image.id)}
                      />
                      <span>Send to client</span>
                    </label>
                    <button
                      type="button"
                      className="btn btn-small btn-danger"
                      onClick={() => removeUploadedImage(image.id)}
                    >
                      Delete
                    </button>
                  </div>
                ))}
              </div>
              <div className="form-actions-inline">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={saveImagePreferences}
                >
                  Save Image Preferences
                </button>
              </div>
            </div>
          )}
        </fieldset>

        {/* Signature Section */}
        <SignaturePad onSignatureCapture={handleSignatureCapture} />

        {signature && (
          <div className="signature-preview">
            <p className="signature-status">✓ Signature captured</p>
          </div>
        )}

        {successMessage && <div className="alert alert-success">{successMessage}</div>}
        {errorMessage && <div className="alert alert-error">{errorMessage}</div>}

        {/* Form Actions */}
        <div className="form-actions">
          <button 
            type="reset" 
            className="btn btn-secondary"
            onClick={() => {
              setFormData({
                job_title: '',
                job_description: '',
                client_name: '',
                client_email: '',
                client_phone: '',
                service_location: '',
                technician_name: '',
                service_date: '',
                labor_hours: '',
                materials_used: '',
                cost_estimate: '',
                notes: ''
              })
              setSignature(null)
              setSelectedFiles([])
              setUploadedImages([])
            }}
          >
            Clear Form
          </button>
          <button 
            type="submit" 
            className="btn btn-primary"
            disabled={loading}
          >
            {loading ? 'Submitting...' : 'Submit JobCard'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default JobCardForm
