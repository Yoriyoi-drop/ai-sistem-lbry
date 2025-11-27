import React, { useState, useEffect } from 'react';
import axios from 'axios';

const NeuralSecurityDashboard = () => {
  const [selectedThreatType, setSelectedThreatType] = useState('xss');
  const [inputContent, setInputContent] = useState('');
  const [detectionResult, setDetectionResult] = useState(null);
  const [modelStatus, setModelStatus] = useState({});
  const [loading, setLoading] = useState(false);
  const [trainingStatus, setTrainingStatus] = useState('Not started');
  const [bulkContents, setBulkContents] = useState('');

  // Fetch model status on component mount
  useEffect(() => {
    fetchModelStatus();
  }, []);

  const fetchModelStatus = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/neural-security/model-status');
      setModelStatus(response.data);
    } catch (error) {
      console.error('Error fetching model status:', error);
    }
  };

  const detectThreat = async () => {
    if (!inputContent.trim()) return;
    
    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:8000/neural-security/detect', {
        content: inputContent,
        threat_type: selectedThreatType
      });
      setDetectionResult(response.data);
    } catch (error) {
      console.error('Neural detection error:', error);
    } finally {
      setLoading(false);
    }
  };

  const startTraining = async () => {
    setTrainingStatus('Starting...');
    try {
      const response = await axios.get('http://127.0.0.1:8000/neural-security/train-model');
      setTrainingStatus('Training started in background');
      // Check status after a delay
      setTimeout(fetchModelStatus, 5000);
    } catch (error) {
      console.error('Training error:', error);
      setTrainingStatus('Error starting training');
    }
  };

  const bulkDetect = async () => {
    if (!bulkContents.trim()) return;
    
    setLoading(true);
    try {
      const contentList = bulkContents.split('\n').filter(line => line.trim());
      const response = await axios.post('http://127.0.0.1:8000/neural-security/bulk-detect', {
        contents: contentList,
        threat_type: selectedThreatType
      });
      
      setDetectionResult({
        ...response.data,
        isBulk: true
      });
    } catch (error) {
      console.error('Bulk detection error:', error);
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

  const threatTypes = [
    { value: 'xss', label: 'XSS Detection', icon: '🛡️' },
    { value: 'sqli', label: 'SQL Injection', icon: '🔍' },
    { value: 'cmd_injection', label: 'Command Injection', icon: '⚙️' },
    { value: 'path_traversal', label: 'Path Traversal', icon: '📁' }
  ];

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-gray-800 dark:text-white mb-6">Neural Network Security Detection</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        {/* Model Status Panel */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-white">Model Status</h2>
          
          {modelStatus.model_status ? (
            <div className="space-y-3">
              {Object.entries(modelStatus.model_status).map(([type, status]) => (
                <div key={type} className="flex justify-between items-center">
                  <span className="text-gray-600 dark:text-gray-300 capitalize">{type.replace('_', ' ')}</span>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    status.loaded 
                      ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100' 
                      : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100'
                  }`}>
                    {status.loaded ? 'READY' : 'NEEDS TRAINING'}
                  </span>
                </div>
              ))}
              
              <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                <p className="text-sm text-gray-600 dark:text-gray-300">
                  Ready: {modelStatus.ready_models}/{modelStatus.total_models}
                </p>
                <button
                  onClick={startTraining}
                  className="mt-2 w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
                >
                  {trainingStatus.startsWith('Training') ? '🔄 Training...' : 'Train Neural Models'}
                </button>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">{trainingStatus}</p>
              </div>
            </div>
          ) : (
            <p className="text-gray-500 dark:text-gray-400">Loading model status...</p>
          )}
        </div>

        {/* Threat Type Selector */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-white">Select Threat Type</h2>
          
          <div className="space-y-2">
            {threatTypes.map((type) => (
              <div
                key={type.value}
                className={`flex items-center p-3 rounded-lg cursor-pointer transition-colors ${
                  selectedThreatType === type.value
                    ? 'bg-blue-100 dark:bg-blue-900 border border-blue-300 dark:border-blue-700'
                    : 'bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600'
                }`}
                onClick={() => setSelectedThreatType(type.value)}
              >
                <span className="text-lg mr-3">{type.icon}</span>
                <span className="font-medium text-gray-800 dark:text-white">{type.label}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Input Panel */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-white">Test Neural Detection</h2>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Input Content
            </label>
            <textarea
              value={inputContent}
              onChange={(e) => setInputContent(e.target.value)}
              placeholder="Enter content to analyze..."
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 h-32 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            />
          </div>
          
          <button
            onClick={detectThreat}
            disabled={loading}
            className="w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 transition-colors"
          >
            {loading ? 'Analyzing with Neural Network...' : 'Detect with Neural Network'}
          </button>
        </div>
      </div>

      {/* Bulk Detection Panel */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-white">Bulk Detection</h2>
        
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Multiple contents (one per line)
          </label>
          <textarea
            value={bulkContents}
            onChange={(e) => setBulkContents(e.target.value)}
            placeholder="Enter multiple content lines to analyze..."
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 h-32 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          />
        </div>
        
        <button
          onClick={bulkDetect}
          disabled={loading}
          className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 disabled:opacity-50 transition-colors"
        >
          {loading ? 'Bulk Analyzing...' : 'Bulk Detect (Neural Network)'}
        </button>
      </div>

      {/* Detection Result Display */}
      {detectionResult && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4 text-gray-800 dark:text-white">Detection Result</h3>
          
          {detectionResult.isBulk ? (
            // Bulk results display
            <div>
              <h4 className="font-medium text-gray-700 dark:text-gray-300 mb-3">Bulk Analysis Results ({detectionResult.total_processed} items)</h4>
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {detectionResult.results.map((result, index) => (
                  <div key={index} className="border border-gray-200 dark:border-gray-700 rounded p-3">
                    <div className="flex justify-between items-start">
                      <div>
                        <span className="font-medium text-gray-800 dark:text-white">Item {index + 1}:</span>
                        <span className="ml-2 text-sm text-gray-600 dark:text-gray-300">{result.content_preview.substring(0, 50)}{result.content_preview.length > 50 ? '...' : ''}</span>
                      </div>
                      <span className={`px-2 py-1 rounded text-xs font-medium ${getThreatColor(result.severity)}`}>
                        {result.severity} ({(result.confidence * 100).toFixed(1)}%)
                      </span>
                    </div>
                    <div className="mt-2">
                      <span className={`inline-block px-2 py-1 rounded text-xs ${
                        result.is_malicious 
                          ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100' 
                          : 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100'
                      }`}>
                        {result.is_malicious ? '❌ MALICIOUS' : '✅ SAFE'}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
              <p className="mt-3 text-sm text-gray-600 dark:text-gray-300">
                Processing time: {detectionResult.processing_time.toFixed(3)} seconds
              </p>
            </div>
          ) : (
            // Single result display
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div className="border border-gray-200 dark:border-gray-700 rounded p-3">
                <p className="text-sm text-gray-600 dark:text-gray-300">Threat Type</p>
                <p className="text-lg font-bold text-gray-800 dark:text-white capitalize">{detectionResult.threat_type.replace('_', ' ')}</p>
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
                <p className="text-sm text-gray-600 dark:text-gray-300">Malicious</p>
                <p className={`text-lg font-bold ${
                  detectionResult.is_malicious 
                    ? 'text-red-600 dark:text-red-400' 
                    : 'text-green-600 dark:text-green-400'
                }`}>
                  {detectionResult.is_malicious ? 'YES' : 'NO'}
                </p>
              </div>
            </div>
          )}

          <div className="mt-4">
            <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Content Preview:</p>
            <code className="text-xs p-3 bg-gray-100 dark:bg-gray-700 rounded block overflow-x-auto">
              {detectionResult.content_preview}
            </code>
            {detectionResult.processing_time && (
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
                Processing time: {detectionResult.processing_time.toFixed(4)} seconds
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default NeuralSecurityDashboard;