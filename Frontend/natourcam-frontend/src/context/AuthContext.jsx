import React, { createContext, useState, useEffect, useContext } from 'react';
import { authAPI, setAuthToken, isAuthenticated } from '../services/api';
import { handleApiError } from '../services/api';

// Create Auth Context
const AuthContext = createContext();

// Auth Provider Component
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Check if user is authenticated on app load
  useEffect(() => {
    const checkAuthStatus = async () => {
      if (isAuthenticated()) {
        try {
          const response = await authAPI.getProfile();
          setUser(response.data);
        } catch (err) {
          // If token is invalid, remove it
          setAuthToken(null);
          setError(handleApiError(err, 'Authentication check'));
        }
      }
      setLoading(false);
    };

    checkAuthStatus();
  }, []);

  // Login function
  const login = async (credentials) => {
    try {
      setLoading(true);
      setError('');
      
      const response = await authAPI.login(credentials);
      const { token, user } = response.data;
      
      // Set token in localStorage and axios headers
      setAuthToken(token);
      
      // Set user in state
      setUser(user);
      
      return { success: true };
    } catch (err) {
      const errorMessage = handleApiError(err, 'Login');
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  // Register function
  const register = async (userData) => {
    try {
      setLoading(true);
      setError('');
      
      const response = await authAPI.register(userData);
      
      return { success: true, data: response.data };
    } catch (err) {
      const errorMessage = handleApiError(err, 'Registration');
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  // Logout function
  const logout = async () => {
    try {
      await authAPI.logout();
    } catch (err) {
      console.error('Logout error:', handleApiError(err, 'Logout'));
    } finally {
      // Clear token and user data regardless of API response
      setAuthToken(null);
      setUser(null);
    }
  };

  // Update profile function
  const updateProfile = async (profileData) => {
    try {
      setLoading(true);
      setError('');
      
      const response = await authAPI.updateProfile(profileData);
      setUser(response.data);
      
      return { success: true, data: response.data };
    } catch (err) {
      const errorMessage = handleApiError(err, 'Profile update');
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  // Clear error
  const clearError = () => {
    setError('');
  };

  // Context value
  const value = {
    user,
    loading,
    error,
    login,
    register,
    logout,
    updateProfile,
    clearError,
    isAuthenticated: !!user,
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  
  return context;
};

export default AuthContext;