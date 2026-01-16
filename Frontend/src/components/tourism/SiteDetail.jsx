import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { tourismAPI } from '../../services/api';
import { useAuth } from '../../contexts/AuthContext';

const SiteDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const [site, setSite] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchSite();
  }, [id]);

  const fetchSite = async () => {
    try {
      setLoading(true);
      const response = await tourismAPI.getSite(id);
      setSite(response.data);
    } catch (err) {
      setError('Failed to fetch site details');
      console.error('Error fetching site:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleBookNow = () => {
    if (!isAuthenticated) {
      // Redirect to login if not authenticated
      navigate('/login', { state: { from: `/sites/${id}` } });
    } else {
      // Navigate to booking form with site ID
      navigate(`/bookings/new/${id}`, { state: { site } });
    }
  };

  if (loading) {
    return <div className="loading">Loading site details...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  if (!site) {
    return <div className="error-message">Site not found</div>;
  }

  return (
    <div className="site-detail-container">
      <div className="site-header">
        <h1>{site.name}</h1>
        <p className="site-region">📍 {site.region?.name}</p>
      </div>

      <div className="site-detail-layout">
        {/* Left Column - Images */}
        <div className="site-images-column">
          {site.images && site.images.length > 0 ? (
            <div className="site-image-gallery-vertical">
              {site.images.map((image, index) => (
                <div key={image.id} className="gallery-image-wrapper">
                  <img 
                    src={image.image} 
                    alt={image.caption || `${site.name} ${index + 1}`} 
                    className={`gallery-image ${image.is_primary ? 'primary-image' : ''}`}
                  />
                  {image.caption && (
                    <p className="image-caption">{image.caption}</p>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="no-images-placeholder">
              <span>📷</span>
              <p>No images available</p>
            </div>
          )}
        </div>

        {/* Right Column - Details */}
        <div className="site-info-column">
          <div className="site-details-card">
            <div className="site-info-section">
              <h2>About This Site</h2>
              <p className="site-description-text">{site.description}</p>
            </div>

            <div className="site-quick-info">
              <div className="info-item">
                <span className="info-icon">💰</span>
                <div className="info-content">
                  <h3>Entrance Fee</h3>
                  <p className="info-value">{site.entrance_fee ? `${site.entrance_fee} FCFA` : 'Free Entry'}</p>
                </div>
              </div>

              <div className="info-item">
                <span className="info-icon">🕐</span>
                <div className="info-content">
                  <h3>Opening Hours</h3>
                  <p className="info-value">
                    {site.opening_time ? `${site.opening_time} - ${site.closing_time}` : 'Open Daily'}
                  </p>
                </div>
              </div>

              <div className="info-item">
                <span className="info-icon">📍</span>
                <div className="info-content">
                  <h3>Location</h3>
                  <p className="info-value">{site.address || 'See map for location'}</p>
                </div>
              </div>

              {site.latitude && site.longitude && (
                <div className="info-item">
                  <span className="info-icon">🗺️</span>
                  <div className="info-content">
                    <h3>Coordinates</h3>
                    <p className="info-value">
                      {site.latitude}°, {site.longitude}°
                    </p>
                  </div>
                </div>
              )}
            </div>

            {site.bilingual_content && site.bilingual_content.length > 0 && (
              <div className="bilingual-content">
                <h2>Additional Information</h2>
                {site.bilingual_content.map((content) => (
                  <div key={content.id} className="content-item">
                    <h3>{content.title} ({content.language.toUpperCase()})</h3>
                    <p>{content.description}</p>
                  </div>
                ))}
              </div>
            )}

            <div className="action-buttons">
              <button className="book-now-button" onClick={handleBookNow}>
                🎫 Book Your Visit Now
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SiteDetail;