import React from 'react';
import ScoreBadge from './ScoreBadge';

export default function PathwayCard({ match, rankIndex }) {
  return (
    <div className={`pathway-card card-rank-${rankIndex}`}>
      <ScoreBadge 
        score={match.score} 
        status={match.eligibility_status} 
        role={match.rank_role} 
      />

      <h3 className="pathway-title">{match.title}</h3>
      <div className="pathway-meta">
        <span className="meta-item">⏳ {match.estimated_duration}</span>
        <span className="meta-item">💰 Cost: <strong className="cost-tag">{match.cost_category}</strong></span>
      </div>

      <div className="card-section">
        <h4 className="section-label">Why it matches</h4>
        <ul className="bullet-list">
          {match.reasons.map((reason, i) => (
            <li key={i}>{reason}</li>
          ))}
        </ul>
      </div>

      <div className="card-section">
        <h4 className="section-label">Student Evidence & Proof</h4>
        <div className="evidence-box">
          {match.evidence.map((ev, i) => (
            <div key={i} className="evidence-chip">
              🔍 {ev}
            </div>
          ))}
        </div>
      </div>

      {match.missing_requirements && match.missing_requirements.length > 0 && (
        <div className="card-section warning-box">
          <h4 className="section-label warn-title">⚠️ Action Required / Missing Prerequisites</h4>
          <ul className="bullet-list warn-list">
            {match.missing_requirements.map((req, i) => (
              <li key={i}>{req}</li>
            ))}
          </ul>
        </div>
      )}

      {match.risks_tradeoffs && match.risks_tradeoffs.length > 0 && (
        <div className="card-section">
          <h4 className="section-label">⚖️ Tradeoffs & Considerations</h4>
          <ul className="bullet-list muted-list">
            {match.risks_tradeoffs.map((tradeoff, i) => (
              <li key={i}>{tradeoff}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="card-section next-actions-box">
        <h4 className="section-label action-title">🚀 Immediate Next Steps</h4>
        <ol className="ordered-list">
          {match.next_actions.map((act, i) => (
            <li key={i}>{act}</li>
          ))}
        </ol>
      </div>

      {match.related_outcomes && match.related_outcomes.length > 0 && (
        <div className="card-tags">
          {match.related_outcomes.map((out, i) => (
            <span key={i} className="outcome-tag">🎯 {out}</span>
          ))}
        </div>
      )}
    </div>
  );
}
