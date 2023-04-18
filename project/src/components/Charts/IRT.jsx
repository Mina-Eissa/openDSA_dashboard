import React, { useState } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import { create, all } from 'mathjs';
import Papa from 'papaparse';

const math = create(all)

function IRT() {
  const [result, setResult] = useState(null);
  const [plotData, setPlotData] = useState({ x: [], y: [] });

  const handleClick = () => {
    axios.get('/file.csv') // assuming data.csv is in the public directory
      .then(response => {
        const csvData = response.data;
        const parsedData = Papa.parse(csvData, { header: true }).data;
        const matrixData = parsedData.map(row => Object.values(row).map(val => parseInt(val)));
        const data = { matrix: { data: matrixData } };
        console.log(data);

        axios
          .post('http://localhost:8000/estimate', data)
          .then(response => {
            const x = response.data.Ability ?? [];
            const a = response.data.Discrimination ?? [];
            const b = response.data.Difficulty ?? [];
            const sigmoid = (x, a, b) => {
              const denominator = 1 + Math.exp(-a * (x - b));
              return denominator === 0 ? NaN : 1 / denominator;
            };
            const y = x.map((val, idx) => sigmoid(val, a[idx], b[idx]));
            const sortedData = x.map((value, index) => [value, y[index]])
              .sort((a, b) => a[0] - b[0]);
            const sortedX = sortedData.map(pair => pair[0]);
            const sortedY = sortedData.map(pair => pair[1]);
            setPlotData({ x: sortedX, y: sortedY });
          })
          .catch(error => {
            console.error(error);
          });
      })
      .catch(error => {
        console.error(error);
      });
  };

  return (
    <div>
      <button onClick={handleClick}>estimate</button>
      <Plot
        data={[
          {
            x: plotData.x,
            y: plotData.y,
            type: 'scatter',
            mode: 'lines+markers',
            line: { color: 'black' },
            marker: { symbol: 'circle', size: 8 }
          }
        ]}
        layout={{
          width: 500,
          height: 500,
          title: 'IRT model',
          xaxis: { title: 'Latent trait' },
          yaxis: { title: 'Item response' }
        }}
      />
    </div>
  );
}

export default IRT;
