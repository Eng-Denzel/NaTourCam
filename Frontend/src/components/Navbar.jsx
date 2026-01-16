import React, { useState, useRef, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';

const Navbar = () => {
  const { user, logout } = useAuth();
  const { language, toggleLanguage, t } = useLanguage();
  const navigate = useNavigate();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setDropdownOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const toggleDropdown = () => {
    setDropdownOpen(!dropdownOpen);
  };

  const closeDropdown = () => {
    setDropdownOpen(false);
  };

  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/" className="nav-logo">
          NaTourCam
        </Link>
        
        <ul className="nav-menu">
          <li className="nav-item">
            <Link to="/" className="nav-link">
              {t('nav.home')}
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/sites" className="nav-link">
              {t('nav.sites')}
            </Link>
          </li>
          
          {user ? (
            <>
              <li className="nav-item">
                <Link to="/dashboard" className="nav-link">
                  {t('nav.bookings')}
                </Link>
              </li>
              {user.is_superuser && (
                <li className="nav-item">
                  <Link to="/admin" className="nav-link admin-link">
                    🛡️ {t('nav.admin')}
                  </Link>
                </li>
              )}
              <li className="nav-item profile-dropdown" ref={dropdownRef}>
                <button 
                  onClick={toggleDropdown} 
                  className="nav-link btn-link profile-button"
                >
                  <span className="profile-icon">👤</span>
                  {user.first_name || user.username}
                  <span className={`dropdown-arrow ${dropdownOpen ? 'open' : ''}`}>▼</span>
                </button>
                
                {dropdownOpen && (
                  <div className="dropdown-menu">
                    <Link 
                      to="/profile" 
                      className="dropdown-item"
                      onClick={closeDropdown}
                    >
                      <span className="dropdown-icon">👤</span>
                      {t('nav.profile')}
                    </Link>
                    <Link 
                      to="/bookings" 
                      className="dropdown-item"
                      onClick={closeDropdown}
                    >
                      <span className="dropdown-icon">📅</span>
                      {t('nav.bookings')}
                    </Link>
                    <Link 
                      to="/dashboard" 
                      className="dropdown-item"
                      onClick={closeDropdown}
                    >
                      <span className="dropdown-icon">📊</span>
                      Dashboard
                    </Link>
                    <div className="dropdown-divider"></div>
                    <button 
                      onClick={() => {
                        closeDropdown();
                        handleLogout();
                      }} 
                      className="dropdown-item logout-item"
                    >
                      <span className="dropdown-icon">🚪</span>
                      {t('nav.logout')}
                    </button>
                  </div>
                )}
              </li>
            </>
          ) : (
            <>
              <li className="nav-item">
                <Link to="/login" className="nav-link">
                  {t('nav.login')}
                </Link>
              </li>
              <li className="nav-item">
                <Link to="/register" className="nav-link">
                  {t('nav.register')}
                </Link>
              </li>
            </>
          )}
          
          {/* Language Toggle Button */}
          <li className="nav-item">
            <button 
              onClick={toggleLanguage} 
              className="nav-link btn-link language-toggle"
              title={language === 'en' ? 'Switch to French' : 'Passer à l\'anglais'}
            >
              {language === 'en' ? '🇫🇷 FR' : '🇬🇧 EN'}
            </button>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;