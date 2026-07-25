import React from 'react';

export default function PersonaQuickSelect({ onSelectPersona, isSubmitting }) {
  const sampleProfiles = [
    {
      id: 'class10',
      label: 'Class 10 Student',
      desc: 'High Math & Science scores seeking stream choice',
      badge: 'Stream Choice'
    },
    {
      id: 'class12',
      label: 'Class 12 PCB Student',
      desc: 'Biology cutoff evaluation & course eligibility',
      badge: 'Degree / Course'
    },
    {
      id: 'aryan',
      label: "Aryan's College Portfolio",
      desc: 'AI, LLM, Python & React practical evidence matching',
      badge: 'Career Matching'
    },
    {
      id: 'dashboard',
      label: 'Data & Dashboard Specialist',
      desc: 'Analytics & SQL portfolio career match',
      badge: 'College Data'
    },
    {
      id: 'ux',
      label: 'UX & Product Designer',
      desc: 'User research & UI design evidence matching',
      badge: 'College Design'
    }
  ];

  return (
    <div className="quick-select-container">
      <h3 className="quick-select-title">⚡ Instant Demo Personas</h3>
      <p className="quick-select-sub">
        Click any preset profile to instantly evaluate deterministic matching across all stages:
      </p>

      <div className="persona-grid">
        {sampleProfiles.map((p) => (
          <button
            key={p.id}
            className="persona-btn"
            disabled={isSubmitting}
            onClick={() => onSelectPersona(p.id)}
          >
            <span className="persona-badge">{p.badge}</span>
            <span className="persona-name">{p.label}</span>
            <span className="persona-desc">{p.desc}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
