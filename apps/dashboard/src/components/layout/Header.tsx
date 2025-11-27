import React from 'react';
import { Bell, Search, User, Menu, ChevronDown } from 'lucide-react';
import { useAuth } from '../../hooks';

interface HeaderProps {
  sidebarOpen: boolean;
  toggleSidebar: () => void;
}

export const Header: React.FC<HeaderProps> = ({ sidebarOpen, toggleSidebar }) => {
  const { user, logout } = useAuth();

  return (
    <header className="bg-gray-800 border-b border-gray-700">
      <div className="flex items-center justify-between h-16 px-4">
        <div className="flex items-center">
          <button 
            onClick={toggleSidebar}
            className="p-2 rounded-lg hover:bg-gray-700 mr-2"
          >
            <Menu className="w-5 h-5" />
          </button>
          <div className="flex items-center">
            <h1 className="text-xl font-bold text-white">Infinite AI Security</h1>
          </div>
        </div>

        <div className="flex-1 max-w-lg mx-8">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <input
              type="text"
              placeholder="Search..."
              className="w-full pl-10 pr-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <button className="p-2 rounded-full hover:bg-gray-700 relative">
            <Bell className="w-5 h-5 text-gray-300" />
            <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>

          <div className="flex items-center">
            <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white mr-2">
              <User className="w-4 h-4" />
            </div>
            <div className="hidden md:block">
              <div className="text-sm font-medium text-white">{user?.username || 'User'}</div>
              <div className="text-xs text-gray-400">Administrator</div>
            </div>
            <ChevronDown className="w-4 h-4 text-gray-400 ml-1 hidden md:block" />
          </div>
        </div>
      </div>
    </header>
  );
};