import React from 'react';
import { Link } from 'react-router-dom';
import './Homepage.css';

const Homepage = () => {
  console.log('Rendering Homepage');
  return (
    <div className="homepage">
      <header className="hero-section">
        <div className="hero-content">
          <h1>Welcome to NaTourCam</h1>
          <p>Discover the beauty of Cameroon's tourist sites</p>
          <Link to="/sites" className="btn btn-primary">
            Explore Sites
          </Link>
        </div>
      </header>

      <section className="features-section">
        <div className="container">
          <h2>Why Choose NaTourCam?</h2>
          <div className="features-grid">
            <div className="feature-card">
              <h3>Discover Hidden Gems</h3>
              <p>Find unique tourist destinations across Cameroon</p>
            </div>
            <div className="feature-card">
              <h3>Easy Booking</h3>
              <p>Book your visits with our simple booking system</p>
            </div>
            <div className="feature-card">
              <h3>Local Experiences</h3>
              <p>Experience authentic Cameroonian culture</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Homepage;