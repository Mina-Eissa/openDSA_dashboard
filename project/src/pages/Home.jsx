import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { ColumnSeries,ChartComponent, SeriesCollectionDirective,Tooltip, DataLabel, SeriesDirective, Category, Legend, Inject, LineSeries ,Zoom, ScrollBar } from '@syncfusion/ej2-react-charts';
import { ScrollingCarousel } from '@trendyol-js/react-carousel';
import { FiBook } from 'react-icons/fi';
import { Header, IRT } from '../components';
import Slider from 'react-slick';

const Home = () => {
  const [data, setData] = useState([]);
  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 3,
    slidesToScroll: 2,
  };
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:4000/api/student_book_data');
        setData(response.data);
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
const primaryyAxis = { minimum: 0, maximum: 1500, interval: 300 };
const load = (args) => {
    args.chart.zoomModule.isZoomed = true;
};
const [book, setBook] = useState('');

const filteredData = data.filter((data) => data.BOOK === book);

    return (
  <div className='m-2 md:m-10 mt-24 p-2 md:p-10 bg-[#F6F6F6] rounded-3xl'>
    <Header category="Page" title="Home" />
    
    <div className='m-5 text-[40px] text-[#066579] font-bold'>Your Books</div>
    <div>
          <ScrollingCarousel>
        <div><button className='text-[25px] bg-white m-6 p-3 h-[100px] w-auto hover:drop-shadow-xl rounded-3xl font-bold' onClick={() => setBook('Introduction to Programming')}><FiBook className='inline mr-'/>Introduction to Programming</button></div> 
        <div><button className='text-[25px] bg-white m-6 p-3 h-[100px] w-[300px] hover:drop-shadow-xl rounded-3xl font-bold' onClick={() => setBook('Database Systems')}>Database Systems</button></div> 
        <div><button className='text-[25px] bg-white m-6 p-3 h-[100px] w-[300px] hover:drop-shadow-xl rounded-3xl font-bold' onClick={() => setBook('Computer Networks')}>Computer Networks</button></div> 
        <div><button className='text-[25px] bg-white m-6 p-3 h-[100px] w-[300px] hover:drop-shadow-xl rounded-3xl font-bold' onClick={() => setBook('Web Development')}>Web Development</button></div> 
        <div><button className='text-[25px] bg-white m-6 p-3 h-[100px] w-[300px] hover:drop-shadow-xl rounded-3xl font-bold' onClick={() => setBook('Operating Systems')}>Operating Systems</button></div> 
        <div><button className='text-[25px] bg-white m-6 p-3 h-[100px] w-[300px] hover:drop-shadow-xl rounded-3xl font-bold' onClick={() => setBook('Data Structures and Algorithms')}>Data Structures and Algorithms</button></div> 
        <div><button className='text-[25px] bg-white m-6 p-3 h-[100px] w-[300px] hover:drop-shadow-xl rounded-3xl font-bold' onClick={() => setBook('Computer Graphics')}>Computer Graphics</button></div> 
        <div><button className='text-[25px] bg-white m-6 p-3 h-[100px] w-[300px] hover:drop-shadow-xl rounded-3xl font-bold' onClick={() => setBook('Software Engineering')}>Software Engineering</button></div> 
      </ScrollingCarousel>  
    </div>
      
    <div className='m-5 text-[40px] text-[#066579] font-bold'>Student Preformance</div>
    <ChartComponent id='charts'  title="Student Performance" 
    primaryXAxis={primaryxAxis} primaryYAxis={primaryyAxis} zoomSettings={zoomsettings} load={load} tooltip={{ enable: true }}>
        
    <Inject services={[ColumnSeries, Legend, Tooltip, DataLabel, LineSeries, Category,Zoom ,ScrollBar]}/>
    <SeriesCollectionDirective>
      <SeriesDirective dataSource={filteredData} xName='STUDENT' yName='EXERCISE_ATTEMPTS' type='Column' name='Attempts' fill='#066579'>
      </SeriesDirective>
      <SeriesDirective dataSource={filteredData} xName='STUDENT' yName='INCORRECT_ATTEMPTS' type='Column' name='Incorrect' fill='#FF7A59' >
      </SeriesDirective>
      <SeriesDirective dataSource={filteredData} xName='STUDENT' yName='HINTS_USED' type='Column' name='Hints' fill='#017F97' >
      </SeriesDirective>
    </SeriesCollectionDirective>
  </ChartComponent>
  <div>
    {/* <IRT/> */}
  </div>
  </div>
);
};

export default Home;
