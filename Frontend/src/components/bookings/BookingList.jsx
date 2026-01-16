import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { bookingsAPI } from '../../services/api';

const BookingList = () => {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingBooking, setEditingBooking] = useState(null);
  const [newDate, setNewDate] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchBookings();
  }, []);

  const fetchBookings = async () => {
    try {
      setLoading(true);
      const response = await bookingsAPI.getBookings();
      setBookings(response.data);
    } catch (err) {
      setError('Failed to fetch bookings');
      console.error('Error fetching bookings:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCancelBooking = async (bookingId) => {
    if (!window.confirm('Are you sure you want to cancel this booking?')) {
      return;
    }

    try {
      await bookingsAPI.deleteBooking(bookingId);
      // Refresh bookings list
      fetchBookings();
    } catch (err) {
      alert('Failed to cancel booking');
      console.error('Error canceling booking:', err);
    }
  };

  const handleEditDate = (booking) => {
    setEditingBooking(booking.id);
    setNewDate(booking.booking_date);
  };

  const handleSaveDate = async (bookingId) => {
    try {
      await bookingsAPI.updateBooking(bookingId, { booking_date: newDate });
      setEditingBooking(null);
      // Refresh bookings list
      fetchBookings();
    } catch (err) {
      alert('Failed to update booking date');
      console.error('Error updating booking:', err);
    }
  };

  const handleCancelEdit = () => {
    setEditingBooking(null);
    setNewDate('');
  };

  const getStatusBadge = (status) => {
    const statusClasses = {
      pending: 'status-badge status-pending',
      confirmed: 'status-badge status-confirmed',
      completed: 'status-badge status-completed',
      cancelled: 'status-badge status-cancelled',
    };
    return statusClasses[status] || 'status-badge';
  };

  if (loading) {
    return <div className="loading">Loading bookings...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="bookings-container">
      <div className="bookings-header">
        <h1>My Bookings</h1>
        <button 
          onClick={() => navigate('/sites')} 
          className="new-booking-button"
        >
          + New Booking
        </button>
      </div>

      {bookings.length === 0 ? (
        <div className="no-bookings">
          <p>You don't have any bookings yet.</p>
          <button 
            onClick={() => navigate('/sites')} 
            className="browse-sites-button"
          >
            Browse Tourist Sites
          </button>
        </div>
      ) : (
        <div className="bookings-list">
          {bookings.map((booking) => (
            <div key={booking.id} className="booking-card">
              <div className="booking-header">
                <h3>{booking.tourist_site_name || `Site #${booking.tourist_site}`}</h3>
                <span className={getStatusBadge(booking.status)}>
                  {booking.status}
                </span>
              </div>

              <div className="booking-details">
                <div className="booking-detail-item">
                  <span className="detail-label">📅 Date:</span>
                  {editingBooking === booking.id ? (
                    <div className="date-edit-container">
                      <input
                        type="date"
                        value={newDate}
                        onChange={(e) => setNewDate(e.target.value)}
                        className="date-input"
                      />
                      <button 
                        onClick={() => handleSaveDate(booking.id)}
                        className="save-button"
                      >
                        ✓
                      </button>
                      <button 
                        onClick={handleCancelEdit}
                        className="cancel-edit-button"
                      >
                        ✕
                      </button>
                    </div>
                  ) : (
                    <span className="detail-value">
                      {new Date(booking.booking_date).toLocaleDateString()}
                    </span>
                  )}
                </div>

                <div className="booking-detail-item">
                  <span className="detail-label">👥 Visitors:</span>
                  <span className="detail-value">{booking.number_of_visitors}</span>
                </div>

                <div className="booking-detail-item">
                  <span className="detail-label">💰 Total Price:</span>
                  <span className="detail-value">${booking.total_price}</span>
                </div>

                {booking.special_requests && (
                  <div className="booking-detail-item full-width">
                    <span className="detail-label">📝 Special Requests:</span>
                    <span className="detail-value">{booking.special_requests}</span>
                  </div>
                )}
              </div>

              <div className="booking-actions">
                {booking.status !== 'cancelled' && booking.status !== 'completed' && (
                  <>
                    {editingBooking !== booking.id && (
                      <button 
                        onClick={() => handleEditDate(booking)}
                        className="edit-button"
                      >
                        ✏️ Change Date
                      </button>
                    )}
                    <button 
                      onClick={() => handleCancelBooking(booking.id)}
                      className="cancel-booking-button"
                    >
                      🗑️ Cancel Booking
                    </button>
                  </>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default BookingList;
