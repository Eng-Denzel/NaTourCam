import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { validateForm } from '../../utils/validation';

const Profile = () => {
  const { user, updateProfile, loading, error, clearError } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    dateOfBirth: '',
    country: '',
    city: '',
    bio: ''
  });
  const [errors, setErrors] = useState({});

  // Initialize form data with user data when user is loaded
  useEffect(() => {
    if (user) {
      setFormData({
        firstName: user.first_name || user.firstName || '',
        lastName: user.last_name || user.lastName || '',
        email: user.email || '',
        phone: user.phone_number || user.phone || '',
        dateOfBirth: user.date_of_birth || user.dateOfBirth || '',
        country: user.country || '',
        city: user.city || '',
        bio: user.bio || ''
      });
    }
  }, [user]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
    
    // Clear API error when user starts typing
    if (error) {
      clearError();
    }
  };

  const validationRules = {
    firstName: [
      { type: 'required', message: 'First name is required' },
      { type: 'minLength', value: 2, message: 'First name must be at least 2 characters' }
    ],
    lastName: [
      { type: 'required', message: 'Last name is required' },
      { type: 'minLength', value: 2, message: 'Last name must be at least 2 characters' }
    ],
    email: [
      { type: 'required', message: 'Email is required' },
      { type: 'email', message: 'Please enter a valid email address' }
    ],
    phone: [
      { type: 'phone', message: 'Please enter a valid phone number' }
    ],
    dateOfBirth: [
      { type: 'date', message: 'Please enter a valid date' }
    ],
    country: [
      { type: 'required', message: 'Country is required' }
    ],
    city: [
      { type: 'required', message: 'City is required' }
    ]
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate form
    const { isValid, errors: validationErrors } = validateForm(formData, validationRules);
    
    if (!isValid) {
      setErrors(validationErrors);
      return;
    }
    
    // Clear previous errors
    setErrors({});
    
    // Attempt to update profile
    const result = await updateProfile(formData);
    
    if (result.success) {
      setIsEditing(false);
    }
  };

  // If user is not loaded, show loading state
  if (!user) {
    return <div className="loading">Loading profile...</div>;
  }

  return (
    <div className="profile-page">
      <div className="profile-header">
        <h2>User Profile</h2>
        <button 
          className="edit-button"
          onClick={() => {
            setIsEditing(!isEditing);
            // Clear errors when toggling edit mode
            setErrors({});
            if (error) clearError();
          }}
        >
          {isEditing ? 'Cancel' : 'Edit Profile'}
        </button>
      </div>

      {/* Display API errors */}
      {error && <div className="error-message">{error}</div>}

      {isEditing ? (
        <form onSubmit={handleSubmit} className="profile-form">
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="firstName">First Name:</label>
              <input
                type="text"
                id="firstName"
                name="firstName"
                value={formData.firstName}
                onChange={handleChange}
                className={errors.firstName ? 'error' : ''}
              />
              {errors.firstName && <div className="field-error">{errors.firstName}</div>}
            </div>
            <div className="form-group">
              <label htmlFor="lastName">Last Name:</label>
              <input
                type="text"
                id="lastName"
                name="lastName"
                value={formData.lastName}
                onChange={handleChange}
                className={errors.lastName ? 'error' : ''}
              />
              {errors.lastName && <div className="field-error">{errors.lastName}</div>}
            </div>
          </div>
          
          <div className="form-group">
            <label htmlFor="email">Email:</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className={errors.email ? 'error' : ''}
            />
            {errors.email && <div className="field-error">{errors.email}</div>}
          </div>
          
          <div className="form-group">
            <label htmlFor="phone">Phone:</label>
            <input
              type="tel"
              id="phone"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              className={errors.phone ? 'error' : ''}
            />
            {errors.phone && <div className="field-error">{errors.phone}</div>}
          </div>
          
          <div className="form-group">
            <label htmlFor="dateOfBirth">Date of Birth:</label>
            <input
              type="date"
              id="dateOfBirth"
              name="dateOfBirth"
              value={formData.dateOfBirth}
              onChange={handleChange}
              className={errors.dateOfBirth ? 'error' : ''}
            />
            {errors.dateOfBirth && <div className="field-error">{errors.dateOfBirth}</div>}
          </div>
          
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="country">Country:</label>
              <input
                type="text"
                id="country"
                name="country"
                value={formData.country}
                onChange={handleChange}
                className={errors.country ? 'error' : ''}
              />
              {errors.country && <div className="field-error">{errors.country}</div>}
            </div>
            <div className="form-group">
              <label htmlFor="city">City:</label>
              <input
                type="text"
                id="city"
                name="city"
                value={formData.city}
                onChange={handleChange}
                className={errors.city ? 'error' : ''}
              />
              {errors.city && <div className="field-error">{errors.city}</div>}
            </div>
          </div>
          
          <div className="form-group">
            <label htmlFor="bio">Bio:</label>
            <textarea
              id="bio"
              name="bio"
              value={formData.bio}
              onChange={handleChange}
              rows="4"
              className={errors.bio ? 'error' : ''}
            />
            {errors.bio && <div className="field-error">{errors.bio}</div>}
          </div>
          
          <button type="submit" className="save-button" disabled={loading}>
            {loading ? 'Saving...' : 'Save Changes'}
          </button>
        </form>
      ) : (
        <div className="profile-details">
          <div className="profile-field">
            <label>Name:</label>
            <span>{user.first_name} {user.last_name}</span>
          </div>
          <div className="profile-field">
            <label>Email:</label>
            <span>{user.email}</span>
          </div>
          <div className="profile-field">
            <label>Phone:</label>
            <span>{user.phone_number || 'Not provided'}</span>
          </div>
          <div className="profile-field">
            <label>Date of Birth:</label>
            <span>{user.date_of_birth || 'Not provided'}</span>
          </div>
          <div className="profile-field">
            <label>Location:</label>
            <span>{user.city || 'Not provided'}, {user.country || 'Not provided'}</span>
          </div>
          <div className="profile-field">
            <label>Bio:</label>
            <span>{user.bio || 'No bio provided'}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default Profile;