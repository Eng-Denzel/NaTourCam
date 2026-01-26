import React, { useState } from 'react';
import useAttractions from '../../hooks/useAttractions';

const Attractions = () => {
  const { attractions, categories, loading, error } = useAttractions();
  const [filter, setFilter] = useState('all');

  const filteredAttractions = filter === 'all' 
    ? attractions 
    : attractions.filter(attraction => attraction.category?.name === filter);

  if (loading && attractions.length === 0) {
    return <div className="loading">Loading attractions...</div>;
  }

  if (error) {
    return <div className="error-message">Error: {error}</div>;
  }

  return (
    <div className="attractions-page">
      <div className="page-header">
        <h2>Tourist Attractions</h2>
        <div className="filters">
          <select 
            value={filter} 
            onChange={(e) => setFilter(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Categories</option>
            {categories.map(category => (
              <option key={category.id} value={category.name}>
                {category.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {attractions.length === 0 && !loading ? (
        <div className="no-data">
          <p>No attractions found.</p>
        </div>
      ) : (
        <div className="attractions-grid">
          {filteredAttractions.map(attraction => (
            <div key={attraction.id} className="attraction-card">
              <img 
                src={attraction.images?.[0]?.image || '/placeholder-image.jpg'} 
                alt={attraction.name} 
                className="attraction-image"
              />
              <div className="attraction-info">
                <h3>{attraction.name}</h3>
                <p className="attraction-location">
                  {attraction.city}, {attraction.country}
                </p>
                <p className="attraction-description">
                  {attraction.description}
                </p>
                <div className="attraction-details">
                  <span className="attraction-category">
                    {attraction.category?.name || 'Uncategorized'}
                  </span>
                  <span className="attraction-rating">
                    ★ {attraction.analytics?.average_rating || 'N/A'}
                  </span>
                  <span className="attraction-price">
                    {attraction.entry_fee > 0 ? `Entry: FCFA ${attraction.entry_fee}` : 'Free Entry'}
                  </span>
                </div>
                <button className="view-details-button">View Details</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Attractions;