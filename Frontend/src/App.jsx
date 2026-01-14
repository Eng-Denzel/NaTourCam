import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext.jsx';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import UserDashboard from './components/dashboard/UserDashboard';
import SiteList from './components/tourism/SiteList';
import SiteDetail from './components/tourism/SiteDetail';
import BookingForm from './components/bookings/BookingForm';
import './App.css';

// Protected Route component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return isAuthenticated ? children : <Navigate to="/login" />;
};

// Public Route component (redirects authenticated users)
const PublicRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return !isAuthenticated ? children : <Navigate to="/dashboard" />;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Routes>
            <Route path="/" element={<Navigate to="/sites" />} />
            
            {/* Public routes */}
            <Route 
              path="/login" 
              element={
                <PublicRoute>
                  <Login />
                </PublicRoute>
              } 
            />
            <Route 
              path="/register" 
              element={
                <PublicRoute>
                  <Register />
                </PublicRoute>
              } 
            />
            
            {/* Protected routes */}
            <Route 
              path="/dashboard" 
              element={
                <ProtectedRoute>
                  <UserDashboard />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/sites" 
              element={<SiteList />} 
            />
            
            <Route 
              path="/sites/:id" 
              element={<SiteDetail />} 
            />
            
            <Route 
              path="/bookings/new/:id" 
              element={
                <ProtectedRoute>
                  <BookingForm />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/bookings/new" 
              element={
                <ProtectedRoute>
                  <BookingForm />
                </ProtectedRoute>
              } 
            />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
