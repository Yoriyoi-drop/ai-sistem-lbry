-- Multi-Tenant Database Schema for Infinite AI Security Platform
-- Based on B2B SaaS transformation strategy

-- Organizations (Tenants)
CREATE TABLE IF NOT EXISTS organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    tier VARCHAR(50) NOT NULL DEFAULT 'starter', -- starter/professional/enterprise
    status VARCHAR(50) DEFAULT 'trial', -- trial/active/suspended
    created_at TIMESTAMP DEFAULT NOW(),
    settings JSONB DEFAULT '{}',
    billing_email VARCHAR(255),
    stripe_customer_id VARCHAR(255),
    max_users INTEGER DEFAULT 5, -- tier-based limits
    max_scans_per_month INTEGER DEFAULT 1000, -- tier-based limits
    api_calls_remaining INTEGER DEFAULT 10000, -- tier-based limits
    api_calls_reset_date DATE DEFAULT CURRENT_DATE + INTERVAL '1 month'
);

-- Users with organization reference
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE,
    hashed_password VARCHAR(255),
    role VARCHAR(50) DEFAULT 'member', -- owner/admin/member/viewer
    is_active BOOLEAN DEFAULT true,
    auth_provider VARCHAR(50) DEFAULT 'local', -- local/google/github/saml
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Scans with organization reference
CREATE TABLE IF NOT EXISTS scans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    repository_url VARCHAR(500),
    status VARCHAR(50) DEFAULT 'queued', -- queued/running/completed/failed
    scan_type VARCHAR(50) DEFAULT 'full', -- full/incremental/custom
    findings JSONB DEFAULT '{}',
    severity_summary JSONB DEFAULT '{}',
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    scan_cost_credits DECIMAL(10,4) DEFAULT 0.0000
);

-- Usage Tracking for consumption-based pricing
CREATE TABLE IF NOT EXISTS usage_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    metric_type VARCHAR(100) NOT NULL, -- scans/api_calls/agent_hours/ai_credits
    quantity INTEGER NOT NULL DEFAULT 0,
    period DATE NOT NULL, -- for monthly billing
    created_at TIMESTAMP DEFAULT NOW()
);

-- AI Agents Activity with organization reference
CREATE TABLE IF NOT EXISTS agent_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    agent_type VARCHAR(100),
    task_description TEXT,
    duration_seconds INTEGER DEFAULT 0,
    status VARCHAR(50) DEFAULT 'running', -- running/completed/failed
    results JSONB DEFAULT '{}',
    cost_credits DECIMAL(10,4) DEFAULT 0.0000,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Subscription Plans (for the tier system)
CREATE TABLE IF NOT EXISTS subscription_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    tier VARCHAR(50) NOT NULL, -- starter/professional/enterprise
    price_monthly DECIMAL(10,2) NOT NULL,
    features JSONB DEFAULT '[]',
    limits JSONB DEFAULT '{}', -- { "max_users": 10, "max_scans_per_month": 10000 }
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Organization Subscriptions
CREATE TABLE IF NOT EXISTS organization_subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    plan_id UUID REFERENCES subscription_plans(id),
    status VARCHAR(50) DEFAULT 'active', -- active/cancelled/expired/past_due
    started_at TIMESTAMP DEFAULT NOW(),
    ends_at TIMESTAMP,
    trial_ends_at TIMESTAMP,
    auto_renew BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- API Keys with organization reference
CREATE TABLE IF NOT EXISTS api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    key_hash VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    permissions JSONB DEFAULT '["read", "write"]',
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    last_used_at TIMESTAMP
);

-- Row-Level Security (RLS) setup for multi-tenant isolation
-- Enable RLS on all tenant-specific tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE scans ENABLE ROW LEVEL SECURITY;
ALTER TABLE usage_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_keys ENABLE ROW LEVEL SECURITY;

-- Create RLS policies to ensure tenants can only access their own data
-- Users can only see users in their organization
CREATE POLICY users_org_isolation ON users
    FOR ALL TO authenticated_user
    USING (organization_id = current_setting('app.current_organization_id')::UUID);

-- Scans can only be accessed by correct organization
CREATE POLICY scans_org_isolation ON scans
    FOR ALL TO authenticated_user
    USING (organization_id = current_setting('app.current_organization_id')::UUID);

-- Usage metrics can only be accessed by correct organization
CREATE POLICY usage_metrics_org_isolation ON usage_metrics
    FOR ALL TO authenticated_user
    USING (organization_id = current_setting('app.current_organization_id')::UUID);

-- Agent sessions can only be accessed by correct organization
CREATE POLICY agent_sessions_org_isolation ON agent_sessions
    FOR ALL TO authenticated_user
    USING (organization_id = current_setting('app.current_organization_id')::UUID);

-- API keys can only be accessed by correct organization
CREATE POLICY api_keys_org_isolation ON api_keys
    FOR ALL TO authenticated_user
    USING (organization_id = current_setting('app.current_organization_id')::UUID);

-- Indexes for performance
CREATE INDEX idx_users_org_id ON users(organization_id);
CREATE INDEX idx_scans_org_id ON scans(organization_id);
CREATE INDEX idx_scans_created_at ON scans(created_at);
CREATE INDEX idx_usage_metrics_org_id ON usage_metrics(organization_id);
CREATE INDEX idx_usage_metrics_period ON usage_metrics(period);
CREATE INDEX idx_agent_sessions_org_id ON agent_sessions(organization_id);
CREATE INDEX idx_agent_sessions_created_at ON agent_sessions(created_at);
CREATE INDEX idx_org_subscriptions_org_id ON organization_subscriptions(organization_id);

-- Function to set current organization in session for RLS
CREATE OR REPLACE FUNCTION set_current_org(org_id UUID)
RETURNS void AS $$
BEGIN
    PERFORM set_config('app.current_organization_id', org_id::text, true);
END;
$$ LANGUAGE plpgsql;

-- Insert default subscription plans based on the B2B strategy
INSERT INTO subscription_plans (name, tier, price_monthly, features, limits)
VALUES 
('Starter', 'starter', 499.00, '[
    "Security Scanner (Go) - 1000 scans/month",
    "Basic AI Agent (1 concurrent)",
    "Dashboard + Analytics",
    "Email support",
    "API Access (10K requests/month)"
  ]', '{
    "max_users": 20,
    "max_scans_per_month": 1000,
    "max_api_calls_per_month": 10000,
    "max_ai_agents": 1,
    "max_data_storage_gb": 1
  }'),
('Professional', 'professional', 1499.00, '[
    "Everything in Starter",
    "Security Scanner - 10K scans/month",
    "Multi-Agent AI (3 concurrent agents)",
    "Labyrinth Defense - Basic tier",
    "Compliance reports (SOC2, ISO 27001)",
    "Slack/Teams integration",
    "Priority support (4h response)",
    "API Access (100K requests/month)",
    "Custom security policies"
  ]', '{
    "max_users": 100,
    "max_scans_per_month": 10000,
    "max_api_calls_per_month": 100000,
    "max_ai_agents": 3,
    "max_data_storage_gb": 10
  }'),
('Enterprise', 'enterprise', 0.00, '[
    "Everything in Professional",
    "Unlimited scans & agents",
    "Advanced Labyrinth with custom rules",
    "Dedicated Security Engineer",
    "99.99% SLA",
    "On-premise deployment option",
    "SSO (SAML, OAuth)",
    "Advanced RBAC",
    "Custom integrations",
    "White-label option",
    "24/7 phone support"
  ]', '{
    "max_users": 10000,
    "max_scans_per_month": 1000000,
    "max_api_calls_per_month": 10000000,
    "max_ai_agents": 100,
    "max_data_storage_gb": 1000,
    "custom_features": true
  }')
ON CONFLICT DO NOTHING;