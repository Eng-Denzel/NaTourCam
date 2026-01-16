import React, { useState, useEffect } from 'react';
import { useNavigate, useParams, useLocation } from 'react-router-dom';
import { bookingsAPI, tourismAPI } from '../../services/api';

const BookingForm = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { id: siteId } = useParams();
  const [site, setSite] = useState(location.state?.site || null);
  
  const [formData, setFormData] = useState({
    tourist_site: siteId || site?.id,
    booking_date: '',
    number_of_visitors: 1,
    special_requests: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch site details if not passed via state
  useEffect(() => {
    if (siteId && !site) {
      const fetchSite = async () => {
        try {
          const response = await tourismAPI.getSite(siteId);
          setSite(response.data);
        } catch (err) {
          console.error('Error fetching site:', err);
        }
      };
      fetchSite();
    }
  }, [siteId, site]);

  // Update formData when site is loaded
  useEffect(() => {
    if (site && site.id) {
      setFormData(prev => ({
        ...prev,
        tourist_site: site.id
      }));
    }
  }, [site]);

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
      // Validate that we have a site ID
      if (!formData.tourist_site) {
        setError('Site information is missing. Please try again.');
        setLoading(false);
        return;
      }

      // Calculate total price (this would typically come from the backend)
      const totalPrice = site?.entrance_fee 
        ? site.entrance_fee * formData.number_of_visitors 
        : 0;

      const bookingData = {
        ...formData,
        total_price: totalPrice,
      };

      console.log('Submitting booking data:', bookingData);

      const response = await bookingsAPI.createBooking(bookingData);
      
      console.log('Booking response:', response);
      
      if (response.status === 201) {
        // Booking created successfully - redirect to bookings page
        alert('Booking created successfully!');
        navigate('/bookings');
      }
    } catch (err) {
      const errorMessage = err.response?.data?.message || err.response?.data?.error || 'Failed to create booking. Please try again.';
      setError(errorMessage);
      console.error('Booking error:', err);
      console.error('Error response:', err.response?.data);
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