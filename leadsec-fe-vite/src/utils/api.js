import axios from 'axios'

// const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Ensure cookies (Flask session) are sent with requests
api.defaults.withCredentials = true

export const jobcardAPI = {
  createJobcard: (data) => api.post('/jobcards', data),
  getJobcard: (id) => api.get(`/jobcards/${id}`),
  getAllJobcards: (params) => api.get('/jobcards', { params }),
  updateJobcard: (id, data) => api.put(`/jobcards/${id}`, data),
  downloadPDF: (id) => api.get(`/jobcards/${id}/pdf`, { responseType: 'blob' }),
  sendToClient: (id) => api.post(`/jobcards/${id}/send-to-client`),
  uploadImages: (jobcardId, formData) => api.post(`/jobcards/${jobcardId}/images`, formData, {
    headers: {
      'Content-Type': undefined
    }
  }),
  getImages: (jobcardId) => api.get(`/jobcards/${jobcardId}/images`),
  updateImage: (imageId, data) => api.put(`/images/${imageId}`, data),
  deleteImage: (imageId) => api.delete(`/images/${imageId}`),
  healthCheck: () => api.get('/health')
}

export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  logout: () => api.post('/auth/logout'),
  me: () => api.get('/auth/me')
}

export default api
