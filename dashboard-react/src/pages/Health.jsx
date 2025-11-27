import React, { useState, useEffect } from 'react';
import axios from 'axios';

const HealthPage = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [systemStatus, setSystemStatus] = useState({
    overall: 'Healthy',
    lastCheck: 'Just now',
    uptime: '14 days, 2 hours'
  });
  const [services, setServices] = useState([
    { name: 'API Gateway', status: 'Operational', responseTime: '12ms', uptime: '99.9%' },
    { name: 'Security Engine', status: 'Operational', responseTime: '45ms', uptime: '99.8%' },
    { name: 'Database', status: 'Operational', responseTime: '8ms', uptime: '99.95%' },
    { name: 'Cache Layer', status: 'Operational', responseTime: '2ms', uptime: '99.9%' },
    { name: 'Message Queue', status: 'Operational', responseTime: '5ms', uptime: '99.7%' },
    { name: 'Monitoring System', status: 'Operational', responseTime: '15ms', uptime: '99.9%' }
  ]);
  const [metrics, setMetrics] = useState([
    { name: 'CPU Usage', value: '65%', status: 'normal', max: 100 },
    { name: 'Memory Usage', value: '78%', status: 'normal', max: 100 },
    { name: 'Disk Usage', value: '45%', status: 'normal', max: 100 },
    { name: 'Network I/O', value: '2.4 Gbps', status: 'normal', max: 10 },
    { name: 'Active Connections', value: '1,248', status: 'normal', max: 10000 },
    { name: 'Requests/Sec', value: '142', status: 'normal', max: 1000 }
  ]);
  const [alerts, setAlerts] = useState([
    { id: 1, level: 'info', message: 'System performing normally', time: '2 hours ago', service: 'Overall System' },
    { id: 2, level: 'info', message: 'Database backup completed successfully', time: '4 hours ago', service: 'Database' },
    { id: 3, level: 'warning', message: 'Memory usage approaching threshold', time: '6 hours ago', service: 'Application Server' },
    { id: 4, level: 'info', message: 'New security rule deployed', time: '1 day ago', service: 'Security Engine' }
  ]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  // Simulate system metrics updating
  useEffect(() => {
    const interval = setInterval(() => {
      // In a real app, this would fetch real data from the backend
      setSystemStatus(prev => ({
        ...prev,
        lastCheck: 'Just now'
      }));
    }, 30000); // Update every 30 seconds

    return () => clearInterval(interval);
  }, []);

  const runHealthCheck = async () => {
    setLoading(true);
    setMessage('Running health check...');

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));

      // Update metrics to simulate new data
      setMetrics(prev => prev.map(metric => {
        // Simulate slight changes in metrics
        let newValue = metric.value;
        if (metric.name === 'CPU Usage') {
          newValue = `${Math.floor(Math.random() * 20) + 60}%`;
        } else if (metric.name === 'Memory Usage') {
          newValue = `${Math.floor(Math.random() * 10) + 75}%`;
        }
        return { ...metric, value: newValue };
      }));

      setMessage('Health check completed successfully');
    } catch (error) {
      setMessage('Health check failed');
    } finally {
      setLoading(false);
    }
  };

  const restartServices = async () => {
    setLoading(true);
    setMessage('Restarting services...');

    try {
      // Simulate API call to restart services
      await new Promise(resolve => setTimeout(resolve, 2000));

      // Update service status to simulate restart
      setServices(prev => prev.map(service => ({
        ...service,
        status: 'Restarting',
        responseTime: '...'
      })));

      // After restart, restore normal status
      setTimeout(() => {
        setServices(prev => prev.map(service => ({
          ...service,
          status: 'Operational',
          responseTime: service.responseTime === '...' ? '10ms' : service.responseTime
        })));
        setMessage('Services restarted successfully');
      }, 1500);
    } catch (error) {
      setMessage('Service restart failed');
    } finally {
      setLoading(false);
    }
  };

  const generateReport = async () => {
    setLoading(true);
    setMessage('Generating report...');

    try {
      // Simulate API call to generate report
      await new Promise(resolve => setTimeout(resolve, 2500));
      setMessage('Report generated successfully. Download started...');
    } catch (error) {
      setMessage('Report generation failed');
    } finally {
      setLoading(false);
    }
  };

  const getDetailedStatus = async () => {
    setLoading(true);
    setMessage('Loading detailed status...');

    try {
      // Simulate API call to get more detailed status
      await new Promise(resolve => setTimeout(resolve, 1000));
      setMessage('Detailed status loaded');

      // Update with new status information
      setSystemStatus({
        overall: 'Healthy',
        lastCheck: new Date().toLocaleTimeString(),
        uptime: '14 days, 2 hours, 15 minutes'
      });
    } catch (error) {
      setMessage('Failed to load detailed status');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-gray-800 dark:text-white mb-6">Server Health</h1>

      {message && (
        <div className={`mb-4 p-3 rounded-md ${
          message.includes('completed') || message.includes('successfully') || message.includes('loaded') ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100' :
          message.includes('failed') ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100' :
          message.includes('running') || message.includes('generating') || message.includes('restarting') ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100' :
          'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100'
        }`}>
          {message}
        </div>
      )}

      {loading && (
        <div className="flex justify-center items-center mb-6">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      )}

      {/* Navigation Tabs */}
      <div className="flex border-b border-gray-200 dark:border-gray-700 mb-6">
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'overview' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 dark:text-gray-400'}`}
          onClick={() => setActiveTab('overview')}
        >
          System Overview
        </button>
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'metrics' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 dark:text-gray-400'}`}
          onClick={() => setActiveTab('metrics')}
        >
          System Metrics
        </button>
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'alerts' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 dark:text-gray-400'}`}
          onClick={() => setActiveTab('alerts')}
        >
          Alerts & Events
        </button>
      </div>

      {/* System Overview */}
      {activeTab === 'overview' && (
        <div>
          {/* System Status Card */}
          <div className="bg-gradient-to-r from-green-50 to-green-100 dark:from-green-900 dark:to-green-800 border border-green-200 dark:border-green-700 rounded-lg p-6 mb-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-12 h-12 rounded-full bg-green-500 flex items-center justify-center">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                </div>
              </div>
              <div className="ml-4">
                <h2 className="text-2xl font-bold text-gray-800 dark:text-white">System Status: {systemStatus.overall}</h2>
                <p className="text-gray-600 dark:text-gray-300">Last check: {systemStatus.lastCheck} • Uptime: {systemStatus.uptime}</p>
              </div>
            </div>
          </div>

          {/* Service Status Grid */}
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">Service Status</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {services.map((service, index) => (
                <div key={index} className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                  <div className="flex justify-between items-start">
                    <h3 className="font-medium text-gray-800 dark:text-white">{service.name}</h3>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      service.status === 'Operational'
                        ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100'
                        : service.status === 'Restarting'
                          ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100'
                          : service.status === 'Degraded'
                            ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100'
                            : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100'
                    }`}>
                      {service.status}
                    </span>
                  </div>
                  <div className="mt-2 space-y-1 text-sm text-gray-600 dark:text-gray-300">
                    <div>Response: {service.responseTime}</div>
                    <div>Uptime: {service.uptime}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">System Actions</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <button
                onClick={runHealthCheck}
                disabled={loading}
                className="px-4 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors disabled:opacity-50"
              >
                Run Health Check
              </button>
              <button
                onClick={restartServices}
                disabled={loading}
                className="px-4 py-3 bg-gray-600 text-white rounded-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 transition-colors disabled:opacity-50"
              >
                Restart All Services
              </button>
              <button
                onClick={generateReport}
                disabled={loading}
                className="px-4 py-3 bg-purple-600 text-white rounded-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 transition-colors disabled:opacity-50"
              >
                Generate Report
              </button>
            </div>
          </div>
        </div>
      )}

      {/* System Metrics */}
      {activeTab === 'metrics' && (
        <div className="space-y-6">
          <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-semibold text-gray-800 dark:text-white">System Metrics</h2>
              <button
                onClick={getDetailedStatus}
                disabled={loading}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors disabled:opacity-50"
              >
                Refresh Metrics
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {metrics.map((metric, index) => (
                <div key={index} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                  <div className="flex justify-between items-center mb-2">
                    <h3 className="font-medium text-gray-800 dark:text-white">{metric.name}</h3>
                    <span className={`text-lg font-bold ${
                      metric.status === 'normal' ? 'text-green-600 dark:text-green-400' :
                      metric.status === 'warning' ? 'text-yellow-600 dark:text-yellow-400' :
                      'text-red-600 dark:text-red-400'
                    }`}>
                      {metric.value}
                    </span>
                  </div>

                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
                    <div
                      className={`h-2.5 rounded-full ${
                        metric.status === 'normal' ? 'bg-green-600' :
                        metric.status === 'warning' ? 'bg-yellow-500' :
                        'bg-red-600'
                      }`}
                      style={{ width: `${Math.min(100, parseInt(metric.value) || 0)}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">CPU Usage Over Time</h3>
              <div className="h-64 flex items-center justify-center border border-gray-200 dark:border-gray-700 rounded-lg">
                <div className="text-center">
                  <p className="text-gray-500 dark:text-gray-400 mb-2">CPU Usage Trend</p>
                  <p className="text-sm text-gray-400 dark:text-gray-500">Visualization would appear here</p>
                </div>
              </div>
            </div>

            <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">Memory Usage</h3>
              <div className="h-64 flex items-center justify-center border border-gray-200 dark:border-gray-700 rounded-lg">
                <div className="text-center">
                  <p className="text-gray-500 dark:text-gray-400 mb-2">Memory Usage Trend</p>
                  <p className="text-sm text-gray-400 dark:text-gray-500">Visualization would appear here</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Alerts & Events */}
      {activeTab === 'alerts' && (
        <div>
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-white">Recent Alerts & Events</h2>
            <button
              onClick={() => setMessage('Viewing full log... (simulated)')}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
            >
              View Full Log
            </button>
          </div>

          <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
            <ul className="divide-y divide-gray-200 dark:divide-gray-700">
              {alerts.map((alert) => (
                <li key={alert.id} className="p-4 hover:bg-gray-50 dark:hover:bg-gray-700">
                  <div className="flex items-center">
                    <div className={`flex-shrink-0 w-3 h-3 rounded-full mr-3 ${
                      alert.level === 'info' ? 'bg-blue-500' :
                      alert.level === 'warning' ? 'bg-yellow-500' :
                      'bg-red-500'
                    }`}></div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-800 dark:text-white">{alert.message}</p>
                      <p className="text-sm text-gray-500 dark:text-gray-400">{alert.service} • {alert.time}</p>
                    </div>
                    <div className={`text-xs px-2 py-1 rounded-full ${
                      alert.level === 'info' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100' :
                      alert.level === 'warning' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100' :
                      'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100'
                    }`}>
                      {alert.level.toUpperCase()}
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          </div>

          <div className="mt-6 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">System Health Score</h3>
            <div className="flex items-center">
              <div className="relative w-48 h-48">
                <svg className="w-full h-full" viewBox="0 0 100 100">
                  <circle className="text-gray-200 dark:text-gray-700 stroke-current" strokeWidth="10" cx="50" cy="50" r="40" fill="transparent"></circle>
                  <circle
                    className="text-green-500 stroke-current"
                    strokeWidth="10"
                    strokeLinecap="round"
                    cx="50"
                    cy="50"
                    r="40"
                    fill="transparent"
                    strokeDasharray="251.2"
                    strokeDashoffset={251.2 - (251.2 * 95 / 100)}
                    transform="rotate(-90 50 50)"
                  ></circle>
                  <text x="50" y="50" fontSize="20" textAnchor="middle" fill="currentColor" className="text-gray-800 dark:text-white font-bold">95%</text>
                </svg>
              </div>
              <div className="ml-6">
                <h4 className="text-xl font-semibold text-gray-800 dark:text-white">Excellent</h4>
                <p className="text-gray-600 dark:text-gray-300 mt-2">
                  System health is in excellent condition. All services are operational and performing optimally.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default HealthPage;