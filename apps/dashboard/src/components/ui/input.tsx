import React from 'react';
import './input.css';

/**
 * Input component
 * 
 * @created 2025-11-26
 */

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  icon?: React.ReactNode;
  fullWidth?: boolean;
}

export const Input: React.FC<InputProps> = ({
  label,
  error,
  helperText,
  icon,
  fullWidth = false,
  className = '',
  id,
  ...props
}) => {
  const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`;

  const inputClass = [
    'input',
    error && 'input-error',
    icon && 'input-with-icon',
    fullWidth && 'input-full-width',
    className,
  ].filter(Boolean).join(' ');

  return (
    <div className="input-wrapper">
      {label && (
        <label htmlFor={inputId} className="input-label">
          {label}
        </label>
      )}
      <div className="input-container">
        {icon && <span className="input-icon">{icon}</span>}
        <input
          id={inputId}
          className={inputClass}
          {...props}
        />
      </div>
      {error && (
        <span className="input-error-text">{error}</span>
      )}
      {!error && helperText && (
        <span className="input-helper-text">{helperText}</span>
      )}
    </div>
  );
};

export default Input;
