"""
Migration script to implement multi-tenant schema for Infinite AI Security Platform
Based on B2B SaaS transformation strategy
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# Revision identifiers
revision = '006_add_multitenant_schema'
down_revision = '005_add_subscriptions_table'
branch_labels = None
depends_on = None

def upgrade():
    # Create custom enum types if they don't exist
    subscription_tier_enum = postgresql.ENUM('starter', 'professional', 'enterprise', name='subscriptiontier', create_type=False)
    subscription_tier_enum.create(op.get_bind(), checkfirst=True)
    
    subscription_status_enum = postgresql.ENUM('active', 'cancelled', 'expired', 'past_due', 'trial', name='subscriptionstatus', create_type=False)
    subscription_status_enum.create(op.get_bind(), checkfirst=True)

    # Create organizations table
    op.create_table('organizations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('tier', sa.Enum('starter', 'professional', 'enterprise', name='subscriptiontier'), default='starter'),
        sa.Column('status', sa.String(50), default='trial'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('settings', postgresql.JSONB, default={}),
        sa.Column('billing_email', sa.String(255)),
        sa.Column('stripe_customer_id', sa.String(255)),
        sa.Column('max_users', sa.Integer, default=5),
        sa.Column('max_scans_per_month', sa.Integer, default=1000),
        sa.Column('api_calls_remaining', sa.Integer, default=10000),
        sa.Column('api_calls_reset_date', sa.Date, server_default=sa.text("CURRENT_DATE + INTERVAL '1 month'")),
    )
    
    # Create indexes for organizations
    op.create_index('idx_organizations_tier', 'organizations', ['tier'])
    op.create_index('idx_organizations_status', 'organizations', ['status'])

    # Create users table with organization reference
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('username', sa.String(100), unique=True),
        sa.Column('hashed_password', sa.String(255)),
        sa.Column('role', sa.Enum('owner', 'admin', 'member', 'viewer', name='roleenum'), default='member'),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('auth_provider', sa.String(50), default='local'),
        sa.Column('last_login', sa.DateTime()),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), onupdate=sa.text('now()')),
    )
    
    # Create indexes for users
    op.create_index('idx_users_org_id', 'users', ['organization_id'])
    op.create_index('idx_users_email', 'users', ['email'])

    # Create scans table with organization reference
    op.create_table('scans',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL')),
        sa.Column('repository_url', sa.String(500)),
        sa.Column('status', sa.Enum('pending', 'running', 'completed', 'failed', 'cancelled', name='scanstatus'), default='pending'),
        sa.Column('scan_type', sa.String(50), default='full'),
        sa.Column('findings', postgresql.JSONB, default={}),
        sa.Column('severity_summary', postgresql.JSONB, default={}),
        sa.Column('scan_cost_credits', sa.Numeric(10, 4), default=0.0000),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('completed_at', sa.DateTime()),
    )
    
    # Create indexes for scans
    op.create_index('idx_scans_org_id', 'scans', ['organization_id'])
    op.create_index('idx_scans_user_id', 'scans', ['user_id'])
    op.create_index('idx_scans_created_at', 'scans', ['created_at'])

    # Create usage_metrics table
    op.create_table('usage_metrics',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('metric_type', sa.String(100), nullable=False),
        sa.Column('quantity', sa.Integer, default=0),
        sa.Column('period', sa.Date, nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
    )
    
    # Create indexes for usage_metrics
    op.create_index('idx_usage_metrics_org_id', 'usage_metrics', ['organization_id'])
    op.create_index('idx_usage_metrics_period', 'usage_metrics', ['period'])

    # Create agent_sessions table
    op.create_table('agent_sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('agent_type', sa.String(100)),
        sa.Column('task_description', sa.Text),
        sa.Column('duration_seconds', sa.Integer, default=0),
        sa.Column('status', sa.String(50), default='running'),
        sa.Column('results', postgresql.JSONB, default={}),
        sa.Column('cost_credits', sa.Numeric(10, 4), default=0.0000),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
    )
    
    # Create indexes for agent_sessions
    op.create_index('idx_agent_sessions_org_id', 'agent_sessions', ['organization_id'])
    op.create_index('idx_agent_sessions_user_id', 'agent_sessions', ['user_id'])
    op.create_index('idx_agent_sessions_created_at', 'agent_sessions', ['created_at'])

    # Create subscription_plans table
    op.create_table('subscription_plans',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('tier', sa.Enum('starter', 'professional', 'enterprise', name='subscriptiontier'), nullable=False),
        sa.Column('price_monthly', sa.Numeric(10, 2), nullable=False),
        sa.Column('features', postgresql.JSONB, default=[]),
        sa.Column('limits', postgresql.JSONB, default={}),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), onupdate=sa.text('now()')),
    )
    
    # Create indexes for subscription_plans
    op.create_index('idx_subscription_plans_tier', 'subscription_plans', ['tier'])
    op.create_index('idx_subscription_plans_active', 'subscription_plans', ['is_active'])

    # Create organization_subscriptions table
    op.create_table('organization_subscriptions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('plan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('subscription_plans.id'), nullable=False),
        sa.Column('status', sa.Enum('active', 'cancelled', 'expired', 'past_due', 'trial', name='subscriptionstatus'), default='active'),
        sa.Column('started_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('ends_at', sa.DateTime()),
        sa.Column('trial_ends_at', sa.DateTime()),
        sa.Column('auto_renew', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), onupdate=sa.text('now()')),
    )
    
    # Create indexes for organization_subscriptions
    op.create_index('idx_org_subscriptions_org_id', 'organization_subscriptions', ['organization_id'])
    op.create_index('idx_org_subscriptions_status', 'organization_subscriptions', ['status'])

    # Create api_keys table
    op.create_table('api_keys',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('key_hash', sa.String(255), unique=True, nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('permissions', postgresql.JSONB, default=['read', 'write']),
        sa.Column('expires_at', sa.DateTime()),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('last_used_at', sa.DateTime()),
    )
    
    # Create indexes for api_keys
    op.create_index('idx_api_keys_org_id', 'api_keys', ['organization_id'])
    op.create_index('idx_api_keys_user_id', 'api_keys', ['user_id'])

    # Enable Row Level Security (RLS) on tenant-specific tables
    op.execute("ALTER TABLE users ENABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE scans ENABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE usage_metrics ENABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE agent_sessions ENABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE api_keys ENABLE ROW LEVEL SECURITY;")
    
    # Create RLS policies to ensure tenants can only access their own data
    op.execute("""
        CREATE POLICY users_org_isolation ON users
        FOR ALL
        USING (organization_id = uuid(current_setting('app.current_organization_id', true)));
    """)
    op.execute("""
        CREATE POLICY scans_org_isolation ON scans
        FOR ALL
        USING (organization_id = uuid(current_setting('app.current_organization_id', true)));
    """)
    op.execute("""
        CREATE POLICY usage_metrics_org_isolation ON usage_metrics
        FOR ALL
        USING (organization_id = uuid(current_setting('app.current_organization_id', true)));
    """)
    op.execute("""
        CREATE POLICY agent_sessions_org_isolation ON agent_sessions
        FOR ALL
        USING (organization_id = uuid(current_setting('app.current_organization_id', true)));
    """)
    op.execute("""
        CREATE POLICY api_keys_org_isolation ON api_keys
        FOR ALL
        USING (organization_id = uuid(current_setting('app.current_organization_id', true)));
    """)

    # Create function to set current organization in session for RLS
    op.execute("""
        CREATE OR REPLACE FUNCTION set_current_org(org_id UUID)
        RETURNS void AS $$
        BEGIN
            PERFORM set_config('app.current_organization_id', org_id::text, true);
        END;
        $$ LANGUAGE plpgsql;
    """)

    # Insert default subscription plans based on the B2B strategy
    op.execute("""
        INSERT INTO subscription_plans (name, tier, price_monthly, features, limits)
        VALUES 
        ('Starter', 'starter', 499.00, 
          '["Security Scanner (Go) - 1000 scans/month", "Basic AI Agent (1 concurrent)", "Dashboard + Analytics", "Email support", "API Access (10K requests/month)"]', 
          '{"max_users": 20, "max_scans_per_month": 1000, "max_api_calls_per_month": 10000, "max_ai_agents": 1, "max_data_storage_gb": 1}'
        ),
        ('Professional', 'professional', 1499.00, 
          '["Everything in Starter", "Security Scanner - 10K scans/month", "Multi-Agent AI (3 concurrent agents)", "Labyrinth Defense - Basic tier", "Compliance reports (SOC2, ISO 27001)", "Slack/Teams integration", "Priority support (4h response)", "API Access (100K requests/month)", "Custom security policies"]', 
          '{"max_users": 100, "max_scans_per_month": 10000, "max_api_calls_per_month": 100000, "max_ai_agents": 3, "max_data_storage_gb": 10}'
        ),
        ('Enterprise', 'enterprise', 0.00, 
          '["Everything in Professional", "Unlimited scans & agents", "Advanced Labyrinth with custom rules", "Dedicated Security Engineer", "99.99% SLA", "On-premise deployment option", "SSO (SAML, OAuth)", "Advanced RBAC", "Custom integrations", "White-label option", "24/7 phone support"]', 
          '{"max_users": 10000, "max_scans_per_month": 1000000, "max_api_calls_per_month": 10000000, "max_ai_agents": 100, "max_data_storage_gb": 1000, "custom_features": true}'
        );
    """)

def downgrade():
    # Drop RLS policies
    op.execute("DROP POLICY IF EXISTS users_org_isolation ON users;")
    op.execute("DROP POLICY IF EXISTS scans_org_isolation ON scans;")
    op.execute("DROP POLICY IF EXISTS usage_metrics_org_isolation ON usage_metrics;")
    op.execute("DROP POLICY IF EXISTS agent_sessions_org_isolation ON agent_sessions;")
    op.execute("DROP POLICY IF EXISTS api_keys_org_isolation ON api_keys;")

    # Drop the function
    op.execute("DROP FUNCTION IF EXISTS set_current_org(UUID);")

    # Disable RLS
    op.execute("ALTER TABLE users DISABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE scans DISABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE usage_metrics DISABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE agent_sessions DISABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE api_keys DISABLE ROW LEVEL SECURITY;")

    # Drop tables in reverse order to respect foreign key constraints
    op.drop_table('api_keys')
    op.drop_table('organization_subscriptions')
    op.drop_table('subscription_plans')
    op.drop_table('agent_sessions')
    op.drop_table('usage_metrics')
    op.drop_table('scans')
    op.drop_table('users')
    op.drop_table('organizations')

    # Drop indexes
    op.drop_index('idx_api_keys_user_id', table_name='api_keys')
    op.drop_index('idx_api_keys_org_id', table_name='api_keys')
    op.drop_index('idx_org_subscriptions_status', table_name='organization_subscriptions')
    op.drop_index('idx_org_subscriptions_org_id', table_name='organization_subscriptions')
    op.drop_index('idx_subscription_plans_active', table_name='subscription_plans')
    op.drop_index('idx_subscription_plans_tier', table_name='subscription_plans')
    op.drop_index('idx_agent_sessions_created_at', table_name='agent_sessions')
    op.drop_index('idx_agent_sessions_user_id', table_name='agent_sessions')
    op.drop_index('idx_agent_sessions_org_id', table_name='agent_sessions')
    op.drop_index('idx_usage_metrics_period', table_name='usage_metrics')
    op.drop_index('idx_usage_metrics_org_id', table_name='usage_metrics')
    op.drop_index('idx_scans_created_at', table_name='scans')
    op.drop_index('idx_scans_user_id', table_name='scans')
    op.drop_index('idx_scans_org_id', table_name='scans')
    op.drop_index('idx_users_email', table_name='users')
    op.drop_index('idx_users_org_id', table_name='users')
    op.drop_index('idx_organizations_status', table_name='organizations')
    op.drop_index('idx_organizations_tier', table_name='organizations')

    # Drop enums
    op.execute("DROP TYPE IF EXISTS subscriptionstatus;")
    op.execute("DROP TYPE IF EXISTS subscriptiontier;")