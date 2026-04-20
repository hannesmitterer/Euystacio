# Resilience and Security Operations Guide

This guide documents the enhanced resilience and security features for decentralized operations in the Euystacio ecosystem.

## Table of Contents

1. [Real-time Monitoring Dashboard](#1-real-time-monitoring-dashboard)
2. [Forensic Response Automation](#2-forensic-response-automation)
3. [Secure Firmware Updates](#3-secure-firmware-updates)
4. [Distributed Encrypted Backups](#4-distributed-encrypted-backups)
5. [Hardened Communication Protocols](#5-hardened-communication-protocols)

---

## 1. Real-time Monitoring Dashboard

### Overview

The monitoring infrastructure uses Grafana, Loki, and Prometheus to provide real-time visibility into system health, security events, and performance metrics.

### Components

- **Grafana**: Visualization and dashboarding
- **Loki**: Log aggregation and querying
- **Promtail**: Log shipping agent
- **Prometheus**: Metrics collection

### Quick Start

```bash
# Start monitoring stack
docker-compose -f docker-compose.monitoring.yml up -d

# Access Grafana dashboard
open http://localhost:3000
# Default credentials: admin/admin (change on first login)
```

### Configuration

All monitoring configurations are located in the `monitoring/` directory:

```
monitoring/
├── grafana/
│   ├── dashboards/          # Pre-configured dashboards
│   └── provisioning/        # Datasource configurations
├── loki/
│   └── loki-config.yml      # Loki configuration
├── promtail/
│   └── promtail-config.yml  # Log shipping configuration
└── prometheus.yml           # Metrics collection config
```

### Key Features

- **Node Status Monitoring**: Real-time health checks
- **Latency Tracking**: Request/response time metrics
- **Intrusion Detection**: Security event visualization
- **Log Aggregation**: Centralized log management with 30-day retention

### Dashboards

The main dashboard (`euystacio-dashboard.json`) provides:

- Node health status gauges
- System latency graphs
- Intrusion detection alerts table
- Application and security logs
- Critical events counter

---

## 2. Forensic Response Automation

### Overview

Automated log monitoring with intelligent response to suspicious activities, including automatic Tor/VPN routing activation.

### Components

- `scripts/forensic_watcher.py`: Log monitoring daemon
- `scripts/activate_tor.sh`: Tor routing activation
- `scripts/activate_vpn.sh`: VPN routing activation
- `scripts/forensic_config.json`: Detection rules

### Installation

```bash
# Install dependencies (Debian/Ubuntu)
sudo apt-get update
sudo apt-get install tor openvpn python3

# Make scripts executable
chmod +x scripts/forensic_watcher.py
chmod +x scripts/activate_tor.sh
chmod +x scripts/activate_vpn.sh
```

### Usage

```bash
# Monitor logs (dry run - no automatic responses)
python3 scripts/forensic_watcher.py

# Enable automated responses (requires root)
sudo python3 scripts/forensic_watcher.py --enable-response

# Custom configuration
python3 scripts/forensic_watcher.py --config my_forensic_config.json

# Scan specific logs once
python3 scripts/forensic_watcher.py --logs /var/log/app.log --no-follow
```

### Detection Patterns

The system detects:

- Multiple failed authentication attempts
- Port scanning activity
- SQL injection attempts
- Unauthorized access attempts
- Brute force attacks
- Command injection attempts
- Directory traversal attempts
- XSS attempts

### Response Actions

1. **tor_routing**: Activate Tor for anonymity
2. **vpn_routing**: Activate VPN for secure communication
3. **block_and_alert**: Block IP and send alert
4. **monitor**: Log and continue monitoring

### Configuration

Edit `scripts/forensic_config.json`:

```json
{
  "response_enabled": false,
  "tor_enabled": false,
  "vpn_enabled": false,
  "alert_threshold": 5,
  "time_window_seconds": 300,
  "suspicious_patterns": [
    {
      "name": "Pattern Name",
      "pattern": "regex pattern",
      "severity": "high|medium|low",
      "action": "tor_routing|vpn_routing|block_and_alert|monitor"
    }
  ]
}
```

---

## 3. Secure Firmware Updates

### Overview

Cryptographically verified firmware updates with checksum validation and automatic rollback capability.

### Features

- SHA-512 checksum verification
- GPG signature verification
- Automatic backup before update
- Rollback on failure
- Version tracking

### Usage

```bash
# Update to specific version
python3 scripts/secure_updater.py update --version 2.1.0

# Verify file integrity
python3 scripts/secure_updater.py verify \
  --file update.tar.gz \
  --checksum abc123... \
  --signature update.tar.gz.sig

# Create backup
python3 scripts/secure_updater.py backup

# Rollback to previous version
python3 scripts/secure_updater.py rollback

# Rollback to specific backup
python3 scripts/secure_updater.py rollback --backup /var/backups/euystacio/backup_20260120.tar.gz
```

### Update Server Setup

Configure update server in `scripts/update_config.json`:

```json
{
  "update_server": "https://updates.euystacio.io",
  "gpg_key_id": "your-gpg-key-id",
  "verify_checksums": true,
  "verify_signatures": true,
  "auto_rollback": true
}
```

### Update Package Format

Update packages should include:

1. **manifest.json**: Metadata and checksums
   ```json
   {
     "version": "2.1.0",
     "package_url": "https://updates.euystacio.io/updates/2.1.0/euystacio-2.1.0.tar.gz",
     "signature_url": "https://updates.euystacio.io/updates/2.1.0/euystacio-2.1.0.tar.gz.sig",
     "checksum": "sha512-hash-here",
     "package_name": "euystacio-2.1.0.tar.gz"
   }
   ```

2. **Package file**: Compressed update archive
3. **Signature file**: GPG detached signature

---

## 4. Distributed Encrypted Backups

### Overview

Automated backup system with GnuPG encryption and IPFS distributed storage.

### Features

- Automatic GnuPG encryption
- IPFS distributed storage
- Local backup retention
- Metadata tracking
- Easy restore process

### Installation

```bash
# Install dependencies
sudo apt-get install gnupg tar
sudo apt-get install ipfs  # or download from https://ipfs.io

# Initialize IPFS (first time only)
ipfs init

# Start IPFS daemon
ipfs daemon &
```

### Usage

```bash
# Create encrypted backup
python3 scripts/distributed_backup.py create

# List all backups
python3 scripts/distributed_backup.py list

# Restore from IPFS (using CID)
python3 scripts/distributed_backup.py restore \
  --source QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG \
  --restore-dir /tmp/restored

# Restore from local file
python3 scripts/distributed_backup.py restore \
  --source /var/backups/euystacio/backup_20260120_120000.tar.gz.gpg \
  --restore-dir /tmp/restored
```

### Configuration

Edit `scripts/backup_config.json`:

```json
{
  "backup_directories": [
    "/path/to/important/data"
  ],
  "exclude_patterns": [
    "*.tmp",
    "*.log",
    "__pycache__"
  ],
  "gpg_recipient": "your-email@example.com",
  "ipfs_enabled": true,
  "max_local_backups": 10
}
```

### GPG Setup

```bash
# Generate GPG key (if needed)
gpg --full-generate-key

# List keys
gpg --list-keys

# Export public key for sharing
gpg --armor --export your-email@example.com > public_key.asc

# Import trusted key (for verification)
gpg --import trusted_key.asc
```

### Automated Backups

Add to crontab for daily backups:

```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /usr/bin/python3 /path/to/scripts/distributed_backup.py create >> /var/log/euystacio/backup.log 2>&1
```

---

## 5. Hardened Communication Protocols

### Overview

QUIC protocol implementation with mandatory TLS 1.3 encryption for low-latency, secure communication.

### Features

- QUIC protocol (HTTP/3 ready)
- Mandatory TLS 1.3 encryption
- No fallback to unencrypted protocols
- Low latency
- Built-in multiplexing

### Installation

```bash
# Install aioquic library
pip install aioquic

# Install OpenSSL (for certificate generation)
sudo apt-get install openssl
```

### Server Usage

```bash
# Start QUIC server
python3 scripts/quic_server.py

# Custom host and port
python3 scripts/quic_server.py --host 0.0.0.0 --port 4433

# Custom configuration
python3 scripts/quic_server.py --config my_quic_config.json
```

### Client Usage

```bash
# Send ping message
python3 scripts/quic_client.py --message ping

# Request status
python3 scripts/quic_client.py --message status

# Send data
python3 scripts/quic_client.py --message data

# Connect to remote server
python3 scripts/quic_client.py --host server.example.com --port 4433
```

### Certificate Management

```bash
# Generate self-signed certificate (development)
mkdir -p certs
openssl req -x509 -newkey rsa:2048 \
  -keyout certs/key.pem \
  -out certs/cert.pem \
  -days 365 -nodes \
  -subj '/CN=euystacio.local'

# For production, use Let's Encrypt:
certbot certonly --standalone -d yourdomain.com
# Then update quic_config.json with certificate paths
```

### Configuration

Edit `scripts/quic_config.json`:

```json
{
  "host": "0.0.0.0",
  "port": 4433,
  "certificate": "certs/cert.pem",
  "private_key": "certs/key.pem",
  "disable_unencrypted": true,
  "tls_version": "1.3",
  "security": {
    "enforce_tls_1.3": true,
    "disable_legacy_protocols": true,
    "reject_unencrypted": true
  }
}
```

### Security Settings

The QUIC implementation enforces:

- TLS 1.3 only (no downgrade to 1.2 or earlier)
- No unencrypted connections
- Certificate validation
- Modern cipher suites only

### Integration with Application

To integrate QUIC server with your application:

```python
from scripts.quic_server import QUICServer
import asyncio

# Create and run server
server = QUICServer()
asyncio.run(server.run())
```

---

## Security Best Practices

### General

1. **Keep all software updated**: Regularly update dependencies
2. **Use strong encryption**: All backups and communications are encrypted
3. **Monitor logs**: Use Grafana dashboards to watch for anomalies
4. **Regular backups**: Automate daily encrypted backups
5. **Test recovery**: Periodically test backup restoration

### Access Control

1. **Limit root access**: Use sudo for privileged operations
2. **Key management**: Keep GPG private keys secure
3. **Certificate security**: Protect TLS private keys
4. **Network segmentation**: Use firewalls to restrict access

### Incident Response

1. **Enable forensic watcher**: Monitor for intrusions
2. **Review alerts**: Check Grafana for security events
3. **Automated responses**: Enable Tor/VPN routing when needed
4. **Log retention**: Keep logs for at least 30 days

---

## Troubleshooting

### Monitoring Stack Issues

```bash
# Check container status
docker-compose -f docker-compose.monitoring.yml ps

# View logs
docker-compose -f docker-compose.monitoring.yml logs grafana
docker-compose -f docker-compose.monitoring.yml logs loki

# Restart services
docker-compose -f docker-compose.monitoring.yml restart
```

### Forensic Watcher Issues

```bash
# Check logs
tail -f /var/log/euystacio/forensic_watcher.log

# Verify Tor is running
systemctl status tor

# Test VPN connection
ping -c 4 8.8.8.8
```

### Backup Issues

```bash
# Check IPFS daemon
ipfs id

# Test GPG encryption
echo "test" | gpg --encrypt --recipient your-email@example.com | gpg --decrypt

# Verify backup integrity
python3 scripts/distributed_backup.py list
```

### QUIC Server Issues

```bash
# Check if port is available
netstat -tuln | grep 4433

# Verify certificate
openssl x509 -in certs/cert.pem -text -noout

# Test connection
python3 scripts/quic_client.py --message ping
```

---

## Support

For issues or questions:

- GitHub Issues: https://github.com/hannesmitterer/Euystacio/issues
- Documentation: https://github.com/hannesmitterer/Euystacio
- Security Issues: security@euystacio.io

---

**Last Updated**: January 2026  
**Version**: 1.0.0
