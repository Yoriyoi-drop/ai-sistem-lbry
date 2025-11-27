import React, { useState, useEffect } from 'react';

const LogsPage = () => {
  const [activeTab, setActiveTab] = useState('security');
  const [searchTerm, setSearchTerm] = useState('');
  const [logLevel, setLogLevel] = useState('all');
  const [logs, setLogs] = useState([]);

  // Simulate log data
  useEffect(() => {
    const mockLogs = [
      {
        id: 1,
        timestamp: '2023-10-15 14:32:45',
        level: 'INFO',
        source: 'API Gateway',
        message: 'Successful API request from 192.168.1.100',
        details: 'GET /api/users - 200 OK - 12ms'
      },
      {
        id: 2,
        timestamp: '2023-10-15 14:32:47',
        level: 'WARNING',
        source: 'Security Engine',
        message: 'Anomalous behavior detected',
        details: 'Unusual request pattern from IP 203.0.113.45'
      },
      {
        id: 3,
        timestamp: '2023-10-15 14:33:01',
        level: 'ERROR',
        source: 'Database',
        message: 'Connection timeout to analytics database',
        details: 'Retrying connection in 5 seconds'
      },
      {
        id: 4,
        timestamp: '2023-10-15 14:33:15',
        level: 'INFO',
        source: 'Threat Detector',
        message: 'Threat scan completed',
        details: '245 requests analyzed - 0 threats detected'
      },
      {
        id: 5,
        timestamp: '2023-10-15 14:33:22',
        level: 'CRITICAL',
        source: 'Firewall',
        message: 'SQL injection attempt blocked',
        details: 'IP 192.168.1.105 - Payload: 1 OR 1=1'
      },
      {
        id: 6,
        timestamp: '2023-10-15 14:34:01',
        level: 'INFO',
        source: 'Cache Layer',
        message: 'Cache hit ratio: 89%',
        details: 'Performance within normal parameters'
      },
      {
        id: 7,
        timestamp: '2023-10-15 14:34:12',
        level: 'DEBUG',
        source: 'Neural Engine',
        message: 'Model prediction completed',
        details: 'Confidence: 0.87 - Threat type: XSS'
      },
      {
        id: 8,
        timestamp: '2023-10-15 14:34:35',
        level: 'WARNING',
        source: 'Authentication',
        message: 'Multiple failed login attempts',
        details: 'User admin from IP 203.0.113.200 - 6 attempts in 2 minutes'
      }
    ];
    
    setLogs(mockLogs);
  }, []);

  const filteredLogs = logs.filter(log => {
    const matchesSearch = log.message.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         log.source.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         log.details.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesLevel = logLevel === 'all' || log.level.toLowerCase() === logLevel.toLowerCase();
    
    return matchesSearch && matchesLevel;
  });

  const getLogLevelColor = (level) => {
    switch(level) {
      case 'CRITICAL': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100';
      case 'ERROR': return 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-100';
      case 'WARNING': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100';
      case 'INFO': return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100';
      case 'DEBUG': return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
    }
  };

  const logCounts = {
    security: logs.filter(log => ['CRITICAL', 'ERROR', 'WARNING'].includes(log.level)).length,
    application: logs.filter(log => ['INFO', 'DEBUG'].includes(log.level)).length,
    system: logs.length
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-gray-800 dark:text-white mb-6">Logs</h1>
      
      {/* Navigation Tabs */}
      <div className="flex border-b border-gray-200 dark:border-gray-700 mb-6">
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'security' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 dark:text-gray-400'}`}
          onClick={() => setActiveTab('security')}
        >
          Security Logs ({logCounts.security})
        </button>
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'application' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 dark:text-gray-400'}`}
          onClick={() => setActiveTab('application')}
        >
          Application Logs ({logCounts.application})
        </button>
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'system' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 dark:text-gray-400'}`}
          onClick={() => setActiveTab('system')}
        >
          System Logs ({logCounts.system})
        </button>
      </div>

      {/* Filters and Search */}
      <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4 mb-6">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
          <div className="flex flex-1 space-x-4">
            <div className="flex-1">
              <input
                type="text"
                placeholder="Search logs..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              />
            </div>
            <select
              value={logLevel}
              onChange={(e) => setLogLevel(e.target.value)}
              className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            >
              <option value="all">All Levels</option>
              <option value="critical">Critical</option>
              <option value="error">Error</option>
              <option value="warning">Warning</option>
              <option value="info">Info</option>
              <option value="debug">Debug</option>
            </select>
          </div>
          <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors whitespace-nowrap">
            Export Logs
          </button>
        </div>
      </div>

      {/* Log Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4">
          <div className="text-sm text-gray-500 dark:text-gray-400">Total Logs</div>
          <div className="text-2xl font-bold text-gray-800 dark:text-white">{logs.length}</div>
        </div>
        <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4">
          <div className="text-sm text-gray-500 dark:text-gray-400">Errors</div>
          <div className="text-2xl font-bold text-red-600 dark:text-red-400">
            {logs.filter(log => log.level === 'ERROR').length}
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4">
          <div className="text-sm text-gray-500 dark:text-gray-400">Warnings</div>
          <div className="text-2xl font-bold text-yellow-600 dark:text-yellow-400">
            {logs.filter(log => log.level === 'WARNING').length}
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4">
          <div className="text-sm text-gray-500 dark:text-gray-400">Critical</div>
          <div className="text-2xl font-bold text-red-800 dark:text-red-600">
            {logs.filter(log => log.level === 'CRITICAL').length}
          </div>
        </div>
      </div>

      {/* Logs Table */}
      <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead className="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Timestamp</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Level</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Source</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Message</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Details</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
              {filteredLogs.map((log) => (
                <tr key={log.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{log.timestamp}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getLogLevelColor(log.level)}`}>
                      {log.level}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800 dark:text-white">{log.source}</td>
                  <td className="px-6 py-4 text-sm text-gray-800 dark:text-white max-w-xs truncate">{log.message}</td>
                  <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400 max-w-md truncate">{log.details}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        {filteredLogs.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500 dark:text-gray-400">No logs match your search criteria</p>
          </div>
        )}
      </div>

      {/* Log Actions */}
      <div className="mt-6 flex justify-between">
        <div className="text-sm text-gray-500 dark:text-gray-400">
          Showing {filteredLogs.length} of {logs.length} logs
        </div>
        <div className="flex space-x-3">
          <button className="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-white rounded-md hover:bg-gray-300 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500 transition-colors">
            Clear Filters
          </button>
          <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors">
            Refresh Logs
          </button>
        </div>
      </div>
    </div>
  );
};

export default LogsPage;