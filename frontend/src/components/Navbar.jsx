import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="bg-blue-600 text-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center">
            <span className="text-xl font-bold">Infinite AI Security</span>
          </Link>
          
          <div className="flex space-x-4">
            <Link 
              to="/" 
              className="px-3 py-2 rounded-md hover:bg-blue-700 transition-colors"
            >
              Dashboard
            </Link>
            <Link 
              to="/sql-injection" 
              className="px-3 py-2 rounded-md hover:bg-blue-700 transition-colors"
            >
              SQL Injection
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;