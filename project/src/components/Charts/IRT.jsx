import React, { useState } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import { create, all } from 'mathjs';
import Papa from 'papaparse';

const math = create(all)

function IRT() {
  const [result, setResult] = useState(null);
  const [plotData, setPlotData] = useState({ icc: { x: [], y: [] }, tcc: { x: [], y: [] }});

  const handleClick = () => {
    axios.get('/file1.csv') // assuming data.csv is in the public directory
      // .then(response => {
      //   const csvData = response.data;
      //   const parsedData = Papa.parse(csvData, { header: true }).data;
      //   const matrixData = parsedData.map(row => Object.values(row).map(val => parseInt(val)));
      //   const data = { matrix: { data: matrixData } };
      //   console.log(data);
    const data = 'attemps_test.csv'; // Replace this with the actual file name
        axios
          .post(`http://localhost:8000/estimate/${data}`)
          // .post('http://localhost:8000/estimate', data)
          .then(response => {
            const x = response.data.Ability ?? [];
            const a = response.data.Discrimination ?? []; // use the first element for all items
            const b = response.data.Difficulty ?? [];
            console.log(x,a[0],b[0])
            const sigmoid = (x, a, b) => {
              const denominator = 1 + Math.exp(-a * (x - b));
              return denominator === 0 ? NaN : 1 / denominator;
            };
            const y = x.map((val) => sigmoid(val, a[18], b[18]));
            console.log(y)
            const sortedData = x.map((value, index) => [value, y[index]])
              .sort((a, b) => a[0] - b[0]);
            const sortedX = sortedData.map(pair => pair[0]);
            const sortedY = sortedData.map(pair => pair[1]);
            // Calculate mean discrimination and difficulty for all exercises
            const meanA = math.mean(response.data.Discrimination);
            const meanB = math.mean(response.data.Difficulty);

            // Calculate item response probabilities for a range of ability values
            const minAbility = Math.min(...response.data.Ability);
            const maxAbility = Math.max(...response.data.Ability);
            const range = maxAbility - minAbility;
            const step = range / 100;
            const abilityValues = math.range(minAbility, maxAbility, step).toArray();
            const y2 = abilityValues.map((val) => sigmoid(val, meanA, meanB));

            // Plot the test characteristic curve
            setPlotData({
              icc: { x: sortedX, y: sortedY },
              tcc: { x: abilityValues, y: y2 }
            });
          })
          .catch(error => {
            console.error(error);
          });
      // })
      // .catch(error => {
      //   console.error(error);
      // });
  };
  return (
    <div>
      <button onClick={handleClick}>estimate</button>
      <Plot
        data={[
          {
            x: plotData.icc.x,
            y: plotData.icc.y,
            type: 'scatter',
            mode: 'lines+markers',
            line: { color: 'black' },
            marker: { symbol: 'circle', size: 8 }
          }
        ]}
        layout={{
          width: 800,
          height: 600,
          title: 'IRT model',
          xaxis: { title: 'Latent trait' },
          yaxis: { title: 'Item response' }
        }}
      />
      <div>
    <h2>Test Characteristic Curve</h2>
    <Plot
      data={[
        {
          x: plotData.tcc.x,
          y: plotData.tcc.y,
          type: "scatter",
          mode: "lines",
          line: { color: 'black' },
          marker: { symbol: 'circle', size: 8 }
        },
      ]}
      layout={{ width: 800, height: 600, title: "Test Characteristic Curve" }}
    />
  </div>
    </div>
    
  );
}

export default IRT;
