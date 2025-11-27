#!/bin/bash

####################################################################
# NexaForge AI System - 24/7 Setup Script
# Membuat sistem AI berjalan non-stop dengan auto-restart
####################################################################

set -e

# Colors untuk output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_PATH="/home/whale-d/Unduhan/backup/ai-p/infinite_ai_security"
SERVICE_NAME="nexaforge"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}-24-7.service"
DOCKER_COMPOSE_FILE="docker-compose-24-7.yml"

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  NexaForge AI System - 24/7 Setup Installation            ║"
echo "║  Sistem AI akan berjalan non-stop otomatis                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}Error: Script ini harus dijalankan dengan sudo${NC}"
   exit 1
fi

echo -e "${YELLOW}[1/6]${NC} Memeriksa Docker..."
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker tidak ditemukan. Silakan install Docker terlebih dahulu.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker ditemukan${NC}"

echo -e "${YELLOW}[2/6]${NC} Memeriksa Docker Compose..."
if ! command -v docker compose &> /dev/null; then
    echo -e "${RED}Docker Compose tidak ditemukan. Silakan install Docker Compose terlebih dahulu.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker Compose ditemukan${NC}"

echo -e "${YELLOW}[3/6]${NC} Memeriksa file docker-compose-24-7.yml..."
if [ ! -f "$PROJECT_PATH/$DOCKER_COMPOSE_FILE" ]; then
    echo -e "${RED}File $DOCKER_COMPOSE_FILE tidak ditemukan di $PROJECT_PATH${NC}"
    exit 1
fi
echo -e "${GREEN}✓ File docker-compose-24-7.yml ditemukan${NC}"

echo -e "${YELLOW}[4/6]${NC} Menghentikan layanan lama (jika ada)..."
if systemctl is-active --quiet nexaforge 2>/dev/null; then
    systemctl stop nexaforge || true
    sleep 2
fi
echo -e "${GREEN}✓ Layanan lama dihentikan${NC}"

echo -e "${YELLOW}[5/6]${NC} Membuat/Update systemd service..."
if [ -f "$SERVICE_FILE" ]; then
    echo -e "${YELLOW}  • Menghapus service lama...${NC}"
    systemctl disable ${SERVICE_NAME}-24-7 2>/dev/null || true
    systemctl daemon-reload
fi

# Copy service file
cp "$PROJECT_PATH/nexaforge-24-7.service" "$SERVICE_FILE"
chmod 644 "$SERVICE_FILE"

# Update service file dengan path yang benar
sed -i "s|WorkingDirectory=.*|WorkingDirectory=$PROJECT_PATH|g" "$SERVICE_FILE"

echo -e "${GREEN}✓ Service file dibuat/diupdate${NC}"

echo -e "${YELLOW}[6/6]${NC} Mengaktifkan dan menjalankan service..."
systemctl daemon-reload
systemctl enable ${SERVICE_NAME}-24-7
systemctl start ${SERVICE_NAME}-24-7

sleep 3

# Verifikasi status
if systemctl is-active --quiet ${SERVICE_NAME}-24-7; then
    echo -e "${GREEN}✓ Service berhasil dijalankan${NC}"
else
    echo -e "${RED}✗ Service gagal dijalankan${NC}"
    echo -e "${YELLOW}Debug info:${NC}"
    systemctl status ${SERVICE_NAME}-24-7
    exit 1
fi

echo ""
echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✓ INSTALASI BERHASIL                                     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}📋 INFORMASI PENTING:${NC}"
echo ""
echo -e "${GREEN}1. Sistem AI Anda sekarang berjalan 24/7${NC}"
echo "   • Container akan auto-restart jika crash"
echo "   • Service akan auto-start setelah reboot server"
echo ""
echo -e "${GREEN}2. Command yang berguna:${NC}"
echo ""
echo "   • Lihat status:"
echo "     ${BLUE}sudo systemctl status ${SERVICE_NAME}-24-7${NC}"
echo ""
echo "   • Melihat logs real-time:"
echo "     ${BLUE}sudo journalctl -u ${SERVICE_NAME}-24-7 -f${NC}"
echo ""
echo "   • Melihat logs N baris terakhir:"
echo "     ${BLUE}sudo journalctl -u ${SERVICE_NAME}-24-7 -n 100${NC}"
echo ""
echo "   • Mematikan service (untuk maintenance):"
echo "     ${BLUE}sudo systemctl stop ${SERVICE_NAME}-24-7${NC}"
echo ""
echo "   • Menjalankan kembali service:"
echo "     ${BLUE}sudo systemctl start ${SERVICE_NAME}-24-7${NC}"
echo ""
echo "   • Restart service:"
echo "     ${BLUE}sudo systemctl restart ${SERVICE_NAME}-24-7${NC}"
echo ""
echo "   • Melihat container yang berjalan:"
echo "     ${BLUE}docker ps${NC}"
echo ""
echo "   • Melihat logs container tertentu:"
echo "     ${BLUE}docker logs -f [nama-container]${NC}"
echo ""
echo "   • Melihat resource usage:"
echo "     ${BLUE}docker stats${NC}"
echo ""
echo -e "${GREEN}3. Akses Dashboard:${NC}"
echo "   • Grafana Dashboard: http://localhost:3000"
echo "   • Prometheus: http://localhost:9090"
echo "   • API: http://localhost:8000"
echo ""
echo -e "${YELLOW}⚠️  CATATAN:${NC}"
echo "   • Setiap container memiliki HEALTHCHECK"
echo "   • Jika container tidak sehat, Docker otomatis restart"
echo "   • Restart policy: 'always' untuk semua service"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

exit 0
