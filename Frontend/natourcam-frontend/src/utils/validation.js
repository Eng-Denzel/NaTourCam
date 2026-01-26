// Validation utility functions

export const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
};

export const validatePassword = (password) => {
  // At least 8 characters, one uppercase, one lowercase, one number
  const re = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$/;
  return re.test(password);
};

export const validatePhone = (phone) => {
  // Cameroon phone number format
  const re = /^(\+237|237)?[2368]\d{7,8}$/;
  return re.test(phone);
};

export const validateRequired = (value) => {
  return value && value.trim().length > 0;
};

export const validateDate = (date) => {
  return !isNaN(Date.parse(date));
};

export const validateNumber = (number) => {
  return !isNaN(parseFloat(number)) && isFinite(number) && parseFloat(number) > 0;
};

// Form validation function
export const validateForm = (formData, rules) => {
  const errors = {};

  for (const field in rules) {
    const value = formData[field];
    const fieldRules = rules[field];
    
    for (const rule of fieldRules) {
      switch (rule.type) {
        case 'required':
          if (!validateRequired(value)) {
            errors[field] = rule.message || `${field} is required`;
          }
          break;
        case 'email':
          if (value && !validateEmail(value)) {
            errors[field] = rule.message || 'Please enter a valid email';
          }
          break;
        case 'password':
          if (value && !validatePassword(value)) {
            errors[field] = rule.message || 'Password must be at least 8 characters with uppercase, lowercase and number';
          }
          break;
        case 'phone':
          if (value && !validatePhone(value)) {
            errors[field] = rule.message || 'Please enter a valid phone number';
          }
          break;
        case 'date':
          if (value && !validateDate(value)) {
            errors[field] = rule.message || 'Please enter a valid date';
          }
          break;
        case 'number':
          if (value && !validateNumber(value)) {
            errors[field] = rule.message || 'Please enter a valid number';
          }
          break;
        case 'minLength':
          if (value && value.length < rule.value) {
            errors[field] = rule.message || `Minimum length is ${rule.value} characters`;
          }
          break;
        case 'maxLength':
          if (value && value.length > rule.value) {
            errors[field] = rule.message || `Maximum length is ${rule.value} characters`;
          }
          break;
        case 'custom':
          if (value && !rule.validator(value)) {
            errors[field] = rule.message || 'Invalid value';
          }
          break;
        default:
          break;
      }
      
      // If there's an error for this field, break to avoid overwriting
      if (errors[field]) break;
    }
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
};