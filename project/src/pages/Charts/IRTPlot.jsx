import React from 'react';

import { ChartsHeader, IRT } from '../../components';


const IRTPlot = () => (
  <div className="m-4 md:m-10 mt-24 p-10 bg-white dark:bg-secondary-dark-bg rounded-3xl">
    <ChartsHeader category="ICC" title="Inflation Rate" />
    <div className="w-full">
      <IRT />
    </div>
  </div>
);

export default IRTPlot;