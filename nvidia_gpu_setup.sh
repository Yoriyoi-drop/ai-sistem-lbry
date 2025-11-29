#!/bin/bash

# 🚀 NEXAFORGE - NVIDIA GPU Setup for L0 (Hardware & Runtime Layer)
# This script will install NVIDIA drivers and CUDA toolkit (if not already installed)

set -e

echo "🚀 Installing NVIDIA GPU drivers and CUDA toolkit..."
echo "=================================================="

# Check if running on a system with NVIDIA GPU
if ! command -v lspci &> /dev/null; then
    echo "❌ lspci command not found. Please install pciutils: sudo apt install pciutils"
    exit 1
fi

# Look for NVIDIA GPU
nvidia_gpu=$(lspci | grep -i nvidia)
if [ -z "$nvidia_gpu" ]; then
    echo "❌ No NVIDIA GPU detected in the system"
    echo "   If you have an NVIDIA GPU, please check hardware connection"
    echo "   and ensure it's properly seated."
    exit 0
else
    echo "✅ Found NVIDIA GPU:"
    echo "$nvidia_gpu"
fi

# Check if NVIDIA drivers are already installed
if command -v nvidia-smi &> /dev/null; then
    echo "✅ NVIDIA drivers are already installed:"
    nvidia-smi --query-gpu=name,driver_version --format=csv
else
    echo "🔄 Installing NVIDIA drivers..."

    # Check for secure boot
    if mokutil --sb-state 2>/dev/null | grep -q "enabled"; then
        echo "⚠️  Secure Boot is enabled. During driver installation, you will be asked"
        echo "    to set a MOK password. Remember this password and press 'Enter' when"
        echo "    prompted during the reboot."
    fi

    # Add graphics drivers PPA
    sudo apt update
    sudo apt install ubuntu-drivers-common -y
    
    # Install recommended NVIDIA drivers
    sudo ubuntu-drivers autoinstall
    
    # Reboot required after driver installation
    echo "✅ NVIDIA drivers installed successfully"
    echo "🔄 System needs to be rebooted to load the drivers"
    read -p "Do you want to reboot now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Rebooting now..."
        sudo reboot
    else
        echo "Please reboot manually with 'sudo reboot' before continuing."
    fi
fi

# Check if CUDA is installed
if command -v nvcc &> /dev/null; then
    echo "✅ CUDA toolkit is already installed:"
    nvcc --version
else
    echo "🔄 Installing CUDA toolkit..."
    
    # Setup CUDA repository
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
    sudo dpkg -i cuda-keyring_1.1-1_all.deb
    rm cuda-keyring_1.1-1_all.deb
    sudo apt-get update
    
    # Install CUDA meta package
    sudo apt-get install -y cuda
    
    # Add CUDA paths to user's environment
    cat << 'EOF' >> ~/.bashrc_cuda
# CUDA Toolkit setup for NexaForge
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
EOF
    
    # Source the environment
    source ~/.bashrc_cuda
    
    echo "✅ CUDA toolkit installed successfully"
    echo "   Added CUDA paths to ~/.bashrc_cuda"
    echo "   Run 'source ~/.bashrc_cuda' or restart terminal to use CUDA"
fi

# Verify installation
echo ""
echo "🔍 Verifying NVIDIA driver and CUDA installation..."

if command -v nvidia-smi &> /dev/null && command -v nvcc &> /dev/null; then
    echo "✅ Installation verified:"
    nvidia-smi --query-gpu=name,driver_version --format=csv
    nvcc --version
    echo ""
    echo "🚀 NVIDIA GPU setup for L0 complete!"
    echo "   You now have:"
    echo "   - NVIDIA GPU drivers"
    echo "   - CUDA toolkit"
    echo "   - Ready for AI model deployment"
else
    echo "❌ Installation verification failed"
    echo "   Please check NVIDIA driver and CUDA installation"
    exit 1
fi