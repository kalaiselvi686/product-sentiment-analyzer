import React from 'react';

export default function ProductCard({ product }) {
  if (!product) return null;

  return (
    <div className="card product-header-card">
      <div>
        <h2 className="product-title-text">{product.name || 'Analyzed Product'}</h2>
        <div className="product-meta">
          <span>Source: <strong>{product.source || 'Web Scraper'}</strong></span>
          {product.url && (
            <span>
              URL:{' '}
              <a href={product.url} target="_blank" rel="noreferrer" style={{ color: '#3b82f6', textDecoration: 'none' }}>
                {product.url.length > 50 ? product.url.substring(0, 50) + '...' : product.url}
              </a>
            </span>
          )}
        </div>
      </div>

      <div style={{ textAlign: 'right' }}>
        <div style={{ fontSize: '1.75rem', fontWeight: 'bold', color: '#1e293b' }}>
          ★ {product.rating ? Number(product.rating).toFixed(1) : 'N/A'} <span style={{ fontSize: '1rem', color: '#64748b' }}>/ 5</span>
        </div>
        <div style={{ fontSize: '0.875rem', color: '#64748b' }}>
          Based on {product.total_reviews || 0} reviews
        </div>
      </div>
    </div>
  );
}
