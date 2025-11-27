# Panduan Implementasi End-to-End: Infinite AI Security Platform

Dokumen ini menjelaskan bagaimana alur data dari frontend ke backend dan Rust security engine berfungsi.

## Arsitektur Sistem

1. **Frontend (React Dashboard)**: Terletak di `dashboard-react/`
2. **Backend API (FastAPI)**: Terletak di `apps/api/src/`
3. **Rust Security Engine**: Terletak di `packages/security-engine/labyrinth_rust/`

## Alur Data: User Input -> Backend -> Rust Engine -> Dashboard

### 1. Frontend ke Backend
- Komponen React `SQLInjectionDetector.jsx` mengirim permintaan ke `/sql-injection/detect`
- Lokasi file: `dashboard-react/src/components/security/SQLInjectionDetector.jsx`

### 2. Backend ke Rust Engine
- Endpoint `/sql-injection/detect` di `apps/api/src/api/v1/security_scans.py` menghubungi Rust engine melalui `labyrinth_client.py`
- Rust engine berjalan di `http://localhost:8081` sesuai konfigurasi `LABYRINTH_RUST_URL`

### 3. Rust Engine
- Menganalisis payload menggunakan neural network berbasis `ndarray`
- Mengembalikan hasil deteksi ancaman ke backend
- Lokasi: `packages/security-engine/labyrinth_rust/src/main.rs`

### 4. Backend ke Frontend
- Hasil analisis dikembalikan ke frontend sebagai JSON
- Ditampilkan di dashboard

## File-file Kunci yang Diubah

### Rust Engine
- `packages/security-engine/labyrinth_rust/Cargo.toml`: Ditambahkan dependensi `ndarray`
- `packages/security-engine/labyrinth_rust/src/main.rs`: Implementasi neural network yang realistis

### Backend API
- `apps/api/src/services/labyrinth_client.py`: Klien untuk komunikasi dengan Rust engine
- `apps/api/src/api/v1/security_scans.py`: Endpoint baru untuk security scanning
- `apps/api/src/api/v1/api.py`: Ditambahkan router security scan
- `apps/api/requirements.txt`: Ditambahkan dependensi `aiohttp`

### Frontend
- `dashboard-react/src/components/security/SQLInjectionDetector.jsx`: Sudah ada, menghubungi API backend

## Cara Menjalankan Sistem Secara Lengkap

1. **Jalankan Rust Engine**:
   ```bash
   cd packages/security-engine/labyrinth_rust
   cargo run
   ```
   Rust engine akan berjalan di `http://localhost:8081`

2. **Jalankan Backend API**:
   ```bash
   cd apps/api
   pip install -r requirements.txt
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```
   Backend akan berjalan di `http://localhost:8000`

3. **Jalankan Frontend**:
   ```bash
   cd dashboard-react
   npm install
   npm run dev
   ```
   Frontend akan berjalan di `http://localhost:5173`

4. **Gunakan Dashboard**:
   - Buka `http://localhost:5173` di browser
   - Navigasi ke halaman SQL Injection Detection
   - Masukkan query untuk dianalisis

## Pengujian Integrasi

Endpoint yang tersedia:
- `POST /sql-injection/detect`: Mendeteksi SQL injection
- `POST /security/analyze-threat`: Menganalisis ancaman umum
- `GET /security/labyrinth/stats`: Mendapatkan statistik dari Rust engine
- `GET /security/labyrinth/health`: Memeriksa kesehatan Rust engine

## Teknologi yang Digunakan

- **Frontend**: React, Vite, Tailwind CSS
- **Backend**: FastAPI, SQLAlchemy, Redis
- **Security Engine**: Rust dengan neural network berbasis `ndarray`

## Penjelasan Teknis

### Neural Network di Rust
Fungsi `neural_network_predict` sekarang menggunakan implementasi yang realistis:
- Forward pass melalui multiple layers
- Bobot dan bias diinisialisasi menggunakan `ndarray`
- Aktivasi ReLU untuk hidden layers dan Sigmoid untuk output layer

### Komunikasi Backend-Rust
- Menggunakan `aiohttp` untuk HTTP requests asynchronous
- Klien `labyrinth_client` mengelola koneksi ke Rust engine
- Error handling dan logging disertakan

Sistem ini sekarang memiliki alur kerja yang lengkap dari input pengguna hingga analisis keamanan menggunakan engine Rust yang powerful.