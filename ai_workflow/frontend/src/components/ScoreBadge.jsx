import React from 'react';

export default function ScoreBadge({ score, status, role }) {
  const getScoreColor = (val) => {
    if (val >= 85) return 'score-high';
    if (val >= 75) return 'score-medium';
    return 'score-standard';
  };

  const getStatusBadge = (st) => {
    if (st === 'eligible') return { label: 'Eligible', class: 'status-eligible' };
    if (st === 'conditionally_eligible') return { label: 'Conditional', class: 'status-conditional' };
    return { label: 'Not Eligible', class: 'status-ineligible' };
  };

  const getRoleLabel = (r) => {
    if (r === 'best_fit') return '★ Best Fit';
    if (r === 'strong_alternative') return '◈ Strong Alternative';
    return '🛡 Safe / Affordable Backup';
  };

  const statusInfo = getStatusBadge(status);

  return (
    <div className="badge-header-group">
      <span className={`role-badge role-${role}`}>
        {getRoleLabel(role)}
      </span>

      <div className="score-and-status">
        <div className={`score-ring ${getScoreColor(score)}`}>
          <span className="score-val">{score}%</span>
          <span className="score-lbl">Fit Score</span>
        </div>

        <span className={`status-tag ${statusInfo.class}`}>
          {statusInfo.label}
        </span>
      </div>
    </div>
  );
}
