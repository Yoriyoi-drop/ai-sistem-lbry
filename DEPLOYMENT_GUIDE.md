# 🚀 Infinite AI Security - Multi-AI System Deployment

## 📋 Deskripsi Sistem

Sistem ini terdiri dari berbagai AI agent dengan peran spesifik dalam operasi keamanan:

- **AstraMind (Strategist)**: Perencanaan strategi keamanan
- **SpectraLogic (Analyzer)**: Analisis dan penilaian kerentanan keamanan
- **ForgeRun (Executor)**: Implementasi ukuran keamanan
- **GuardianOS (Validator)**: Validasi dan kepatuhan keamanan
- **ChronaCore (Memory)**: Manajemen memori dan konteks keamanan
- **NexaFlow (Orchestrator)**: Koordinasi tugas keamanan
- **GateLambda (Gateway)**: Gerbang API keamanan
- **CorePulse (Model Server)**: Pengelolaan model keamanan

## 🚀 Deployment

### Persyaratan
- Docker
- Docker Compose
- Python 3.8+

### Jalankan Sistem

```bash
# Membangun dan menjalankan semua layanan
./deploy.sh

# Atau gunakan skrip manajemen
./manage.sh start
```

### Endpoint API

- **NexaFlow (Orchestrator)**: http://localhost:8000
- **AstraMind**: http://localhost:8001
- **SpectraLogic**: http://localhost:8002
- **ForgeRun**: http://localhost:8003
- **GuardianOS**: http://localhost:8004
- **ChronaCore**: http://localhost:8005
- **GateLambda**: http://localhost:8080

## 🔧 Manajemen Sistem

Gunakan skrip `manage.sh` untuk mengelola sistem:

```bash
# Cek status layanan
./manage.sh status

# Lihat log layanan
./manage.sh logs forgerun

# Restart sistem
./manage.sh restart

# Hentikan sistem
./manage.sh stop
```

## 📊 Konfigurasi Lingkungan

Buat file `.env` berdasarkan `.env.example` untuk menyimpan konfigurasi rahasia dan lingkungan.

## 🛠️ Arsitektur

Sistem menggunakan pendekatan microservices dengan Docker Compose untuk manajemen kontainer. Setiap AI agent berjalan sebagai layanan terpisah dengan konfigurasi role yang ditentukan melalui environment variables.

## 🔐 Keamanan

Semua komunikasi antar layanan terjadi melalui jaringan privat Docker. Setiap layanan memiliki role dan batasan yang ketat sesuai prinsip least privilege.