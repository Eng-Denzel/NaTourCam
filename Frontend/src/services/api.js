import axios from 'axios';

// Create an axios instance with default configuration
const api = axios.create({
  baseURL: '/api', // Use proxy path
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the auth token if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle errors globally
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response);
    return response;
  },
  (error) => {
    console.error('API Error:', error);
    if (error.response?.status === 401) {
      // Unauthorized, remove token and redirect to login
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Authentication API calls
export const authAPI = {
  register: (userData) => api.post('/auth/register/', userData),
  login: (credentials) => api.post('/auth/login/', credentials),
  logout: () => api.post('/auth/logout/'),
  getUser: () => api.get('/auth/users/me/'),
  updateUser: (userData) => api.put('/auth/users/me/', userData),
  getUsers: () => api.get('/auth/users/'),  // Admin only
  adminUpdateUser: (userId, userData) => api.patch(`/auth/users/${userId}/update/`, userData),  // Admin only
};

// Tourism API calls
export const tourismAPI = {
  getSites: (params) => api.get('/tourism/sites/', { params }),
  getSite: (id) => api.get(`/tourism/sites/${id}/`),
  getRegions: () => api.get('/tourism/regions/'),
  getContent: (params) => api.get('/tourism/content/', { params }),
  adminCreateSite: (siteData) => api.post('/tourism/sites/create/', siteData),  // Admin only
  adminUpdateSite: (siteId, siteData) => api.patch(`/tourism/sites/${siteId}/update/`, siteData),  // Admin only
  adminUploadSiteImage: (siteId, formData) => api.post(`/tourism/sites/${siteId}/images/upload/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),  // Admin only
  adminDeleteSiteImage: (imageId) => api.delete(`/tourism/images/${imageId}/delete/`),  // Admin only
  adminSetPrimaryImage: (imageId) => api.patch(`/tourism/images/${imageId}/set-primary/`),  // Admin only
};

// Bookings API calls
export const bookingsAPI = {
  getBookings: () => api.get('/bookings/bookings/'),
  getBooking: (id) => api.get(`/bookings/bookings/${id}/`),
  createBooking: (bookingData) => api.post('/bookings/bookings/', bookingData),
  updateBooking: (id, bookingData) => api.patch(`/bookings/bookings/${id}/`, bookingData),
  deleteBooking: (id) => api.delete(`/bookings/bookings/${id}/`),
  getPayment: (id) => api.get(`/bookings/payments/${id}/`),
  getReviews: () => api.get('/bookings/reviews/'),
  createReview: (reviewData) => api.post('/bookings/reviews/', reviewData),
  getBookingsSummary: () => api.get('/bookings/summary/'),
};

export default api;