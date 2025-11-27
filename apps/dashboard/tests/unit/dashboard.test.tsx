/**
 * Dashboard page unit tests
 *
 * @created 2025-11-26
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import Dashboard from '../../src/pages/Dashboard';
import { BrowserRouter } from 'react-router-dom';
import { Provider } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import { useAuth } from '../../src/hooks/useAuth';

// Mock the useAuth hook
vi.mock('../../src/hooks/useAuth', () => ({
  useAuth: vi.fn(),
}));

// Mock the Redux store
const mockStore = configureStore({
  reducer: {
    security: () => ({
      stats: {
        totalEvents: 150,
        criticalEvents: 12,
        activeThreats: 8,
        blockedRequests: 250
      },
      loading: false
    }),
    agents: () => ({
      agents: [
        { id: 1, name: 'Test Agent', status: 'online' },
        { id: 2, name: 'Test Agent 2', status: 'offline' }
      ],
      loading: false
    })
  },
});

const MockDashboard = () => {
  return (
    <Provider store={mockStore}>
      <BrowserRouter future={{
        v7_startTransition: true,
        v7_relativeSplatPath: true
      }}>
        <Dashboard />
      </BrowserRouter>
    </Provider>
  );
};

describe('Dashboard Page', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    (useAuth as vi.Mock).mockReturnValue({
      login: vi.fn(),
      register: vi.fn(),
      logout: vi.fn(),
      user: { id: 1, username: 'testuser', email: 'test@example.com' },
      loading: false,
      error: null,
    });
  });

  it('renders dashboard title', () => {
    render(<MockDashboard />);
    
    const title = screen.getByText('Dashboard Overview');
    expect(title).toBeInTheDocument();
    
    const subtitle = screen.getByText('Welcome to the Infinite AI Security Platform');
    expect(subtitle).toBeInTheDocument();
  });

  it('renders stats cards with correct data', () => {
    render(<MockDashboard />);
    
    expect(screen.getByText('150')).toBeInTheDocument(); // Total Security Events
    expect(screen.getByText('12')).toBeInTheDocument(); // Critical Events
    expect(screen.getByText('8')).toBeInTheDocument(); // Active Threats
    expect(screen.getByText('250')).toBeInTheDocument(); // Blocked Requests
  });

  it('renders agent status information', () => {
    render(<MockDashboard />);
    
    const agentStatusCard = screen.getByText('AI Agents Status');
    expect(agentStatusCard).toBeInTheDocument();
  });

  it('renders recent security events', () => {
    render(<MockDashboard />);
    
    const eventsTable = screen.getByText('Recent Security Events');
    expect(eventsTable).toBeInTheDocument();
    
    // Check for some example events
    expect(screen.getByText('SQL Injection')).toBeInTheDocument();
    expect(screen.getByText('XSS Attempt')).toBeInTheDocument();
  });

  it('renders system health information', () => {
    render(<MockDashboard />);
    
    const healthCard = screen.getByText('System Health');
    expect(healthCard).toBeInTheDocument();
    
    expect(screen.getByText('CPU Usage')).toBeInTheDocument();
    expect(screen.getByText('Memory Usage')).toBeInTheDocument();
  });

  it('renders chart placeholders', () => {
    render(<MockDashboard />);
    
    expect(screen.getByText('Security Events Over Time')).toBeInTheDocument();
    expect(screen.getByText('Threat Distribution by Type')).toBeInTheDocument();
  });
});