#!/bin/bash
# Skrip deploy minimal untuk Infinite AI Security

echo "🚀 Memulai deploy sistem Infinite AI Security (versi minimal)..."

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

# Cek ketersediaan docker dan docker-compose
echo "🔍 Mengecek ketersediaan Docker dan Docker Compose..."
check_docker
check_docker_compose

# Membangun dan menjalankan layanan dengan versi minimal
echo ""
echo "🔨 Membangun dan menjalankan layanan AI (versi minimal)..."
docker-compose -f docker-compose-minimal.yml up -d --build

# Tunggu beberapa detik agar layanan bisa mulai
echo ""
echo "⏳ Menunggu layanan untuk mulai..."
sleep 10

# Cek status layanan
echo ""
echo "📊 Status layanan (versi minimal):"
echo "----------------------------------"
docker-compose -f docker-compose-minimal.yml ps

echo ""
echo "🌐 Endpoint yang tersedia (versi minimal):"
echo "------------------------------------------"
echo "NexaFlow (Orchestrator): http://localhost:8000"
echo "AstraMind (Strategist): http://localhost:8001"
echo "SpectraLogic (Analyzer): http://localhost:8002"
echo "ForgeRun (Executor): http://localhost:8003"
echo ""
echo "✅ Deploy Infinite AI Security (versi minimal) selesai!"
echo "Sistem siap digunakan untuk operasi keamanan otomatis."