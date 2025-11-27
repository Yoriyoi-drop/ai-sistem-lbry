import React from 'react';
import './ForgotPassword.css';

/**
 * Forgot Password page component
 * 
 * @created 2025-11-26
 */
export const ForgotPassword = () => {
  const [email, setEmail] = React.useState('');
  const [submitted, setSubmitted] = React.useState(false);
  const [loading, setLoading] = React.useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      // TODO: Implement forgot password API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      setSubmitted(true);
    } catch (error) {
      console.error('Password reset request failed:', error);
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    return (
      <div className="forgot-password-container">
        <div className="forgot-password-card">
          <div className="success-icon">✅</div>
          <h1>Check Your Email</h1>
          <p>
            We've sent a password reset link to <strong>{email}</strong>
          </p>
          <p className="hint">
            Click the link in the email to reset your password.
          </p>
          <a href="/login" className="btn-secondary">
            Back to Login
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="forgot-password-container">
      <div className="forgot-password-card">
        <h1>🔑 Reset Password</h1>
        <p>Enter your email address and we'll send you a reset link</p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoFocus
              placeholder="you@example.com"
            />
          </div>

          <button
            type="submit"
            className="btn-primary"
            disabled={loading}
          >
            {loading ? 'Sending...' : 'Send Reset Link'}
          </button>
        </form>

        <div className="back-link">
          <a href="/login">← Back to Login</a>
        </div>
      </div>
    </div>
  );
};

export default ForgotPassword;
