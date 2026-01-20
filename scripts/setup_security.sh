#!/bin/bash
#
# Quick Start Script for Resilience & Security Features
# Sets up monitoring, backup, and security automation
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Euystacio Security & Resilience Setup${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo -e "${YELLOW}Warning: Running as root. Some features may not work correctly.${NC}"
    echo -e "${YELLOW}Consider running as a regular user with sudo access.${NC}"
    echo ""
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check dependencies
echo -e "${BLUE}[1/6] Checking dependencies...${NC}"

MISSING_DEPS=()

if ! command_exists docker; then
    MISSING_DEPS+=("docker")
fi

if ! command_exists docker-compose; then
    MISSING_DEPS+=("docker-compose")
fi

if ! command_exists python3; then
    MISSING_DEPS+=("python3")
fi

if ! command_exists gpg; then
    MISSING_DEPS+=("gnupg")
fi

if [ ${#MISSING_DEPS[@]} -ne 0 ]; then
    echo -e "${RED}Missing dependencies: ${MISSING_DEPS[*]}${NC}"
    echo ""
    echo "Install with:"
    echo "  Ubuntu/Debian: sudo apt-get install docker.io docker-compose python3 gnupg"
    echo "  macOS: brew install docker docker-compose python3 gnupg"
    exit 1
else
    echo -e "${GREEN}✓ All required dependencies installed${NC}"
fi

echo ""

# Install Python dependencies
echo -e "${BLUE}[2/6] Installing Python dependencies...${NC}"

if command_exists pip3; then
    pip3 install -r requirements.txt --quiet
    echo -e "${GREEN}✓ Python dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠ pip3 not found, skipping Python dependencies${NC}"
fi

echo ""

# Setup monitoring stack
echo -e "${BLUE}[3/6] Setting up monitoring stack...${NC}"

read -p "Start monitoring stack (Grafana, Loki, Prometheus)? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker-compose -f docker-compose.monitoring.yml up -d
    echo -e "${GREEN}✓ Monitoring stack started${NC}"
    echo -e "  Grafana: ${BLUE}http://localhost:3000${NC} (admin/admin)"
    echo -e "  Prometheus: ${BLUE}http://localhost:9090${NC}"
    echo -e "  Loki: ${BLUE}http://localhost:3100${NC}"
else
    echo -e "${YELLOW}⚠ Skipping monitoring stack${NC}"
fi

echo ""

# Configure forensic watcher
echo -e "${BLUE}[4/6] Configuring forensic response automation...${NC}"

read -p "Configure forensic log watcher? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Create log directory
    sudo mkdir -p /var/log/euystacio
    sudo chown $USER:$USER /var/log/euystacio
    
    echo -e "${GREEN}✓ Log directory created: /var/log/euystacio${NC}"
    echo ""
    echo "To start the forensic watcher:"
    echo -e "  ${YELLOW}python3 scripts/forensic_watcher.py${NC}"
    echo ""
    echo "To enable automated responses (requires root):"
    echo -e "  ${YELLOW}sudo python3 scripts/forensic_watcher.py --enable-response${NC}"
else
    echo -e "${YELLOW}⚠ Skipping forensic watcher${NC}"
fi

echo ""

# Configure backups
echo -e "${BLUE}[5/6] Configuring distributed backups...${NC}"

read -p "Configure encrypted backups? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Create backup directory
    sudo mkdir -p /var/backups/euystacio
    sudo chown $USER:$USER /var/backups/euystacio
    
    echo -e "${GREEN}✓ Backup directory created: /var/backups/euystacio${NC}"
    
    # Check GPG key
    if gpg --list-keys | grep -q "@"; then
        echo -e "${GREEN}✓ GPG key found${NC}"
    else
        echo -e "${YELLOW}⚠ No GPG key found${NC}"
        echo ""
        read -p "Generate new GPG key? [y/N] " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "Generating GPG key (this may take a moment)..."
            gpg --batch --gen-key <<EOF
Key-Type: RSA
Key-Length: 2048
Name-Real: Euystacio Backup
Name-Email: backup@euystacio.local
Expire-Date: 0
%no-protection
%commit
EOF
            echo -e "${GREEN}✓ GPG key generated${NC}"
        fi
    fi
    
    echo ""
    echo "To create a backup:"
    echo -e "  ${YELLOW}python3 scripts/distributed_backup.py create${NC}"
    echo ""
    echo "To list backups:"
    echo -e "  ${YELLOW}python3 scripts/distributed_backup.py list${NC}"
else
    echo -e "${YELLOW}⚠ Skipping backup configuration${NC}"
fi

echo ""

# Setup QUIC server
echo -e "${BLUE}[6/6] Configuring QUIC server...${NC}"

read -p "Generate self-signed certificate for QUIC server? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    mkdir -p certs
    
    if [ ! -f certs/cert.pem ]; then
        openssl req -x509 -newkey rsa:2048 \
            -keyout certs/key.pem \
            -out certs/cert.pem \
            -days 365 -nodes \
            -subj '/CN=euystacio.local' 2>/dev/null
        
        echo -e "${GREEN}✓ Self-signed certificate generated${NC}"
        echo -e "  Certificate: ${BLUE}certs/cert.pem${NC}"
        echo -e "  Private Key: ${BLUE}certs/key.pem${NC}"
    else
        echo -e "${GREEN}✓ Certificate already exists${NC}"
    fi
    
    echo ""
    echo "To start QUIC server:"
    echo -e "  ${YELLOW}python3 scripts/quic_server.py${NC}"
    echo ""
    echo "To test with client:"
    echo -e "  ${YELLOW}python3 scripts/quic_client.py --message ping${NC}"
else
    echo -e "${YELLOW}⚠ Skipping QUIC certificate${NC}"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Next steps:"
echo ""
echo -e "1. Read the full guide: ${BLUE}RESILIENCE_SECURITY_GUIDE.md${NC}"
echo ""
echo "2. Start monitoring:"
echo -e "   ${YELLOW}docker-compose -f docker-compose.monitoring.yml up -d${NC}"
echo -e "   Open: ${BLUE}http://localhost:3000${NC}"
echo ""
echo "3. Start forensic watcher:"
echo -e "   ${YELLOW}python3 scripts/forensic_watcher.py${NC}"
echo ""
echo "4. Create encrypted backup:"
echo -e "   ${YELLOW}python3 scripts/distributed_backup.py create${NC}"
echo ""
echo "5. Start QUIC server:"
echo -e "   ${YELLOW}python3 scripts/quic_server.py${NC}"
echo ""
echo -e "For help and documentation, visit:"
echo -e "${BLUE}https://github.com/hannesmitterer/Euystacio${NC}"
echo ""
