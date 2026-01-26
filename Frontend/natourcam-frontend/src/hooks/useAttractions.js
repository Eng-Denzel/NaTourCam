import { useState, useEffect } from 'react';
import { attractionsAPI } from '../services/api';
import { handleApiError } from '../services/api';

const useAttractions = () => {
  const [attractions, setAttractions] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Fetch attractions
  const fetchAttractions = async (params = {}) => {
    try {
      setLoading(true);
      setError('');
      
      const response = await attractionsAPI.getAttractions(params);
      setAttractions(response.data);
    } catch (err) {
      const errorMessage = handleApiError(err, 'Fetch attractions');
      setError(errorMessage);
      console.error('Error fetching attractions:', errorMessage);
    } finally {
      setLoading(false);
    }
  };

  // Fetch categories
  const fetchCategories = async () => {
    try {
      const response = await attractionsAPI.getCategories();
      setCategories(response.data);
    } catch (err) {
      const errorMessage = handleApiError(err, 'Fetch categories');
      setError(errorMessage);
      console.error('Error fetching categories:', errorMessage);
    }
  };

  // Fetch attraction by ID
  const fetchAttraction = async (id) => {
    try {
      setLoading(true);
      setError('');
      
      const response = await attractionsAPI.getAttraction(id);
      return response.data;
    } catch (err) {
      const errorMessage = handleApiError(err, 'Fetch attraction');
      setError(errorMessage);
      console.error('Error fetching attraction:', errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Create attraction
  const createAttraction = async (attractionData) => {
    try {
      setLoading(true);
      setError('');
      
      const response = await attractionsAPI.createAttraction(attractionData);
      // Refresh attractions list
      fetchAttractions();
      return response.data;
    } catch (err) {
      const errorMessage = handleApiError(err, 'Create attraction');
      setError(errorMessage);
      console.error('Error creating attraction:', errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Fetch reviews for an attraction
  const fetchReviews = async (attractionId) => {
    try {
      const response = await attractionsAPI.getReviews(attractionId);
      return response.data;
    } catch (err) {
      const errorMessage = handleApiError(err, 'Fetch reviews');
      setError(errorMessage);
      console.error('Error fetching reviews:', errorMessage);
      throw err;
    }
  };

  // Create review for an attraction
  const createReview = async (reviewData) => {
    try {
      const response = await attractionsAPI.createReview(reviewData);
      return response.data;
    } catch (err) {
      const errorMessage = handleApiError(err, 'Create review');
      setError(errorMessage);
      console.error('Error creating review:', errorMessage);
      throw err;
    }
  };

  // Initialize data
  useEffect(() => {
    fetchAttractions();
    fetchCategories();
  }, []);

  return {
    attractions,
    categories,
    loading,
    error,
    fetchAttractions,
    fetchAttraction,
    createAttraction,
    fetchReviews,
    createReview,
  };
};

export default useAttractions;