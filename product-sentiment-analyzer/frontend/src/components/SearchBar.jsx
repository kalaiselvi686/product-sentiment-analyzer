import React, { useState } from 'react';

export default function SearchBar({ onSearch, isLoading }) {
  const [inputUrl, setInputUrl] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!inputUrl.trim()) return;
    onSearch(inputUrl.trim());
  };

  const handleDemoClick = () => {
    setInputUrl('demo');
    onSearch('demo');
  };

  return (
    <div className="search-section">
      <h1>Product Sentiment Analyzer</h1>
      <p>Enter any e-commerce product URL to scrape live reviews and extract NLP sentiment intelligence.</p>

      <form onSubmit={handleSubmit} className="search-form">
        <input
          type="text"
          className="search-input"
          placeholder="Paste Product URL (e.g., https://amazon.com/dp/... or type 'demo')"
          value={inputUrl}
          onChange={(e) => setInputUrl(e.target.value)}
          disabled={isLoading}
        />
        <button type="submit" className="search-btn" disabled={isLoading || !inputUrl.trim()}>
          {isLoading ? (
            <>
              <span>Analyzing...</span>
            </>
          ) : (
            <>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
              <span>Analyze Product</span>
            </>
          )}
        </button>
      </form>

      <button onClick={handleDemoClick} className="demo-link-btn" disabled={isLoading}>
        ⚡ Quick Demo Mode (Loads pre-analyzed sample reviews)
      </button>
    </div>
  );
}
