import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [result, setResult] = useState(null);

  const handleClick = () => {
    const data = {
      matrix: {
        data: [
          [1, 0, 1, 1, 0],
          [0, 1, 1, 1, 0],
          [1, 1, 0, 1, 1],
          [1, 1, 0, 1, 0],
          [0, 0, 1, 0, 1]
        ]
      }
    };

    axios.post('http://localhost:8000/estimate', data)
      .then(response => {
        setResult(response.data);
      })
      .catch(error => {
        console.error(error);
      });
  };

  return (
    <div>
      <button onClick={handleClick}>Estimate</button>
      {result && (
        <div>
          <h2>Discrimination:</h2>
          <ul>
            {result.Discrimination.map((d, i) => (
              <li key={i}>{d}</li>
            ))}
          </ul>
          <h2>Difficulty:</h2>
          <ul>
            {result.Difficulty.map((d, i) => (
              <li key={i}>{d}</li>
            ))}
          </ul>
          <h2>Ability:</h2>
          <ul>
            {result.Ability.map((a, i) => (
              <li key={i}>{a}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
