#!/bin/bash
# Skrip deploy otomatis untuk Infinite AI Security

echo "🚀 Memulai deploy sistem Infinite AI Security..."

# Fungsi untuk mengecek apakah docker-compose tersedia
check_docker_compose() {
    if ! [ -x "$(command -v docker-compose)" ]; then
        echo "❌ docker-compose tidak ditemukan. Silakan install docker-compose terlebih dahulu."
        exit 1
    fi
}

# Fungsi untuk mengecek apakah docker tersedia
check_docker() {
    if ! [ -x "$(command -v docker)" ]; then
        echo "❌ Docker tidak ditemukan. Silakan install Docker terlebih dahulu."
        exit 1
    fi
}

# Fungsi untuk mengecek status layanan
check_service_status() {
    local service_name=$1
    local status=$(docker-compose ps | grep "$service_name" | awk '{print $3}')
    if [[ "$status" == "Up" ]]; then
        echo "✅ $service_name: BERJALAN"
    else
        echo "❌ $service_name: TIDAK BERJALAN (Status: $status)"
    fi
}

# Cek ketersediaan docker dan docker-compose
echo "🔍 Mengecek ketersediaan Docker dan Docker Compose..."
check_docker
check_docker_compose

# Membangun dan menjalankan semua layanan
echo ""
echo "🔨 Membangun dan menjalankan semua layanan AI..."
docker-compose up -d --build

# Tunggu beberapa detik agar layanan bisa mulai
echo ""
echo "⏳ Menunggu layanan untuk mulai..."
sleep 10

# Cek status semua layanan
echo ""
echo "📊 Status semua layanan:"
echo "------------------------"
docker-compose ps

# Cek status spesifik setiap layanan
echo ""
echo "🔍 Detail status layanan:"
echo "------------------------"
check_service_status "astramind"
check_service_status "spectralogic"
check_service_status "forgerun"
check_service_status "guardianos"
check_service_status "chronacore"
check_service_status "nexaflow"
check_service_status "gatelambda"
check_service_status "corepulse"

# Tampilkan log dari layanan utama
echo ""
echo "📋 Log dari layanan utama (NexaFlow):"
echo "-------------------------------------"
docker-compose logs nexaflow --tail=10

echo ""
echo "🌐 Endpoint yang tersedia:"
echo "--------------------------"
echo "Orchestrator (NexaFlow): http://localhost:8000"
echo "AstraMind (Strategist): http://localhost:8001"
echo "SpectraLogic (Analyzer): http://localhost:8002"
echo "ForgeRun (Executor): http://localhost:8003"
echo "GuardianOS (Validator): http://localhost:8004"
echo "ChronaCore (Memory): http://localhost:8005"
echo "Gateway (GateLambda): http://localhost:8080"
echo ""
echo "🔧 Untuk restart layanan tertentu:"
echo "   docker-compose restart [nama_layanan]"
echo "   Contoh: docker-compose restart forgerun"
echo ""
echo "📋 Untuk lihat log layanan tertentu:"
echo "   docker-compose logs [nama_layanan]"
echo "   Contoh: docker-compose logs astramind"
echo ""
echo "🛑 Untuk menghentikan semua layanan:"
echo "   docker-compose down"
echo ""
echo "✅ Deploy Infinite AI Security selesai!"
echo "Sistem siap digunakan untuk operasi keamanan otomatis."