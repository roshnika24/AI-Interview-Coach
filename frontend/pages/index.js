import { useState } from 'react';
import Head from 'next/head';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function Home() {
  const [step, setStep] = useState('config'); // config, question, feedback
  const [loading, setLoading] = useState(false);

  // Config State
  const [role, setRole] = useState('SDE');
  const [difficulty, setDifficulty] = useState('Medium');

  // Question State
  const [questionData, setQuestionData] = useState(null);
  const [userAnswer, setUserAnswer] = useState('');

  // Feedback State
  const [feedbackData, setFeedbackData] = useState(null);

  const startInterview = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/generate-question`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ role, difficulty }),
      });
      const data = await res.json();
      if (res.ok) {
        setQuestionData(data);
        setStep('question');
      } else {
        alert('Failed to generate question');
      }
    } catch (e) {
      alert('Error connecting to server. Is custom API Key set?');
    } finally {
      setLoading(false);
    }
  };

  const submitAnswer = async () => {
    if (!userAnswer.trim()) return;
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/evaluate-answer`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: questionData.question,
          role,
          difficulty,
          user_answer: userAnswer
        }),
      });
      const data = await res.json();
      if (res.ok) {
        setFeedbackData(data);
        setStep('feedback');
      } else {
        alert('Failed to evaluate answer');
      }
    } catch (e) {
      alert('Error connecting to server');
    } finally {
      setLoading(false);
    }
  };

  const nextQuestion = () => {
    setQuestionData(null);
    setUserAnswer('');
    setFeedbackData(null);
    // Directly fetch new question without going back to config
    startInterview();
  };

  const fullReset = () => {
    setQuestionData(null);
    setUserAnswer('');
    setFeedbackData(null);
    setStep('config');
  };

  return (
    <div className="min-h-screen">
      <Head>
        <title>AI Interview Coach</title>
        <meta name="description" content="Master your tech interviews with AI" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="true" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
      </Head>

      <main className="container">
        <div className="header-section">
          <h1>AI Interview Coach</h1>
          <p className="subtitle">Master your technical interviews with personalized AI feedback</p>
        </div>

        <div className="card">
          {step === 'config' && (
            <div className="animate-fade-in content-wrapper">
              <div className="form-group">
                <label>Target Role</label>
                <select value={role} onChange={(e) => setRole(e.target.value)}>
                  <option value="SDE">Software Development Engineer (SDE)</option>
                  <option value="Data Analyst">Data Analyst</option>
                  <option value="SDET">Software Development Engineer in Test (SDET)</option>
                </select>
              </div>

              <div className="form-group">
                <label>Difficulty Level</label>
                <select value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
                  <option value="Easy">Easy</option>
                  <option value="Medium">Medium</option>
                  <option value="Hard">Hard</option>
                </select>
              </div>

              <button className="primary-btn" onClick={startInterview} disabled={loading}>
                {loading ? 'Generating Interview Question...' : 'Start Interview Session'}
              </button>
            </div>
          )}

          {step === 'question' && questionData && (
            <div className="animate-slide-up content-wrapper">
              <div className="question-header">
                <span className="badge">{role}</span>
                <span className={`badge ${difficulty.toLowerCase()}`}>{difficulty}</span>
              </div>

              <div className="question-text">
                {questionData.question}
              </div>

              {questionData.context && (
                <div className="context-box">
                  <strong>Context:</strong> {questionData.context}
                </div>
              )}

              <div className="form-group">
                <label>Your Answer</label>
                <textarea
                  rows={10}
                  value={userAnswer}
                  onChange={(e) => setUserAnswer(e.target.value)}
                  placeholder="Type your detailed answer here. Focus on key concepts and examples..."
                />
              </div>

              <button className="primary-btn" onClick={submitAnswer} disabled={loading || !userAnswer.trim()}>
                {loading ? 'Analyzing Answer...' : 'Submit Response'}
              </button>
            </div>
          )}

          {step === 'feedback' && feedbackData && (
            <div className="feedback-view animate-fade-in">
              <div className="score-container">
                <div className="score-circle">
                  <span className="score-value">{feedbackData.score}</span>
                  <span className="score-label">/10</span>
                </div>
              </div>

              <div className="feedback-section">
                <h3>💡 Feedback</h3>
                <p className="feedback-text">{feedbackData.feedback}</p>
              </div>

              {feedbackData.missing_key_points && feedbackData.missing_key_points.length > 0 && (
                <div className="feedback-section">
                  <h3>⚠ Missing Key Points</h3>
                  <ul className="missing-points-list">
                    {feedbackData.missing_key_points.map((point, i) => (
                      <li key={i}>{point}</li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="feedback-section">
                <h3>✅ Model Answer</h3>
                <div className="model-answer">
                  {feedbackData.model_answer}
                </div>
              </div>

              <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
                <button className="primary-btn" onClick={nextQuestion} style={{ marginTop: 0 }}>
                  Next Question
                </button>
                <button className="secondary-btn" onClick={fullReset} style={{ marginTop: 0 }}>
                  Change Settings
                </button>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
