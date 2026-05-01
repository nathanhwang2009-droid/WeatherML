import React, { useState } from 'react';

function PredictionForm({ metadata, onSubmit, loading }) {
  const [formData, setFormData] = useState({
    date: '',
    weather_code: metadata.weather_codes[0] || '',
    ...Object.fromEntries(metadata.numeric_features.map(f => [f, '0'])),
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.date) {
      alert('Date is required');
      return;
    }
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Date
        <input 
          type="date" 
          name="date" 
          value={formData.date}
          onChange={handleChange}
          required 
        />
      </label>

      <label>
        Weather code
        <select 
          name="weather_code" 
          value={formData.weather_code}
          onChange={handleChange}
        >
          {metadata.weather_codes.map(code => (
            <option key={code} value={code}>{code}</option>
          ))}
        </select>
      </label>

      <div className="grid">
        {metadata.numeric_features.map(feature => (
          <label key={feature}>
            {feature}
            <input 
              type="number" 
              step="any" 
              name={feature}
              value={formData[feature]}
              onChange={handleChange}
              required 
            />
          </label>
        ))}
      </div>

      <button type="submit" disabled={loading}>
        {loading ? 'Predicting...' : 'Predict'}
      </button>
    </form>
  );
}

export default PredictionForm;
