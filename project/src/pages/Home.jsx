import React , { useState , useEffect }  from 'react';
import axios from 'axios';
import { ColumnSeries,ChartComponent, SeriesCollectionDirective,Tooltip, DataLabel, SeriesDirective, Category, Legend, Inject, LineSeries ,Zoom, ScrollBar } from '@syncfusion/ej2-react-charts';


  const Home = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
      const fetchData = async () => {
        try {
          const response = await axios.post('http://localhost:8000/api/student_book_data');
          setData(response.data);
          console.log(response.data);
        } catch (error) {
          console.error(error);
        }
      };
      fetchData();
    }, []);

    const zoomsettings = {
      enableMouseWheelZooming: true,
      enablePinchZooming: true,
      enableSelectionZooming: true,
      mode: 'X',
      enableScrollbar: true,
  };
  const primaryxAxis = { 
      zoomFactor: 0.5,
      valueType: 'Category',
      title: 'Students',
      labelFormat: 'y',
      intervalType: 'Years',
      edgeLabelPlacement: 'Shift' };
  const primaryyAxis = { minimum: 0, maximum: 20, interval: 5 };
  const load = (args) => {
      args.chart.zoomModule.isZoomed = true;
  };
  const [book, setBook] = useState('Introduction to Programming');
  
  const handleBookChange = (event) => {
    setBook(event.target.value);
  };
  
  const filteredData = data.filter((data) => data.BOOK === book);
  

      return (
    <div className='mt-24'>
       <select onChange={handleBookChange} value={book}>
        <option value="Introduction to Programming">Introduction to Programming</option>
        <option value="Database Systems">Database Systems</option>
        <option value="Computer Networks">Computer Networks</option>
        <option value="Web Development">Web Development</option>
        <option value="Operating Systems">Operating Systems</option>
        <option value="Artificial Intelligence">Artificial Intelligence</option>
        <option value="Computer Graphics">Computer Graphics</option>
      </select>
      <ChartComponent id='charts'  title="Student Performance" 
      primaryXAxis={primaryxAxis} primaryYAxis={primaryyAxis} zoomSettings={zoomsettings} load={load} tooltip={{ enable: true }}>
          
      <Inject services={[ColumnSeries, Legend, Tooltip, DataLabel, LineSeries, Category,Zoom ,ScrollBar]}/>
      <SeriesCollectionDirective>
        <SeriesDirective dataSource={filteredData} xName='STUDENT' yName='EXERCISE_ATTEMPTS' type='Column' name='Attempts'>
        </SeriesDirective>
        <SeriesDirective dataSource={filteredData} xName='STUDENT' yName='INCORRECT_ATTEMPTS' type='Column' name='Incorrect' >
        </SeriesDirective>
        <SeriesDirective dataSource={filteredData} xName='STUDENT' yName='HINTS_USED' type='Column' name='Hints' >
        </SeriesDirective>
      </SeriesCollectionDirective>
    </ChartComponent>
    </div>
  );
};

export default Home;
