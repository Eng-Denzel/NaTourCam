import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { validateForm } from '../../utils/validation';

const Register = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [errors, setErrors] = useState({});
  const { register, loading, error, clearError } = useAuth();
  const navigate = useNavigate();

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
    password: [
      { type: 'required', message: 'Password is required' },
      { type: 'minLength', value: 8, message: 'Password must be at least 8 characters' }
    ],
    confirmPassword: [
      { type: 'required', message: 'Please confirm your password' }
    ]
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Basic validation for password match
    if (formData.password !== formData.confirmPassword) {
      setErrors(prev => ({
        ...prev,
        confirmPassword: 'Passwords do not match'
      }));
      return;
    }
    
    // Validate form
    const { isValid, errors: validationErrors } = validateForm(formData, validationRules);
    
    if (!isValid) {
      setErrors(validationErrors);
      return;
    }
    
    // Clear previous errors
    setErrors({});
    
    // Prepare data for API (exclude confirmPassword)
    const { confirmPassword, ...registrationData } = formData;
    
    // Attempt registration
    const result = await register(registrationData);
    
    if (result.success) {
      navigate('/login');
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-container">
        <h2>Create an Account</h2>
        
        {/* Display validation errors */}
        {Object.keys(errors).length > 0 && (
          <div className="error-message">
            Please correct the following errors:
            <ul>
              {Object.entries(errors).map(([field, message]) => (
                <li key={field}>{message}</li>
              ))}
            </ul>
          </div>
        )}
        
        {/* Display API errors */}
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit} className="auth-form">
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
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              className={errors.password ? 'error' : ''}
            />
            {errors.password && <div className="field-error">{errors.password}</div>}
          </div>
          
          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password:</label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              className={errors.confirmPassword ? 'error' : ''}
            />
            {errors.confirmPassword && <div className="field-error">{errors.confirmPassword}</div>}
          </div>
          
          <button type="submit" className="auth-button" disabled={loading}>
            {loading ? 'Registering...' : 'Register'}
          </button>
        </form>
        
        <p className="auth-switch">
          Already have an account? <Link to="/login">Login here</Link>
        </p>
      </div>
    </div>
  );
};

export default Register;