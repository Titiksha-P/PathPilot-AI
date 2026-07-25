import React from 'react';

export default function Home({ onStartEvaluation, setSelectedStage }) {
  return (
    <div className="home-container">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-badge-pill">SIH25094 Solution • One-Stop Career & Education Engine</div>
        <h1 className="hero-title">
          Adaptive Guidance Powered by <span className="gradient-text">Verifiable Evidence</span> & Deterministic Rules
        </h1>
        <p className="hero-description">
          From Class 10 stream selection to Class 12 degree eligibility and College career portfolio matching — receive 
          auditable, non-hallucinated pathway recommendations with zero AI quota failures.
        </p>

        <div className="hero-actions">
          <button 
            className="btn-primary hero-btn"
            onClick={() => onStartEvaluation('class10')}
          >
            🚀 Evaluate Your Profile
          </button>
        </div>
      </section>

      {/* 3 Student Stages Grid */}
      <section className="stages-section">
        <h2 className="section-heading">Supported Student Stages</h2>
        <div className="stages-grid">
          <div className="stage-card">
            <div className="stage-icon">📘</div>
            <span className="stage-tag">Stage 1</span>
            <h3>Class 10 Stream Guidance</h3>
            <p>Matches academic marks, aptitude, and interest tokens to Science (PCM/PCB), Commerce, Humanities, or Vocational diplomas.</p>
            <ul className="stage-features">
              <li>✓ Subject weight scoring</li>
              <li>✓ Minimum score thresholds</li>
              <li>✓ Cost/Budget alignment</li>
            </ul>
            <button className="btn-secondary" onClick={() => onStartEvaluation('class10')}>
              Class 10 Advisor →
            </button>
          </div>

          <div className="stage-card highlight-card">
            <div className="stage-icon">🎓</div>
            <span className="stage-tag">Stage 2</span>
            <h3>Class 12 Course & Eligibility</h3>
            <p>Verifies degree requirements (MBBS, B.Tech, B.Sc, BBA, Law) with hard prerequisite checks and entrance readiness (NEET, JEE, CLAT).</p>
            <ul className="stage-features">
              <li>✓ Stream restriction checks</li>
              <li>✓ Percentage cutoffs</li>
              <li>✓ Entrance exam readiness</li>
            </ul>
            <button className="btn-primary" onClick={() => onStartEvaluation('class12')}>
              Class 12 Advisor →
            </button>
          </div>

          <div className="stage-card">
            <div className="stage-icon">🚀</div>
            <span className="stage-tag">Stage 3</span>
            <h3>College Portfolio Career Matcher</h3>
            <p>Analyzes practical project evidence, technology stack capabilities, and documented skills against real industry roles.</p>
            <ul className="stage-features">
              <li>✓ Practical context matching</li>
              <li>✓ Project evidence validation</li>
              <li>✓ Skill gap analysis</li>
            </ul>
            <button className="btn-secondary" onClick={() => onStartEvaluation('college')}>
              College Advisor →
            </button>
          </div>
        </div>
      </section>

      {/* Architecture Advantage Section */}
      <section className="architecture-section">
        <h2 className="section-heading">Why Deterministic Matching Matters</h2>
        <div className="architecture-grid">
          <div className="arch-item">
            <h4>🎯 Zero Hallucination Risk</h4>
            <p>Scoring, cutoff checks, and ranking algorithms execute strictly in deterministic Python code. Gemini is used solely to parse unstructured text into standardized JSON.</p>
          </div>

          <div className="arch-item">
            <h4>🛡️ Top-3 Balanced Selection</h4>
            <p>Always delivers 3 ranked pathways: <strong>Best Fit</strong> (highest score), <strong>Strong Alternative</strong>, and <strong>Safe / Affordable Backup</strong>.</p>
          </div>

          <div className="arch-item">
            <h4>⚡ 100% Rate Limit Safe</h4>
            <p>Intake includes exponential backoff retry for HTTP 429/503 errors and complete offline capability without needing API tokens.</p>
          </div>
        </div>
      </section>
    </div>
  );
}
