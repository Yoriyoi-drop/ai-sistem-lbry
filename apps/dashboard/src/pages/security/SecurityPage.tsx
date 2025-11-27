import React from 'react';
import { Layout } from '../../components/layout';
import { Card } from '../../components/ui';

export const SecurityPage = () => {
  return (
    <Layout>
      <div className="page-header">
        <h1 className="page-title">Security Overview</h1>
        <p className="page-subtitle">Monitor threats and vulnerabilities</p>
      </div>

      <div style={{ display: 'grid', gap: 20 }}>
        <Card title="Active Threats">
          <p>No active threats detected.</p>
        </Card>

        <Card title="Vulnerabilities">
          <p>System is secure.</p>
        </Card>
      </div>
    </Layout>
  );
};

export default SecurityPage;
