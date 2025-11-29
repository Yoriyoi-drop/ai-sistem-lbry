#!/bin/bash

# WSL2 Setup for NexaForge (L1 layer component)
# This script is for Windows users who will run WSL2 Ubuntu 22.04

echo "🔍 Checking if running in WSL..."
if grep -qE "(Microsoft|WSL)" /proc/version &> /dev/null ; then
    echo "✅ Running in WSL2 environment"

    # Check WSL version
    echo "🔍 Checking WSL version..."
    wsl -l -v 2>/dev/null | grep -i $(hostname) | grep -q "WSL2" && echo "✅ WSL2 detected" || echo "⚠️  Not running on WSL2 - some features may not work optimally"

    # For WSL2, recommend additional setup
    echo "💡 For optimal WSL2 performance, consider:"
    echo "   1. Adding to .wslconfig in Windows (%USERPROFILE%/.wslconfig):"
    echo "      [wsl2]"
    echo "      memory=16GB"
    echo "      processors=8"
    echo "      swap=8GB"
    echo "      localhostForwarding=true"
    echo ""
    echo "   2. GPU support: Install NVIDIA WSL driver if you have an NVIDIA GPU"
    echo "      Download from: https://developer.nvidia.com/cuda-wsl"
else
    echo "ℹ️  Not running in WSL environment - this script is for WSL2 users"
fi