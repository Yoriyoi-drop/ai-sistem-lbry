import React, { useState, useEffect } from 'react';
import axios from 'axios';

const SettingsPage = () => {
  const [activeTab, setActiveTab] = useState('general');
  const [settings, setSettings] = useState({
    general: {
      appName: 'Infinite AI Security Platform',
      appDescription: 'Advanced AI-powered security platform',
      appUrl: 'https://security.example.com',
      timezone: 'UTC',
      language: 'en-US'
    },
    security: {
      twoFactorAuth: true,
      sessionTimeout: 30,
      passwordComplexity: 'high',
      ipWhitelist: ['192.168.1.0/24', '10.0.0.0/8'],
      failedLoginAttempts: 5,
      lockoutDuration: 15
    },
    notifications: {
      emailAlerts: true,
      criticalOnly: false,
      emailAddresses: ['admin@example.com', 'security@example.com'],
      slackWebhook: '',
      smsAlerts: false,
      smsNumbers: []
    },
    api: {
      rateLimit: 1000,
      requestTimeout: 30,
      corsOrigins: ['http://localhost:3000', 'https://app.example.com'],
      apiKeyExpiry: 30
    }
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  // Load settings from API on component mount
  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    setLoading(true);
    try {
      // In a real app, this would fetch from backend API
      //const response = await axios.get('/api/settings');
      //setSettings(response.data);
    } catch (error) {
      setMessage('Failed to load settings');
      console.error('Error loading settings:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (tab, field, value) => {
    setSettings(prev => ({
      ...prev,
      [tab]: {
        ...prev[tab],
        [field]: value
      }
    }));
  };

  const handleArrayChange = (tab, field, index, value) => {
    const newArray = [...settings[tab][field]];
    newArray[index] = value;
    handleInputChange(tab, field, newArray);
  };

  const addArrayItem = (tab, field, value = '') => {
    const newArray = [...settings[tab][field], value];
    handleInputChange(tab, field, newArray);
  };

  const removeArrayItem = (tab, field, index) => {
    const newArray = settings[tab][field].filter((_, i) => i !== index);
    handleInputChange(tab, field, newArray);
  };

  const saveSettings = async () => {
    setLoading(true);
    setMessage('');
    try {
      // Simulate API call to save settings
      await new Promise(resolve => setTimeout(resolve, 800)); // Simulate network delay
      setMessage('Settings saved successfully!');
      // In a real app: await axios.post('/api/settings', settings);
    } catch (error) {
      setMessage('Failed to save settings');
      console.error('Error saving settings:', error);
    } finally {
      setLoading(false);
    }
  };

  const resetToDefaults = () => {
    const defaultSettings = {
      general: {
        appName: 'Infinite AI Security Platform',
        appDescription: 'Advanced AI-powered security platform',
        appUrl: 'https://security.example.com',
        timezone: 'UTC',
        language: 'en-US'
      },
      security: {
        twoFactorAuth: true,
        sessionTimeout: 30,
        passwordComplexity: 'high',
        ipWhitelist: ['192.168.1.0/24', '10.0.0.0/8'],
        failedLoginAttempts: 5,
        lockoutDuration: 15
      },
      notifications: {
        emailAlerts: true,
        criticalOnly: false,
        emailAddresses: ['admin@example.com', 'security@example.com'],
        slackWebhook: '',
        smsAlerts: false,
        smsNumbers: []
      },
      api: {
        rateLimit: 1000,
        requestTimeout: 30,
        corsOrigins: ['http://localhost:3000', 'https://app.example.com'],
        apiKeyExpiry: 30
      }
    };
    setSettings(defaultSettings);
    setMessage('Settings reset to defaults');
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-gray-800 dark:text-white mb-6">Settings</h1>

      {message && (
        <div className={`mb-4 p-3 rounded-md ${
          message.includes('successfully') ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100' :
          message.includes('Failed') ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100' :
          'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100'
        }`}>
          {message}
        </div>
      )}

      {/* Navigation Tabs */}
      <div className="flex border-b border-gray-200 dark:border-gray-700 mb-6">
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'general' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 dark:text-gray-400'}`}
          onClick={() => setActiveTab('general')}
        >
          General
        </button>
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'security' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 dark:text-gray-400'}`}
          onClick={() => setActiveTab('security')}
        >
          Security
        </button>
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'notifications' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 dark:text-gray-400'}`}
          onClick={() => setActiveTab('notifications')}
        >
          Notifications
        </button>
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'api' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 dark:text-gray-400'}`}
          onClick={() => setActiveTab('api')}
        >
          API
        </button>
      </div>

      {/* Loading indicator */}
      {loading && (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      )}

      {/* General Settings */}
      {!loading && activeTab === 'general' && (
        <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 space-y-6">
          <h2 className="text-xl font-semibold text-gray-800 dark:text-white">General Settings</h2>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Application Name</label>
              <input
                type="text"
                value={settings.general.appName}
                onChange={(e) => handleInputChange('general', 'appName', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Description</label>
              <textarea
                value={settings.general.appDescription}
                onChange={(e) => handleInputChange('general', 'appDescription', e.target.value)}
                rows="3"
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Application URL</label>
              <input
                type="text"
                value={settings.general.appUrl}
                onChange={(e) => handleInputChange('general', 'appUrl', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Timezone</label>
                <select
                  value={settings.general.timezone}
                  onChange={(e) => handleInputChange('general', 'timezone', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                >
                  <option value="UTC">UTC</option>
                  <option value="US/Eastern">US/Eastern</option>
                  <option value="US/Central">US/Central</option>
                  <option value="US/Mountain">US/Mountain</option>
                  <option value="US/Pacific">US/Pacific</option>
                  <option value="Europe/London">Europe/London</option>
                  <option value="Europe/Paris">Europe/Paris</option>
                  <option value="Asia/Tokyo">Asia/Tokyo</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Language</label>
                <select
                  value={settings.general.language}
                  onChange={(e) => handleInputChange('general', 'language', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                >
                  <option value="en-US">English (US)</option>
                  <option value="en-GB">English (UK)</option>
                  <option value="es-ES">Spanish</option>
                  <option value="fr-FR">French</option>
                  <option value="de-DE">German</option>
                  <option value="ja-JP">Japanese</option>
                  <option value="zh-CN">Chinese</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Security Settings */}
      {!loading && activeTab === 'security' && (
        <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 space-y-6">
          <h2 className="text-xl font-semibold text-gray-800 dark:text-white">Security Settings</h2>

          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-sm font-medium text-gray-800 dark:text-white">Two-Factor Authentication</h3>
                <p className="text-sm text-gray-500 dark:text-gray-400">Require 2FA for all user accounts</p>
              </div>
              <button
                onClick={() => handleInputChange('security', 'twoFactorAuth', !settings.security.twoFactorAuth)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full ${
                  settings.security.twoFactorAuth ? 'bg-blue-600' : 'bg-gray-200 dark:bg-gray-600'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                    settings.security.twoFactorAuth ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Session Timeout (minutes)</label>
              <input
                type="number"
                value={settings.security.sessionTimeout}
                onChange={(e) => handleInputChange('security', 'sessionTimeout', parseInt(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Password Complexity</label>
              <select
                value={settings.security.passwordComplexity}
                onChange={(e) => handleInputChange('security', 'passwordComplexity', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              >
                <option value="low">Low (8+ characters)</option>
                <option value="medium">Medium (8+ chars, number, uppercase)</option>
                <option value="high">High (8+ chars, number, uppercase, special char)</option>
                <option value="very_high">Very High (12+ chars, 2 numbers, uppercase, lowercase, special char)</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">IP Whitelist</label>
              <div className="space-y-2">
                {settings.security.ipWhitelist.map((ip, index) => (
                  <div key={index} className="flex">
                    <input
                      type="text"
                      value={ip}
                      onChange={(e) => handleArrayChange('security', 'ipWhitelist', index, e.target.value)}
                      placeholder="e.g., 192.168.1.0/24"
                      className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    />
                    <button
                      onClick={() => removeArrayItem('security', 'ipWhitelist', index)}
                      className="ml-2 px-3 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 transition-colors"
                    >
                      Remove
                    </button>
                  </div>
                ))}
                <button
                  onClick={() => addArrayItem('security', 'ipWhitelist')}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
                >
                  Add IP Range
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Failed Login Attempts</label>
                <input
                  type="number"
                  value={settings.security.failedLoginAttempts}
                  onChange={(e) => handleInputChange('security', 'failedLoginAttempts', parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Lockout Duration (minutes)</label>
                <input
                  type="number"
                  value={settings.security.lockoutDuration}
                  onChange={(e) => handleInputChange('security', 'lockoutDuration', parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Notifications Settings */}
      {!loading && activeTab === 'notifications' && (
        <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 space-y-6">
          <h2 className="text-xl font-semibold text-gray-800 dark:text-white">Notification Settings</h2>

          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-sm font-medium text-gray-800 dark:text-white">Email Alerts</h3>
                <p className="text-sm text-gray-500 dark:text-gray-400">Send email notifications for security events</p>
              </div>
              <button
                onClick={() => handleInputChange('notifications', 'emailAlerts', !settings.notifications.emailAlerts)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full ${
                  settings.notifications.emailAlerts ? 'bg-blue-600' : 'bg-gray-200 dark:bg-gray-600'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                    settings.notifications.emailAlerts ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>

            {settings.notifications.emailAlerts && (
              <>
                <div className="flex items-center justify-between ml-6">
                  <div>
                    <h3 className="text-sm font-medium text-gray-800 dark:text-white">Critical Only</h3>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Only send emails for critical events</p>
                  </div>
                  <button
                    onClick={() => handleInputChange('notifications', 'criticalOnly', !settings.notifications.criticalOnly)}
                    className={`relative inline-flex h-6 w-11 items-center rounded-full ${
                      settings.notifications.criticalOnly ? 'bg-blue-600' : 'bg-gray-200 dark:bg-gray-600'
                    }`}
                  >
                    <span
                      className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                        settings.notifications.criticalOnly ? 'translate-x-6' : 'translate-x-1'
                      }`}
                    />
                  </button>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email Addresses</label>
                  <div className="space-y-2">
                    {settings.notifications.emailAddresses.map((email, index) => (
                      <div key={index} className="flex">
                        <input
                          type="email"
                          value={email}
                          onChange={(e) => handleArrayChange('notifications', 'emailAddresses', index, e.target.value)}
                          placeholder="email@example.com"
                          className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                        />
                        <button
                          onClick={() => removeArrayItem('notifications', 'emailAddresses', index)}
                          className="ml-2 px-3 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 transition-colors"
                        >
                          Remove
                        </button>
                      </div>
                    ))}
                    <button
                      onClick={() => addArrayItem('notifications', 'emailAddresses')}
                      className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
                    >
                      Add Email Address
                    </button>
                  </div>
                </div>
              </>
            )}

            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-sm font-medium text-gray-800 dark:text-white">SMS Alerts</h3>
                <p className="text-sm text-gray-500 dark:text-gray-400">Send SMS notifications for critical events</p>
              </div>
              <button
                onClick={() => handleInputChange('notifications', 'smsAlerts', !settings.notifications.smsAlerts)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full ${
                  settings.notifications.smsAlerts ? 'bg-blue-600' : 'bg-gray-200 dark:bg-gray-600'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                    settings.notifications.smsAlerts ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>

            {settings.notifications.smsAlerts && (
              <div className="ml-6">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">SMS Numbers</label>
                <div className="space-y-2">
                  {settings.notifications.smsNumbers.map((number, index) => (
                    <div key={index} className="flex">
                      <input
                        type="tel"
                        value={number}
                        onChange={(e) => handleArrayChange('notifications', 'smsNumbers', index, e.target.value)}
                        placeholder="+1234567890"
                        className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                      />
                      <button
                        onClick={() => removeArrayItem('notifications', 'smsNumbers', index)}
                        className="ml-2 px-3 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 transition-colors"
                      >
                        Remove
                      </button>
                    </div>
                  ))}
                  <button
                    onClick={() => addArrayItem('notifications', 'smsNumbers')}
                    className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
                  >
                    Add Phone Number
                  </button>
                </div>
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Slack Webhook URL</label>
              <input
                type="text"
                value={settings.notifications.slackWebhook}
                onChange={(e) => handleInputChange('notifications', 'slackWebhook', e.target.value)}
                placeholder="https://hooks.slack.com/services/..."
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              />
            </div>
          </div>
        </div>
      )}

      {/* API Settings */}
      {!loading && activeTab === 'api' && (
        <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 space-y-6">
          <h2 className="text-xl font-semibold text-gray-800 dark:text-white">API Settings</h2>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Rate Limit (requests per minute)</label>
              <input
                type="number"
                value={settings.api.rateLimit}
                onChange={(e) => handleInputChange('api', 'rateLimit', parseInt(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Request Timeout (seconds)</label>
              <input
                type="number"
                value={settings.api.requestTimeout}
                onChange={(e) => handleInputChange('api', 'requestTimeout', parseInt(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">API Key Expiry (days)</label>
              <input
                type="number"
                value={settings.api.apiKeyExpiry}
                onChange={(e) => handleInputChange('api', 'apiKeyExpiry', parseInt(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">CORS Allowed Origins</label>
              <div className="space-y-2">
                {settings.api.corsOrigins.map((origin, index) => (
                  <div key={index} className="flex">
                    <input
                      type="text"
                      value={origin}
                      onChange={(e) => handleArrayChange('api', 'corsOrigins', index, e.target.value)}
                      placeholder="https://example.com"
                      className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    />
                    <button
                      onClick={() => removeArrayItem('api', 'corsOrigins', index)}
                      className="ml-2 px-3 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 transition-colors"
                    >
                      Remove
                    </button>
                  </div>
                ))}
                <button
                  onClick={() => addArrayItem('api', 'corsOrigins')}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
                >
                  Add Origin
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Action Buttons */}
      {!loading && (
        <div className="mt-6 flex justify-between">
          <button
            onClick={resetToDefaults}
            className="px-6 py-3 bg-gray-600 text-white rounded-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 transition-colors"
          >
            Reset to Defaults
          </button>
          <button
            onClick={saveSettings}
            disabled={loading}
            className="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors disabled:opacity-50"
          >
            {loading ? 'Saving...' : 'Save Settings'}
          </button>
        </div>
      )}
    </div>
  );
};

export default SettingsPage;