import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './hooks';
import { Layout } from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import Agents from './pages/Agents';
import SecurityScans from './pages/SecurityScans';
import Threats from './pages/Threats';
import Security from './pages/Security';
import Settings from './pages/Settings';
import Workflow from './pages/Workflow';
import Login from './pages/auth/Login';
import './App.css';

const App: React.FC = () => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!user) {
    return (
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    );
  }

  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/agents" element={<Agents />} />
        <Route path="/scans" element={<SecurityScans />} />
        <Route path="/threats" element={<Threats />} />
        <Route path="/security" element={<Security />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/workflow" element={<Workflow />} />
        <Route path="*" element={<Navigate to="/dashboard" />} />
      </Routes>
    </Layout>
  );
};

export default App;