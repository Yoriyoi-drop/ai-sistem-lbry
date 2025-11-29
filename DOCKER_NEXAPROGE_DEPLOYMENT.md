# Infinite AI Security - Nexaproge Docker Deployment

Docker deployment untuk Infinite AI Security Platform dengan nama tag Nexaproge.

## Prerequisites

- Docker
- Docker Compose
- Docker Hub account (jika ingin push image)

## Build dan Push ke Docker Hub

```bash
# Jalankan script untuk build dan push
./push_nexaproge_to_docker.sh [dockerhub_username]
```

## Menjalankan Aplikasi

### Menggunakan Docker Compose
```bash
# Jalankan semua services
./run_nexaproge_docker.sh up

# Build ulang dan jalankan
./run_nexaproge_docker.sh rebuild

# Lihat logs
./run_nexaproge_docker.sh logs

# Stop services
./run_nexaproge_docker.sh stop
```

### Atau secara manual
```bash
# Build image
docker build -f Dockerfile.nexaproge -t nexaproge/infinite-ai-security:nexaproge .

# Jalankan container
docker run -d -p 8000:8000 --name infinite-ai-security-container nexaproge/infinite-ai-security:nexaproge
```

## Akses API

Setelah dijalankan, API dapat diakses di:
- API: http://localhost:8000
- Health Check: http://localhost:8000/health

## Struktur File

- `Dockerfile.nexaproge` - Dockerfile untuk versi utama
- `docker-compose.nexaproge.yml` - Konfigurasi Docker Compose
- `push_nexaproge_to_docker.sh` - Script untuk push ke Docker Hub
- `run_nexaproge_docker.sh` - Script untuk menjalankan aplikasi

## Services

- `infinite-ai-security-nexaproge` - Aplikasi utama (port 8000)
- `redis` - Cache dan task queue (port 6379)
- `postgres` - Database (port 5432)