import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-800 border-t border-gray-700 py-4 px-6">
      <div className="flex flex-col md:flex-row justify-between items-center">
        <div className="text-gray-400 text-sm">
          © {new Date().getFullYear()} Infinite AI Security Platform. All rights reserved.
        </div>
        <div className="flex space-x-6 mt-2 md:mt-0">
          <a href="#" className="text-gray-400 hover:text-gray-300 text-sm">Privacy Policy</a>
          <a href="#" className="text-gray-400 hover:text-gray-300 text-sm">Terms of Service</a>
          <a href="#" className="text-gray-400 hover:text-gray-300 text-sm">Documentation</a>
          <a href="#" className="text-gray-400 hover:text-gray-300 text-sm">Support</a>
        </div>
      </div>
      <div className="mt-2 text-center text-xs text-gray-500">
        Powered by AI Security Technology • Securing Your Digital Infrastructure
      </div>
    </footer>
  );
};