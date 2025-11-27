import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SQLInjectionDetector from './components/SQLInjectionDetector';
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <main className="container mx-auto py-8 px-4">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/sql-injection" element={<SQLInjectionDetector />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;