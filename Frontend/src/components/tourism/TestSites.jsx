import React, { useState, useEffect } from 'react';
import { tourismAPI } from '../../services/api';

const TestSites = () => {
  const [sites, setSites] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSites = async () => {
      try {
        setLoading(true);
        const response = await tourismAPI.getSites();
        setSites(response.data);
        console.log('Sites data:', response.data);
      } catch (err) {
        setError('Failed to fetch tourist sites: ' + err.message);
        console.error('Error fetching sites:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchSites();
  }, []);

  if (loading) {
    return <div>Loading tourist sites...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <h2>Test Sites</h2>
      <pre>{JSON.stringify(sites, null, 2)}</pre>
    </div>
  );
};

export default TestSites;