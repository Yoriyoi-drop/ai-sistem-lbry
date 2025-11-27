import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AdvancedSecurityDashboard = () => {
  const [recentDetections, setRecentDetections] = useState([]);
  const [xssInput, setXssInput] = useState('');
  const [cmdInput, setCmdInput] = useState('');
  const [pathInput, setPathInput] = useState('');
  const [usernameInput, setUsernameInput] = useState('');
  const [passwordInput, setPasswordInput] = useState('');
  const [detectionResult, setDetectionResult] = useState(null);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [loading, setLoading] = useState(false);

  // Fetch recent detections on component mount
  useEffect(() => {
    fetchRecentDetections();
  }, []);

  const fetchRecentDetections = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/advanced-security/recent-detections?limit=10');
      setRecentDetections(response.data.detections || []);
    } catch (error) {
      console.error('Error fetching recent detections:', error);
    }
  };

  const detectXSS = async () => {
    if (!xssInput.trim()) return;
    
    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:8000/advanced-security/detect-xss', {
        content: xssInput
      });
      setDetectionResult(response.data);
    } catch (error) {
      console.error('XSS detection error:', error);
    } finally {
      setLoading(false);
    }
  };

  const detectCommandInjection = async () => {
    if (!cmdInput.trim()) return;
    
    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:8000/advanced-security/detect-command-injection', {
        command: cmdInput
      });
      setDetectionResult(response.data);
    } catch (error) {
      console.error('Command injection detection error:', error);
    } finally {
      setLoading(false);
    }
  };

  const detectPathTraversal = async () => {
    if (!pathInput.trim()) return;
    
    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:8000/advanced-security/detect-path-traversal', {
        path: pathInput
      });
      setDetectionResult(response.data);
    } catch (error) {
      console.error('Path traversal detection error:', error);
    } finally {
      setLoading(false);
    }
  };

  const detectAuthBruteforce = async () => {
    if (!usernameInput.trim() || !passwordInput.trim()) return;
    
    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:8000/advanced-security/detect-auth-bruteforce', {
        username: usernameInput,
        password: passwordInput
      });
      setDetectionResult(response.data);
    } catch (error) {
      console.error('Auth brute force detection error:', error);
    } finally {
      setLoading(false);
    }
  };

  const getThreatColor = (severity) => {
    switch(severity) {
      case 'CRITICAL': return 'text-red-600 bg-red-100 dark:bg-red-900 dark:text-red-100';
      case 'HIGH': return 'text-orange-600 bg-orange-100 dark:bg-orange-900 dark:text-orange-100';
      case 'MEDIUM': return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900 dark:text-yellow-100';
      case 'LOW': return 'text-green-600 bg-green-100 dark:bg-green-900 dark:text-green-100';
      default: return 'text-gray-600 bg-gray-100 dark:bg-gray-700 dark:text-gray-300';
    }
  };

  const getThreatIcon = (threatType) => {
    switch(threatType) {
      case 'XSS': return '🛡️';
      case 'SQL_INJECTION': return '🔍';
      case 'COMMAND_INJECTION': return '⚙️';
      case 'PATH_TRAVERSAL': return '📁';
      case 'AUTH_BRUTEFORCE': return '🔐';
      default: return '⚠️';
    }
  };

  return (
    <div className="max-w-7xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-gray-800 dark:text-white mb-8">Advanced Security Dashboard</h1>
      
      {/* Navigation Tabs */}
      <div className="flex border-b border-gray-200 dark:border-gray-700 mb-6">
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'dashboard' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 dark:text-gray-400'}`}
          onClick={() => setActiveTab('dashboard')}
        >
          Dashboard
        </button>
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'xss' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 dark:text-gray-400'}`}
          onClick={() => setActiveTab('xss')}
        >
          XSS Detection
        </button>
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'command' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 dark:text-gray-400'}`}
          onClick={() => setActiveTab('command')}
        >
          Command Injection
        </button>
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'path' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 dark:text-gray-400'}`}
          onClick={() => setActiveTab('path')}
        >
          Path Traversal
        </button>
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'auth' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 dark:text-gray-400'}`}
          onClick={() => setActiveTab('auth')}
        >
          Auth Bruteforce
        </button>
      </div>

      {/* Dashboard Tab */}
      {activeTab === 'dashboard' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Threat Level Summary */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-white">Threat Level Summary</h2>
            
            <div className="space-y-4">
              {['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'].map(level => {
                const count = recentDetections.filter(d => d.severity === level).length;
                return (
                  <div key={level} className="flex items-center justify-between">
                    <span className="text-gray-600 dark:text-gray-300">{level}</span>
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${getThreatColor(level)}`}>
                      {count}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Recent Detections */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-white">Recent Detections</h2>
            
            <div className="space-y-3 max-h-64 overflow-y-auto">
              {recentDetections.length > 0 ? (
                recentDetections.map((detection, index) => (
                  <div key={index} className="border border-gray-200 dark:border-gray-700 rounded p-3">
                    <div className="flex justify-between items-start">
                      <div className="flex items-center">
                        <span className="mr-2">{getThreatIcon(detection.threat_type)}</span>
                        <span className="font-medium text-gray-800 dark:text-white">{detection.threat_type}</span>
                      </div>
                      <span className={`px-2 py-1 rounded text-xs font-medium ${getThreatColor(detection.severity)}`}>
                        {detection.severity}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
                      Confidence: {(detection.confidence * 100).toFixed(0)}%
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      {new Date(detection.timestamp).toLocaleString()}
                    </p>
                  </div>
                ))
              ) : (
                <p className="text-gray-500 dark:text-gray-400 text-center py-4">No recent detections</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* XSS Detection Tab */}
      {activeTab === 'xss' && (
        <div className="space-y-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-white">XSS Detection</h2>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Test XSS Payload
              </label>
              <textarea
                value={xssInput}
                onChange={(e) => setXssInput(e.target.value)}
                placeholder="<script>alert('XSS')</script>"
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 h-32 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              />
              <button
                onClick={detectXSS}
                disabled={loading}
                className="mt-3 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 transition-colors"
              >
                {loading ? 'Analyzing...' : 'Detect XSS'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Command Injection Tab */}
      {activeTab === 'command' && (
        <div className="space-y-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-white">Command Injection Detection</h2>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Test Command
              </label>
              <input
                type="text"
                value={cmdInput}
                onChange={(e) => setCmdInput(e.target.value)}
                placeholder="ls | cat /etc/passwd"
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              />
              <button
                onClick={detectCommandInjection}
                disabled={loading}
                className="mt-3 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 transition-colors"
              >
                {loading ? 'Analyzing...' : 'Detect Command Injection'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Path Traversal Tab */}
      {activeTab === 'path' && (
        <div className="space-y-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-white">Path Traversal Detection</h2>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Test Path
              </label>
              <input
                type="text"
                value={pathInput}
                onChange={(e) => setPathInput(e.target.value)}
                placeholder="../../../etc/passwd"
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              />
              <button
                onClick={detectPathTraversal}
                disabled={loading}
                className="mt-3 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 transition-colors"
              >
                {loading ? 'Analyzing...' : 'Detect Path Traversal'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Auth Bruteforce Tab */}
      {activeTab === 'auth' && (
        <div className="space-y-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-white">Auth Bruteforce Detection</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Username
                </label>
                <input
                  type="text"
                  value={usernameInput}
                  onChange={(e) => setUsernameInput(e.target.value)}
                  placeholder="admin"
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Password
                </label>
                <input
                  type="text"
                  value={passwordInput}
                  onChange={(e) => setPasswordInput(e.target.value)}
                  placeholder="password"
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>
              
              <button
                onClick={detectAuthBruteforce}
                disabled={loading}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 transition-colors"
              >
                {loading ? 'Analyzing...' : 'Detect Auth Bruteforce'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Detection Result Display */}
      {detectionResult && (
        <div className="mt-6 bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4 text-gray-800 dark:text-white">Detection Result</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div className="border border-gray-200 dark:border-gray-700 rounded p-3">
              <p className="text-sm text-gray-600 dark:text-gray-300">Threat Type</p>
              <p className="text-lg font-bold text-gray-800 dark:text-white">{detectionResult.threat_type}</p>
            </div>
            <div className="border border-gray-200 dark:border-gray-700 rounded p-3">
              <p className="text-sm text-gray-600 dark:text-gray-300">Severity</p>
              <p className={`text-lg font-bold ${getThreatColor(detectionResult.severity)}`}>
                {detectionResult.severity}
              </p>
            </div>
            <div className="border border-gray-200 dark:border-gray-700 rounded p-3">
              <p className="text-sm text-gray-600 dark:text-gray-300">Confidence</p>
              <p className="text-lg font-bold text-blue-600 dark:text-blue-400">
                {(detectionResult.confidence * 100).toFixed(1)}%
              </p>
            </div>
            <div className="border border-gray-200 dark:border-gray-700 rounded p-3">
              <p className="text-sm text-gray-600 dark:text-gray-300">Timestamp</p>
              <p className="text-lg font-bold text-gray-800 dark:text-white">
                {new Date(detectionResult.timestamp).toLocaleString()}
              </p>
            </div>
          </div>

          <div className="mb-4">
            <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Detected Patterns:</p>
            <div className="flex flex-wrap gap-2">
              {detectionResult.detected_patterns.map((pattern, index) => (
                <span key={index} className="px-2 py-1 bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100 text-sm rounded">
                  {pattern}
                </span>
              ))}
            </div>
          </div>

          <div>
            <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Explanation:</p>
            <p className="text-gray-700 dark:text-gray-300">{detectionResult.explanation}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdvancedSecurityDashboard;