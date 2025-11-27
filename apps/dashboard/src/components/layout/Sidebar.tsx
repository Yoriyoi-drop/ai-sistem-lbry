import React from 'react';
import { 
  LayoutDashboard,
  Shield,
  Bot,
  Activity,
  Network,
  Settings,
  BarChart3,
  Users,
  Bell,
  Lock,
  HelpCircle,
  LogOut
} from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';

interface SidebarProps {
  isOpen: boolean;
}

interface NavItem {
  name: string;
  icon: React.ReactNode;
  href: string;
}

export const Sidebar: React.FC<SidebarProps> = ({ isOpen }) => {
  const location = useLocation();

  const navItems: NavItem[] = [
    { name: 'Dashboard', icon: <LayoutDashboard className="w-5 h-5" />, href: '/dashboard' },
    { name: 'Agents', icon: <Bot className="w-5 h-5" />, href: '/agents' },
    { name: 'Security Scans', icon: <Shield className="w-5 h-5" />, href: '/scans' },
    { name: 'Threats', icon: <Activity className="w-5 h-5" />, href: '/threats' },
    { name: 'Security', icon: <Shield className="w-5 h-5" />, href: '/security' },
    { name: 'Workflow', icon: <Network className="w-5 h-5" />, href: '/workflow' },
    { name: 'Analytics', icon: <BarChart3 className="w-5 h-5" />, href: '/analytics' },
    { name: 'Settings', icon: <Settings className="w-5 h-5" />, href: '/settings' },
  ];

  return (
    <aside className={`bg-gray-800 border-r border-gray-700 transition-all duration-300 ${isOpen ? 'w-64' : 'w-16'}`}>
      <div className="h-full flex flex-col">
        <div className="p-4 border-b border-gray-700 flex items-center">
          <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold">
            {isOpen ? 'IA' : 'I'}
          </div>
          {isOpen && (
            <h2 className="ml-3 text-lg font-semibold text-white">Infinite AI Security</h2>
          )}
        </div>

        <nav className="flex-1 px-2 py-4">
          <ul className="space-y-1">
            {navItems.map((item, index) => (
              <li key={index}>
                <Link
                  to={item.href}
                  className={`flex items-center px-3 py-2 rounded-lg text-gray-300 hover:bg-gray-700 ${
                    location.pathname === item.href ? 'bg-gray-700 text-white' : ''
                  }`}
                >
                  <span className="flex-shrink-0">
                    {item.icon}
                  </span>
                  {isOpen && (
                    <span className="ml-3">{item.name}</span>
                  )}
                </Link>
              </li>
            ))}
          </ul>

          <div className="pt-4 mt-4 border-t border-gray-700">
            <Link
              to="/help"
              className="flex items-center px-3 py-2 rounded-lg text-gray-300 hover:bg-gray-700"
            >
              <HelpCircle className="w-5 h-5" />
              {isOpen && <span className="ml-3">Help Center</span>}
            </Link>
            <button
              onClick={() => {
                // Logout functionality would go here
              }}
              className="flex items-center w-full px-3 py-2 rounded-lg text-gray-300 hover:bg-gray-700"
            >
              <LogOut className="w-5 h-5" />
              {isOpen && <span className="ml-3">Logout</span>}
            </button>
          </div>
        </nav>

        {isOpen && (
          <div className="p-4 border-t border-gray-700">
            <div className="text-xs text-gray-400">
              <p>Version 2.0.0</p>
              <p className="mt-1">Last updated: Today</p>
            </div>
          </div>
        )}
      </div>
    </aside>
  );
};