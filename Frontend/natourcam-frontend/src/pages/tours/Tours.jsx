import React, { useState, useEffect } from 'react';

const Tours = () => {
  const [tours, setTours] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  // Mock data for tours
  const mockTours = [
    {
      id: 1,
      title: 'Mount Cameroon Adventure',
      description: '7-day trekking expedition to the summit of Mount Cameroon',
      duration: 7,
      difficulty: 'Challenging',
      price: 150000,
      currency: 'FCFA',
      startDate: '2026-03-15',
      endDate: '2026-03-22',
      image: '/placeholder-tour.jpg'
    },
    {
      id: 2,
      title: 'Waza Wildlife Safari',
      description: '3-day safari tour in Waza National Park with expert guides',
      duration: 3,
      difficulty: 'Moderate',
      price: 80000,
      currency: 'FCFA',
      startDate: '2026-04-10',
      endDate: '2026-04-13',
      image: '/placeholder-tour.jpg'
    },
    {
      id: 3,
      title: 'Kribi Coastal Getaway',
      description: '5-day beach vacation with water sports and relaxation',
      duration: 5,
      difficulty: 'Easy',
      price: 120000,
      currency: 'FCFA',
      startDate: '2026-05-01',
      endDate: '2026-05-06',
      image: '/placeholder-tour.jpg'
    }
  ];

  useEffect(() => {
    // TODO: Fetch tours from API
    setTimeout(() => {
      setTours(mockTours);
      setLoading(false);
    }, 1000);
  }, []);

  const filteredTours = filter === 'all' 
    ? tours 
    : tours.filter(tour => tour.difficulty === filter);

  if (loading) {
    return <div className="loading">Loading tours...</div>;
  }

  return (
    <div className="tours-page">
      <div className="page-header">
        <h2>Tour Packages</h2>
        <div className="filters">
          <select 
            value={filter} 
            onChange={(e) => setFilter(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Difficulties</option>
            <option value="Easy">Easy</option>
            <option value="Moderate">Moderate</option>
            <option value="Challenging">Challenging</option>
            <option value="Difficult">Difficult</option>
          </select>
        </div>
      </div>

      <div className="tours-grid">
        {filteredTours.map(tour => (
          <div key={tour.id} className="tour-card">
            <img 
              src={tour.image} 
              alt={tour.title} 
              className="tour-image"
            />
            <div className="tour-info">
              <h3>{tour.title}</h3>
              <p className="tour-description">
                {tour.description}
              </p>
              <div className="tour-details">
                <div className="tour-meta">
                  <span className="tour-duration">Duration: {tour.duration} days</span>
                  <span className="tour-difficulty difficulty-{tour.difficulty.toLowerCase()}">
                    {tour.difficulty}
                  </span>
                </div>
                <div className="tour-dates">
                  <span>{tour.startDate} to {tour.endDate}</span>
                </div>
                <div className="tour-price">
                  <span>{tour.currency} {tour.price.toLocaleString()}</span>
                </div>
              </div>
              <button className="book-tour-button">Book This Tour</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Tours;