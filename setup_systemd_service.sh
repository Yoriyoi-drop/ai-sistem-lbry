#!/bin/bash
# Setup script for Infinite AI Security systemd service

echo "Setting up Infinite AI Security as a systemd service..."

# First, ensure the service file exists in the home directory with correct content
SERVICE_FILE="/home/whale-d/Unduhan/backup/ai-p/infinite_ai_security/infinite-ai-security.service"

# Create the service file with the correct content
cat > "$SERVICE_FILE" << 'EOF'
[Unit]
Description=Infinite AI Security with Ollama
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStartPre=/bin/sleep 30
ExecStart=/bin/bash -c 'cd /home/whale-d/Unduhan/backup/ai-p/infinite_ai_security && (command -v docker-compose >/dev/null 2>&1 && docker-compose -f docker-compose.ollama.yml -f docker-compose.yml up -d) || (command -v docker >/dev/null 2>&1 && docker compose -f docker-compose.ollama.yml -f docker-compose.yml up -d)'
ExecStop=/bin/bash -c 'cd /home/whale-d/Unduhan/backup/ai-p/infinite_ai_security && (command -v docker-compose >/dev/null 2>&1 && docker-compose -f docker-compose.ollama.yml -f docker-compose.yml down) || (command -v docker >/dev/null 2>&1 && docker compose -f docker-compose.ollama.yml -f docker-compose.yml down)'
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

# Use the Docker socket approach for now since sudo is required
sudo -H -u root sh -c "cp '$SERVICE_FILE' /etc/systemd/system/"

# Reload systemd daemon
sudo -H -u root systemctl daemon-reload

# Enable the service to start on boot
sudo -H -u root systemctl enable infinite-ai-security.service

echo "Service has been installed and enabled!"
echo ""
echo "To start the service now:"
echo "  sudo -H -u root systemctl start infinite-ai-security"
echo ""
echo "To check service status:"
echo "  sudo -H -u root systemctl status infinite-ai-security"
echo ""
echo "To view logs:"
echo "  sudo -H -u root journalctl -u infinite-ai-security -f"
echo ""
echo "The service will now start automatically on boot."