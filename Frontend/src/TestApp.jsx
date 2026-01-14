import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SimpleTest from './components/SimpleTest';

function TestApp() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<div>Root route</div>} />
          <Route path="/simple-test" element={<SimpleTest />} />
        </Routes>
      </div>
    </Router>
  );
}

export default TestApp;