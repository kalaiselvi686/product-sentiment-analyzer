import React from 'react';

export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
        </svg>
        <span>Product Sentiment Analyzer</span>
      </div>
      <div className="navbar-badge">
        College Major Project MVP
      </div>
    </nav>
  );
}
