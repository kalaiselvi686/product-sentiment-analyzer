import React, { useState } from 'react';

export default function ReviewList({ reviews }) {
  const [filter, setFilter] = useState('ALL');

  if (!reviews || reviews.length === 0) {
    return (
      <div className="card">
        <h3 className="card-title">Product Reviews</h3>
        <p style={{ color: '#64748b' }}>No reviews available for display.</p>
      </div>
    );
  }

  const filteredReviews = reviews.filter((r) => {
    if (filter === 'POSITIVE') return r.sentiment === 'Positive';
    if (filter === 'NEGATIVE') return r.sentiment === 'Negative';
    if (filter === 'NEUTRAL') return r.sentiment === 'Neutral';
    return true;
  });

  const renderStars = (rating) => {
    const num = Math.min(5, Math.max(1, rating || 5));
    return '★'.repeat(num) + '☆'.repeat(5 - num);
  };

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px', marginBottom: '20px' }}>
        <h3 className="card-title" style={{ margin: 0 }}>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" strokeWidth="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
          </svg>
          Collected Customer Reviews ({filteredReviews.length})
        </h3>

        {/* Filter buttons */}
        <div style={{ display: 'flex', gap: '6px' }}>
          {['ALL', 'POSITIVE', 'NEGATIVE', 'NEUTRAL'].map((type) => (
            <button
              key={type}
              onClick={() => setFilter(type)}
              style={{
                padding: '6px 12px',
                fontSize: '0.8rem',
                borderRadius: '6px',
                border: '1px solid #cbd5e1',
                cursor: 'pointer',
                fontWeight: filter === type ? '700' : '500',
                backgroundColor: filter === type ? '#3b82f6' : '#ffffff',
                color: filter === type ? '#ffffff' : '#475569',
              }}
            >
              {type}
            </button>
          ))}
        </div>
      </div>

      <div className="review-list">
        {filteredReviews.length === 0 ? (
          <div style={{ padding: '20px', textCenter: 'center', color: '#64748b' }}>
            No reviews match the selected filter standard.
          </div>
        ) : (
          filteredReviews.map((item, index) => (
            <div key={item._id || index} className="review-item">
              <div className="review-item-header">
                <span className="review-stars">{renderStars(item.rating)}</span>
                <span className={`sentiment-tag ${item.sentiment ? item.sentiment.toLowerCase() : 'neutral'}`}>
                  {item.sentiment} ({item.sentiment_score !== undefined ? item.sentiment_score : '0.00'})
                </span>
              </div>
              <p className="review-text">{item.review_text || item.text}</p>
              <div className="review-footer">
                <span>Source: {item.source || 'Scraper'}</span>
                <span>Rating: {item.rating || 5}/5</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
