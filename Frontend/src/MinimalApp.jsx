import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Homepage from './components/Homepage';

function MinimalApp() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Homepage />} />
          <Route path="/test" element={<div>Test route working</div>} />
        </Routes>
      </div>
    </Router>
  );
}

export default MinimalApp;