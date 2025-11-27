import React from 'react';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  return (
    <div className="max-w-6xl mx-auto">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Infinite AI Security Platform</h1>
        <p className="text-xl text-gray-600">Advanced threat detection and security analysis</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
        <Link 
          to="/sql-injection" 
          className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow border border-blue-200"
        >
          <div className="text-blue-600 mb-4">
            <svg className="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
            </svg>
          </div>
          <h3 className="text-xl font-semibold text-gray-800 mb-2">SQL Injection Detection</h3>
          <p className="text-gray-600">Real-time detection of SQL injection attempts with confidence scoring</p>
        </Link>

        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200 opacity-50">
          <div className="text-gray-400 mb-4">
            <svg className="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
            </svg>
          </div>
          <h3 className="text-xl font-semibold text-gray-600 mb-2">XSS Protection</h3>
          <p className="text-gray-500">Cross-site scripting detection (Coming Soon)</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200 opacity-50">
          <div className="text-gray-400 mb-4">
            <svg className="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
          </div>
          <h3 className="text-xl font-semibold text-gray-600 mb-2">Rate Limiting</h3>
          <p className="text-gray-500">API rate limiting and DDoS protection (Coming Soon)</p>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">Current Threat Level</h2>
        <div className="flex items-center justify-between">
          <div className="text-4xl font-bold text-green-600">LOW</div>
          <div className="text-gray-600">
            <p>Monitored endpoints: 12 active</p>
            <p>Threats detected today: 0</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;