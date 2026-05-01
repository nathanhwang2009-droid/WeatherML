import React from 'react';

function Results({ prediction }) {
  return (
    <div className="results">
      <h2>Prediction Result</h2>
      <p className="prediction-value">{prediction.toFixed(2)}</p>
    </div>
  );
}

export default Results;
