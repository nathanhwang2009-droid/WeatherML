import React, { useState, useEffect } from 'react';
import './App.css';
import PredictionForm from './components/PredictionForm';
import Results from './components/Results';

function App() {
  const [metadata, setMetadata] = useState({ weather_codes: [], numeric_features: [] });
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('/api/metadata')
      .then(res => res.json())
      .then(data => setMetadata(data))
      .catch(err => setError('Failed to load metadata'));
  }, []);

  const handlePredict = async (formData) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      const data = await res.json();
      setPrediction(data.prediction);
    } catch (err) {
      setError('Prediction failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>WeatherML Predictor</h1>
      {error && <div className="error">{error}</div>}
      <PredictionForm 
        metadata={metadata} 
        onSubmit={handlePredict} 
        loading={loading}
      />
      {prediction !== null && <Results prediction={prediction} />}
    </div>
  );
}

export default App;
