import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { bookingsAPI } from '../../services/api';

const BookingForm = ({ site }) => {
  const navigate = useNavigate();
  const { id: siteId } = useParams();
  
  const [formData, setFormData] = useState({
    tourist_site: siteId || site?.id,
    booking_date: '',
    number_of_visitors: 1,
    special_requests: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Calculate total price (this would typically come from the backend)
      const totalPrice = site?.entrance_fee 
        ? site.entrance_fee * formData.number_of_visitors 
        : 0;

      const bookingData = {
        ...formData,
        total_price: totalPrice,
      };

      const response = await bookingsAPI.createBooking(bookingData);
      
      if (response.status === 201) {
        // Booking created successfully - redirect to bookings page
        alert('Booking created successfully!');
        navigate('/bookings');
      }
    } catch (err) {
      setError('Failed to create booking. Please try again.');
      console.error('Booking error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="booking-form-container">
      <h2>Book Your Visit</h2>
      
      {site && (
        <div className="site-summary">
          <h3>{site.name}</h3>
          <p>{site.description.substring(0, 100)}...</p>
          {site.entrance_fee && (
            <p>Entrance Fee: ${site.entrance_fee} per person</p>
          )}
        </div>
      )}
      
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit} className="booking-form">
        <div className="form-group">
          <label htmlFor="booking_date">Visit Date:</label>
          <input
            type="date"
            id="booking_date"
            name="booking_date"
            value={formData.booking_date}
            onChange={handleChange}
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="number_of_visitors">Number of Visitors:</label>
          <input
            type="number"
            id="number_of_visitors"
            name="number_of_visitors"
            min="1"
            max="50"
            value={formData.number_of_visitors}
            onChange={handleChange}
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="special_requests">Special Requests:</label>
          <textarea
            id="special_requests"
            name="special_requests"
            value={formData.special_requests}
            onChange={handleChange}
            rows="4"
            placeholder="Any special requirements or requests..."
          />
        </div>
        
        <div className="form-actions">
          <button 
            type="button" 
            onClick={() => navigate(-1)} 
            className="cancel-button"
          >
            Cancel
          </button>
          <button 
            type="submit" 
            disabled={loading}
            className="submit-button"
          >
            {loading ? 'Processing...' : 'Confirm Booking'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default BookingForm;