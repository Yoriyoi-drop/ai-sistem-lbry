# 🚀 NexaForge AI System - 24/7 Non-Stop Setup Guide

Panduan lengkap untuk membuat sistem AI Anda berjalan 24/7 non-stop dengan auto-restart.

---

## 📋 Komponen yang Diaktifkan

### 1. ✅ Docker Auto-Restart (`restart: always`)
- Container otomatis hidup jika crash
- Auto-start setelah server reboot
- Menangani error dan freeze otomatis

### 2. ✅ Systemd Service (`nexaforge-24-7.service`)
- Mengelola lifecycle docker compose
- Auto-start pada boot
- Graceful shutdown

### 3. ✅ Health Checks (`healthcheck`)
- Setiap container memiliki health endpoint
- Auto-restart jika service tidak sehat
- Monitoring real-time

---

## 🔧 Setup Instructions

### Opsi 1: Setup Otomatis (Recommended)

```bash
# 1. Buat script executable
chmod +x /home/whale-d/Unduhan/backup/ai-p/infinite_ai_security/setup-24-7.sh
chmod +x /home/whale-d/Unduhan/backup/ai-p/infinite_ai_security/setup-healthcheck.sh

# 2. Jalankan setup dengan sudo
sudo /home/whale-d/Unduhan/backup/ai-p/infinite_ai_security/setup-24-7.sh

# 3. Setup health checks (opsional)
/home/whale-d/Unduhan/backup/ai-p/infinite_ai_security/setup-healthcheck.sh
```

### Opsi 2: Setup Manual

#### Step 1: Copy Docker Compose File
```bash
cd /home/whale-d/Unduhan/backup/ai-p/infinite_ai_security
cp docker-compose-24-7.yml docker-compose.yml.backup  # Backup yang lama
```

#### Step 2: Create Systemd Service
```bash
sudo cp nexaforge-24-7.service /etc/systemd/system/nexaforge-24-7.service
sudo systemctl daemon-reload
```

#### Step 3: Enable & Start Service
```bash
sudo systemctl enable nexaforge-24-7
sudo systemctl start nexaforge-24-7
```

#### Step 4: Verify Status
```bash
sudo systemctl status nexaforge-24-7
docker ps
```

---

## 🎯 Fitur Utama

### Auto-Restart pada Crash
```yaml
restart: always
```
**Efek:**
- Container hidup otomatis jika mati
- Tidak ada delay (immediate restart)
- Berlaku untuk ALL containers

### Health Checks
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```
**Efek:**
- Check health setiap 30 detik
- Jika 3x gagal → auto-restart
- Start period: 40 detik sebelum mulai check

### Dependency Management
```yaml
depends_on:
  db:
    condition: service_healthy
```
**Efek:**
- Service tunggu dependency healthy dulu
- Tidak mulai kalau database belum ready
- Graceful startup sequence

---

## 📊 Monitoring

### Check Status Service
```bash
# Lihat status systemd service
sudo systemctl status nexaforge-24-7

# Lihat status container
docker ps

# Lihat stats real-time
docker stats
```

### View Logs
```bash
# Real-time logs dari systemd
sudo journalctl -u nexaforge-24-7 -f

# Last 100 logs
sudo journalctl -u nexaforge-24-7 -n 100

# Logs container tertentu
docker logs -f astramind
docker logs -f spectralogic
docker logs -f forgerun
docker logs -f guardianos
docker logs -f infinite-ai-api
```

### Health Monitoring
```bash
# Jalankan monitoring dashboard
python3 /home/whale-d/Unduhan/backup/ai-p/infinite_ai_security/healthcheck/monitor_health.py

# Atau gunakan simple check
curl http://localhost:8000/health
curl http://localhost:8001/health  # astramind
curl http://localhost:8002/health  # spectralogic
curl http://localhost:8003/health  # forgerun
curl http://localhost:8004/health  # guardianos
```

---

## 🎮 Commands Penting

### Control Service

```bash
# Start service
sudo systemctl start nexaforge-24-7

# Stop service (graceful shutdown)
sudo systemctl stop nexaforge-24-7

# Restart service
sudo systemctl restart nexaforge-24-7

# Check status
sudo systemctl status nexaforge-24-7

# Enable auto-start on boot
sudo systemctl enable nexaforge-24-7

# Disable auto-start on boot
sudo systemctl disable nexaforge-24-7
```

### Control Containers

```bash
# List running containers
docker ps

# Start all containers (dari docker-compose directory)
cd /home/whale-d/Unduhan/backup/ai-p/infinite_ai_security
docker compose -f docker-compose-24-7.yml up -d

# Stop all containers
docker compose -f docker-compose-24-7.yml down

# Restart specific container
docker restart astramind

# View container logs
docker logs -f [nama-container]

# Check container health
docker inspect --format='{{.State.Health.Status}}' astramind
```

### Manual Docker Operations

```bash
# Pull latest images
docker compose -f docker-compose-24-7.yml pull

# Rebuild images
docker compose -f docker-compose-24-7.yml build --no-cache

# Check resource usage
docker stats

# Remove unused resources
docker system prune -a
```

---

## 🔍 Troubleshooting

### Container Not Starting
```bash
# Check logs
docker logs [container-name]

# Check systemd service logs
sudo journalctl -u nexaforge-24-7 -n 50

# Check if ports are in use
sudo netstat -tulpn | grep -E ':8000|:8001|:8002|:8003'

# Try manual start
cd /home/whale-d/Unduhan/backup/ai-p/infinite_ai_security
docker compose -f docker-compose-24-7.yml up
```

### Health Check Failing
```bash
# Verify endpoint responds
curl -v http://localhost:8000/health

# Check if service is actually running
docker ps -a

# Rebuild container if needed
docker compose -f docker-compose-24-7.yml build --no-cache [service-name]

# Force restart
docker compose -f docker-compose-24-7.yml restart [service-name]
```

### Port Already in Use
```bash
# Find what's using the port
sudo lsof -i :[port-number]

# Kill the process
sudo kill -9 [PID]

# Or use different port in docker-compose-24-7.yml
# Ubah "8000:8000" menjadi "8005:8000"
```

### Service Won't Stop Gracefully
```bash
# Force stop service
sudo systemctl kill nexaforge-24-7

# Check if process still running
ps aux | grep docker

# Force remove containers
docker compose -f docker-compose-24-7.yml down -v --remove-orphans
```

---

## 📈 Performance Optimization

### Resource Limits
```yaml
# Tambahkan ke container di docker-compose-24-7.yml
resources:
  limits:
    cpus: '2'
    memory: 4G
  reservations:
    cpus: '1'
    memory: 2G
```

### Logging
```yaml
# Prevent log files getting too large
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

### Network Optimization
```yaml
# Use host network for better performance
network_mode: "host"

# Or keep bridge but optimize
networks:
  ai-security-network:
    driver: bridge
    driver_opts:
      com.docker.network.driver.mtu: 9000
```

---

## 📊 Dashboard Access

Setelah setup berhasil, akses:

- **Grafana Dashboard**: http://localhost:3000
  - Default: admin / admin123
  
- **Prometheus**: http://localhost:9090
  - Metrics & time series data
  
- **API**: http://localhost:8000
  - Main API endpoint
  
- **Container Status**: `docker ps`
  - See all running containers

---

## 🛡️ Security Notes

### 1. Change Default Passwords
```bash
# Edit docker-compose-24-7.yml
# Ubah POSTGRES_PASSWORD dan REDIS_PASSWORD
# Ubah GRAFANA_PASSWORD

# Atau set dari environment
export POSTGRES_PASSWORD="your-secure-password"
export REDIS_PASSWORD="your-secure-password"
export GRAFANA_PASSWORD="your-secure-password"
```

### 2. Setup SSL/TLS
```bash
# Ubah di nginx/nginx.conf
# Setup SSL certificates di nginx/ssl/
# Uncomment HTTPS section di nginx config
```

### 3. Firewall Rules
```bash
# Allow only necessary ports
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw allow 3000/tcp # Grafana (jika needed)
sudo ufw allow 9090/tcp # Prometheus (jika needed)
```

---

## 🚀 Auto-Scaling (Advanced)

### Limit Resources
```yaml
services:
  astramind:
    resources:
      limits:
        cpus: '1.5'
        memory: 2G
      reservations:
        cpus: '1'
        memory: 1G
```

### Restart Policies
```yaml
# Already set to 'always'
# Tapi bisa customize:
restart_policy:
  condition: on-failure
  delay: 5s
  max_attempts: 3
  window: 120s
```

---

## 📝 Backup & Recovery

### Backup Configuration
```bash
# Backup docker-compose
cp /home/whale-d/Unduhan/backup/ai-p/infinite_ai_security/docker-compose-24-7.yml \
   /home/whale-d/Unduhan/backup/ai-p/infinite_ai_security/docker-compose-24-7.yml.backup

# Backup database volumes
docker volume ls
docker volume inspect infinite_ai_security_postgres_data

# Export database
docker exec infinite-ai-db pg_dump -U postgres infinite_security > backup.sql
```

### Recovery
```bash
# Restore from backup
docker compose -f docker-compose-24-7.yml down -v
docker compose -f docker-compose-24-7.yml up -d

# Restore database
docker exec -i infinite-ai-db psql -U postgres < backup.sql
```

---

## ✅ Checklist Verifikasi

- [ ] Docker terinstall dan berjalan
- [ ] Docker Compose terinstall
- [ ] `docker-compose-24-7.yml` sudah dibuat
- [ ] `nexaforge-24-7.service` sudah di `/etc/systemd/system/`
- [ ] Service sudah enable: `sudo systemctl enable nexaforge-24-7`
- [ ] Service sudah start: `sudo systemctl start nexaforge-24-7`
- [ ] Semua container berstatus "healthy"
- [ ] Health endpoints merespons dengan 200 OK
- [ ] Dashboard accessible di http://localhost:3000
- [ ] Logs clean tanpa error

---

## 🎉 Hasil Akhir

Dengan setup ini, sistem AI Anda akan:

✅ Berjalan 24/7 non-stop
✅ Auto-restart setelah crash
✅ Auto-start setelah server reboot
✅ Self-healing jika ada issue
✅ Monitored dengan Prometheus + Grafana
✅ Hanya bisa dihentikan manual via `systemctl stop`

---

## 📞 Support & Debug

Jika ada masalah:

```bash
# 1. Check service status
sudo systemctl status nexaforge-24-7

# 2. View recent logs
sudo journalctl -u nexaforge-24-7 -n 50

# 3. Check container status
docker ps -a

# 4. View container logs
docker logs [container-name]

# 5. Test health endpoints
curl http://localhost:8000/health
curl http://localhost:8001/health

# 6. Check resource usage
docker stats

# 7. Verify network connectivity
docker exec [container-name] ping -c 2 8.8.8.8
```

**Hubungi developer jika ada issue yang tidak terpecahkan.**

---

**Last Updated**: 27 November 2025
**Version**: 1.0 (Production Ready)
