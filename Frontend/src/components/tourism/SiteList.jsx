import React, { useState, useEffect } from 'react';
import { tourismAPI } from '../../services/api';
import SiteCard from './SiteCard';

const SiteList = () => {
  const [sites, setSites] = useState([]);
  const [regions, setRegions] = useState([]);
  const [selectedRegion, setSelectedRegion] = useState('');
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
        console.log('Fetching sites...');
        const response = await tourismAPI.getSites(selectedRegion);
        console.log('Sites response:', response);
        console.log('Sites data:', response.data);
        setSites(response.data);
        console.log('Sites state updated');
      } catch (err) {
        console.error('Error fetching sites:', err);
        console.error('Error response:', err.response);
        setError('Failed to fetch tourist sites: ' + (err.response?.data?.detail || err.message));
      } finally {
        setLoading(false);
      }
    };

    fetchSites();
  }, [selectedRegion]);

  const handleRegionChange = (event) => {
    setSelectedRegion(event.target.value);
  };

  if (loading && sites.length === 0) {
    return <div className="loading">Loading tourist sites...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="site-list-container">
      <h2>Explore Tourist Sites</h2>
      <div className="filters">
        <select value={selectedRegion} onChange={handleRegionChange}>
          <option value="">All Regions</option>
          {regions.map((region) => (
            <option key={region.id} value={region.id}>
              {region.name}
            </option>
          ))}
        </select>
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