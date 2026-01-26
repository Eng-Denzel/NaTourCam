import React from 'react';

const Home = () => {
  return (
    <div className="home-page">
      <header className="hero-section">
        <h1>Welcome to NaTourCam</h1>
        <p>Discover amazing attractions and book unforgettable tours in Cameroon</p>
      </header>

      <section className="features-section">
        <div className="feature-card">
          <h2>Explore Attractions</h2>
          <p>Discover the most beautiful places in Cameroon</p>
        </div>
        <div className="feature-card">
          <h2>Book Tours</h2>
          <p>Find and book the perfect tour for your next adventure</p>
        </div>
        <div className="feature-card">
          <h2>Manage Bookings</h2>
          <p>View and manage all your tour bookings in one place</p>
        </div>
      </section>

      <section className="cta-section">
        <h2>Ready for your next adventure?</h2>
        <button className="cta-button">Explore Tours</button>
      </section>
    </div>
  );
};

export default Home;