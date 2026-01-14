import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext.jsx';
import { bookingsAPI } from '../../services/api';
import Logout from '../auth/Logout';

const UserDashboard = () => {
  const { user } = useAuth();
  const [bookingsSummary, setBookingsSummary] = useState({
    total_bookings: 0,
    completed_bookings: 0,
    pending_bookings: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchBookingsSummary();
  }, []);

  const fetchBookingsSummary = async () => {
    try {
      setLoading(true);
      const response = await bookingsAPI.getBookingsSummary();
      setBookingsSummary(response.data);
    } catch (err) {
      setError('Failed to fetch bookings summary');
      console.error('Error fetching summary:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Welcome, {user?.first_name || user?.username}!</h1>
        <Logout />
      </div>

      <div className="dashboard-summary">
        <div className="summary-card">
          <h3>Total Bookings</h3>
          <p className="summary-value">{bookingsSummary.total_bookings}</p>
        </div>

        <div className="summary-card">
          <h3>Completed</h3>
          <p className="summary-value completed">{bookingsSummary.completed_bookings}</p>
        </div>

        <div className="summary-card">
          <h3>Pending</h3>
          <p className="summary-value pending">{bookingsSummary.pending_bookings}</p>
        </div>
      </div>

      <div className="dashboard-content">
        <div className="dashboard-section">
          <h2>Recent Bookings</h2>
          <p>Recent bookings will be displayed here.</p>
        </div>

        <div className="dashboard-section">
          <h2>Upcoming Visits</h2>
          <p>Upcoming visits will be displayed here.</p>
        </div>
      </div>
    </div>
  );
};

export default UserDashboard;