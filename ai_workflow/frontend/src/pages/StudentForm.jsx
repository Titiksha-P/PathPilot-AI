import React, { useState } from 'react';
import PersonaQuickSelect from '../components/PersonaQuickSelect';

export default function StudentForm({ selectedStage, setSelectedStage, onSubmitProfile, isSubmitting }) {
  const [formData, setFormData] = useState({
    name: 'Aarav Sharma',
    stage: selectedStage,
    current_class_or_program: 'Class 10',
    stream: 'science pcb',
    marks: {
      mathematics: 88,
      science: 85,
      english: 78,
      overall: 84
    },
    aptitude: {
      numerical: 82,
      logical: 85,
      scientific: 80
    },
    entrance_readiness: {
      neet: 75,
      jee: 60
    },
    interests: ['technology', 'engineering', 'coding', 'mathematics'],
    preferences: {
      budget: 'medium',
      work_styles: ['problem solving', 'building']
    },
    resumeText: ''
  });

  const handleStageChange = (stage) => {
    setSelectedStage(stage);
    setFormData((prev) => ({
      ...prev,
      stage,
      current_class_or_program: stage === 'class10' ? 'Class 10' : stage === 'class12' ? 'Class 12 (PCB)' : 'B.Tech CS 3rd Year'
    }));
  };

  const handleScoreChange = (category, key, value) => {
    const num = parseFloat(value) || 0;
    setFormData((prev) => ({
      ...prev,
      [category]: {
        ...prev[category],
        [key]: Math.min(100, Math.max(0, num))
      }
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.stage === 'college' && formData.resumeText.trim()) {
      onSubmitProfile({
        text: formData.resumeText,
        stage: 'college'
      });
    } else {
      const profile = {
        name: formData.name || 'Student',
        stage: formData.stage,
        current_class_or_program: formData.current_class_or_program,
        stream: formData.stream,
        marks: formData.marks,
        aptitude: formData.aptitude,
        entrance_readiness: formData.entrance_readiness,
        interests: formData.interests,
        preferences: formData.preferences,
        skills: formData.stage === 'college' ? [
          { name: "Python", level: "advanced", evidence: "Built orchestration pipeline", contexts: ["llm", "api integration"] },
          { name: "React", level: "intermediate", evidence: "Developed Web Dashboard", contexts: ["frontend", "web apps"] }
        ] : [],
        projects: formData.stage === 'college' ? [
          { name: "SIH Career Advisor", summary: "Google ADK & Gemini Engine", technologies: ["Python", "ADK", "Pydantic"], capabilities: ["AI Agents", "Orchestration"] }
        ] : []
      };
      onSubmitProfile({ profile });
    }
  };

  const handlePresetSelect = (presetId) => {
    onSubmitProfile({ preset: presetId });
  };

  return (
    <div className="form-page-container">
      <div className="form-header">
        <h2>Evaluate Student Profile</h2>
        <p>Select student stage or pick a preset persona for instant verification</p>
      </div>

      <PersonaQuickSelect 
        onSelectPersona={handlePresetSelect} 
        isSubmitting={isSubmitting} 
      />

      <div className="divider-or"><span>OR BUILD CUSTOM PROFILE</span></div>

      <form className="intake-form" onSubmit={handleSubmit}>
        <div className="form-stage-selector">
          <label className="input-label">Student Stage:</label>
          <div className="stage-radio-group">
            <button
              type="button"
              className={`stage-radio-btn ${formData.stage === 'class10' ? 'active' : ''}`}
              onClick={() => handleStageChange('class10')}
            >
              📘 Class 10
            </button>
            <button
              type="button"
              className={`stage-radio-btn ${formData.stage === 'class12' ? 'active' : ''}`}
              onClick={() => handleStageChange('class12')}
            >
              🎓 Class 12
            </button>
            <button
              type="button"
              className={`stage-radio-btn ${formData.stage === 'college' ? 'active' : ''}`}
              onClick={() => handleStageChange('college')}
            >
              🚀 College Portfolio
            </button>
          </div>
        </div>

        <div className="form-grid">
          <div className="form-group">
            <label className="input-label">Student Name</label>
            <input 
              type="text" 
              className="form-input"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            />
          </div>

          {formData.stage === 'class12' && (
            <div className="form-group">
              <label className="input-label">Current Stream</label>
              <select 
                className="form-select"
                value={formData.stream}
                onChange={(e) => setFormData({ ...formData, stream: e.target.value })}
              >
                <option value="science pcm">Science (PCM)</option>
                <option value="science pcb">Science (PCB)</option>
                <option value="science pcmb">Science (PCMB)</option>
                <option value="commerce math">Commerce with Math</option>
                <option value="humanities arts">Humanities / Arts</option>
              </select>
            </div>
          )}

          <div className="form-group">
            <label className="input-label">Budget Category</label>
            <select 
              className="form-select"
              value={formData.preferences.budget}
              onChange={(e) => setFormData({
                ...formData,
                preferences: { ...formData.preferences, budget: e.target.value }
              })}
            >
              <option value="low">Low Cost</option>
              <option value="medium">Medium Cost</option>
              <option value="high">High / Flexible</option>
            </select>
          </div>
        </div>

        {/* Dynamic Inputs Based on Stage */}
        {formData.stage !== 'college' ? (
          <div className="scores-input-section">
            <h3 className="section-subtitle">Academic & Aptitude Scores (0 to 100%)</h3>
            <div className="scores-grid">
              <div className="score-input-card">
                <label>Mathematics %</label>
                <input 
                  type="number" 
                  min="0" 
                  max="100" 
                  value={formData.marks.mathematics || 88}
                  onChange={(e) => handleScoreChange('marks', 'mathematics', e.target.value)}
                />
              </div>

              <div className="score-input-card">
                <label>Science / Physics %</label>
                <input 
                  type="number" 
                  min="0" 
                  max="100" 
                  value={formData.marks.science || 85}
                  onChange={(e) => handleScoreChange('marks', 'science', e.target.value)}
                />
              </div>

              {formData.stage === 'class12' && (
                <div className="score-input-card">
                  <label>Biology / Chem %</label>
                  <input 
                    type="number" 
                    min="0" 
                    max="100" 
                    value={formData.marks.biology || 84}
                    onChange={(e) => handleScoreChange('marks', 'biology', e.target.value)}
                  />
                </div>
              )}

              <div className="score-input-card">
                <label>Overall Marks %</label>
                <input 
                  type="number" 
                  min="0" 
                  max="100" 
                  value={formData.marks.overall || 84}
                  onChange={(e) => handleScoreChange('marks', 'overall', e.target.value)}
                />
              </div>
            </div>
          </div>
        ) : (
          <div className="college-resume-input">
            <label className="input-label">Paste Unstructured Resume / Portfolio Text</label>
            <textarea
              className="form-textarea"
              rows={5}
              placeholder="e.g. Aryan Shelar, B.Tech CSE. Built SIH Career Guidance ADK Agent using Python, Pydantic, and Gemini. Passionate about AI agents, backend automation, and React..."
              value={formData.resumeText}
              onChange={(e) => setFormData({ ...formData, resumeText: e.target.value })}
            />
          </div>
        )}

        <div className="form-actions">
          <button type="submit" className="btn-primary submit-btn" disabled={isSubmitting}>
            {isSubmitting ? '⏳ Processing Engine...' : '⚡ Run Guidance Matcher'}
          </button>
        </div>
      </form>
    </div>
  );
}
