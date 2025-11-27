#!/bin/bash
# Skrip untuk menjalankan Infinite AI Security secara otomatis dengan update otomatis

# Fungsi untuk menampilkan status
show_status() {
    echo "📊 Status layanan Infinite AI Security:"
    docker-compose ps
}

# Fungsi untuk memulai layanan
start_services() {
    echo "🚀 Memulai layanan Infinite AI Security..."
    
    # Build dan jalankan layanan
    docker-compose up -d --build
    
    # Tunggu sebentar agar layanan bisa mulai
    sleep 10
    
    # Tampilkan status
    show_status
    
    echo "✅ Layanan telah dimulai"
    echo "   Akses: http://localhost:8000 (NexaFlow)"
    echo "   Lihat status lengkap: docker-compose ps"
}

# Fungsi untuk menghentikan layanan
stop_services() {
    echo "🛑 Menghentikan layanan Infinite AI Security..."
    
    # Hentikan semua layanan
    docker-compose down
    
    echo "✅ Layanan telah dihentikan"
}

# Fungsi untuk restart layanan
restart_services() {
    echo "🔄 Merestart layanan Infinite AI Security..."
    
    # Hentikan layanan lama
    docker-compose down
    
    # Tunggu sebentar
    sleep 5
    
    # Jalankan layanan baru
    docker-compose up -d --build
    
    # Tunggu sebentar agar layanan bisa mulai
    sleep 10
    
    # Tampilkan status
    show_status
    
    echo "✅ Layanan telah direstart"
}

# Fungsi untuk menjalankan update otomatis
run_auto_update() {
    echo "🔄 Menjalankan sistem dengan update otomatis..."
    
    # Pastikan update_project.sh ada dan bisa dieksekusi
    if [ ! -f "update_project.sh" ]; then
        echo "❌ File update_project.sh tidak ditemukan"
        exit 1
    fi
    
    # Jalankan update otomatis di background
    nohup ./update_project.sh auto-update > auto_update_service.log 2>&1 &
    AUTO_UPDATE_PID=$!
    
    echo "✅ Service update otomatis dijalankan di background"
    echo "   PID: $AUTO_UPDATE_PID"
    echo "   Log: auto_update_service.log"
}

# Fungsi untuk menjalankan semua secara otomatis
run_auto() {
    echo "🤖 Menjalankan Infinite AI Security secara otomatis..."
    
    # Update dependencies dan konfigurasi
    echo "🔄 Update dependencies..."
    ./update_project.sh update-deps
    
    echo "⚙️ Update konfigurasi..."
    ./update_project.sh update-config
    
    echo "🔧 Update skrip utama..."
    ./update_project.sh update-main
    
    # Mulai layanan
    start_services
    
    # Jalankan update otomatis
    run_auto_update
    
    # Setup monitoring
    setup_monitoring
    
    echo "✅ Sistem Infinite AI Security berjalan otomatis!"
    echo "   Untuk menghentikan: $0 stop"
    echo "   Untuk restart: $0 restart"
    echo "   Untuk cek status: $0 status"
}

# Fungsi untuk setup monitoring dan restart otomatis
setup_monitoring() {
    echo "🔍 Setup monitoring otomatis..."
    
    # Buat skrip monitoring
    cat > monitor_service.py << 'EOF'
import time
import subprocess
import logging
import os
from datetime import datetime
import signal
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('monitor_service.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ServiceMonitor:
    def __init__(self):
        self.running = True
        
        # Tangkap sinyal untuk shutdown yang proper
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        logger.info(f"Signal {signum} received, shutting down monitor...")
        self.running = False
    
    def check_service_status(self):
        """Cek status layanan docker-compose"""
        try:
            result = subprocess.run(["docker-compose", "ps", "--format", "json"], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                logger.error("Gagal mengecek status layanan")
                return False
            
            # Parse output dan cek apakah semua layanan up
            lines = result.stdout.strip().split('\n')
            all_up = True
            
            for line in lines:
                if line.strip():
                    try:
                        import json
                        service_info = json.loads(line)
                        if service_info.get('State') != 'running':
                            logger.warning(f"Layanan {service_info.get('Name', 'unknown')} tidak berjalan: {service_info.get('State')}")
                            all_up = False
                    except:
                        continue
            
            if all_up:
                logger.info("Semua layanan berjalan dengan baik")
            else:
                logger.warning("Beberapa layanan mungkin tidak berjalan")
            
            return all_up
            
        except subprocess.TimeoutExpired:
            logger.error("Timeout saat mengecek status layanan")
            return False
        except Exception as e:
            logger.error(f"Error saat mengecek status layanan: {e}")
            return False
    
    def restart_services(self):
        """Restart layanan docker-compose"""
        try:
            logger.info("Restarting services...")
            subprocess.run(["docker-compose", "down"], check=True, timeout=60)
            time.sleep(5)
            subprocess.run(["docker-compose", "up", "-d", "--build"], check=True, timeout=120)
            time.sleep(10)
            logger.info("Services restarted successfully")
        except Exception as e:
            logger.error(f"Error saat merestart layanan: {e}")
    
    def run(self):
        """Jalankan loop monitoring"""
        logger.info("Service Monitor dimulai")
        
        # Cek status awal
        last_status = self.check_service_status()
        
        while self.running:
            try:
                # Cek status layanan
                current_status = self.check_service_status()
                
                # Jika status berubah dari up ke down, restart layanan
                if last_status and not current_status:
                    logger.warning("Layanan terdeteksi down, mencoba restart...")
                    self.restart_services()
                    time.sleep(30)  # Tunggu sebentar setelah restart
                    current_status = self.check_service_status()
                
                # Update status terakhir
                last_status = current_status
                
                # Tunggu sebelum pengecekan berikutnya (5 menit)
                for _ in range(300):  # 300 detik = 5 menit
                    if not self.running:
                        break
                    time.sleep(1)
                    
            except Exception as e:
                logger.error(f"Error di loop monitoring: {e}")
                time.sleep(60)  # Tunggu 1 menit jika error
        
        logger.info("Service Monitor berhenti")

if __name__ == "__main__":
    monitor = ServiceMonitor()
    monitor.run()
EOF
    
    # Jalankan monitoring di background
    nohup python monitor_service.py > monitor_service.log 2>&1 &
    MONITOR_PID=$!
    
    echo "✅ Service monitoring dijalankan di background"
    echo "   PID: $MONITOR_PID"
    echo "   Log: monitor_service.log"
}

# Fungsi untuk cek status
check_status() {
    echo "📊 Status sistem Infinite AI Security:"
    echo "======================================"
    echo "Tanggal: $(date)"
    echo ""
    
    echo "Layanan docker-compose:"
    docker-compose ps
    echo ""
    
    # Cek apakah update otomatis berjalan
    if pgrep -f "auto_update.py" > /dev/null; then
        echo "✅ Update otomatis: BERJALAN"
        pgrep -fl "auto_update.py"
    else
        echo "❌ Update otomatis: TIDAK BERJALAN"
    fi
    echo ""
    
    # Cek apakah monitoring berjalan
    if pgrep -f "monitor_service.py" > /dev/null; then
        echo "✅ Monitoring: BERJALAN"
        pgrep -fl "monitor_service.py"
    else
        echo "❌ Monitoring: TIDAK BERJALAN"
    fi
    echo ""
    
    # Tampilkan log terbaru dari layanan utama
    if [ -f "infinite_ai_security.log" ]; then
        echo "5 baris terakhir dari log utama:"
        tail -5 infinite_ai_security.log
    fi
}

# Fungsi untuk membersihkan proses
cleanup_processes() {
    echo "🧹 Membersihkan proses..."
    
    # Hentikan semua proses update otomatis
    pkill -f "auto_update.py"
    pkill -f "monitor_service.py"
    
    # Hentikan layanan docker
    docker-compose down
    
    echo "✅ Proses dibersihkan"
}

# Fungsi untuk bantuan
show_help() {
    echo "🤖 Skrip Otomatisasi Infinite AI Security"
    echo ""
    echo "Penggunaan: $0 [perintah]"
    echo ""
    echo "Perintah yang tersedia:"
    echo "  start         - Jalankan layanan"
    echo "  stop          - Hentikan layanan"
    echo "  restart       - Restart layanan"
    echo "  auto          - Jalankan otomatis dengan update dan monitoring"
    echo "  status        - Cek status sistem"
    echo "  cleanup       - Bersihkan semua proses"
    echo "  logs          - Tampilkan log layanan"
    echo "  help          - Tampilkan bantuan ini"
    echo ""
    echo "Contoh:"
    echo "  $0 auto       - Jalankan sistem otomatis"
    echo "  $0 status     - Cek status"
    echo "  $0 logs       - Lihat log"
}

# Proses argumen command line
case "$1" in
    "start")
        start_services
        ;;
    "stop")
        stop_services
        ;;
    "restart")
        restart_services
        ;;
    "auto")
        run_auto
        ;;
    "status")
        check_status
        ;;
    "cleanup")
        cleanup_processes
        ;;
    "logs")
        if [ -z "$2" ]; then
            docker-compose logs --tail=20
        else
            docker-compose logs "$2" --tail=50
        fi
        ;;
    "help"|"--help"|"-h")
        show_help
        ;;
    "")
        show_help
        ;;
    *)
        echo "Argumen tidak dikenal: $1"
        echo "Gunakan '$0 help' untuk bantuan"
        exit 1
        ;;
esac