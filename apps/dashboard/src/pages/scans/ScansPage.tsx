import React from 'react';
import { Layout } from '../../components/layout';
import { Card, Button } from '../../components/ui';

export const ScansPage = () => {
    return (
        <Layout>
            <div className="page-header">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                        <h1 className="page-title">Security Scans</h1>
                        <p className="page-subtitle">Manage and run security scans</p>
                    </div>
                    <Button variant="primary">New Scan</Button>
                </div>
            </div>

            <Card>
                <div style={{ padding: 20, textAlign: 'center', color: '#718096' }}>
                    No scan history available.
                </div>
            </Card>
        </Layout>
    );
};

export default ScansPage;
