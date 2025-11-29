# Panduan Menjalankan Model AI di Infinite AI Security

## Status Saat Ini
Model AI sudah berjalan menggunakan Ollama dan dapat diakses melalui API.

## Model Tersedia
- `qwen2.5:7b-instruct` (7.6B parameter)
- `llama3.1:latest` (8.0B parameter) 
- `mistral:latest` (7.2B parameter)

## Cara Mengakses Model

### 1. Melalui API
```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5:7b-instruct",
    "prompt": "Hello, how are you?",
    "stream": false
  }'
```

### 2. Melalui Antarmuka Web
Buka http://localhost:3001 di browser Anda untuk mengakses Ollama Web UI.

### 3. Melalui CLI Ollama
```bash
# Pastikan Anda berada di direktori yang benar
cd /home/whale-d/Unduhan/backup/ai-p/infinite_ai_security

# Jalankan Ollama (jika belum berjalan)
docker compose -f docker-compose.ollama.yml up -d

# Gunakan Ollama CLI
ollama run qwen2.5:7b-instruct
```

## Menjalankan Layanan Penuh
Jika Anda ingin menjalankan keseluruhan sistem AI Security (meskipun saat ini ada masalah dengan dependency build):
```bash
# Untuk layanan Ollama saja
docker compose -f docker-compose.ollama.yml up -d

# Untuk sistem 24/7 (mungkin akan gagal karena masalah dependency)
docker compose -f docker-compose-24-7.yml up -d
```

## File Utilitas
- `run_ai_model.sh` - Script untuk menjalankan dan menguji model AI
- `test_ai_curl.py` - Script Python untuk menguji model (menggunakan curl)

## Status Layanan
- Ollama API: http://localhost:11434
- Ollama Web UI: http://localhost:3001
- Model utama: qwen2.5:7b-instruct (konfigurasi default dari .env.ollama)

AI model telah berhasil dijalankan dan siap digunakan untuk tugas-tugas keamanan dan permintaan lainnya.