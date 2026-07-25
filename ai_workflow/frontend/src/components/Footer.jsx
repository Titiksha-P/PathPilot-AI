import React from 'react';

export default function Footer() {
  return (
    <footer className="footer-container">
      <div className="footer-content">
        <p className="footer-title">SIH25094 — Adaptive Career & Education Guidance Engine</p>
        <p className="footer-sub">
          Hybrid LLM Profile Parser + 100% Deterministic Verification & Matching Engine
        </p>
        <div className="footer-badges">
          <span className="tech-badge">Google ADK</span>
          <span className="tech-badge">Gemini AI</span>
          <span className="tech-badge">Deterministic Python Engine</span>
          <span className="tech-badge">Pydantic Schemas</span>
        </div>
      </div>
    </footer>
  );
}
