#!/bin/bash
#
# Activate Tor Routing Script
# Redirects network traffic through Tor network for enhanced privacy
#
# WARNING: This script requires Tor to be installed and configured
# Install: sudo apt-get install tor
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}[Tor Routing] Activating Tor routing...${NC}"

# Check if Tor is installed
if ! command -v tor &> /dev/null; then
    echo -e "${RED}[ERROR] Tor is not installed${NC}"
    echo "Install with: sudo apt-get install tor"
    exit 1
fi

# Check if running as root (required for iptables)
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}[ERROR] Please run as root${NC}"
    echo "Try: sudo $0"
    exit 1
fi

# Tor configuration
TOR_UID=$(id -u debian-tor 2>/dev/null || id -u tor 2>/dev/null || echo "")
TOR_PORT="9050"
TOR_TRANS_PORT="9040"
TOR_DNS_PORT="5353"

if [ -z "$TOR_UID" ]; then
    echo -e "${RED}[ERROR] Cannot determine Tor user UID${NC}"
    exit 1
fi

echo -e "${GREEN}[INFO] Tor UID: $TOR_UID${NC}"

# Start Tor service if not running
if ! systemctl is-active --quiet tor; then
    echo -e "${YELLOW}[INFO] Starting Tor service...${NC}"
    systemctl start tor
    sleep 3
fi

# Check if Tor is running
if ! systemctl is-active --quiet tor; then
    echo -e "${RED}[ERROR] Failed to start Tor service${NC}"
    exit 1
fi

# Backup current iptables rules
echo -e "${YELLOW}[INFO] Backing up current iptables rules...${NC}"
iptables-save > /tmp/iptables_backup_$(date +%s).rules

# Flush existing rules
echo -e "${YELLOW}[INFO] Flushing existing iptables rules...${NC}"
iptables -F
iptables -t nat -F

# Allow Tor traffic
echo -e "${YELLOW}[INFO] Configuring iptables for Tor routing...${NC}"

# Don't redirect Tor's own traffic
iptables -t nat -A OUTPUT -m owner --uid-owner $TOR_UID -j RETURN

# Allow loopback
iptables -t nat -A OUTPUT -o lo -j RETURN

# Allow local network (adjust as needed)
iptables -t nat -A OUTPUT -d 192.168.0.0/16 -j RETURN
iptables -t nat -A OUTPUT -d 10.0.0.0/8 -j RETURN
iptables -t nat -A OUTPUT -d 172.16.0.0/12 -j RETURN

# Redirect DNS requests to Tor DNS port
iptables -t nat -A OUTPUT -p udp --dport 53 -j REDIRECT --to-ports $TOR_DNS_PORT

# Redirect all TCP traffic to Tor transparent proxy
iptables -t nat -A OUTPUT -p tcp --syn -j REDIRECT --to-ports $TOR_TRANS_PORT

# Log the activation
echo "$(date) - Tor routing activated" >> /var/log/euystacio/forensic_actions.log

echo -e "${GREEN}[SUCCESS] Tor routing activated!${NC}"
echo -e "${GREEN}All network traffic is now routed through Tor${NC}"
echo ""
echo -e "${YELLOW}To deactivate:${NC}"
echo "  sudo iptables -F"
echo "  sudo iptables -t nat -F"
echo "  Restore from backup: sudo iptables-restore < /tmp/iptables_backup_*.rules"
echo ""
echo -e "${YELLOW}Check Tor connection:${NC}"
echo "  curl --socks5 localhost:9050 https://check.torproject.org/api/ip"
