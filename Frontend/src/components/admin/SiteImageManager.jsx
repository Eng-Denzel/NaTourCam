import React, { useState } from 'react';
import { tourismAPI } from '../../services/api';
import './SiteImageManager.css';

const SiteImageManager = ({ siteId, images, onImagesUpdate }) => {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  const handleImageUpload = async (e) => {
    const files = Array.from(e.target.files);
    if (files.length === 0) return;

    setUploading(true);
    setError(null);

    try {
      // Upload each file separately
      for (const file of files) {
        const formData = new FormData();
        formData.append('image', file);
        formData.append('caption', '');
        formData.append('is_primary', 'false');

        await tourismAPI.adminUploadSiteImage(siteId, formData);
      }

      // Trigger refresh
      onImagesUpdate();
      
      // Clear the file input
      e.target.value = '';
    } catch (err) {
      console.error('Error uploading images:', err);
      setError(err.response?.data?.error || 'Failed to upload images. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteImage = async (imageId) => {
    if (!confirm('Are you sure you want to delete this image?')) return;

    setError(null);

    try {
      await tourismAPI.adminDeleteSiteImage(imageId);
      onImagesUpdate();
    } catch (err) {
      console.error('Error deleting image:', err);
      setError(err.response?.data?.error || 'Failed to delete image. Please try again.');
    }
  };

  const handleSetPrimary = async (imageId) => {
    setError(null);

    try {
      await tourismAPI.adminSetPrimaryImage(imageId);
      onImagesUpdate();
    } catch (err) {
      console.error('Error setting primary image:', err);
      setError(err.response?.data?.error || 'Failed to set primary image. Please try again.');
    }
  };

  return (
    <div className="site-image-manager">
      <h3>Site Images</h3>
      
      {error && (
        <div className="error-message">
          <span>⚠️ {error}</span>
        </div>
      )}

      <div className="image-upload-section">
        <label htmlFor="image-upload" className="upload-button">
          {uploading ? 'Uploading...' : '📷 Upload Images'}
        </label>
        <input
          id="image-upload"
          type="file"
          accept="image/*"
          multiple
          onChange={handleImageUpload}
          disabled={uploading || !siteId}
          style={{ display: 'none' }}
        />
        {!siteId && (
          <p className="info-text">Save the site first to upload images</p>
        )}
      </div>

      {images && images.length > 0 && (
        <div className="images-grid">
          {images.map((image) => (
            <div key={image.id} className="image-card">
              <img src={image.image} alt={image.caption || 'Site image'} />
              <div className="image-actions">
                {image.is_primary && <span className="primary-badge">Primary</span>}
                {!image.is_primary && (
                  <button
                    className="btn-set-primary"
                    onClick={() => handleSetPrimary(image.id)}
                    title="Set as primary"
                  >
                    ⭐
                  </button>
                )}
                <button
                  className="btn-delete-image"
                  onClick={() => handleDeleteImage(image.id)}
                  title="Delete image"
                >
                  🗑️
                </button>
              </div>
              {image.caption && <p className="image-caption">{image.caption}</p>}
            </div>
          ))}
        </div>
      )}

      {(!images || images.length === 0) && siteId && (
        <p className="no-images-text">No images uploaded yet. Click the button above to add images.</p>
      )}
    </div>
  );
};

export default SiteImageManager;
