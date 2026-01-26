import axios from 'axios';
import { formatError } from '../utils/errorHandler';

// Create axios instance with default configuration
const api = axios.create({
  baseURL: 'http://localhost:8000/api', // Django development server
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle network errors
    if (!error.response) {
      console.error('Network Error:', error.message);
      return Promise.reject(new Error('Network Error - Please check your connection'));
    }
    
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (credentials) => api.post('/accounts/login/', credentials),
  register: (userData) => api.post('/accounts/register/', userData),
  logout: () => api.post('/accounts/logout/'),
  checkAuth: () => api.get('/accounts/check-auth/'),
  getProfile: () => api.get('/accounts/profile/'),
  updateProfile: (profileData) => api.put('/accounts/profile/', profileData),
};

// Attractions API
export const attractionsAPI = {
  getCategories: () => api.get('/attractions/categories/'),
  getAttractions: (params) => api.get('/attractions/', { params }),
  getAttraction: (id) => api.get(`/attractions/${id}/`),
  createAttraction: (attractionData) => api.post('/attractions/create/', attractionData),
  getReviews: (attractionId) => api.get(`/attractions/${attractionId}/reviews/`),
  createReview: (reviewData) => api.post('/attractions/reviews/create/', reviewData),
};

// Tours API
export const toursAPI = {
  getTours: (params) => api.get('/tours/', { params }),
  getTour: (id) => api.get(`/tours/${id}/`),
  createTour: (tourData) => api.post('/tours/create/', tourData),
  getItinerary: (tourId) => api.get(`/tours/${tourId}/itinerary/`),
  createItinerary: (itineraryData) => api.post('/tours/itinerary/create/', itineraryData),
  getAvailability: (tourId) => api.get(`/tours/${tourId}/availability/`),
  createAvailability: (availabilityData) => api.post('/tours/availability/create/', availabilityData),
};

// Bookings API
export const bookingsAPI = {
  getBookings: (params) => api.get('/bookings/', { params }),
  getBooking: (id) => api.get(`/bookings/${id}/`),
  createBooking: (bookingData) => api.post('/bookings/create/', bookingData),
  cancelBooking: (id) => api.post(`/bookings/${id}/cancel/`),
  createPayment: (paymentData) => api.post('/bookings/payment/create/', paymentData),
};

// Notifications API
export const notificationsAPI = {
  getNotifications: (params) => api.get('/notifications/', { params }),
  getNotification: (id) => api.get(`/notifications/${id}/`),
  getUnreadCount: () => api.get('/notifications/unread-count/'),
  markAllRead: () => api.post('/notifications/mark-all-read/'),
  getPreferences: () => api.get('/notifications/preferences/'),
  updatePreferences: (preferencesData) => api.put('/notifications/preferences/', preferencesData),
};

// Analytics API
export const analyticsAPI = {
  getUserAnalytics: () => api.get('/analytics/user/'),
  getAttractionAnalytics: (attractionId) => api.get(`/analytics/attraction/${attractionId}/`),
  getTourAnalytics: (tourId) => api.get(`/analytics/tour/${tourId}/`),
  getAdminDashboard: () => api.get('/analytics/admin/dashboard/'),
};

// Generic API error handler
export const handleApiError = (error, context = '') => {
  const formattedError = formatError(error);
  console.error(`[API Error] ${context}:`, formattedError);
  return formattedError;
};

// Set auth token
export const setAuthToken = (token) => {
  if (token) {
    localStorage.setItem('authToken', token);
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    localStorage.removeItem('authToken');
    delete api.defaults.headers.common['Authorization'];
  }
};

// Check if user is authenticated
export const isAuthenticated = () => {
  const token = localStorage.getItem('authToken');
  return !!token;
};

export default api;