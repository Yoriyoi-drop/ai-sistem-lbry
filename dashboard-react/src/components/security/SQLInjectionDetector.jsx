import React, { useState } from 'react';
import axios from 'axios';

const SQLInjectionDetector = () => {
  const [sqlQuery, setSqlQuery] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const detectSQLInjection = async () => {
    if (!sqlQuery.trim()) {
      setError('Please enter a SQL query to analyze');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post('http://127.0.0.1:8000/sql-injection/detect', {
        query: sqlQuery
      });

      setResult(response.data);
    } catch (err) {
      setError('Error detecting SQL injection. Please make sure the backend is running.');
      console.error('API Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getThreatColor = (threatLevel) => {
    switch(threatLevel) {
      case 'CRITICAL': return 'text-red-600 bg-red-100';
      case 'HIGH': return 'text-orange-600 bg-orange-100';
      case 'MEDIUM': return 'text-yellow-600 bg-yellow-100';
      case 'LOW': return 'text-green-600 bg-green-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white dark:bg-gray-800 rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-6">SQL Injection Detection</h2>
      
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Enter SQL Query to Analyze
        </label>
        <textarea
          value={sqlQuery}
          onChange={(e) => setSqlQuery(e.target.value)}
          placeholder="SELECT * FROM users WHERE id = 1 OR 1=1"
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 h-32 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
        />
        <button
          onClick={detectSQLInjection}
          disabled={loading}
          className="mt-3 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 transition-colors"
        >
          {loading ? 'Analyzing...' : 'Detect SQL Injection'}
        </button>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-100 rounded-md">
          {error}
        </div>
      )}

      {result && (
        <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 mt-4 bg-white dark:bg-gray-700">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-3">Analysis Results</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div className="border border-gray-200 dark:border-gray-600 rounded p-3">
              <p className="text-sm text-gray-600 dark:text-gray-300">Threat Level</p>
              <p className={`text-lg font-bold ${getThreatColor(result.threat_level)}`}>
                {result.threat_level}
              </p>
            </div>
            <div className="border border-gray-200 dark:border-gray-600 rounded p-3">
              <p className="text-sm text-gray-600 dark:text-gray-300">Confidence Score</p>
              <p className="text-lg font-bold text-blue-600 dark:text-blue-400">
                {(result.confidence * 100).toFixed(1)}%
              </p>
            </div>
          </div>

          <div className="mb-4">
            <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Malicious Query:</p>
            <div className={`px-3 py-2 rounded ${result.is_malicious ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100' : 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100'}`}>
              {result.is_malicious ? '⚠️ YES - This query contains SQL injection patterns' : '✅ NO - No SQL injection patterns detected'}
            </div>
          </div>

          {result.detected_patterns.length > 0 && (
            <div className="mb-4">
              <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Detected Patterns:</p>
              <div className="flex flex-wrap gap-2">
                {result.detected_patterns.map((pattern, index) => (
                  <span key={index} className="px-2 py-1 bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100 text-sm rounded">
                    {pattern}
                  </span>
                ))}
              </div>
            </div>
          )}

          <div className="mb-4">
            <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Analysis Explanation:</p>
            <p className="text-gray-700 dark:text-gray-300">{result.explanation}</p>
          </div>

          <div className="mt-4 p-3 bg-gray-50 dark:bg-gray-600 rounded">
            <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Query Sample:</p>
            <code className="text-xs p-2 bg-gray-100 dark:bg-gray-800 rounded break-all block">
              {result.query_sample}
            </code>
          </div>
        </div>
      )}
    </div>
  );
};

export default SQLInjectionDetector;