import React, { useState, useEffect } from 'react';
import { tourismAPI } from '../../services/api';
import SiteImageManager from './SiteImageManager';
import './SiteForm.css';

const SiteForm = ({ site, onClose, onSuccess }) => {
  const [regions, setRegions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    region: '',
    latitude: '',
    longitude: '',
    address: '',
    entrance_fee: '',
    opening_time: '',
    closing_time: '',
    is_active: true,
  });

  useEffect(() => {
    fetchRegions();
    
    // If editing, populate form with site data
    if (site) {
      setFormData({
        name: site.name || '',
        description: site.description || '',
        region: site.region?.id || '',
        latitude: site.latitude || '',
        longitude: site.longitude || '',
        address: site.address || '',
        entrance_fee: site.entrance_fee || '',
        opening_time: site.opening_time || '',
        closing_time: site.closing_time || '',
        is_active: site.is_active !== undefined ? site.is_active : true,
      });
    }
  }, [site]);

  const fetchRegions = async () => {
    try {
      const response = await tourismAPI.getRegions();
      setRegions(response.data);
    } catch (err) {
      console.error('Error fetching regions:', err);
      setError('Failed to load regions');
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Prepare data for submission
      const submitData = {
        name: formData.name,
        description: formData.description,
        region: formData.region ? parseInt(formData.region) : null,
        is_active: formData.is_active,
      };

      // Only include optional fields if they have values
      if (formData.latitude && formData.latitude !== '') {
        submitData.latitude = parseFloat(formData.latitude);
      }
      if (formData.longitude && formData.longitude !== '') {
        submitData.longitude = parseFloat(formData.longitude);
      }
      if (formData.entrance_fee && formData.entrance_fee !== '') {
        submitData.entrance_fee = parseFloat(formData.entrance_fee);
      }
      if (formData.address && formData.address !== '') {
        submitData.address = formData.address;
      }
      if (formData.opening_time && formData.opening_time !== '') {
        submitData.opening_time = formData.opening_time;
      }
      if (formData.closing_time && formData.closing_time !== '') {
        submitData.closing_time = formData.closing_time;
      }

      if (site) {
        // Update existing site
        await tourismAPI.adminUpdateSite(site.id, submitData);
      } else {
        // Create new site
        await tourismAPI.adminCreateSite(submitData);
      }

      onSuccess();
      onClose();
    } catch (err) {
      console.error('Error saving site:', err);
      const errorMessage = err.response?.data?.error || 
                          JSON.stringify(err.response?.data) || 
                          'Failed to save site. Please check all fields and try again.';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content site-form-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{site ? '✏️ Edit Tourist Site' : '➕ Add New Tourist Site'}</h2>
          <button className="close-button" onClick={onClose}>✕</button>
        </div>

        {error && (
          <div className="error-banner">
            <span>⚠️ {error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="site-form">
          <div className="form-grid">
            <div className="form-group full-width">
              <label htmlFor="name">Site Name *</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                placeholder="Enter site name"
              />
            </div>

            <div className="form-group full-width">
              <label htmlFor="description">Description *</label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleChange}
                required
                rows="4"
                placeholder="Enter site description"
              />
            </div>

            <div className="form-group">
              <label htmlFor="region">Region *</label>
              <select
                id="region"
                name="region"
                value={formData.region}
                onChange={handleChange}
                required
              >
                <option value="">Select a region</option>
                {regions.map((region) => (
                  <option key={region.id} value={region.id}>
                    {region.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="entrance_fee">Entrance Fee (FCFA)</label>
              <input
                type="number"
                id="entrance_fee"
                name="entrance_fee"
                value={formData.entrance_fee}
                onChange={handleChange}
                min="0"
                step="0.01"
                placeholder="0.00"
              />
            </div>

            <div className="form-group">
              <label htmlFor="latitude">Latitude</label>
              <input
                type="number"
                id="latitude"
                name="latitude"
                value={formData.latitude}
                onChange={handleChange}
                step="0.000001"
                placeholder="e.g., 4.0511"
              />
            </div>

            <div className="form-group">
              <label htmlFor="longitude">Longitude</label>
              <input
                type="number"
                id="longitude"
                name="longitude"
                value={formData.longitude}
                onChange={handleChange}
                step="0.000001"
                placeholder="e.g., 9.7679"
              />
            </div>

            <div className="form-group full-width">
              <label htmlFor="address">Address</label>
              <input
                type="text"
                id="address"
                name="address"
                value={formData.address}
                onChange={handleChange}
                placeholder="Enter site address"
              />
            </div>

            <div className="form-group">
              <label htmlFor="opening_time">Opening Time</label>
              <input
                type="time"
                id="opening_time"
                name="opening_time"
                value={formData.opening_time}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="closing_time">Closing Time</label>
              <input
                type="time"
                id="closing_time"
                name="closing_time"
                value={formData.closing_time}
                onChange={handleChange}
              />
            </div>

            <div className="form-group full-width">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="is_active"
                  checked={formData.is_active}
                  onChange={handleChange}
                />
                <span>Active (visible to users)</span>
              </label>
            </div>
          </div>

          {/* Image Manager - Only show for existing sites */}
          {site && site.id && (
            <SiteImageManager
              siteId={site.id}
              images={site.images || []}
              onImagesUpdate={onSuccess}
            />
          )}

          <div className="form-actions">
            <button
              type="button"
              className="btn-cancel"
              onClick={onClose}
              disabled={loading}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn-submit"
              disabled={loading}
            >
              {loading ? 'Saving...' : site ? 'Update Site' : 'Create Site'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SiteForm;
