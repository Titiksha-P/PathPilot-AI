import React from 'react';

export default function Navbar({ activePage, setActivePage, selectedStage, setSelectedStage }) {
  return (
    <header className="navbar-container">
      <div className="navbar-content">
        <div className="brand-logo" onClick={() => setActivePage('home')}>
          <div className="logo-badge">SIH</div>
          <div className="brand-text">
            <span className="brand-title">Career & Edu Guidance</span>
            <span className="brand-sub">One-Stop Adaptive Engine</span>
          </div>
        </div>

        <nav className="nav-links">
          <button 
            className={`nav-link ${activePage === 'home' ? 'active' : ''}`}
            onClick={() => setActivePage('home')}
          >
            Home
          </button>
          <button 
            className={`nav-link ${activePage === 'form' ? 'active' : ''}`}
            onClick={() => setActivePage('form')}
          >
            Evaluate Profile
          </button>
          {activePage === 'result' && (
            <button 
              className="nav-link active result-tab"
              onClick={() => setActivePage('result')}
            >
              Guidance Results
            </button>
          )}
        </nav>

        <div className="stage-quick-pills">
          <span className="stage-pill-label">Stage:</span>
          {['class10', 'class12', 'college'].map((stage) => (
            <button
              key={stage}
              className={`stage-pill ${selectedStage === stage ? 'active' : ''}`}
              onClick={() => {
                setSelectedStage(stage);
                if (activePage !== 'form') setActivePage('form');
              }}
            >
              {stage === 'class10' ? 'Class 10' : stage === 'class12' ? 'Class 12' : 'College'}
            </button>
          ))}
        </div>
      </div>
    </header>
  );
}
