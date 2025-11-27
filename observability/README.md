# 📊 Infinite AI Security Platform - Observability System

This document provides an overview of the observability system for the Infinite AI Security Platform, including monitoring, logging, alerting, and metrics collection.

## 🏗️ Architecture Overview

The observability stack consists of:

- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboarding
- **Alertmanager**: Alert routing and notification
- **Node Exporter**: System metrics collection
- **Loki**: Log aggregation (alternative to ELK stack)
- **Promtail**: Log collection agent
- **Service-specific exporters**: For database, cache, etc.

## 📈 Metrics Collection

### Application Metrics
- `http_requests_total`: Total HTTP requests by method, endpoint, and status
- `http_request_duration_seconds`: Request latency histogram
- `active_connections`: Number of active connections
- `security_scans_total`: Total security scans by type and status
- `threats_detected_total`: Total threats detected by type and severity
- `api_errors_total`: Total API errors by type and endpoint

### Security Metrics
- `threat_level`: Current threat level (0-100) by severity
- `security_findings_total`: Security findings by scan type and severity
- `failed_logins_total`: Total failed login attempts
- `blocked_ips`: Number of currently blocked IPs

### Infrastructure Metrics
- System resource usage (CPU, memory, disk)
- Database performance metrics
- Cache performance metrics
- Network metrics

## 🔔 Alerting Rules

### Security Alerts
- **HighThreatDetectionRate**: Triggered when more than 10 threats are detected in 5 minutes
- **HighFailedLoginRate**: Triggered when more than 20 failed login attempts occur in 5 minutes
- **CriticalFindings**: Triggered immediately when critical security findings are detected
- **HighSeverityFindings**: Triggered when more than 5 high severity findings are detected in 10 minutes

### Performance Alerts
- **HighResponseTime**: Triggered when 95th percentile response time exceeds 2 seconds
- **ServiceDown**: Triggered when a service becomes unavailable
- **HighMemoryUsage**: Triggered when memory usage exceeds 90%
- **HighCPUUsage**: Triggered when CPU usage exceeds 90%

### API Health Alerts
- **HighAPIErrorRate**: Triggered when API error rate exceeds 0.1 errors per second

## 📊 Dashboards

### Main Platform Dashboard
- System Health Overview
- Total HTTP Requests
- Security Threats Detected
- API Response Time (P50, P95)
- Security Scans by Type
- Threats by Severity
- System Resources (CPU/Memory)
- Active Connections
- API Error Rate

## 🔧 Integration Points

### Python API Integration
- Metrics collection using Prometheus client library
- Structured logging with JSON formatter
- Security event logging
- Health check endpoints
- Custom metrics for security operations

### Go Scanner Integration
- Exposes standard Prometheus metrics endpoint
- Tracks scan statistics
- Error monitoring
- Performance metrics

### Rust Labyrinth Integration
- Metrics for threat detection and response
- Honeypot interaction tracking
- Deception system metrics
- Performance and resource usage

## 🚀 Deployment

### Docker Compose
The entire observability stack can be deployed using:
```bash
cd observability
docker-compose up -d
```

### Components:
- Prometheus (port 9090) - Metrics collection
- Grafana (port 3000) - Dashboards (default login: admin/admin)
- Alertmanager (port 9093) - Alerting
- Node Exporter (port 9100) - System metrics
- PostgreSQL Exporter (port 9187) - Database metrics
- Redis Exporter (port 9121) - Cache metrics
- Loki (port 3100) - Log aggregation
- Promtail - Log collection agent

## 📋 Configuration Files

- `prometheus.yml`: Main Prometheus configuration with service discovery
- `alertmanager.yml`: Alert routing and notification configuration
- `rules.yml`: Alerting rules for security and performance metrics
- `dashboard.json`: Main Grafana dashboard definition
- `promtail-config.yml`: Log collection configuration

## 🔍 Log Structure

All application logs use a structured JSON format:

```json
{
  "timestamp": "2024-12-26T10:30:00.123Z",
  "level": "INFO",
  "logger": "security",
  "message": "User login event",
  "module": "auth",
  "function": "login",
  "line": 123,
  "user_id": "user123",
  "ip_address": "192.168.1.100",
  "action": "login"
}
```

## 🛡️ Security Monitoring

The observability system provides comprehensive security monitoring including:
- Real-time threat detection metrics
- Authentication event tracking
- Access control monitoring
- Configuration change logging
- Security scan result monitoring
- Network intrusion detection

## 📊 Performance Monitoring

Performance metrics include:
- API response times
- System resource utilization
- Database query performance
- Cache hit/miss ratios
- Throughput measurements
- Error rates

---
*Infinite AI Security Platform - Comprehensive Observability System*