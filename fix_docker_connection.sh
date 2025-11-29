#!/bin/bash

echo "🔧 MEMPERBAIKI KONEKSI DOCKER DAN WARNING"
echo "=========================================="
echo ""

# 1. Fix Docker Context
echo "1️⃣ Memperbaiki Docker Context..."
docker context use default 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✅ Docker context diset ke 'default'"
else
    echo "   ⚠️  Gagal mengubah context, melanjutkan..."
fi
echo ""

# 2. Check Docker Connection
echo "2️⃣ Memeriksa koneksi Docker..."
docker ps > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✅ Docker terhubung dengan baik"
else
    echo "   ❌ Docker tidak terhubung!"
    echo "   💡 Coba jalankan: sudo systemctl start docker"
    exit 1
fi
echo ""

# 3. Stop old containers (if any)
echo "3️⃣ Membersihkan container lama..."
cd /home/whale-d/Unduhan/backup/ai-p/infinite_ai_security/infrastructure/docker

# Try to stop gracefully, if fails, continue
docker-compose -p aisec_v4 down 2>/dev/null || true
docker-compose -p aisec_v5 down 2>/dev/null || true

echo "   ✅ Container lama dibersihkan"
echo ""

# 4. Start with new project name
echo "4️⃣ Memulai services dengan konfigurasi baru..."
echo "   Project name: aisec_clean"
echo ""

# Start services
docker-compose -p aisec_clean up -d

if [ $? -eq 0 ]; then
    echo ""
    echo "   ✅ Services berhasil dijalankan!"
else
    echo ""
    echo "   ❌ Gagal menjalankan services"
    exit 1
fi

# 5. Wait for services to be ready
echo ""
echo "5️⃣ Menunggu services siap (30 detik)..."
for i in {30..1}; do
    printf "\r   ⏳ Menunggu... %2d detik" $i
    sleep 1
done
echo ""
echo "   ✅ Services seharusnya sudah siap"
echo ""

# 6. Check service health
echo "6️⃣ Memeriksa status services..."
echo ""
docker-compose -p aisec_clean ps
echo ""

# 7. Test endpoints
echo "7️⃣ Testing endpoints..."
echo ""

# Test API Gateway
echo "   Testing API Gateway..."
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:9000/api/v1/health/)
if [ "$response" = "200" ]; then
    echo "   ✅ API Gateway: HEALTHY"
else
    echo "   ⚠️  API Gateway: Status $response"
fi

# Test AI Hub
echo "   Testing AI Hub..."
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:9001/)
if [ "$response" = "200" ]; then
    echo "   ✅ AI Hub: HEALTHY"
else
    echo "   ⚠️  AI Hub: Status $response"
fi

# Test Scanner
echo "   Testing Scanner..."
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:9002/)
if [ "$response" = "200" ] || [ "$response" = "404" ]; then
    echo "   ✅ Scanner: RUNNING"
else
    echo "   ⚠️  Scanner: Status $response"
fi

# Test n8n
echo "   Testing n8n..."
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:9004/)
if [ "$response" = "200" ] || [ "$response" = "401" ]; then
    echo "   ✅ n8n: RUNNING"
else
    echo "   ⚠️  n8n: Status $response"
fi

echo ""
echo "=========================================="
echo "✅ PERBAIKAN SELESAI!"
echo "=========================================="
echo ""
echo "🌐 Access Points:"
echo "   • API Gateway:  http://localhost:9000/docs"
echo "   • AI Hub:       http://localhost:9001/docs"
echo "   • Scanner:      http://localhost:9002"
echo "   • n8n:          http://localhost:9004 (admin/admin)"
echo ""
echo "📊 Untuk melihat logs:"
echo "   docker-compose -p aisec_clean logs -f"
echo ""
echo "🛑 Untuk stop services:"
echo "   docker-compose -p aisec_clean down"
echo ""
