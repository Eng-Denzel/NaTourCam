import React from 'react';
import { Link } from 'react-router-dom';
import { useLanguage } from '../contexts/LanguageContext';
import './Homepage.css';

const Homepage = () => {
  const { t } = useLanguage();
  console.log('Rendering Homepage');
  return (
    <div className="homepage">
      <header className="hero-section">
        <div className="hero-content">
          <h1>{t('home.title')}</h1>
          <p>{t('home.subtitle')}</p>
          <Link to="/sites" className="btn btn-primary">
            {t('home.exploreButton')}
          </Link>
        </div>
      </header>

      <section className="features-section">
        <div className="container">
          <h2>{t('home.whyChoose')}</h2>
          <div className="features-grid">
            <div className="feature-card">
              <h3>{t('home.authenticExperiences')}</h3>
              <p>{t('home.authenticDesc')}</p>
            </div>
            <div className="feature-card">
              <h3>{t('home.easyBooking')}</h3>
              <p>{t('home.easyDesc')}</p>
            </div>
            <div className="feature-card">
              <h3>{t('home.expertGuides')}</h3>
              <p>{t('home.expertDesc')}</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Homepage;