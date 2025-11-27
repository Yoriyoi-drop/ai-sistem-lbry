import React, { useEffect, useState } from 'react';
import { Layout } from '../../components/layout';
import { Card, Button } from '../../components/ui';
import { useAgents } from '../../hooks';
import { formatDate } from '../../utils';

export const AgentsPage = () => {
  const { agents, loading, fetchAgents, startAgent, stopAgent } = useAgents();
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  useEffect(() => {
    fetchAgents();
  }, []);

  return (
    <Layout>
      <div className="page-header">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h1 className="page-title">AI Agents</h1>
            <p className="page-subtitle">Manage your security agents</p>
          </div>
          <Button variant="primary" icon="➕">Deploy New Agent</Button>
        </div>
      </div>

      {loading ? (
        <div>Loading agents...</div>
      ) : (
        <div className={`agents-${viewMode}`}>
          {agents.length === 0 ? (
            <Card padding="large" className="text-center">
              <h3>No Agents Deployed</h3>
              <p>Deploy your first AI security agent to start monitoring.</p>
              <Button variant="primary" style={{ marginTop: 16 }}>Deploy Agent</Button>
            </Card>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: 20 }}>
              {agents.map(agent => (
                <Card key={agent.id} title={agent.name} footer={
                  <div style={{ display: 'flex', gap: 10, justifyContent: 'flex-end' }}>
                    {agent.status === 'active' ? (
                      <Button size="small" variant="danger" onClick={() => stopAgent(agent.id)}>Stop</Button>
                    ) : (
                      <Button size="small" variant="success" onClick={() => startAgent(agent.id)}>Start</Button>
                    )}
                    <Button size="small" variant="secondary">Configure</Button>
                  </div>
                }>
                  <div style={{ marginBottom: 10 }}>
                    <span className={`status-badge status-${agent.status}`}>
                      {agent.status}
                    </span>
                    <span style={{ float: 'right', fontSize: 12, color: '#718096' }}>
                      {agent.agent_type}
                    </span>
                  </div>
                  <p style={{ fontSize: 14, color: '#4a5568' }}>
                    {agent.description || 'No description provided.'}
                  </p>
                  <div style={{ marginTop: 10, fontSize: 12, color: '#718096' }}>
                    Last active: {agent.last_active ? formatDate(agent.last_active) : 'Never'}
                  </div>
                </Card>
              ))}
            </div>
          )}
        </div>
      )}
    </Layout>
  );
};

export default AgentsPage;
