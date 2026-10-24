import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export default function RatingChart({ ratingDistribution }) {
  if (!ratingDistribution) return null;

  const data = [
    { rating: '1 Star', count: ratingDistribution[1] || 0 },
    { rating: '2 Stars', count: ratingDistribution[2] || 0 },
    { rating: '3 Stars', count: ratingDistribution[3] || 0 },
    { rating: '4 Stars', count: ratingDistribution[4] || 0 },
    { rating: '5 Stars', count: ratingDistribution[5] || 0 },
  ];

  const barColors = ['#ef4444', '#f97316', '#eab308', '#84cc16', '#22c55e'];

  return (
    <div className="card">
      <h3 className="card-title">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" strokeWidth="2">
          <line x1="18" y1="20" x2="18" y2="10"></line>
          <line x1="12" y1="20" x2="12" y2="4"></line>
          <line x1="6" y1="20" x2="6" y2="14"></line>
        </svg>
        Rating Breakdown (1-5 Stars)
      </h3>
      <div style={{ width: '100%', height: 280 }}>
        <ResponsiveContainer>
          <BarChart data={data} margin={{ top: 20, right: 20, left: -10, bottom: 20 }}>
            <XAxis dataKey="rating" tickLine={false} />
            <YAxis allowDecimals={false} />
            <Tooltip formatter={(value) => [`${value} reviews`, 'Count']} />
            <Bar dataKey="count" radius={[6, 6, 0, 0]}>
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={barColors[index]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
