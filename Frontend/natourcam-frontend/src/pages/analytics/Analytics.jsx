import React, { useState, useEffect } from 'react';

const Analytics = () => {
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState('month');

  // Mock data for analytics
  const mockAnalyticsData = {
    userStats: {
      totalBookings: 12,
      totalSpent: 850000,
      favoriteCategories: ['Mountain', 'Wildlife', 'Beach']
    },
    tourStats: {
      totalTours: 24,
      averageRating: 4.7,
      totalRevenue: 24500000
    },
    bookingStats: {
      totalBookings: 128,
      revenue: 18500000,
      topDestinations: [
        { name: 'Mount Cameroon', bookings: 32 },
        { name: 'Waza National Park', bookings: 28 },
        { name: 'Kribi Beach', bookings: 24 }
      ]
    },
    systemStats: {
      totalUsers: 1240,
      totalAttractions: 42,
      totalTours: 36
    }
  };

  useEffect(() => {
    // TODO: Fetch analytics data from API
    setTimeout(() => {
      setAnalyticsData(mockAnalyticsData);
      setLoading(false);
    }, 1000);
  }, [timeRange]);

  if (loading) {
    return <div className="loading">Loading analytics...</div>;
  }

  return (
    <div className="analytics-page">
      <div className="page-header">
        <h2>Analytics Dashboard</h2>
        <div className="filters">
          <select 
            value={timeRange} 
            onChange={(e) => setTimeRange(e.target.value)}
            className="filter-select"
          >
            <option value="week">Last 7 Days</option>
            <option value="month">Last 30 Days</option>
            <option value="quarter">Last 90 Days</option>
            <option value="year">Last Year</option>
          </select>
        </div>
      </div>

      <div className="analytics-grid">
        <div className="analytics-card">
          <h3>User Statistics</h3>
          <div className="stat-item">
            <span className="stat-label">Total Bookings:</span>
            <span className="stat-value">{analyticsData.userStats.totalBookings}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Total Spent:</span>
            <span className="stat-value">FCFA {analyticsData.userStats.totalSpent.toLocaleString()}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Favorite Categories:</span>
            <span className="stat-value">{analyticsData.userStats.favoriteCategories.join(', ')}</span>
          </div>
        </div>

        <div className="analytics-card">
          <h3>Tour Statistics</h3>
          <div className="stat-item">
            <span className="stat-label">Total Tours:</span>
            <span className="stat-value">{analyticsData.tourStats.totalTours}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Average Rating:</span>
            <span className="stat-value">{analyticsData.tourStats.averageRating} ★</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Total Revenue:</span>
            <span className="stat-value">FCFA {analyticsData.tourStats.totalRevenue.toLocaleString()}</span>
          </div>
        </div>

        <div className="analytics-card">
          <h3>Booking Statistics</h3>
          <div className="stat-item">
            <span className="stat-label">Total Bookings:</span>
            <span className="stat-value">{analyticsData.bookingStats.totalBookings}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Revenue:</span>
            <span className="stat-value">FCFA {analyticsData.bookingStats.revenue.toLocaleString()}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Top Destinations:</span>
            <ul className="top-destinations">
              {analyticsData.bookingStats.topDestinations.map((dest, index) => (
                <li key={index}>{dest.name} ({dest.bookings} bookings)</li>
              ))}
            </ul>
          </div>
        </div>

        <div className="analytics-card">
          <h3>System Statistics</h3>
          <div className="stat-item">
            <span className="stat-label">Total Users:</span>
            <span className="stat-value">{analyticsData.systemStats.totalUsers}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Total Attractions:</span>
            <span className="stat-value">{analyticsData.systemStats.totalAttractions}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Total Tours:</span>
            <span className="stat-value">{analyticsData.systemStats.totalTours}</span>
          </div>
        </div>
      </div>

      <div className="charts-section">
        <div className="chart-container">
          <h3>Bookings Over Time</h3>
          <div className="chart-placeholder">
            {/* Chart would be rendered here using a library like Chart.js */}
            <p>Bookings trend chart would appear here</p>
          </div>
        </div>
        <div className="chart-container">
          <h3>Revenue by Category</h3>
          <div className="chart-placeholder">
            {/* Chart would be rendered here using a library like Chart.js */}
            <p>Revenue by category chart would appear here</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;