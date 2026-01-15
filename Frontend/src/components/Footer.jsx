import React from 'react';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-section">
          <h3>NaTourCam</h3>
          <p>Discover the beauty of Cameroon's tourist sites with our comprehensive guide and booking system.</p>
          <div className="social-links">
            <a href="#" aria-label="Facebook">FB</a>
            <a href="#" aria-label="Twitter">TW</a>
            <a href="#" aria-label="Instagram">IG</a>
          </div>
        </div>
        
        <div className="footer-section">
          <h4>Quick Links</h4>
          <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/sites">Tourist Sites</a></li>
            <li><a href="/dashboard">Dashboard</a></li>
          </ul>
        </div>
        
        <div className="footer-section">
          <h4>Contact Us</h4>
          <address>
            <p>Email: info@natourcam.com</p>
            <p>Phone: +237 123 456 789</p>
            <p>Address: Yaoundé, Cameroon</p>
          </address>
        </div>
      </div>
      
      <div className="footer-bottom">
        <p>© {new Date().getFullYear()} NaTourCam. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;