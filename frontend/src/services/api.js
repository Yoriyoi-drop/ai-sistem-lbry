// API service for frontend
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Create axios instance with defaults
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// System metrics
export const getSystemMetrics = () => {
  return apiClient.get('/monitoring/system-overview');
};

// Agents
export const getAgents = () => {
  return apiClient.get('/agents');
};

export const startAgent = (agentId) => {
  return apiClient.post(`/agents/${agentId}/start`);
};

export const stopAgent = (agentId) => {
  return apiClient.post(`/agents/${agentId}/stop`);
};

// Workflows
export const getWorkflows = () => {
  return apiClient.get('/workflows');
};

export const createWorkflow = (workflowData) => {
  return apiClient.post('/workflows', workflowData);
};

export const updateWorkflow = (workflowId, workflowData) => {
  return apiClient.put(`/workflows/${workflowId}`, workflowData);
};

export const deleteWorkflow = (workflowId) => {
  return apiClient.delete(`/workflows/${workflowId}`);
};

// User and authentication
export const login = (credentials) => {
  return apiClient.post('/auth/login', credentials);
};

export const logout = () => {
  return apiClient.post('/auth/logout');
};

export const getCurrentUser = () => {
  return apiClient.get('/users/me');
};

// API keys
export const getApiKeys = () => {
  return apiClient.get('/tokens');
};

export const createApiKey = (keyData) => {
  return apiClient.post('/tokens', keyData);
};

export const deleteApiKey = (keyId) => {
  return apiClient.delete(`/tokens/${keyId}`);
};

// Subscription and billing
export const getSubscription = () => {
  return apiClient.get('/billing/subscription');
};

export const updateSubscription = (tier) => {
  return apiClient.post('/billing/subscription', { tier });
};

export const getUsage = () => {
  return apiClient.get('/billing/usage');
};

// Model management
export const getModels = () => {
  return apiClient.get('/models');
};

export const getModelInfo = (modelId) => {
  return apiClient.get(`/models/${modelId}`);
};

export const executeModel = (modelId, inputData) => {
  return apiClient.post(`/models/${modelId}/execute`, inputData);
};