import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ErrorBoundary } from 'react-error-boundary';
import { Toaster } from 'react-hot-toast';
import Header from '@components/layout/Header';
import Sidebar from '@components/layout/Sidebar';
import Dashboard from '@pages/Dashboard';
import WorkflowsPage from '@pages/Workflows';
import NodesPage from '@pages/Nodes';
import TeamsPage from '@pages/Teams';
import QueuePage from '@pages/Queue';
import HealthPage from '@pages/Health';
import AlertsPage from '@pages/Alerts';
import LogsPage from '@pages/Logs';
import SettingsPage from '@pages/Settings';
import SQLInjectionDetector from '@components/security/SQLInjectionDetector';
import AdvancedSecurityDashboard from '@components/security/AdvancedSecurityDashboard';
import NeuralSecurityDashboard from '@components/security/NeuralSecurityDashboard';
import HFSecurityDashboard from '@components/security/HFSecurityDashboard';
import './index.css';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function ErrorFallback({ error }) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-light-bg dark:bg-dark-bg">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-error-light dark:text-error-dark mb-4">
          Something went wrong
        </h2>
        <pre className="text-sm text-light-text-secondary dark:text-dark-text-secondary">
          {error.message}
        </pre>
      </div>
    </div>
  );
}

function App() {
  const [sidebarOpen, setSidebarOpen] = React.useState(false);
  const [windowWidth, setWindowWidth] = React.useState(window.innerWidth);

  React.useEffect(() => {
    const handleResize = () => {
      setWindowWidth(window.innerWidth);
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // For large screens, sidebar should always be open (unless explicitly closed by user)
  const isLargeScreen = windowWidth >= 1024;
  const effectiveSidebarOpen = isLargeScreen ? true : sidebarOpen;

  return (
    <ErrorBoundary FallbackComponent={ErrorFallback}>
      <QueryClientProvider client={queryClient}>
        <Router>
          <div className="min-h-screen bg-light-bg dark:bg-dark-bg">
            <Header onMenuClick={() => setSidebarOpen(!sidebarOpen)} />

            <div className="flex pt-16">
              <Sidebar
                isOpen={effectiveSidebarOpen}
                onClose={() => setSidebarOpen(false)}
              />

              <main className="flex-1 p-4 md:p-6 lg:p-8 ml-0">
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/workflows" element={<WorkflowsPage />} />
                  <Route path="/nodes" element={<NodesPage />} />
                  <Route path="/teams" element={<TeamsPage />} />
                  <Route path="/queue" element={<QueuePage />} />
                  <Route path="/health" element={<HealthPage />} />
                  <Route path="/alerts" element={<AlertsPage />} />
                  <Route path="/logs" element={<LogsPage />} />
                  <Route path="/settings" element={<SettingsPage />} />
                  <Route path="/sql-injection" element={<SQLInjectionDetector />} />
                  <Route path="/advanced-security" element={<AdvancedSecurityDashboard />} />
                  <Route path="/neural-security" element={<NeuralSecurityDashboard />} />
                  <Route path="/hf-security" element={<HFSecurityDashboard />} />
                </Routes>
              </main>
            </div>

            <Toaster
              position="top-right"
              toastOptions={{
                className: 'bg-light-panel dark:bg-dark-panel',
                style: {
                  background: 'var(--color-panel)',
                  color: 'var(--color-text)',
                },
              }}
            />
          </div>
        </Router>
      </QueryClientProvider>
    </ErrorBoundary>
  );
}

export default App;
