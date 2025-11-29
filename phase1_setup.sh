#!/bin/bash

# 🚀 NEXAFORGE - PHASE 1: FOUNDATION SETUP (L0-L1)
# Script setup untuk Ubuntu 22.04 LTS dengan Docker & systemd automation

set -e  # Hentikan jika ada error

echo "🚀 Starting NexaForge Phase 1: Foundation Setup (L0-L1)"
echo "====================================================="

# Cek OS
if [[ -f /etc/os-release ]]; then
    . /etc/os-release
    if [[ "$ID" != "ubuntu" || "$VERSION_ID" != "22.04" ]]; then
        echo "❌ Script ini hanya untuk Ubuntu 22.04 LTS"
        exit 1
    fi
else
    echo "❌ Tidak dapat menentukan versi OS"
    exit 1
fi

echo "✅ OS check passed: Ubuntu 22.04"

# Perbarui sistem
echo "🔄 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install utilities umum
echo "🔧 Installing common utilities..."
sudo apt install -y curl wget vim git unzip htop iotop nvtop

# Install Docker
echo "🐳 Installing Docker..."
if ! command -v docker &> /dev/null; then
    # Hapus versi lama jika ada
    sudo apt remove docker docker-engine docker.io containerd runc || true
    
    # Setup repository Docker
    sudo apt update
    sudo apt install ca-certificates curl gnupg lsb-release -y
    
    # Tambahkan official Docker GPG key
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    
    # Setup repository
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Install Docker
    sudo apt update
    sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin
    
    # Tambahkan user ke grup docker
    sudo usermod -aG docker $USER
    
    echo "✅ Docker installed successfully"
else
    echo "✅ Docker already installed"
fi

# Cek apakah CUDA tersedia (jika GPU NVIDIA)
echo "🔍 Checking NVIDIA GPU availability..."
if command -v nvidia-smi &> /dev/null; then
    echo "✅ NVIDIA GPU detected:"
    nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
    
    # Cek versi CUDA
    if command -v nvcc &> /dev/null; then
        echo "✅ CUDA version:"
        nvcc --version
    else
        echo "⚠️  CUDA not found. You may need to install NVIDIA drivers and CUDA toolkit."
        echo "   Visit: https://developer.nvidia.com/cuda-downloads"
    fi
else
    echo "⚠️  No NVIDIA GPU detected or drivers not installed"
    echo "   If you have an NVIDIA GPU, please install the drivers first"
fi

# Setup systemd service untuk Docker (jika belum running)
echo "⚙️  Configuring Docker service..."
sudo systemctl enable docker
sudo systemctl start docker

# Cek versi Docker
echo "🐳 Docker version:"
docker --version
echo "🐳 Docker Compose version:"
docker compose version

# Setup basic directory structure
echo "📁 Creating directory structure..."
mkdir -p ~/nexaforge/{models,apps,logs,configs,storage}
chmod 755 ~/nexaforge

# Buat file konfigurasi Docker daemon untuk performance
echo "⚙️  Configuring Docker daemon..."
cat << EOF | sudo tee /etc/docker/daemon.json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "default-ulimits": {
    "nofile": {
      "Hard": 64000,
      "Name": "nofile",
      "Soft": 64000
    }
  },
  "max-concurrent-downloads": 10,
  "max-concurrent-uploads": 10,
  "features": {
    "buildkit": true
  }
}
EOF

sudo systemctl restart docker

echo "✅ Docker daemon configured"

# Setup systemd service untuk restart otomatis (contoh template)
echo " systemd service template..."
cat << EOF > ~/nexaforge/configs/nexaforge-template.service
[Unit]
Description=NexaForge Service Template
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
WorkingDirectory=/home/%i/nexaforge/apps

[Install]
WantedBy=multi-user.target
EOF

echo "✅ Systemd template created at ~/nexaforge/configs/nexaforge-template.service"

# Buat file environment
echo "🔐 Creating .env file template..."
cat << EOF > ~/nexaforge/.env
# NEXAFORGE ENVIRONMENT VARIABLES
# Generated: $(date)
COMPOSE_PROJECT_NAME=nexaforge
REGISTRY=docker.io
TAG=latest
GPU_TYPE=nvidia  # Change to 'rocm' if using AMD
STORAGE_PATH=/home/$(whoami)/nexaforge/storage
MODELS_PATH=/home/$(whoami)/nexaforge/models
EOF

echo "✅ Environment file created at ~/nexaforge/.env"

# Cek NVMe storage
echo "🔍 Checking NVMe storage..."
lsblk -d | grep -i nvme || echo "⚠️  No NVMe drives found"

# Summary
echo ""
echo "✅ PHASE 1 SETUP COMPLETED"
echo "=========================="
echo "📁 Directory structure created at ~/nexaforge/"
echo "🐳 Docker version: $(docker --version | cut -d' ' -f3-)"
echo "🐳 Docker Compose: $(docker compose version --short 2>/dev/null || echo 'Not available')"
echo "🔧 User '$USER' added to docker group (re-login required)"
echo ""
echo "📝 Next steps:"
echo "   1. Reboot the system or re-login to apply Docker group changes"
echo "   2. Run 'docker run hello-world' to verify Docker setup"
echo "   3. Place your systemd service files in ~/nexaforge/configs/ if needed"
echo ""

# Test Docker
if groups $USER | grep -q docker; then
    echo "🧪 Testing Docker (user has docker group)..."
    docker run --rm hello-world > /dev/null 2>&1 && echo "✅ Docker test successful" || echo "⚠️  Docker test failed - may need re-login"
else
    echo "⚠️  Warning: User not in docker group. Please re-login or reboot to apply changes."
fi

echo ""
echo "🚀 Phase 1 Complete: Foundation Setup (L0-L1)"