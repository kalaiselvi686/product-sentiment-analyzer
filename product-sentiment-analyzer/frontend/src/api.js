import axios from 'axios';

// Configurable API URL for deployment (Vercel -> Render backend)
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 45000, // Wait up to 45 seconds for web scraping
});

export const scrapeProductReviews = async (url) => {
  try {
    const response = await api.post('/api/scrape', { url });
    return response.data;
  } catch (error) {
    if (error.response && error.response.data) {
      throw new Error(error.response.data.error || 'Failed to analyze product URL.');
    }
    throw new Error('Unable to connect to backend server. Please make sure the Flask backend is running.');
  }
};

export const getStoredProducts = async () => {
  try {
    const response = await api.get('/api/products');
    return response.data;
  } catch (error) {
    console.error('Error fetching products:', error);
    return { success: false, products: [] };
  }
};

export const analyzeSingleText = async (text) => {
  try {
    const response = await api.post('/api/analyze', { text });
    return response.data;
  } catch (error) {
    throw new Error('Single review analysis failed.');
  }
};

export default api;
