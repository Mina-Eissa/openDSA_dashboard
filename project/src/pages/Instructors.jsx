import React from 'react';
import { Header } from '../components';

const Instructors = () => {
  const toolbarOptions = ['Search'];

  const editing = { allowDeleting: true, allowEditing: true };

  return (
    <div className="m-2 md:m-10 mt-24 p-2 md:p-10 bg-white rounded-3xl">
      <Header category="Page" title="Instructors" />
      
    </div>
  );
};
export default Instructors;
