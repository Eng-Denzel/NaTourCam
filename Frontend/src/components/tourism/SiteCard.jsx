import React from 'react';
import { Link } from 'react-router-dom';

const SiteCard = ({ site }) => {
  console.log('SiteCard site prop:', site);
  
  if (!site) {
    return <div>Invalid site data</div>;
  }

  return (
    <div className="site-card">
      <div className="site-info">
        <h3>{site.name || 'Unnamed Site'}</h3>
        <p>{site.description || 'No description available'}</p>
        <Link to={`/sites/${site.id}`}>View Details</Link>
      </div>
    </div>
  );
};

export default SiteCard;