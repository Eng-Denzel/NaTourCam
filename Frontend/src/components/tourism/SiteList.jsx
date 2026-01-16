import React, { useState, useEffect } from 'react';
import { tourismAPI } from '../../services/api';
import SiteCard from './SiteCard';

const SiteList = () => {
  const [sites, setSites] = useState([]);
  const [regions, setRegions] = useState([]);
  const [selectedRegion, setSelectedRegion] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRegions = async () => {
      try {
        const response = await tourismAPI.getRegions();
        setRegions(response.data);
      } catch (err) {
        console.error('Error fetching regions:', err);
      }
    };

    fetchRegions();
  }, []);

  useEffect(() => {
    const fetchSites = async () => {
      try {
        setLoading(true);
        const params = {};
        
        // Add region filter if selected
        if (selectedRegion) {
          params.region = selectedRegion;
        }
        
        // Add search query if provided
        if (searchQuery) {
          params.search = searchQuery;
        }
        
        console.log('Fetching sites with params:', params);
        const response = await tourismAPI.getSites(params);
        console.log('Sites response:', response.data);
        setSites(response.data);
      } catch (err) {
        console.error('Error fetching sites:', err);
        setError('Failed to fetch tourist sites: ' + (err.response?.data?.detail || err.message));
      } finally {
        setLoading(false);
      }
    };

    // Debounce search to avoid too many API calls
    const timeoutId = setTimeout(() => {
      fetchSites();
    }, 300);

    return () => clearTimeout(timeoutId);
  }, [selectedRegion, searchQuery]);

  const handleRegionChange = (event) => {
    setSelectedRegion(event.target.value);
  };

  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
  };

  const handleClearFilters = () => {
    setSelectedRegion('');
    setSearchQuery('');
  };

  if (loading && sites.length === 0) {
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
          <div className="search-container">
            <input
              type="text"
              placeholder="🔍 Search sites..."
              value={searchQuery}
              onChange={handleSearchChange}
              className="search-input"
            />
          </div>
          <div className="region-filter-container">
            <select 
              value={selectedRegion} 
              onChange={handleRegionChange}
              className="region-filter"
            >
              <option value="">📍 All Regions</option>
              {regions.map((region) => (
                <option key={region.id} value={region.id}>
                  {region.name}
                </option>
              ))}
            </select>
          </div>
          {(selectedRegion || searchQuery) && (
            <button onClick={handleClearFilters} className="clear-filters-button">
              ✕ Clear Filters
            </button>
          )}
        </div>
      </div>
      
      {loading ? (
        <div className="loading">Loading sites...</div>
      ) : (
        <>
          <div className="results-info">
            <p>Found {sites.length} tourist site{sites.length !== 1 ? 's' : ''}</p>
          </div>
          <div className="site-list">
            {sites.length > 0 ? (
              sites.map((site) => (
                <SiteCard key={site.id} site={site} />
              ))
            ) : (
              <div className="no-results">
                <p>No tourist sites found matching your criteria.</p>
                <button onClick={handleClearFilters} className="browse-all-button">
                  Browse All Sites
                </button>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default SiteList;