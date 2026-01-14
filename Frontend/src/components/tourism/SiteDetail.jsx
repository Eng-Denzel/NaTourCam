import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { tourismAPI } from '../../services/api';

const SiteDetail = () => {
  const { id } = useParams();
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
        <p className="site-region">{site.region?.name}</p>
      </div>

      {site.images && site.images.length > 0 && (
        <div className="site-image-gallery">
          {site.images.map((image, index) => (
            <img 
              key={image.id} 
              src={image.image} 
              alt={image.caption || `${site.name} ${index + 1}`} 
              className={image.is_primary ? 'primary-image' : ''}
            />
          ))}
        </div>
      )}

      <div className="site-details">
        <div className="site-info-section">
          <h2>Description</h2>
          <p>{site.description}</p>
        </div>

        <div className="site-details-grid">
          <div className="detail-item">
            <h3>Entrance Fee</h3>
            <p>${site.entrance_fee || 'Free'}</p>
          </div>

          <div className="detail-item">
            <h3>Opening Hours</h3>
            <p>
              {site.opening_time ? `${site.opening_time} - ${site.closing_time}` : 'Not specified'}
            </p>
          </div>

          <div className="detail-item">
            <h3>Address</h3>
            <p>{site.address || 'Not specified'}</p>
          </div>

          <div className="detail-item">
            <h3>Location</h3>
            <p>
              {site.latitude && site.longitude 
                ? `Lat: ${site.latitude}, Lng: ${site.longitude}` 
                : 'Not specified'}
            </p>
          </div>
        </div>

        {site.bilingual_content && site.bilingual_content.length > 0 && (
          <div className="bilingual-content">
            <h2>Additional Information</h2>
            {site.bilingual_content.map((content) => (
              <div key={content.id} className="content-item">
                <h3>{content.title} ({content.language})</h3>
                <p>{content.description}</p>
              </div>
            ))}
          </div>
        )}

        <div className="action-buttons">
          <button className="book-now-button">Book Now</button>
        </div>
      </div>
    </div>
  );
};

export default SiteDetail;