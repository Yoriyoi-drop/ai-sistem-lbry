/**
 * Button component unit tests
 *
 * @created 2025-11-26
 */

import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '../ui/button';

describe('Button Component', () => {
  it('renders with default props', () => {
    render(<Button>Click me</Button>);
    const button = screen.getByRole('button', { name: /click me/i });
    expect(button).toBeInTheDocument();
    expect(button).toHaveClass('btn', 'btn-primary', 'btn-medium');
  });

  it('renders with custom variant', () => {
    render(<Button variant="secondary">Secondary Button</Button>);
    const button = screen.getByRole('button', { name: /secondary button/i });
    expect(button).toHaveClass('btn', 'btn-secondary', 'btn-medium');
  });

  it('renders with custom size', () => {
    render(<Button size="large">Large Button</Button>);
    const button = screen.getByRole('button', { name: /large button/i });
    expect(button).toHaveClass('btn', 'btn-primary', 'btn-large');
  });

  it('renders with loading state', () => {
    render(<Button loading={true}>Loading Button</Button>);
    const button = screen.getByRole('button', { name: /loading button/i });
    expect(button).toHaveClass('btn-loading');
    expect(button).toBeDisabled();
  });

  it('renders with icon', () => {
    const TestIcon = () => <span data-testid="test-icon">Icon</span>;
    render(<Button icon={<TestIcon />}>Button with Icon</Button>);
    const icon = screen.getByTestId('test-icon');
    expect(icon).toBeInTheDocument();
  });

  it('renders with fullWidth class', () => {
    render(<Button fullWidth={true}>Full Width Button</Button>);
    const button = screen.getByRole('button', { name: /full width button/i });
    expect(button).toHaveClass('btn-full-width');
  });

  it('applies custom className', () => {
    render(<Button className="custom-class">Custom Button</Button>);
    const button = screen.getByRole('button', { name: /custom button/i });
    expect(button).toHaveClass('custom-class');
  });

  it('is disabled when loading is true', () => {
    render(<Button loading={true}>Loading Button</Button>);
    const button = screen.getByRole('button', { name: /loading button/i });
    expect(button).toBeDisabled();
  });

  it('is disabled when explicitly set', () => {
    render(<Button disabled={true}>Disabled Button</Button>);
    const button = screen.getByRole('button', { name: /disabled button/i });
    expect(button).toBeDisabled();
  });

  it('handles click events', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Clickable Button</Button>);
    const button = screen.getByRole('button', { name: /clickable button/i });
    fireEvent.click(button);
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('does not trigger click when disabled', () => {
    const handleClick = vi.fn();
    render(
      <Button onClick={handleClick} disabled={true}>
        Disabled Button
      </Button>
    );
    const button = screen.getByRole('button', { name: /disabled button/i });
    fireEvent.click(button);
    expect(handleClick).not.toHaveBeenCalled();
  });

  it('does not trigger click when loading', () => {
    const handleClick = vi.fn();
    render(
      <Button onClick={handleClick} loading={true}>
        Loading Button
      </Button>
    );
    const button = screen.getByRole('button', { name: /loading button/i });
    fireEvent.click(button);
    expect(handleClick).not.toHaveBeenCalled();
  });
});