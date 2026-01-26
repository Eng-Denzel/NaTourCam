import React, { useState, useEffect } from 'react';

const Bookings = () => {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  // Mock data for bookings
  const mockBookings = [
    {
      id: 1,
      tourTitle: 'Mount Cameroon Adventure',
      tourOperator: 'Cameroon Adventures Ltd',
      participants: 2,
      totalPrice: 300000,
      currency: 'FCFA',
      status: 'confirmed',
      bookingDate: '2026-01-15',
      tourDate: '2026-03-15'
    },
    {
      id: 2,
      tourTitle: 'Waza Wildlife Safari',
      tourOperator: 'Wildlife Safaris Cameroon',
      participants: 4,
      totalPrice: 320000,
      currency: 'FCFA',
      status: 'pending',
      bookingDate: '2026-01-20',
      tourDate: '2026-04-10'
    },
    {
      id: 3,
      tourTitle: 'Kribi Coastal Getaway',
      tourOperator: 'Coastal Tours Ltd',
      participants: 1,
      totalPrice: 120000,
      currency: 'FCFA',
      status: 'completed',
      bookingDate: '2025-12-10',
      tourDate: '2025-12-20'
    }
  ];

  useEffect(() => {
    // TODO: Fetch bookings from API
    setTimeout(() => {
      setBookings(mockBookings);
      setLoading(false);
    }, 1000);
  }, []);

  const filteredBookings = filter === 'all' 
    ? bookings 
    : bookings.filter(booking => booking.status === filter);

  const getStatusClass = (status) => {
    switch (status) {
      case 'confirmed': return 'status-confirmed';
      case 'pending': return 'status-pending';
      case 'cancelled': return 'status-cancelled';
      case 'completed': return 'status-completed';
      default: return '';
    }
  };

  if (loading) {
    return <div className="loading">Loading bookings...</div>;
  }

  return (
    <div className="bookings-page">
      <div className="page-header">
        <h2>My Bookings</h2>
        <div className="filters">
          <select 
            value={filter} 
            onChange={(e) => setFilter(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Statuses</option>
            <option value="pending">Pending</option>
            <option value="confirmed">Confirmed</option>
            <option value="completed">Completed</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </div>
      </div>

      <div className="bookings-list">
        {filteredBookings.length === 0 ? (
          <div className="no-bookings">
            <p>You don't have any bookings yet.</p>
            <button className="browse-tours-button">Browse Tours</button>
          </div>
        ) : (
          filteredBookings.map(booking => (
            <div key={booking.id} className="booking-card">
              <div className="booking-header">
                <h3>{booking.tourTitle}</h3>
                <span className={`booking-status ${getStatusClass(booking.status)}`}>
                  {booking.status.charAt(0).toUpperCase() + booking.status.slice(1)}
                </span>
              </div>
              <div className="booking-details">
                <div className="booking-info">
                  <p><strong>Tour Operator:</strong> {booking.tourOperator}</p>
                  <p><strong>Participants:</strong> {booking.participants}</p>
                  <p><strong>Booking Date:</strong> {booking.bookingDate}</p>
                  <p><strong>Tour Date:</strong> {booking.tourDate}</p>
                </div>
                <div className="booking-price">
                  <p><strong>Total Price:</strong></p>
                  <p className="price">{booking.currency} {booking.totalPrice.toLocaleString()}</p>
                </div>
              </div>
              <div className="booking-actions">
                <button className="view-details-button">View Details</button>
                {booking.status === 'pending' && (
                  <button className="cancel-booking-button">Cancel Booking</button>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Bookings;