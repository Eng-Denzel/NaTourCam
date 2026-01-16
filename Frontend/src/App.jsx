import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext.jsx';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import UserDashboard from './components/dashboard/UserDashboard';
import SiteList from './components/tourism/SiteList';
import SiteDetail from './components/tourism/SiteDetail';
import BookingForm from './components/bookings/BookingForm';
import BookingList from './components/bookings/BookingList';
import Profile from './components/profile/Profile';
import Homepage from './components/Homepage';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import TestComponent from './components/TestComponent';
import './App.css';

// Protected Route component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  console.log('ProtectedRoute - isAuthenticated:', isAuthenticated, 'loading:', loading);

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return isAuthenticated ? children : <Navigate to="/login" />;
};

// Public Route component (redirects authenticated users)
const PublicRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  console.log('PublicRoute - isAuthenticated:', isAuthenticated, 'loading:', loading);

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
          <Navbar />
          <Routes>
            <Route path="/" element={<Homepage />} />
            
            {/* Test route */}
            <Route
              path="/test"
              element={<div>Test route working</div>}
            />
            
            {/* Test homepage route */}
            <Route
              path="/test-homepage"
              element={
                <div>
                  <h1>Homepage Test</h1>
                  <p>If you can see this, the routing is working correctly.</p>
                </div>
              }
            />
            
            {/* Test component route */}
            <Route
              path="/test-component"
              element={<TestComponent />}
            />
            
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
            
            <Route
              path="/bookings"
              element={
                <ProtectedRoute>
                  <BookingList />
                </ProtectedRoute>
              }
            />
            
            <Route
              path="/profile"
              element={
                <ProtectedRoute>
                  <Profile />
                </ProtectedRoute>
              }
            />
          </Routes>
          <Footer />
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
