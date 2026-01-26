// Error handling utility functions

// Parse API error responses
export const parseApiError = (error) => {
  if (!error) return 'An unknown error occurred';
  
  // If it's a string, return it directly
  if (typeof error === 'string') return error;
  
  // If it's an API error response
  if (error.response) {
    const { status, data } = error.response;
    
    // Handle specific status codes
    switch (status) {
      case 400:
        return data.message || data.detail || 'Bad Request - Please check your input';
      case 401:
        return 'Unauthorized - Please log in again';
      case 403:
        return 'Forbidden - You do not have permission to perform this action';
      case 404:
        return 'Not Found - The requested resource was not found';
      case 409:
        return 'Conflict - The request could not be completed due to a conflict';
      case 500:
        return 'Internal Server Error - Please try again later';
      case 502:
        return 'Bad Gateway - Please try again later';
      case 503:
        return 'Service Unavailable - Please try again later';
      default:
        if (data && typeof data === 'object') {
          // Try to extract error messages from the response data
          if (data.detail) return data.detail;
          if (data.message) return data.message;
          
          // Handle field-specific errors
          const fieldErrors = Object.values(data).filter(val => Array.isArray(val) && val.length > 0);
          if (fieldErrors.length > 0) {
            return fieldErrors[0][0]; // Return the first error message
          }
          
          // Try to stringify the data if it's an object
          try {
            return JSON.stringify(data);
          } catch (e) {
            return 'An error occurred';
          }
        }
        return `HTTP ${status} - An error occurred`;
    }
  }
  
  // Handle network errors
  if (error.request) {
    return 'Network Error - Please check your connection';
  }
  
  // Handle other errors
  return error.message || 'An error occurred';
};

// Format error messages for display
export const formatError = (error) => {
  const parsedError = parseApiError(error);
  
  // Capitalize the first letter
  return parsedError.charAt(0).toUpperCase() + parsedError.slice(1);
};

// Log error to console (in production, you might want to send to a logging service)
export const logError = (error, context = '') => {
  console.error(`[NaTourCam Error] ${context}:`, error);
  
  // In a real application, you might want to send this to a logging service
  // Example: sendToLoggingService({ error, context, timestamp: new Date().toISOString() });
};

// Create a user-friendly error message
export const createUserErrorMessage = (error, action = 'perform this action') => {
  const message = parseApiError(error);
  return `Failed to ${action}. ${message}`;
};

// Handle authentication errors
export const handleAuthError = (error, navigate) => {
  const message = parseApiError(error);
  
  // If it's an authentication error, redirect to login
  if (error.response && (error.response.status === 401 || error.response.status === 403)) {
    // Clear any stored authentication tokens
    localStorage.removeItem('authToken');
    // Redirect to login page
    navigate('/login');
  }
  
  return message;
};