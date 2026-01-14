import React, { useState, useEffect } from 'react';
import { tourismAPI } from '../../services/api';
import SiteCard from './SiteCard';

const SiteList = () => {
  const [sites, setSites] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    search: '',
    region: '',
  });

  useEffect(() => {
    fetchSites();
  }, [filters]);

  const fetchSites = async () => {
    try {
      setLoading(true);
      const params = {};
      
      if (filters.search) {
        params.search = filters.search;
      }
      
      if (filters.region) {
        params.region = filters.region;
      }
      
      const response = await tourismAPI.getSites(params);
      setSites(response.data);
    } catch (err) {
      setError('Failed to fetch tourist sites');
      console.error('Error fetching sites:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchChange = (e) => {
    setFilters({
      ...filters,
      search: e.target.value,
    });
  };

  const handleRegionChange = (e) => {
    setFilters({
      ...filters,
      region: e.target.value,
    });
  };

  if (loading) {
    return <div className="loading">Loading tourist sites...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="site-list-container">
      <div className="site-list-header">
        <h2>Explore Tourist Sites</h2>
        
        <div className="filters">
          <input
            type="text"
            placeholder="Search sites..."
            value={filters.search}
            onChange={handleSearchChange}
            className="search-input"
          />
          
          <select
            value={filters.region}
            onChange={handleRegionChange}
            className="region-filter"
          >
            <option value="">All Regions</option>
            <option value="1">Region 1</option>
            <option value="2">Region 2</option>
          </select>
        </div>
      </div>
      
      <div className="site-list">
        {sites.length > 0 ? (
          sites.map((site) => (
            <SiteCard key={site.id} site={site} />
          ))
        ) : (
          <p>No tourist sites found.</p>
        )}
      </div>
    </div>
  );
};

export default SiteList;