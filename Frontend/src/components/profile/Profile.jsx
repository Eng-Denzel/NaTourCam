import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { authAPI } from '../../services/api';
import './Profile.css';

const Profile = () => {
  const { user, updateUser } = useAuth();
  const navigate = useNavigate();
  const [isEditing, setIsEditing] = useState(false);
  const [showPasswordChange, setShowPasswordChange] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [passwordData, setPasswordData] = useState({
    new_password: '',
    confirm_password: '',
  });
  
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone_number: '',
    date_of_birth: '',
    language: 'en',
  });

  useEffect(() => {
    if (user) {
      setFormData({
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        email: user.email || '',
        phone_number: user.phone_number || '',
        date_of_birth: user.date_of_birth || '',
        language: user.language || 'en',
      });
    }
  }, [user]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handlePasswordChange = (e) => {
    setPasswordData({
      ...passwordData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      // Validate password if changing
      if (showPasswordChange && passwordData.new_password) {
        if (passwordData.new_password !== passwordData.confirm_password) {
          setError('Passwords do not match');
          setLoading(false);
          return;
        }
        if (passwordData.new_password.length < 8) {
          setError('Password must be at least 8 characters long');
          setLoading(false);
          return;
        }
      }

      // Filter out empty optional fields
      const updateData = {};
      Object.keys(formData).forEach(key => {
        if (formData[key] !== '') {
          updateData[key] = formData[key];
        }
      });

      // Add password if changing
      if (showPasswordChange && passwordData.new_password) {
        updateData.password = passwordData.new_password;
      }

      console.log('Sending update data:', updateData);
      const response = await authAPI.updateUser(updateData);
      console.log('Update response:', response);
      
      if (response.status === 200) {
        // Update user in context
        updateUser(response.data);
        setSuccess('Profile updated successfully!');
        setIsEditing(false);
        setShowPasswordChange(false);
        setPasswordData({ new_password: '', confirm_password: '' });
        
        // Clear success message after 3 seconds
        setTimeout(() => setSuccess(null), 3000);
      }
    } catch (err) {
      console.error('Profile update error:', err);
      console.error('Error response data:', err.response?.data);
      console.error('Error response status:', err.response?.status);
      
      // Try to extract meaningful error message
      let errorMessage = 'Failed to update profile. Please try again.';
      
      if (err.response?.data) {
        if (typeof err.response.data === 'string') {
          errorMessage = err.response.data;
        } else if (err.response.data.message) {
          errorMessage = err.response.data.message;
        } else if (err.response.data.error) {
          errorMessage = err.response.data.error;
        } else {
          // Try to format validation errors
          const errors = Object.entries(err.response.data)
            .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`)
            .join('; ');
          if (errors) errorMessage = errors;
        }
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    // Reset form to original user data
    if (user) {
      setFormData({
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        email: user.email || '',
        phone_number: user.phone_number || '',
        date_of_birth: user.date_of_birth || '',
        language: user.language || 'en',
      });
    }
    setIsEditing(false);
    setShowPasswordChange(false);
    setPasswordData({ new_password: '', confirm_password: '' });
    setError(null);
  };

  if (!user) {
    return <div className="loading">Loading profile...</div>;
  }

  return (
    <div className="profile-container">
      <div className="profile-header">
        <div className="profile-title">
          <h1>My Profile</h1>
          <p className="profile-subtitle">Manage your personal information</p>
        </div>
        {!isEditing && (
          <button 
            onClick={() => setIsEditing(true)} 
            className="edit-profile-button"
          >
            ✏️ Edit Profile
          </button>
        )}
      </div>

      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}

      <div className="profile-content">
        <div className="profile-avatar-section">
          <div className="profile-avatar">
            <span className="avatar-icon">👤</span>
          </div>
          <h2>{formData.first_name} {formData.last_name}</h2>
          <p className="profile-username">@{user.username}</p>
        </div>

        <form onSubmit={handleSubmit} className="profile-form">
          <div className="form-section">
            <h3>Personal Information</h3>
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="first_name">First Name *</label>
                <input
                  type="text"
                  id="first_name"
                  name="first_name"
                  value={formData.first_name}
                  onChange={handleChange}
                  disabled={!isEditing}
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="last_name">Last Name *</label>
                <input
                  type="text"
                  id="last_name"
                  name="last_name"
                  value={formData.last_name}
                  onChange={handleChange}
                  disabled={!isEditing}
                  required
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="email">Email *</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  disabled={!isEditing}
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="phone_number">Phone Number</label>
                <input
                  type="tel"
                  id="phone_number"
                  name="phone_number"
                  value={formData.phone_number}
                  onChange={handleChange}
                  disabled={!isEditing}
                  placeholder="+237 XXX XXX XXX"
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="date_of_birth">Date of Birth</label>
              <input
                type="date"
                id="date_of_birth"
                name="date_of_birth"
                value={formData.date_of_birth}
                onChange={handleChange}
                disabled={!isEditing}
              />
            </div>
          </div>

          <div className="form-section">
            <h3>Preferences</h3>
            <div className="form-group">
              <label htmlFor="language">Preferred Language</label>
              <select
                id="language"
                name="language"
                value={formData.language}
                onChange={handleChange}
                disabled={!isEditing}
              >
                <option value="en">English</option>
                <option value="fr">French</option>
              </select>
            </div>
          </div>

          {isEditing && (
            <div className="form-section">
              <div className="password-change-header">
                <h3>Change Password</h3>
                <button
                  type="button"
                  onClick={() => setShowPasswordChange(!showPasswordChange)}
                  className="toggle-password-button"
                >
                  {showPasswordChange ? '✕ Cancel' : '🔒 Change Password'}
                </button>
              </div>
              
              {showPasswordChange && (
                <div className="password-change-fields">
                  <div className="form-group">
                    <label htmlFor="new_password">New Password *</label>
                    <input
                      type="password"
                      id="new_password"
                      name="new_password"
                      value={passwordData.new_password}
                      onChange={handlePasswordChange}
                      placeholder="Enter new password (min 8 characters)"
                      minLength="8"
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="confirm_password">Confirm Password *</label>
                    <input
                      type="password"
                      id="confirm_password"
                      name="confirm_password"
                      value={passwordData.confirm_password}
                      onChange={handlePasswordChange}
                      placeholder="Confirm new password"
                    />
                  </div>
                </div>
              )}
            </div>
          )}

          {isEditing && (
            <div className="form-actions">
              <button 
                type="button" 
                onClick={handleCancel} 
                className="cancel-button"
                disabled={loading}
              >
                Cancel
              </button>
              <button 
                type="submit" 
                className="save-button"
                disabled={loading}
              >
                {loading ? 'Saving...' : '💾 Save Changes'}
              </button>
            </div>
          )}
        </form>
      </div>
    </div>
  );
};

export default Profile;
