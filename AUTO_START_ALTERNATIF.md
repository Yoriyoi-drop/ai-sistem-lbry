# Alternatif: Auto-start Tanpa Systemd

Jika systemd tidak bekerja di lingkungan Anda, berikut adalah metode alternatif untuk menjalankan Infinite AI Security secara otomatis saat boot:

## 1. Menggunakan Crontab untuk Auto-start

Tambahkan baris ini ke crontab Anda:

```bash
# Edit crontab
crontab -e

# Tambahkan baris ini untuk auto-start saat boot
@reboot /home/whale-d/Unduhan/backup/ai-p/infinite_ai_security/autonomous_operation.sh start >> /home/whale-d/Unduhan/backup/ai-p/infinite_ai_security/logs/boot.log 2>&1
```

## 2. Menggunakan Skrip Startup Sederhana

Buat skrip startup di home directory:

```bash
#!/bin/bash
# /home/whale-d/start_infinite_ai.sh

# Tunggu sistem sepenuhnya siap
sleep 30

# Navigasi ke direktori aplikasi
cd /home/whale-d/Unduhan/backup/ai-p/infinite_ai_security

# Pastikan Ollama service berjalan
docker-compose -f docker-compose.ollama.yml up -d ollama

# Tunggu Ollama siap
sleep 30

# Jalankan sistem otomatisasi
./autonomous_operation.sh start
```

Jadikan executable dan tambahkan ke crontab:

```bash
chmod +x /home/whale-d/start_infinite_ai.sh
crontab -e
# Tambahkan baris: @reboot /home/whale-d/start_infinite_ai.sh >> /home/whale-d/startup.log 2>&1
```

## 3. Status Sistem Saat Ini

Sistem Anda saat ini berjalan secara otomatis melalui:

```bash
# Cek status
./master_control.sh status

# Sistem autonomous_operation.sh sedang berjalan dengan PID 48989
# Ini menangani semua fungsionalitas otomatisasi termasuk:
# - Monitoring kesehatan sistem
# - Self-healing (restart otomatis jika gagal)
# - Update model
# - Continuous operation
```

## 4. Menjaga Sistem Tetap Hidup

Jika ingin sistem tetap berjalan setelah restart, pastikan untuk:

1. Jalankan perintah berikut setelah boot:
```bash
cd /home/whale-d/Unduhan/backup/ai-p/infinite_ai_security
./autonomous_operation.sh start
```

2. Atau gunakan metode crontab di atas.

## 5. Menonaktifkan Auto-start

Untuk menonaktifkan auto-start:
- Edit crontab: `crontab -e`
- Hapus atau comment baris @reboot

---

Sistem otomatisasi Anda (autonomous_operation.sh) saat ini berjalan dengan baik dan memiliki semua fungsionalitas yang Anda minta. Jika systemd tidak berfungsi, alternatif crontab adalah solusi yang handal dan sederhana.