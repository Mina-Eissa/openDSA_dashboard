import React , { useState }  from 'react';
import { ColumnSeries,ChartComponent, SeriesCollectionDirective,Tooltip, DataLabel, SeriesDirective, Category, Legend, Inject, LineSeries ,Zoom, ScrollBar } from '@syncfusion/ej2-react-charts';


  const Home = () => {
    const allData = [
      { student: 'Alice', book: 'Book A', exercises_attempted: 10, incorrect_answers: 2, hints_used: 3 },
      { student: 'Bob', book: 'Book A', exercises_attempted: 8, incorrect_answers: 1, hints_used: 0 },
      { student: 'Charlie', book: 'Book A', exercises_attempted: 15, incorrect_answers: 5, hints_used: 7 },
      { student: 'joe', book: 'Book A', exercises_attempted: 12, incorrect_answers: 3, hints_used: 1 },
      { student: 'jasmine', book: 'Book A', exercises_attempted: 6, incorrect_answers: 0, hints_used: 2 },
      { student: 'karin', book: 'Book A', exercises_attempted: 18, incorrect_answers: 4, hints_used: 4 },
      { student: 'osama', book: 'Book A', exercises_attempted: 10, incorrect_answers: 2, hints_used: 3 },
      { student: 'b', book: 'Book B', exercises_attempted: 8, incorrect_answers: 1, hints_used: 0 },
      { student: 'c', book: 'Book B', exercises_attempted: 15, incorrect_answers: 5, hints_used: 7 },
      { student: 'd', book: 'Book B', exercises_attempted: 12, incorrect_answers: 3, hints_used: 1 },
      { student: 'e', book: 'Book B', exercises_attempted: 6, incorrect_answers: 0, hints_used: 2 },
      { student: 'f', book: 'Book B', exercises_attempted: 18, incorrect_answers: 4, hints_used: 4 },
      { student: 'g', book: 'Book B', exercises_attempted: 10, incorrect_answers: 2, hints_used: 3 },
      { student: 'h', book: 'Book B', exercises_attempted: 8, incorrect_answers: 1, hints_used: 0 },
      { student: 'i', book: 'Book C', exercises_attempted: 15, incorrect_answers: 5, hints_used: 7 },
      { student: 'j', book: 'Book C', exercises_attempted: 12, incorrect_answers: 3, hints_used: 1 },
      { student: 'k', book: 'Book C', exercises_attempted: 6, incorrect_answers: 0, hints_used: 2 },
      { student: 'l', book: 'Book C', exercises_attempted: 18, incorrect_answers: 4, hints_used: 4 },
      { student: 'm', book: 'Book C', exercises_attempted: 10, incorrect_answers: 2, hints_used: 3 },
      { student: 'n', book: 'Book C', exercises_attempted: 8, incorrect_answers: 1, hints_used: 0 },
      { student: 'o', book: 'Book D', exercises_attempted: 15, incorrect_answers: 5, hints_used: 7 },
      { student: 'p', book: 'Book D', exercises_attempted: 12, incorrect_answers: 3, hints_used: 1 },
      { student: 'q', book: 'Book D', exercises_attempted: 6, incorrect_answers: 0, hints_used: 2 },
      { student: 'r', book: 'Book D', exercises_attempted: 18, incorrect_answers: 4, hints_used: 4 },
      { student: 's', book: 'Book D', exercises_attempted: 10, incorrect_answers: 2, hints_used: 3 },
      { student: 't', book: 'Book E', exercises_attempted: 8, incorrect_answers: 1, hints_used: 0 },
      { student: 'u', book: 'Book E', exercises_attempted: 15, incorrect_answers: 5, hints_used: 7 },
      { student: 'v', book: 'Book E', exercises_attempted: 12, incorrect_answers: 3, hints_used: 1 },
      { student: 'w', book: 'Book E', exercises_attempted: 6, incorrect_answers: 0, hints_used: 2 },
      { student: 'x', book: 'Book E', exercises_attempted: 18, incorrect_answers: 4, hints_used: 4 },
      { student: 'y', book: 'Book F', exercises_attempted: 10, incorrect_answers: 2, hints_used: 3 },
      { student: 'z', book: 'Book F', exercises_attempted: 8, incorrect_answers: 1, hints_used: 0 },
      { student: 'aa', book: 'Book F', exercises_attempted: 15, incorrect_answers: 5, hints_used: 7 },
      { student: 'bb', book: 'Book F', exercises_attempted: 12, incorrect_answers: 3, hints_used: 1 },
      { student: 'cc', book: 'Book F', exercises_attempted: 6, incorrect_answers: 0, hints_used: 2 },
      { student: 'ee', book: 'Book A', exercises_attempted: 18, incorrect_answers: 4, hints_used: 4 },
    ];
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
  const marker = { visible: true, dataLabel: { visible: true } };
  const load = (args) => {
      args.chart.zoomModule.isZoomed = true;
  };
  const [book, setBook] = useState('Book A');
  
  const handleBookChange = (event) => {
    setBook(event.target.value);
  };
  
  const filteredData = allData.filter((data) => data.book === book);
      return (
    <div className='mt-24'>
       <select onChange={handleBookChange} value={book}>
        <option value="Book A">Book A</option>
        <option value="Book B">Book B</option>
      </select>
      <ChartComponent id='charts'  title="Student Performance" 
      primaryXAxis={primaryxAxis} primaryYAxis={primaryyAxis} zoomSettings={zoomsettings} load={load} tooltip={{ enable: true }}>
          
      <Inject services={[ColumnSeries, Legend, Tooltip, DataLabel, LineSeries, Category,Zoom ,ScrollBar]}/>
      <SeriesCollectionDirective>
        <SeriesDirective dataSource={filteredData} xName='student' yName='exercises_attempted' type='Column' name='Attempts' marker={marker} >
        </SeriesDirective>
        <SeriesDirective dataSource={filteredData} xName='student' yName='incorrect_answers' type='Column' name='Incorrect' marker={marker}>
        </SeriesDirective>
        <SeriesDirective dataSource={filteredData} xName='student' yName='hints_used' type='Column' name='Hints' marker={marker}>
        </SeriesDirective>
      </SeriesCollectionDirective>
    </ChartComponent>
    </div>
  );
};

export default Home;
