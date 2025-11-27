import React, { useState } from 'react';
import axios from 'axios';

const AlertsPage = () => {
  const [activeTab, setActiveTab] = useState('active');
  const [selectedAlert, setSelectedAlert] = useState(null);
  const [selectedAlerts, setSelectedAlerts] = useState(new Set());
  const [message, setMessage] = useState('');

  const [alerts, setAlerts] = useState([
    {
      id: 1,
      severity: 'critical',
      type: 'Security Threat',
      message: 'SQL injection attempt detected on /api/users endpoint',
      source: 'Web Application Firewall',
      time: '2 minutes ago',
      status: 'new',
      details: {
        ip: '192.168.1.105',
        userAgent: 'Mozilla/5.0 (compatible; SQLInjector/1.0)',
        url: '/api/users?id=1 OR 1=1',
        confidence: '98%'
      }
    },
    {
      id: 2,
      severity: 'high',
      type: 'Performance',
      message: 'High CPU usage on security-node-3',
      source: 'System Monitor',
      time: '15 minutes ago',
      status: 'acknowledged',
      details: {
        cpu: '92%',
        threshold: '85%',
        duration: '8 minutes',
        processes: ['threat_analysis', 'data_processing']
      }
    },
    {
      id: 3,
      severity: 'medium',
      type: 'Security Threat',
      message: 'Multiple failed login attempts from single IP',
      source: 'Authentication System',
      time: '1 hour ago',
      status: 'resolved',
      details: {
        ip: '203.0.113.45',
        attempts: 24,
        timeWindow: '15 minutes',
        blocked: true
      }
    },
    {
      id: 4,
      severity: 'low',
      type: 'System',
      message: 'Disk space running low on logs partition',
      source: 'Storage Monitor',
      time: '3 hours ago',
      status: 'new',
      details: {
        partition: '/var/log',
        usage: '87%',
        threshold: '85%',
        available: '12 GB'
      }
    }
  ]);

  const activeAlerts = alerts.filter(alert => alert.status === 'new');
  const acknowledgedAlerts = alerts.filter(alert => alert.status === 'acknowledged');
  const resolvedAlerts = alerts.filter(alert => alert.status === 'resolved');

  const getSeverityColor = (severity) => {
    switch(severity) {
      case 'critical': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100';
      case 'high': return 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-100';
      case 'medium': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100';
      case 'low': return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
    }
  };

  const getSeverityIcon = (severity) => {
    switch(severity) {
      case 'critical': return '🔴';
      case 'high': return '🟠';
      case 'medium': return '🟡';
      case 'low': return '🔵';
      default: return '⚪';
    }
  };

  const updateAlertStatus = (id, newStatus) => {
    setAlerts(alerts.map(alert =>
      alert.id === id ? {...alert, status: newStatus} : alert
    ));
    setMessage(`Alert status updated to ${newStatus}`);

    // Update selectedAlert if it was changed
    if (selectedAlert && selectedAlert.id === id) {
      setSelectedAlert({...selectedAlert, status: newStatus});
    }
  };

  const toggleAlertSelection = (id) => {
    const newSelected = new Set(selectedAlerts);
    if (newSelected.has(id)) {
      newSelected.delete(id);
    } else {
      newSelected.add(id);
    }
    setSelectedAlerts(newSelected);
  };

  const handleAcknowledge = (id, e) => {
    e.stopPropagation();
    updateAlertStatus(id, 'acknowledged');
  };

  const handleResolve = (id, e) => {
    e.stopPropagation();
    updateAlertStatus(id, 'resolved');
  };

  const handleReopen = (id, e) => {
    e.stopPropagation();
    updateAlertStatus(id, 'new');
  };

  const handleBulkAction = (action) => {
    if (selectedAlerts.size === 0) {
      setMessage('Please select at least one alert');
      return;
    }

    setAlerts(alerts.map(alert => {
      if (selectedAlerts.has(alert.id)) {
        switch (action) {
          case 'acknowledge':
            return {...alert, status: 'acknowledged'};
          case 'resolve':
            return {...alert, status: 'resolved'};
          case 'reopen':
            return {...alert, status: 'new'};
          case 'suppress':
            return {...alert, status: 'suppressed'};
          case 'escalate':
            return {...alert, status: 'escalated'};
          default:
            return alert;
        }
      }
      return alert;
    }));

    // Clear selection after bulk action
    setSelectedAlerts(new Set());
    setMessage(`Bulk ${action} action completed for ${selectedAlerts.size} alerts`);
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-gray-800 dark:text-white mb-6">Alerts</h1>

      {message && (
        <div className={`mb-4 p-3 rounded-md ${
          message.includes('updated') || message.includes('completed') ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100' :
          message.includes('select') ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100' :
          'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100'
        }`}>
          {message}
        </div>
      )}

      {/* Navigation Tabs */}
      <div className="flex border-b border-gray-200 dark:border-gray-700 mb-6">
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'active' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 dark:text-gray-400'}`}
          onClick={() => setActiveTab('active')}
        >
          Active Alerts ({activeAlerts.length})
        </button>
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'acknowledged' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 dark:text-gray-400'}`}
          onClick={() => setActiveTab('acknowledged')}
        >
          Acknowledged ({acknowledgedAlerts.length})
        </button>
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'resolved' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 dark:text-gray-400'}`}
          onClick={() => setActiveTab('resolved')}
        >
          Resolved ({resolvedAlerts.length})
        </button>
      </div>

      {/* Alert Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
          <div className="flex items-center">
            <div className="text-3xl">🔴</div>
            <div className="ml-4">
              <p className="text-sm text-gray-500 dark:text-gray-400">Critical Alerts</p>
              <p className="text-2xl font-bold text-red-600 dark:text-red-400">
                {alerts.filter(a => a.severity === 'critical').length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
          <div className="flex items-center">
            <div className="text-3xl">🟠</div>
            <div className="ml-4">
              <p className="text-sm text-gray-500 dark:text-gray-400">High Alerts</p>
              <p className="text-2xl font-bold text-orange-600 dark:text-orange-400">
                {alerts.filter(a => a.severity === 'high').length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
          <div className="flex items-center">
            <div className="text-3xl">🟡</div>
            <div className="ml-4">
              <p className="text-sm text-gray-500 dark:text-gray-400">Medium Alerts</p>
              <p className="text-2xl font-bold text-yellow-600 dark:text-yellow-400">
                {alerts.filter(a => a.severity === 'medium').length}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Alerts List */}
      <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
        <div className="p-4 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-lg font-semibold text-gray-800 dark:text-white">
            {activeTab === 'active' && 'Active Alerts'}
            {activeTab === 'acknowledged' && 'Acknowledged Alerts'}
            {activeTab === 'resolved' && 'Resolved Alerts'}
          </h2>
        </div>

        <div className="divide-y divide-gray-200 dark:divide-gray-700">
          {(activeTab === 'active' ? activeAlerts :
            activeTab === 'acknowledged' ? acknowledgedAlerts :
            resolvedAlerts).map((alert) => (
            <div
              key={alert.id}
              className={`p-4 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer ${selectedAlerts.has(alert.id) ? 'bg-blue-50 dark:bg-blue-900/30' : ''}`}
              onClick={() => setSelectedAlert(alert === selectedAlert ? null : alert)}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start">
                  <input
                    type="checkbox"
                    checked={selectedAlerts.has(alert.id)}
                    onChange={() => toggleAlertSelection(alert.id)}
                    className="mt-1 mr-3 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    onClick={(e) => {
                      e.stopPropagation();
                      toggleAlertSelection(alert.id);
                    }}
                  />
                  <div className="flex-shrink-0">
                    <span className="text-xl">{getSeverityIcon(alert.severity)}</span>
                  </div>
                  <div className="ml-2">
                    <div className="flex items-center">
                      <h3 className="text-sm font-medium text-gray-800 dark:text-white">{alert.type}</h3>
                      <span className={`ml-2 px-2 py-0.5 rounded-full text-xs font-medium ${getSeverityColor(alert.severity)}`}>
                        {alert.severity.toUpperCase()}
                      </span>
                    </div>
                    <p className="mt-1 text-sm text-gray-600 dark:text-gray-300">{alert.message}</p>
                    <div className="mt-2 flex items-center text-xs text-gray-500 dark:text-gray-400">
                      <span>{alert.source}</span>
                      <span className="mx-2">•</span>
                      <span>{alert.time}</span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  {activeTab === 'active' && (
                    <>
                      <button
                        className="px-3 py-1 bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100 text-xs rounded-md hover:bg-green-200 dark:hover:bg-green-800"
                        onClick={(e) => handleResolve(alert.id, e)}
                      >
                        Resolve
                      </button>
                      <button
                        className="px-3 py-1 bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100 text-xs rounded-md hover:bg-blue-200 dark:hover:bg-blue-800"
                        onClick={(e) => handleAcknowledge(alert.id, e)}
                      >
                        Acknowledge
                      </button>
                    </>
                  )}
                  {activeTab === 'acknowledged' && (
                    <button
                      className="px-3 py-1 bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100 text-xs rounded-md hover:bg-green-200 dark:hover:bg-green-800"
                      onClick={(e) => handleResolve(alert.id, e)}
                    >
                      Resolve
                    </button>
                  )}
                  {activeTab === 'resolved' && (
                    <button
                      className="px-3 py-1 bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100 text-xs rounded-md hover:bg-blue-200 dark:hover:bg-blue-800"
                      onClick={(e) => handleReopen(alert.id, e)}
                    >
                      Reopen
                    </button>
                  )}
                </div>
              </div>

              {/* Alert Details */}
              {selectedAlert && selectedAlert.id === alert.id && (
                <div className="mt-4 ml-8 pl-4 border-l-2 border-gray-200 dark:border-gray-700">
                  <h4 className="text-sm font-medium text-gray-800 dark:text-white mb-2">Details</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                    {Object.entries(alert.details).map(([key, value]) => (
                      <div key={key} className="flex">
                        <span className="text-gray-500 dark:text-gray-400 w-32 capitalize">{key}:</span>
                        <span className="text-gray-800 dark:text-white">{value}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Alert Management */}
      {activeTab === 'active' && (
        <div className="mt-6 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">Alert Management</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <button
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
              onClick={() => handleBulkAction('acknowledge')}
            >
              Acknowledge Selected
            </button>
            <button
              className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 transition-colors"
              onClick={() => handleBulkAction('resolve')}
            >
              Resolve Selected
            </button>
            <button
              className="px-4 py-2 bg-yellow-600 text-white rounded-md hover:bg-yellow-700 focus:outline-none focus:ring-2 focus:ring-yellow-500 transition-colors"
              onClick={() => handleBulkAction('escalate')}
            >
              Escalate Selected
            </button>
            <button
              className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 transition-colors"
              onClick={() => handleBulkAction('suppress')}
            >
              Suppress Selected
            </button>
          </div>
          {selectedAlerts.size > 0 && (
            <p className="mt-3 text-sm text-gray-600 dark:text-gray-300">
              {selectedAlerts.size} alert{selectedAlerts.size !== 1 ? 's' : ''} selected
            </p>
          )}
        </div>
      )}
    </div>
  );
};

export default AlertsPage;