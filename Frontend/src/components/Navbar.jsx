import React, { useState, useRef, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Navbar = () => {
  const { user, logout } = useAuth();
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
              Home
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/sites" className="nav-link">
              Tourist Sites
            </Link>
          </li>
          
          {user ? (
            <>
              <li className="nav-item">
                <Link to="/dashboard" className="nav-link">
                  Dashboard
                </Link>
              </li>
              {user.is_superuser && (
                <li className="nav-item">
                  <Link to="/admin" className="nav-link admin-link">
                    🛡️ Admin
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
                      My Profile
                    </Link>
                    <Link 
                      to="/bookings" 
                      className="dropdown-item"
                      onClick={closeDropdown}
                    >
                      <span className="dropdown-icon">📅</span>
                      My Bookings
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
                      Logout
                    </button>
                  </div>
                )}
              </li>
            </>
          ) : (
            <>
              <li className="nav-item">
                <Link to="/login" className="nav-link">
                  Login
                </Link>
              </li>
              <li className="nav-item">
                <Link to="/register" className="nav-link">
                  Register
                </Link>
              </li>
            </>
          )}
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;