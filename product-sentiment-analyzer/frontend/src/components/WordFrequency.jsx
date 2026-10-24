import React from 'react';

export default function WordFrequency({ wordFrequency }) {
  if (!wordFrequency || wordFrequency.length === 0) {
    return (
      <div className="card">
        <h3 className="card-title">Top Key Keywords</h3>
        <p style={{ color: '#64748b', fontSize: '0.9rem' }}>No word frequency data extracted.</p>
      </div>
    );
  }

  return (
    <div className="card">
      <h3 className="card-title">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" strokeWidth="2">
          <path d="M4 7V4h16v3M9 20h6M12 4v16"/>
        </svg>
        Most Frequently Mentioned Words
      </h3>
      <p style={{ color: '#64748b', fontSize: '0.875rem', marginBottom: '16px' }}>
        Key terms extracted from review texts after removing stop words:
      </p>

      <div className="word-cloud-container">
        {wordFrequency.map((item, index) => (
          <div key={index} className="word-chip">
            <span><strong>{item.word}</strong></span>
            <span className="word-count-badge">{item.count}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
