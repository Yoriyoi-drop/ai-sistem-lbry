import React, { useEffect, useState } from 'react';
import { Layout } from '../../components/layout';
import { Card } from '../../components/ui';
import { securityService } from '../../services';
import './Dashboard.css';

/**
 * Main Dashboard page
 * 
 * @created 2025-11-26
 */

export const Dashboard = () => {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const data = await securityService.getSecurityStats();
      setStats(data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="dashboard-loading">Loading...</div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="dashboard">
        <div className="page-header">
          <h1 className="page-title">Dashboard</h1>
          <p className="page-subtitle">Security overview and insights</p>
        </div>

        <div className="dashboard-grid">
          <Card className="stat-card stat-card-primary">
            <div className="stat-icon">🔍</div>
            <div className="stat-content">
              <h3 className="stat-value">{stats?.total_scans || 0}</h3>
              <p className="stat-label">Total Scans</p>
            </div>
          </Card>

          <Card className="stat-card stat-card-danger">
            <div className="stat-icon">⚠️</div>
            <div className="stat-content">
              <h3 className="stat-value">{stats?.critical_threats || 0}</h3>
              <p className="stat-label">Critical Threats</p>
            </div>
          </Card>

          <Card className="stat-card stat-card-success">
            <div className="stat-icon">✅</div>
            <div className="stat-content">
              <h3 className="stat-value">{stats?.resolved_issues || 0}</h3>
              <p className="stat-label">Resolved Issues</p>
            </div>
          </Card>

          <Card className="stat-card stat-card-info">
            <div className="stat-icon">🤖</div>
            <div className="stat-content">
              <h3 className="stat-value">{stats?.active_agents || 0}</h3>
              <p className="stat-label">Active Agents</p>
            </div>
          </Card>
        </div>

        <div className="dashboard-content">
          <Card title="Recent Activity" className="activity-card">
            <div className="activity-list">
              <div className="activity-item">
                <span className="activity-icon">🔍</span>
                <div className="activity-details">
                  <p className="activity-title">Vulnerability scan completed</p>
                  <p className="activity-time">2 hours ago</p>
                </div>
              </div>
              <div className="activity-item">
                <span className="activity-icon">⚠️</span>
                <div className="activity-details">
                  <p className="activity-title">Critical threat detected</p>
                  <p className="activity-time">5 hours ago</p>
                </div>
              </div>
              <div className="activity-item">
                <span className="activity-icon">✅</span>
                <div className="activity-details">
                  <p className="activity-title">Security patch applied</p>
                  <p className="activity-time">1 day ago</p>
                </div>
              </div>
            </div>
          </Card>

          <Card title="Security Score" className="score-card">
            <div className="security-score">
              <div className="score-circle">
                <span className="score-value">85</span>
              </div>
              <p className="score-label">Good Security Posture</p>
            </div>
          </Card>
        </div>
      </div>
    </Layout>
  );
};

export default Dashboard;
