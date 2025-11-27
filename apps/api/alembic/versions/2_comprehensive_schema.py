"""Comprehensive database schema with all security models

Revision ID: 2
Revises: 1
Create Date: 2025-11-26 14:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import enum

# revision identifiers, used by Alembic.
revision = '2'
down_revision = '1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create roles table
    op.create_table('roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_roles_id'), 'roles', ['id'], unique=False)

    # Create permissions table
    op.create_table('permissions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('resource', sa.String(100), nullable=False),
        sa.Column('action', sa.String(50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_permissions_id'), 'permissions', ['id'], unique=False)

    # Create role_permissions association table
    op.create_table('role_permissions',
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('permission_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('role_id', 'permission_id')
    )

    # Update users table to match new schema
    op.drop_index('ix_users_username', table_name='users')
    op.drop_column('users', 'username')
    op.drop_column('users', 'full_name')
    op.drop_column('users', 'is_superuser')
    op.drop_column('users', 'created_at')
    op.drop_column('users', 'updated_at')
    op.add_column('users', sa.Column('username', sa.String(100), nullable=True))
    op.add_column('users', sa.Column('full_name', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('is_superuser', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('role', sa.Enum('ADMIN', 'USER', 'ANALYST', 'VIEWER', name='roleenum'), nullable=True))
    op.add_column('users', sa.Column('api_key', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('last_login', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_index('ix_users_api_key', 'users', ['api_key'], unique=True)
    
    # Update agents table to match new schema
    op.drop_column('agents', 'configuration')
    op.drop_column('agents', 'is_active')
    op.drop_column('agents', 'last_heartbeat')
    op.drop_column('agents', 'created_at')
    op.drop_column('agents', 'updated_at')
    op.drop_column('agents', 'name')
    op.drop_column('agents', 'description')
    op.drop_column('agents', 'agent_type')
    op.drop_column('agents', 'status')
    op.drop_column('agents', 'owner_id')
    op.add_column('agents', sa.Column('name', sa.String(255), nullable=False))
    op.add_column('agents', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('agents', sa.Column('agent_type', sa.String(100), nullable=True))
    op.add_column('agents', sa.Column('status', sa.Enum('ACTIVE', 'INACTIVE', 'ERROR', 'MAINTENANCE', name='agentstatus'), nullable=True))
    op.add_column('agents', sa.Column('configuration', sa.JSON(), nullable=True))
    op.add_column('agents', sa.Column('capabilities', sa.JSON(), nullable=True))
    op.add_column('agents', sa.Column('metrics', sa.JSON(), nullable=True))
    op.add_column('agents', sa.Column('last_active', sa.DateTime(), nullable=True))
    op.add_column('agents', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('agents', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('agents', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_agents_owner', 'agents', 'users', ['owner_id'], ['id'], ondelete='CASCADE')
    op.drop_index('ix_agents_name')
    op.create_index('ix_agents_name', 'agents', ['name'], unique=False)

    # Create security_scans table
    op.create_table('security_scans',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('scan_name', sa.String(255), nullable=False),
        sa.Column('target', sa.String(500), nullable=False),
        sa.Column('scan_type', sa.String(100), nullable=True),
        sa.Column('status', sa.Enum('PENDING', 'RUNNING', 'COMPLETED', 'FAILED', 'CANCELLED', name='scanstatus'), nullable=True),
        sa.Column('progress', sa.Integer(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('results', sa.JSON(), nullable=True),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('agent_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['agent_id'], ['agents.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_security_scans_id'), 'security_scans', ['id'], unique=False)
    op.create_index(op.f('ix_security_scans_scan_name'), 'security_scans', ['scan_name'], unique=False)

    # Create threats table
    op.create_table('threats',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('threat_type', sa.String(100), nullable=False),
        sa.Column('severity', sa.Enum('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO', name='threatlevel'), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('source', sa.String(500), nullable=True),
        sa.Column('detected_at', sa.DateTime(), nullable=True),
        sa.Column('mitigated', sa.Boolean(), nullable=True),
        sa.Column('mitigation_steps', sa.JSON(), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('scan_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['scan_id'], ['security_scans.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_threats_id'), 'threats', ['id'], unique=False)

    # Update vulnerabilities table to match new schema
    op.drop_column('vulnerabilities', 'cve_id')
    op.drop_column('vulnerabilities', 'name')
    op.drop_column('vulnerabilities', 'description')
    op.drop_column('vulnerabilities', 'severity')
    op.drop_column('vulnerabilities', 'cvss_score')
    op.drop_column('vulnerabilities', 'cvss_vector')
    op.drop_column('vulnerabilities', 'cwe_id')
    op.drop_column('vulnerabilities', 'status')
    op.drop_column('vulnerabilities', 'remediation')
    op.drop_column('vulnerabilities', 'references')
    op.drop_column('vulnerabilities', 'is_active')
    op.drop_column('vulnerabilities', 'discovered_at')
    op.drop_column('vulnerabilities', 'updated_at')
    op.drop_column('vulnerabilities', 'scan_id')
    op.add_column('vulnerabilities', sa.Column('cve_id', sa.String(50), nullable=True))
    op.add_column('vulnerabilities', sa.Column('title', sa.String(255), nullable=False))
    op.add_column('vulnerabilities', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('vulnerabilities', sa.Column('severity', sa.Enum('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO', name='threatlevel'), nullable=False))
    op.add_column('vulnerabilities', sa.Column('cvss_score', sa.Float(), nullable=True))
    op.add_column('vulnerabilities', sa.Column('affected_component', sa.String(255), nullable=True))
    op.add_column('vulnerabilities', sa.Column('remediation', sa.Text(), nullable=True))
    op.add_column('vulnerabilities', sa.Column('references', sa.JSON(), nullable=True))
    op.add_column('vulnerabilities', sa.Column('status', sa.String(50), nullable=True))
    op.add_column('vulnerabilities', sa.Column('discovered_at', sa.DateTime(), nullable=True))
    op.add_column('vulnerabilities', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('vulnerabilities', sa.Column('scan_id', sa.Integer(), nullable=True))
    op.create_index('ix_vulnerabilities_cve_id', 'vulnerabilities', ['cve_id'], unique=False)
    op.create_foreign_key('fk_vulnerabilities_scan', 'vulnerabilities', 'security_scans', ['scan_id'], ['id'], ondelete='CASCADE')

    # Create subscriptions table
    op.create_table('subscriptions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('plan_name', sa.String(100), nullable=False),
        sa.Column('status', sa.String(50), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('features', sa.JSON(), nullable=True),
        sa.Column('limits', sa.JSON(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_subscriptions_id'), 'subscriptions', ['id'], unique=False)

    # Create labyrinth_configs table
    op.create_table('labyrinth_configs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('complexity_level', sa.Integer(), nullable=True),
        sa.Column('route_configs', sa.JSON(), nullable=True),
        sa.Column('decoy_nodes', sa.JSON(), nullable=True),
        sa.Column('detection_rules', sa.JSON(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_labyrinth_configs_id'), 'labyrinth_configs', ['id'], unique=False)

    # Update audit_logs table to match new schema
    op.drop_column('audit_logs', 'user_id')
    op.drop_column('audit_logs', 'action')
    op.drop_column('audit_logs', 'resource_type')
    op.drop_column('audit_logs', 'resource_id')
    op.drop_column('audit_logs', 'details')
    op.drop_column('audit_logs', 'ip_address')
    op.drop_column('audit_logs', 'user_agent')
    op.drop_column('audit_logs', 'created_at')
    op.add_column('audit_logs', sa.Column('action', sa.String(100), nullable=False))
    op.add_column('audit_logs', sa.Column('resource_type', sa.String(100), nullable=True))
    op.add_column('audit_logs', sa.Column('resource_id', sa.Integer(), nullable=True))
    op.add_column('audit_logs', sa.Column('details', sa.JSON(), nullable=True))
    op.add_column('audit_logs', sa.Column('ip_address', sa.String(45), nullable=True))
    op.add_column('audit_logs', sa.Column('user_agent', sa.String(500), nullable=True))
    op.add_column('audit_logs', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.add_column('audit_logs', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_audit_logs_user', 'audit_logs', 'users', ['user_id'], ['id'], ondelete='SET NULL')


def downgrade() -> None:
    # Reverse the changes in reverse order
    op.drop_constraint('fk_audit_logs_user', 'audit_logs', type_='foreignkey')
    op.drop_column('audit_logs', 'user_id')
    op.drop_column('audit_logs', 'timestamp')
    op.drop_column('audit_logs', 'user_agent')
    op.drop_column('audit_logs', 'ip_address')
    op.drop_column('audit_logs', 'details')
    op.drop_column('audit_logs', 'resource_id')
    op.drop_column('audit_logs', 'resource_type')
    op.drop_column('audit_logs', 'action')
    op.add_column('audit_logs', sa.Column('user_id', sa.Integer(), nullable=True))
    op.add_column('audit_logs', sa.Column('action', sa.String(), nullable=False))
    op.add_column('audit_logs', sa.Column('resource_type', sa.String(), nullable=True))
    op.add_column('audit_logs', sa.Column('resource_id', sa.Integer(), nullable=True))
    op.add_column('audit_logs', sa.Column('details', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('audit_logs', sa.Column('ip_address', sa.String(), nullable=True))
    op.add_column('audit_logs', sa.Column('user_agent', sa.Text(), nullable=True))
    op.add_column('audit_logs', sa.Column('created_at', sa.DateTime(), nullable=True))

    # Drop new tables in reverse order
    op.drop_table('labyrinth_configs')
    op.drop_table('subscriptions')

    # Revert vulnerabilities table
    op.drop_constraint('fk_vulnerabilities_scan', 'vulnerabilities', type_='foreignkey')
    op.drop_index('ix_vulnerabilities_cve_id')
    op.drop_column('vulnerabilities', 'scan_id')
    op.drop_column('vulnerabilities', 'updated_at')
    op.drop_column('vulnerabilities', 'discovered_at')
    op.drop_column('vulnerabilities', 'status')
    op.drop_column('vulnerabilities', 'references')
    op.drop_column('vulnerabilities', 'remediation')
    op.drop_column('vulnerabilities', 'affected_component')
    op.drop_column('vulnerabilities', 'cvss_score')
    op.drop_column('vulnerabilities', 'severity')
    op.drop_column('vulnerabilities', 'description')
    op.drop_column('vulnerabilities', 'title')
    op.drop_column('vulnerabilities', 'cve_id')
    op.add_column('vulnerabilities', sa.Column('cve_id', sa.String(), nullable=True))
    op.add_column('vulnerabilities', sa.Column('name', sa.String(), nullable=False))
    op.add_column('vulnerabilities', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('vulnerabilities', sa.Column('severity', sa.String(), nullable=True))
    op.add_column('vulnerabilities', sa.Column('cvss_score', sa.String(), nullable=True))
    op.add_column('vulnerabilities', sa.Column('cvss_vector', sa.String(), nullable=True))
    op.add_column('vulnerabilities', sa.Column('cwe_id', sa.String(), nullable=True))
    op.add_column('vulnerabilities', sa.Column('status', sa.String(), nullable=True))
    op.add_column('vulnerabilities', sa.Column('remediation', sa.Text(), nullable=True))
    op.add_column('vulnerabilities', sa.Column('references', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('vulnerabilities', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.add_column('vulnerabilities', sa.Column('discovered_at', sa.DateTime(), nullable=True))
    op.add_column('vulnerabilities', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('vulnerabilities', sa.Column('scan_id', sa.Integer(), nullable=True))

    # Drop threats table
    op.drop_table('threats')

    # Drop security_scans table
    op.drop_table('security_scans')

    # Revert agents table changes
    op.drop_constraint('fk_agents_owner', 'agents', type_='foreignkey')
    op.drop_index('ix_agents_name')
    op.drop_column('agents', 'owner_id')
    op.drop_column('agents', 'updated_at')
    op.drop_column('agents', 'created_at')
    op.drop_column('agents', 'last_active')
    op.drop_column('agents', 'metrics')
    op.drop_column('agents', 'capabilities')
    op.drop_column('agents', 'configuration')
    op.drop_column('agents', 'status')
    op.drop_column('agents', 'agent_type')
    op.drop_column('agents', 'description')
    op.drop_column('agents', 'name')
    op.add_column('agents', sa.Column('name', sa.String(), nullable=False))
    op.add_column('agents', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('agents', sa.Column('agent_type', sa.String(), nullable=False))
    op.add_column('agents', sa.Column('status', sa.String(), nullable=True))
    op.add_column('agents', sa.Column('configuration', sa.Text(), nullable=True))
    op.add_column('agents', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.add_column('agents', sa.Column('last_heartbeat', sa.DateTime(), nullable=True))
    op.add_column('agents', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('agents', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('agents', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.create_index('ix_agents_name', 'agents', ['name'], unique=False)

    # Revert users table changes
    op.drop_index('ix_users_api_key')
    op.drop_index('ix_users_username')
    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'created_at')
    op.drop_column('users', 'last_login')
    op.drop_column('users', 'api_key')
    op.drop_column('users', 'role')
    op.drop_column('users', 'is_superuser')
    op.drop_column('users', 'full_name')
    op.drop_column('users', 'username')
    op.add_column('users', sa.Column('username', sa.String(), nullable=False))
    op.add_column('users', sa.Column('full_name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('is_superuser', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.create_index('ix_users_username', 'users', ['username'], unique=True)

    # Drop new tables in reverse order
    op.drop_table('role_permissions')
    op.drop_table('permissions')
    op.drop_table('roles')