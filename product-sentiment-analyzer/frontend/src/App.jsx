import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import SearchBar from './components/SearchBar';
import ProductCard from './components/ProductCard';
import SummaryCards from './components/SummaryCards';
import SentimentChart from './components/SentimentChart';
import RatingChart from './components/RatingChart';
import WordFrequency from './components/WordFrequency';
import ReviewList from './components/ReviewList';
import { scrapeProductReviews } from './api';

export default function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load initial demo dataset on page load for immediate visual presentation
  useEffect(() => {
    handleSearch('demo');
  }, []);

  const handleSearch = async (url) => {
    setLoading(true);
    setError(null);
    try {
      const result = await scrapeProductReviews(url);
      if (result.success) {
        setData(result);
      } else {
        setError(result.error || 'Unable to collect reviews from this URL. Please check the URL and try again.');
      }
    } catch (err) {
      setError(err.message || 'Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <Navbar />

      <main className="main-content">
        <SearchBar onSearch={handleSearch} isLoading={loading} />

        {/* Error Notification Banner */}
        {error && (
          <div className="error-banner">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            <span>{error}</span>
          </div>
        )}

        {/* Demo Mode Notification Banner */}
        {data && data.is_demo && !loading && (
          <div className="demo-banner">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="16" x2="12" y2="12"></line>
              <line x1="12" y1="8" x2="12.01" y2="8"></line>
            </svg>
            <span>
              <strong>Demo Mode Active:</strong> {data.notice || "Displaying pre-loaded review dataset."}
            </span>
          </div>
        )}

        {/* Loading Spinner */}
        {loading && (
          <div className="loading-container">
            <div className="spinner"></div>
            <h3 style={{ color: '#1e293b', marginBottom: '6px' }}>Analyzing Product Reviews...</h3>
            <p style={{ color: '#64748b' }}>Running Selenium scraper & VADER sentiment classification pipeline.</p>
          </div>
        )}

        {/* Dashboard Content */}
        {!loading && data && data.product && (
          <>
            <ProductCard product={data.product} />
            <SummaryCards summary={data.summary} />

            <div className="analytics-grid">
              <SentimentChart summary={data.summary} />
              <RatingChart ratingDistribution={data.summary?.rating_distribution} />
            </div>

            <WordFrequency wordFrequency={data.word_frequency} />
            <ReviewList reviews={data.reviews} />
          </>
        )}
      </main>

      <footer className="footer">
        Product Sentiment Analyzer & Review Intelligence Dashboard &copy; {new Date().getFullYear()} — Built for College Major Project
      </footer>
    </div>
  );
}
