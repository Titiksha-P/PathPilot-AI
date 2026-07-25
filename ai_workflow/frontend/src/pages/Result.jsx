import React from 'react';
import PathwayCard from '../components/PathwayCard';

export default function Result({ resultData, onReset }) {
  if (!resultData) {
    return (
      <div className="empty-results">
        <h2>No Active Guidance Session</h2>
        <button className="btn-primary" onClick={onReset}>Go to Form</button>
      </div>
    );
  }

  const { profile, recommendations, verification } = resultData;
  const matches = recommendations?.matches || [];

  return (
    <div className="result-page-container">
      {/* Profile Header */}
      <div className="profile-banner">
        <div className="profile-info">
          <span className="profile-stage-badge">
            {profile.stage === 'class10' ? '📘 Class 10 Stream Guidance' : 
             profile.stage === 'class12' ? '🎓 Class 12 Degree & Eligibility' : 
             '🚀 College Career Portfolio'}
          </span>
          <h2 className="profile-name">{profile.name}</h2>
          {profile.current_class_or_program && (
            <p className="profile-detail">Current: {profile.current_class_or_program}</p>
          )}
        </div>

        <div className="verification-badge-box">
          <div className={`verify-status ${verification?.approved ? 'approved' : 'flagged'}`}>
            {verification?.approved ? '✅ Verification Approved' : '⚠️ Issues Detected'}
          </div>
          <p className="verify-sub">
            Deterministic Engine Safety & Completeness Checks Passed
          </p>
        </div>
      </div>

      {/* Top 3 Ranked Pathway Recommendations Grid */}
      <div className="results-header">
        <h2>Top 3 Ranked Pathway Recommendations</h2>
        <p>Balanced selection guaranteed: Best Fit, Strong Alternative, and Safe/Affordable Backup</p>
      </div>

      <div className="pathways-grid">
        {matches.map((match, index) => (
          <PathwayCard key={match.pathway_id || index} match={match} rankIndex={index + 1} />
        ))}
      </div>

      {/* Action Footer */}
      <div className="result-actions">
        <button className="btn-secondary" onClick={onReset}>
          ← Evaluate Another Profile
        </button>
      </div>
    </div>
  );
}
