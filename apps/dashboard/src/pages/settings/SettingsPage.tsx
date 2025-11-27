import React from 'react';
import { Layout } from '../../components/layout';
import { Card, Input, Button } from '../../components/ui';
import { useAuth } from '../../hooks';

export const SettingsPage = () => {
  const { user } = useAuth();

  return (
    <Layout>
      <div className="page-header">
        <h1 className="page-title">Settings</h1>
        <p className="page-subtitle">Manage your account and preferences</p>
      </div>

      <div style={{ display: 'grid', gap: 20, maxWidth: 800 }}>
        <Card title="Profile Settings">
          <div style={{ display: 'grid', gap: 16 }}>
            <Input label="Full Name" defaultValue={user?.full_name} />
            <Input label="Email" defaultValue={user?.email} disabled />
            <Input label="Username" defaultValue={user?.username} disabled />
            <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
              <Button>Save Changes</Button>
            </div>
          </div>
        </Card>

        <Card title="Preferences">
          <p>Notification settings coming soon...</p>
        </Card>
      </div>
    </Layout>
  );
};

export default SettingsPage;
