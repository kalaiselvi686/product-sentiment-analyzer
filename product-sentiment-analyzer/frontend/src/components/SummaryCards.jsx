import React from 'react';

export default function SummaryCards({ summary }) {
  if (!summary) return null;

  return (
    <div className="summary-grid">
      <div className="stat-card">
        <div className="stat-title">Total Reviews</div>
        <div className="stat-value">{summary.total_reviews}</div>
        <div className="stat-sub">Analyzed by VADER</div>
      </div>

      <div className="stat-card positive">
        <div className="stat-title">Positive Sentiment</div>
        <div className="stat-value">{summary.positive_pct}%</div>
        <div className="stat-sub">{summary.positive} positive reviews</div>
      </div>

      <div className="stat-card negative">
        <div className="stat-title">Negative Sentiment</div>
        <div className="stat-value">{summary.negative_pct}%</div>
        <div className="stat-sub">{summary.negative} negative reviews</div>
      </div>

      <div className="stat-card neutral">
        <div className="stat-title">Neutral Sentiment</div>
        <div className="stat-value">{summary.neutral_pct}%</div>
        <div className="stat-sub">{summary.neutral} neutral reviews</div>
      </div>
    </div>
  );
}
