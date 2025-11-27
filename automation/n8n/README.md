# 🔄 n8n Automation Workflows for Infinite AI Security Platform

This directory contains automation workflows for the Infinite AI Security Platform using n8n as the workflow automation engine.

## 🚀 Overview

The n8n automation system provides intelligent, event-driven workflows that automate security operations, including:
- Threat detection and response
- Agent auto-scaling
- Security scanning automation
- Reporting and alerting
- Incident management

## 📁 Directory Structure

```
automation/n8n/
├── workflows/                 # n8n workflow definitions
│   ├── threat_response.json   # Automated threat response workflow
│   ├── agent_auto_scaling.json # Agent auto-scaling workflow
│   └── security_scanning.json  # Security scanning automation
├── credentials/              # n8n credentials storage
├── config/                   # n8n configuration files
├── docker-compose.yml        # Docker Compose setup
├── .env                      # Environment variables
└── README.md                 # This file
```

## 🛠️ Workflows Included

### 1. Threat Response Workflow (`threat_response.json`)
- **Trigger**: Webhook when a security threat is detected
- **Actions**:
  - Analyze threat severity
  - Block malicious IPs for critical threats
  - Initiate security scans of threat sources
  - Send Slack notifications to security team
  - Log incident reports

### 2. Agent Auto-Scaling Workflow (`agent_auto_scaling.json`)
- **Trigger**: Periodic check of agent status and system load
- **Actions**:
  - Calculate system load based on agent performance
  - Scale up by creating new agents when load is high (>70%)
  - Scale down by terminating idle agents when load is low
  - Log scaling events for audit trail

### 3. Security Scanning Automation (`security_scanning.json`)
- **Trigger**: Webhook when a scan request is received
- **Actions**:
  - Validate scan request parameters
  - Initiate security scans via API
  - Monitor scan completion
  - Analyze findings for critical issues
  - Send security alerts for critical findings
  - Generate security reports
  - Create remediation tickets in JIRA

## 🐳 Deployment

### Docker Compose
To deploy the n8n automation system:

```bash
cd automation/n8n
docker-compose up -d
```

The n8n UI will be available at `http://localhost:5678`

### Environment Variables
Update the `.env` file with your specific configuration:
- API endpoints and authentication tokens
- Slack webhook URL for notifications
- JIRA integration details
- Database configuration (if using PostgreSQL)

## 🔐 Security Configuration

The n8n instance is configured with:
- Basic authentication enabled
- Secure cookie settings
- Access to internal IPs blocked
- Request size limits to prevent abuse
- Diagnostics disabled for production

## 🔄 Webhooks Setup

The workflows use these webhook endpoints:

- **Threat Detection**: `POST /webhook/security/threat-detected`
- **Agent Status**: `GET /webhook/monitoring/agent-status` 
- **Scan Requests**: `POST /webhook/automation/scan-request`

## 📊 Workflow Features

### Threat Response
- Real-time threat classification
- Automated IP blocking
- Multi-channel notifications
- Incident reporting

### Auto-Scaling
- Dynamic agent creation/termination
- Load-based decisions
- Cost optimization
- Performance maintenance

### Security Scanning
- Automated scan scheduling
- Result analysis
- Alert generation
- Ticket creation for remediation

## 🔌 API Integration

The workflows interface with the main platform API at:
- `/api/v1/scans` - Security scanning endpoints
- `/api/v1/agents` - Agent management endpoints
- `/api/v1/users` - User management endpoints

## 🚨 Notifications

The system sends notifications via:
- Slack webhooks for immediate alerts
- Email notifications (configurable)
- JIRA ticket creation for remediation tasks

## 🔧 Customization

To customize workflows for your environment:
1. Update the environment variables in `.env`
2. Modify the workflow JSON files to adjust logic
3. Add additional steps to workflows as needed
4. Configure your notification endpoints (Slack, email, etc.)

## 📈 Monitoring

Monitor workflow execution through:
- n8n's built-in execution history
- Logs available in the n8n UI
- Database records for persistent storage
- Integration-specific monitoring

---
*Infinite AI Security Platform - n8n Automation System*