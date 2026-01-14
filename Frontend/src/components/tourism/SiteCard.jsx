import React from 'react';
import { Link } from 'react-router-dom';

const SiteCard = ({ site }) => {
  return (
    <div className="site-card">
      <div className="site-image">
        {site.images && site.images.length > 0 ? (
          <img 
            src={site.images[0].image} 
            alt={site.images[0].caption || site.name} 
          />
        ) : (
          <div className="site-image-placeholder">
            <span>No Image Available</span>
          </div>
        )}
      </div>
      
      <div className="site-info">
        <h3>{site.name}</h3>
        <p className="site-region">{site.region?.name}</p>
        <p className="site-description">
          {site.description.length > 100 
            ? `${site.description.substring(0, 100)}...` 
            : site.description}
        </p>
        
        {site.entrance_fee && (
          <p className="site-price">
            Entrance Fee: ${site.entrance_fee}
          </p>
        )}
        
        <Link to={`/sites/${site.id}`} className="view-details-button">
          View Details
        </Link>
      </div>
    </div>
  );
};

export default SiteCard;