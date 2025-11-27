import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../store';
import { fetchSecurityDataStart } from '../store/slices/securitySlice';
import { fetchAgentsStart } from '../store/slices/agentsSlice';

// Mock chart components - in a real app, these would use Recharts
const ChartPlaceholder: React.FC<{ title: string }> = ({ title }) => (
  <div className="card h-64 flex items-center justify-center">
    <h3 className="text-lg font-semibold text-gray-700">{title}</h3>
    <p className="text-gray-500 mt-2">Chart Visualization Area</p>
  </div>
);

const Dashboard: React.FC = () => {
  const dispatch = useDispatch();
  const { stats, loading: securityLoading } = useSelector((state: RootState) => state.security);
  const { agents, loading: agentsLoading } = useSelector((state: RootState) => state.agents);

  useEffect(() => {
    dispatch(fetchSecurityDataStart());
    dispatch(fetchAgentsStart());
  }, [dispatch]);

  // Calculate agent stats
  const onlineAgents = agents.filter(agent => agent.status === 'online').length;
  const busyAgents = agents.filter(agent => agent.status === 'busy').length;
  const offlineAgents = agents.filter(agent => agent.status === 'offline').length;

  return (
    <div className="dashboard">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Dashboard Overview</h1>
        <p className="text-gray-600">Welcome to the Infinite AI Security Platform</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <div className="card">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-indigo-100 text-indigo-600">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <div className="ml-4">
              <h2 className="text-sm font-medium text-gray-600">Total Security Events</h2>
              <p className="text-2xl font-semibold text-gray-800">{stats.totalEvents}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-red-100 text-red-600">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <div className="ml-4">
              <h2 className="text-sm font-medium text-gray-600">Critical Events</h2>
              <p className="text-2xl font-semibold text-gray-800">{stats.criticalEvents}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-yellow-100 text-yellow-600">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 12H4" />
              </svg>
            </div>
            <div className="ml-4">
              <h2 className="text-sm font-medium text-gray-600">Active Threats</h2>
              <p className="text-2xl font-semibold text-gray-800">{stats.activeThreats}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-green-100 text-green-600">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="ml-4">
              <h2 className="text-sm font-medium text-gray-600">Blocked Requests</h2>
              <p className="text-2xl font-semibold text-gray-800">{stats.blockedRequests}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Agent Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">AI Agents Status</h3>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium text-gray-700">Online</span>
                <span className="text-sm font-medium text-gray-700">{onlineAgents}/{agents.length}</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2.5">
                <div 
                  className="bg-green-600 h-2.5 rounded-full" 
                  style={{ width: `${agents.length > 0 ? (onlineAgents / agents.length) * 100 : 0}%` }}
                ></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium text-gray-700">Busy</span>
                <span className="text-sm font-medium text-gray-700">{busyAgents}/{agents.length}</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2.5">
                <div 
                  className="bg-yellow-500 h-2.5 rounded-full" 
                  style={{ width: `${agents.length > 0 ? (busyAgents / agents.length) * 100 : 0}%` }}
                ></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium text-gray-700">Offline</span>
                <span className="text-sm font-medium text-gray-700">{offlineAgents}/{agents.length}</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2.5">
                <div 
                  className="bg-gray-500 h-2.5 rounded-full" 
                  style={{ width: `${agents.length > 0 ? (offlineAgents / agents.length) * 100 : 0}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Recent Security Events</h3>
          <div className="overflow-y-auto max-h-64">
            {securityLoading ? (
              <p>Loading events...</p>
            ) : (
              <table className="table">
                <thead>
                  <tr>
                    <th>Type</th>
                    <th>Severity</th>
                    <th>Time</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>SQL Injection</td>
                    <td><span className="status-high">High</span></td>
                    <td>Just now</td>
                  </tr>
                  <tr>
                    <td>XSS Attempt</td>
                    <td><span className="status-medium">Medium</span></td>
                    <td>2 min ago</td>
                  </tr>
                  <tr>
                    <td>Brute Force</td>
                    <td><span className="status-low">Low</span></td>
                    <td>5 min ago</td>
                  </tr>
                  <tr>
                    <td>Path Traversal</td>
                    <td><span className="status-high">High</span></td>
                    <td>8 min ago</td>
                  </tr>
                </tbody>
              </table>
            )}
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">System Health</h3>
          <div className="space-y-4">
            <div className="flex justify-between">
              <span className="text-gray-600">CPU Usage</span>
              <span className="font-medium">24%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: '24%' }}></div>
            </div>
            
            <div className="flex justify-between">
              <span className="text-gray-600">Memory Usage</span>
              <span className="font-medium">45%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div className="bg-purple-600 h-2.5 rounded-full" style={{ width: '45%' }}></div>
            </div>
            
            <div className="flex justify-between">
              <span className="text-gray-600">Network Traffic</span>
              <span className="font-medium">12 MB/s</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div className="bg-indigo-600 h-2.5 rounded-full" style={{ width: '68%' }}></div>
            </div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ChartPlaceholder title="Security Events Over Time" />
        <ChartPlaceholder title="Threat Distribution by Type" />
      </div>
    </div>
  );
};

export default Dashboard;