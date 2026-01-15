import React from 'react';
import { Link } from 'react-router-dom';

const SiteCard = ({ site }) => {
  console.log('SiteCard site prop:', site);
  
  if (!site) {
    return <div>Invalid site data</div>;
  }

  return (
    <div className="site-card">
      {site.images && site.images.length > 0 && (
        <div className="site-image">
          {site.images
            .filter(img => img.is_primary)
            .map(img => (
              <img
                key={img.id}
                src={img.image}
                alt={img.caption || site.name}
              />
            ))
          }
          {site.images.filter(img => img.is_primary).length === 0 && (
            <img
              src={site.images[0].image}
              alt={site.images[0].caption || site.name}
            />
          )}
        </div>
      )}
      <div className="site-info">
        <h3>{site.name || 'Unnamed Site'}</h3>
        <p>{site.description || 'No description available'}</p>
        <Link to={`/sites/${site.id}`}>View Details</Link>
      </div>
    </div>
  );
};

export default SiteCard;