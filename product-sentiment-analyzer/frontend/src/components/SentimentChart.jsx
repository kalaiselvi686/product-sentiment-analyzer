import React from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const COLORS = ['#22c55e', '#ef4444', '#eab308'];

export default function SentimentChart({ summary }) {
  if (!summary) return null;

  const data = [
    { name: 'Positive', value: summary.positive },
    { name: 'Negative', value: summary.negative },
    { name: 'Neutral', value: summary.neutral },
  ].filter(item => item.value > 0);

  return (
    <div className="card">
      <h3 className="card-title">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" strokeWidth="2">
          <path d="M21.21 15.89A10 10 0 1 1 8 2.83"></path>
          <path d="M22 12A10 10 0 0 0 12 2v10z"></path>
        </svg>
        Sentiment Distribution
      </h3>
      <div style={{ width: '100%', height: 280 }}>
        {data.length > 0 ? (
          <ResponsiveContainer>
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={95}
                paddingAngle={4}
                dataKey="value"
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
              >
                {data.map((entry, index) => (
                  <Cell 
                    key={`cell-${index}`} 
                    fill={entry.name === 'Positive' ? COLORS[0] : entry.name === 'Negative' ? COLORS[1] : COLORS[2]} 
                  />
                ))}
              </Pie>
              <Tooltip formatter={(value) => [`${value} reviews`, 'Count']} />
              <Legend verticalAlign="bottom" height={36} />
            </PieChart>
          </ResponsiveContainer>
        ) : (
          <div style={{ textAlign: 'center', paddingTop: '100px', color: '#64748b' }}>
            No sentiment data available
          </div>
        )}
      </div>
    </div>
  );
}
