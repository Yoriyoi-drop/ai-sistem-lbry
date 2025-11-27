#!/bin/bash
# Installation script for nexaForge

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root or with sudo"
    exit 1
fi

# Copy the nexaForge script to system-wide location
SCRIPT_PATH="/home/whale-d/Unduhan/backup/ai-p/infinite_ai_security/nexaForge"

if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Error: nexaForge script not found at $SCRIPT_PATH"
    exit 1
fi

# Copy to system location
cp "$SCRIPT_PATH" /usr/local/bin/nexaForge
chmod +x /usr/local/bin/nexaForge

# Create a symlink as well
if [ ! -f /usr/bin/nexaForge ]; then
    ln -s /usr/local/bin/nexaForge /usr/bin/nexaForge 2>/dev/null || true
fi

echo "nexaForge has been installed system-wide!"
echo "You can now run 'nexaForge' from anywhere."
echo ""
echo "Available commands:"
echo "  nexaForge status    - Show status of all services"
echo "  nexaForge start     - Start all services" 
echo "  nexaForge stop      - Stop all services"
echo "  nexaForge restart   - Restart all services"
echo "  nexaForge logs      - Show logs from all services"
echo "  nexaForge migrate   - Run database migrations"
echo "  nexaForge ps        - Show running containers"
echo "  nexaForge config    - Show current configuration"
echo "  nexaForge help      - Show help message"