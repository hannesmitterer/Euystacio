#!/bin/bash
#
# Activate VPN Routing Script
# Redirects network traffic through VPN connection for secure communication
#
# WARNING: This script requires OpenVPN or WireGuard to be installed
# OpenVPN: sudo apt-get install openvpn
# WireGuard: sudo apt-get install wireguard
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}[VPN Routing] Activating VPN routing...${NC}"

# Configuration
VPN_TYPE="${VPN_TYPE:-openvpn}"  # openvpn or wireguard
OPENVPN_CONFIG="${OPENVPN_CONFIG:-/etc/openvpn/client.conf}"
WIREGUARD_CONFIG="${WIREGUARD_CONFIG:-/etc/wireguard/wg0.conf}"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}[ERROR] Please run as root${NC}"
    echo "Try: sudo $0"
    exit 1
fi

# Function to activate OpenVPN
activate_openvpn() {
    echo -e "${YELLOW}[INFO] Activating OpenVPN...${NC}"
    
    # Check if OpenVPN is installed
    if ! command -v openvpn &> /dev/null; then
        echo -e "${RED}[ERROR] OpenVPN is not installed${NC}"
        echo "Install with: sudo apt-get install openvpn"
        exit 1
    fi
    
    # Check if config exists
    if [ ! -f "$OPENVPN_CONFIG" ]; then
        echo -e "${RED}[ERROR] OpenVPN config not found: $OPENVPN_CONFIG${NC}"
        echo "Please configure OpenVPN first"
        exit 1
    fi
    
    # Start OpenVPN
    systemctl start openvpn@client || openvpn --config "$OPENVPN_CONFIG" --daemon
    sleep 5
    
    # Verify connection
    if ip a show tun0 &> /dev/null; then
        echo -e "${GREEN}[SUCCESS] OpenVPN activated (tun0 interface up)${NC}"
    else
        echo -e "${RED}[ERROR] OpenVPN activation failed${NC}"
        exit 1
    fi
}

# Function to activate WireGuard
activate_wireguard() {
    echo -e "${YELLOW}[INFO] Activating WireGuard...${NC}"
    
    # Check if WireGuard is installed
    if ! command -v wg &> /dev/null; then
        echo -e "${RED}[ERROR] WireGuard is not installed${NC}"
        echo "Install with: sudo apt-get install wireguard"
        exit 1
    fi
    
    # Check if config exists
    if [ ! -f "$WIREGUARD_CONFIG" ]; then
        echo -e "${RED}[ERROR] WireGuard config not found: $WIREGUARD_CONFIG${NC}"
        echo "Please configure WireGuard first"
        exit 1
    fi
    
    # Start WireGuard
    wg-quick up wg0
    sleep 3
    
    # Verify connection
    if wg show wg0 &> /dev/null; then
        echo -e "${GREEN}[SUCCESS] WireGuard activated (wg0 interface up)${NC}"
    else
        echo -e "${RED}[ERROR] WireGuard activation failed${NC}"
        exit 1
    fi
}

# Activate based on VPN type
case "$VPN_TYPE" in
    openvpn)
        activate_openvpn
        ;;
    wireguard)
        activate_wireguard
        ;;
    *)
        echo -e "${RED}[ERROR] Unknown VPN type: $VPN_TYPE${NC}"
        echo "Supported types: openvpn, wireguard"
        exit 1
        ;;
esac

# Configure firewall to force VPN routing
echo -e "${YELLOW}[INFO] Configuring firewall rules...${NC}"

# Backup current iptables rules
iptables-save > /tmp/iptables_backup_vpn_$(date +%s).rules

# Get VPN interface
VPN_INTERFACE="tun0"
if [ "$VPN_TYPE" = "wireguard" ]; then
    VPN_INTERFACE="wg0"
fi

# Allow traffic through VPN interface
iptables -A OUTPUT -o $VPN_INTERFACE -j ACCEPT
iptables -A INPUT -i $VPN_INTERFACE -j ACCEPT

# Block non-VPN traffic (optional, uncomment to enforce VPN-only)
# iptables -A OUTPUT ! -o lo ! -o $VPN_INTERFACE -j DROP

# Log the activation
mkdir -p /var/log/euystacio
echo "$(date) - VPN routing activated ($VPN_TYPE)" >> /var/log/euystacio/forensic_actions.log

echo -e "${GREEN}[SUCCESS] VPN routing activated!${NC}"
echo -e "${GREEN}Network traffic is now routed through VPN ($VPN_TYPE)${NC}"
echo ""
echo -e "${YELLOW}To deactivate:${NC}"
if [ "$VPN_TYPE" = "openvpn" ]; then
    echo "  sudo systemctl stop openvpn@client"
elif [ "$VPN_TYPE" = "wireguard" ]; then
    echo "  sudo wg-quick down wg0"
fi
echo "  Restore iptables: sudo iptables-restore < /tmp/iptables_backup_vpn_*.rules"
echo ""
echo -e "${YELLOW}Check VPN connection:${NC}"
echo "  curl https://ifconfig.me"
echo "  ip a show $VPN_INTERFACE"
