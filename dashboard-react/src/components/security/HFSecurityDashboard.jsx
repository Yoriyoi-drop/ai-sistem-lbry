import React, { useState } from 'react';
import axios from 'axios';

const HFSecurityDashboard = () => {
  const [input, setInput] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('threat');

  const analyzeWithHF = async () => {
    if (!input.trim()) {
      alert('Please enter a payload to analyze');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:8000/hf-security/analyze-threat', {
        payload: input,
        source_ip: '127.0.0.1'
      });
      setResult(response.data);
    } catch (error) {
      console.error('HF Analysis Error:', error);
      alert(`Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const detectSQLInjection = async () => {
    if (!input.trim()) {
      alert('Please enter a SQL query to analyze');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:8000/hf-security/sql-injection/detect', {
        query: input
      });
      setResult(response.data);
    } catch (error) {
      console.error('HF SQL Injection Detection Error:', error);
      alert(`Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const getThreatColor = (threatLevel) => {
    switch(threatLevel) {
      case 'CRITICAL': return 'text-red-600 bg-red-100 dark:bg-red-900 dark:text-red-100';
      case 'HIGH': return 'text-orange-600 bg-orange-100 dark:bg-orange-900 dark:text-orange-100';
      case 'MEDIUM': return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900 dark:text-yellow-100';
      case 'LOW': return 'text-green-600 bg-green-100 dark:bg-green-900 dark:text-green-100';
      default: return 'text-gray-600 bg-gray-100 dark:bg-gray-700 dark:text-gray-300';
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-gray-800 dark:text-white mb-6">Hugging Face Security Analysis</h1>
      
      <div className="bg-blue-50 dark:bg-blue-900/30 border border-blue-200 dark:border-blue-700 rounded-lg p-4 mb-6">
        <p className="text-blue-800 dark:text-blue-200">
          <strong>Note:</strong> This uses Hugging Face Inference API for security analysis. 
          Make sure to set your HF_TOKEN environment variable in the backend.
        </p>
      </div>
      
      {/* Tabs */}
      <div className="flex border-b border-gray-200 dark:border-gray-700 mb-6">
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'threat' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 dark:text-gray-400'}`}
          onClick={() => setActiveTab('threat')}
        >
          Threat Analysis
        </button>
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'sql' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 dark:text-gray-400'}`}
          onClick={() => setActiveTab('sql')}
        >
          SQL Injection Detection
        </button>
      </div>

      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          {activeTab === 'threat' ? 'Input Payload to Analyze' : 'SQL Query to Analyze'}
        </label>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={activeTab === 'threat' ? "Enter security payload to analyze..." : "SELECT * FROM users WHERE id = 1 OR 1=1"}
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 h-32 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
        />
        <button
          onClick={activeTab === 'threat' ? analyzeWithHF : detectSQLInjection}
          disabled={loading}
          className="mt-3 px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 disabled:opacity-50 transition-colors"
        >
          {loading 
            ? 'Analyzing with Hugging Face...' 
            : activeTab === 'threat' 
              ? 'Analyze with HF AI' 
              : 'Detect SQL Injection'}
        </button>
      </div>

      {result && (
        <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">
            {activeTab === 'threat' ? 'Threat Analysis Result' : 'SQL Injection Detection Result'}
          </h3>

          {activeTab === 'sql' ? (
            // SQL Injection Result Display
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div className="border border-gray-200 dark:border-gray-600 rounded p-3">
                  <p className="text-sm text-gray-600 dark:text-gray-300">Is Malicious</p>
                  <p className={`text-lg font-bold ${
                    result.is_malicious 
                      ? 'text-red-600 dark:text-red-400' 
                      : 'text-green-600 dark:text-green-400'
                  }`}>
                    {result.is_malicious ? 'YES' : 'NO'}
                  </p>
                </div>
                <div className="border border-gray-200 dark:border-gray-600 rounded p-3">
                  <p className="text-sm text-gray-600 dark:text-gray-300">Threat Level</p>
                  <p className={`text-lg font-bold ${getThreatColor(result.threat_level)}`}>
                    {result.threat_level}
                  </p>
                </div>
                <div className="border border-gray-200 dark:border-gray-600 rounded p-3">
                  <p className="text-sm text-gray-600 dark:text-gray-300">Confidence</p>
                  <p className="text-lg font-bold text-blue-600 dark:text-blue-400">
                    {(result.confidence * 100).toFixed(1)}%
                  </p>
                </div>
              </div>

              <div className="mb-4">
                <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Detected Patterns:</p>
                <div className="flex flex-wrap gap-2">
                  {result.detected_patterns && result.detected_patterns.length > 0 ? (
                    result.detected_patterns.map((pattern, index) => (
                      <span key={index} className="px-2 py-1 bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100 text-sm rounded">
                        {pattern}
                      </span>
                    ))
                  ) : (
                    <p className="text-gray-500 dark:text-gray-400">No specific patterns detected</p>
                  )}
                </div>
              </div>

              <div>
                <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Explanation:</p>
                <p className="text-gray-700 dark:text-gray-300">{result.explanation}</p>
              </div>
            </div>
          ) : (
            // Threat Analysis Result Display
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
                <div className="border border-gray-200 dark:border-gray-600 rounded p-3">
                  <p className="text-sm text-gray-600 dark:text-gray-300">Threat Type</p>
                  <p className="text-lg font-bold text-gray-800 dark:text-white">
                    {result.threat_type}
                  </p>
                </div>
                <div className="border border-gray-200 dark:border-gray-600 rounded p-3">
                  <p className="text-sm text-gray-600 dark:text-gray-300">Severity</p>
                  <p className={`text-lg font-bold ${getThreatColor(result.severity)}`}>
                    {result.severity}
                  </p>
                </div>
                <div className="border border-gray-200 dark:border-gray-600 rounded p-3">
                  <p className="text-sm text-gray-600 dark:text-gray-300">Confidence</p>
                  <p className="text-lg font-bold text-blue-600 dark:text-blue-400">
                    {(result.confidence * 100).toFixed(1)}%
                  </p>
                </div>
              </div>

              <div className="mb-4">
                <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Detected Patterns:</p>
                <div className="flex flex-wrap gap-2">
                  {result.detected_patterns && result.detected_patterns.length > 0 ? (
                    result.detected_patterns.map((pattern, index) => (
                      <span key={index} className="px-2 py-1 bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100 text-sm rounded">
                        {pattern}
                      </span>
                    ))
                  ) : (
                    <p className="text-gray-500 dark:text-gray-400">No specific patterns detected</p>
                  )}
                </div>
              </div>

              <div>
                <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Explanation:</p>
                <p className="text-gray-700 dark:text-gray-300">{result.explanation}</p>
              </div>

              <div className="mt-4 p-3 bg-gray-50 dark:bg-gray-700 rounded">
                <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Query Sample:</p>
                <code className="text-xs p-2 bg-gray-100 dark:bg-gray-800 rounded break-all block">
                  {result.payload || result.query_sample}
                </code>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default HFSecurityDashboard;