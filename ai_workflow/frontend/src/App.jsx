import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import StudentForm from './pages/StudentForm';
import Result from './pages/Result';
import { submitProfile } from './services/api';
import './App.css';

export default function App() {
  const [activePage, setActivePage] = useState('home'); // 'home' | 'form' | 'result'
  const [selectedStage, setSelectedStage] = useState('class10'); // 'class10' | 'class12' | 'college'
  const [guidanceResult, setGuidanceResult] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleStartEvaluation = (stage) => {
    if (stage) setSelectedStage(stage);
    setActivePage('form');
  };

  const handleSubmitProfile = async (payload) => {
    setIsSubmitting(true);
    try {
      const data = await submitProfile(payload);
      setGuidanceResult(data);
      if (data?.profile?.stage) {
        setSelectedStage(data.profile.stage);
      }
      setActivePage('result');
    } catch (err) {
      alert(`Error running guidance matching: ${err.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleReset = () => {
    setActivePage('form');
  };

  return (
    <div className="app-container">
      <Navbar 
        activePage={activePage}
        setActivePage={setActivePage}
        selectedStage={selectedStage}
        setSelectedStage={setSelectedStage}
      />

      <main className="main-content">
        {activePage === 'home' && (
          <Home 
            onStartEvaluation={handleStartEvaluation}
            setSelectedStage={setSelectedStage}
          />
        )}

        {activePage === 'form' && (
          <StudentForm 
            selectedStage={selectedStage}
            setSelectedStage={setSelectedStage}
            onSubmitProfile={handleSubmitProfile}
            isSubmitting={isSubmitting}
          />
        )}

        {activePage === 'result' && (
          <Result 
            resultData={guidanceResult}
            onReset={handleReset}
          />
        )}
      </main>

      <Footer />
    </div>
  );
}
