/**
 * Header component unit tests
 *
 * @created 2025-11-26
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Header } from '../../src/components/layout/Header';
import { BrowserRouter } from 'react-router-dom';
import { useAuth } from '../../src/hooks/useAuth';

// Mock the useAuth hook
vi.mock('../../src/hooks/useAuth', () => ({
  useAuth: vi.fn(),
}));

const MockHeader = (props: any) => {
  return (
    <BrowserRouter future={{
      v7_startTransition: true,
      v7_relativeSplatPath: true
    }}>
      <Header {...props} />
    </BrowserRouter>
  );
};

describe('Header Component', () => {
  const mockToggleSidebar = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    (useAuth as vi.Mock).mockReturnValue({
      user: { username: 'testuser', email: 'test@example.com' },
      logout: vi.fn(),
    });
  });

  it('renders header with user information', () => {
    render(<MockHeader sidebarOpen={true} toggleSidebar={mockToggleSidebar} />);
    
    const header = screen.getByRole('banner');
    expect(header).toBeInTheDocument();
    
    const title = screen.getByText('Infinite AI Security');
    expect(title).toBeInTheDocument();
    
    const userDisplay = screen.getByText('testuser');
    expect(userDisplay).toBeInTheDocument();
  });

  it('calls toggleSidebar when menu button is clicked', () => {
    render(<MockHeader sidebarOpen={true} toggleSidebar={mockToggleSidebar} />);
    
    const menuButton = screen.getByRole('button');
    fireEvent.click(menuButton);
    
    expect(mockToggleSidebar).toHaveBeenCalledTimes(1);
  });

  it('renders with correct initial state when sidebar is closed', () => {
    render(<MockHeader sidebarOpen={false} toggleSidebar={mockToggleSidebar} />);
    
    const menuButton = screen.getByRole('button');
    fireEvent.click(menuButton);
    
    expect(mockToggleSidebar).toHaveBeenCalledTimes(1);
  });

  it('renders search input', () => {
    render(<MockHeader sidebarOpen={true} toggleSidebar={mockToggleSidebar} />);
    
    const searchInput = screen.getByPlaceholderText('Search...');
    expect(searchInput).toBeInTheDocument();
  });

  it('renders notification button', () => {
    render(<MockHeader sidebarOpen={true} toggleSidebar={mockToggleSidebar} />);
    
    const notificationButton = screen.getByLabelText(/notification/i);
    expect(notificationButton).toBeInTheDocument();
  });

  it('renders user dropdown with correct username', () => {
    render(<MockHeader sidebarOpen={true} toggleSidebar={mockToggleSidebar} />);
    
    const username = screen.getByText('testuser');
    expect(username).toBeInTheDocument();
  });
});