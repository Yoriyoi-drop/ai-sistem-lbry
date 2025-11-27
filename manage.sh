#!/bin/bash
# Skrip manajemen layanan untuk Infinite AI Security

case "$1" in
    "start")
        echo "🚀 Memulai semua layanan Infinite AI Security..."
        docker-compose up -d --build
        sleep 5
        echo "📊 Status layanan setelah start:"
        docker-compose ps
        ;;
    "stop")
        echo "🛑 Menghentikan semua layanan Infinite AI Security..."
        docker-compose down
        echo "✅ Semua layanan telah dihentikan."
        ;;
    "restart")
        echo "🔄 Merestart semua layanan Infinite AI Security..."
        docker-compose down
        docker-compose up -d --build
        sleep 5
        echo "📊 Status layanan setelah restart:"
        docker-compose ps
        ;;
    "status")
        echo "📊 Status semua layanan Infinite AI Security:"
        docker-compose ps
        ;;
    "logs")
        if [ -z "$2" ]; then
            echo "📋 Log semua layanan:"
            docker-compose logs --tail=20
        else
            echo "📋 Log layanan $2:"
            docker-compose logs $2 --tail=50
        fi
        ;;
    "build")
        echo "🔨 Membangun ulang semua layanan..."
        docker-compose build --no-cache
        echo "✅ Pembangunan selesai."
        ;;
    *)
        echo "📦 Skrip manajemen layanan Infinite AI Security"
        echo ""
        echo "Penggunaan: $0 [perintah] [opsional: nama_layanan]"
        echo ""
        echo "Perintah yang tersedia:"
        echo "  start     - Memulai semua layanan"
        echo "  stop      - Menghentikan semua layanan"
        echo "  restart   - Merestart semua layanan"
        echo "  status    - Cek status semua layanan"
        echo "  logs      - Tampilkan log (tambahkan nama_layanan untuk log spesifik)"
        echo "  build     - Membangun ulang semua layanan"
        echo ""
        echo "Contoh:"
        echo "  $0 start           - Memulai semua layanan"
        echo "  $0 logs forgerun   - Tampilkan log ForgeRun"
        echo "  $0 restart         - Restart semua layanan"
        ;;
esac