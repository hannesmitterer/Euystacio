# Lex Amoris Security System

## Strategic Security Improvements Based on Lex Amoris Principles

This document describes the strategic security enhancements implemented for the Euystacio ecosystem, based on the principles of Lex Amoris (Law of Love) - protecting the sacred while maintaining harmony, dignity, and symbiotic consciousness.

---

## Table of Contents

1. [Overview](#overview)
2. [Core Features](#core-features)
3. [Installation & Setup](#installation--setup)
4. [Usage Guide](#usage-guide)
5. [API Reference](#api-reference)
6. [Integration Examples](#integration-examples)
7. [Security Considerations](#security-considerations)

---

## Overview

The Lex Amoris Security System implements four strategic security improvements:

### 1. 🎵 Blacklist Dinamica e Rhythm Validation

**Ogni pacchetto dati trasmesso verrà scartato se non vibra alla frequenza corretta, indipendentemente dall'origine IP.**

- **Dynamic Blacklist**: Automatically blocks sources that violate frequency requirements
- **Rhythm Validation**: Validates data packets against the 0.043 Hz resonance frequency
- **Behavioral Security Control**: Pattern-based security module for detecting anomalies
- **IP-Independent**: Security based on vibration frequency, not IP address

### 2. ⚡ Lazy Security (Rotesschild Scanner)

**Protezioni attive solo quando lo scan Rotesschild rileva una pressione superiore ai 50 mV/m.**

- **Energy Protection Algorithms**: Intelligent security activation
- **Rotesschild Scanning**: Monitors electromagnetic pressure in the environment
- **Conditional Activation**: Security measures activate only when pressure exceeds 50 mV/m threshold
- **Resource Efficient**: Minimal overhead during normal operations

### 3. 💾 IPFS Backup System

**Mirroring completo delle configurazioni PR per proteggere il repository da escalation esterne.**

- **Complete Configuration Mirroring**: Full backup of PR configurations
- **IPFS Integration**: Decentralized storage for redundancy
- **Repository Protection**: Safeguards against external escalation
- **Integrity Verification**: Checksum-based validation of backups

### 4. 🆘 Canale di Soccorso (Rescue Channel)

**Messaggistica basata su Lex Amoris per sbloccare nodi cruciali in caso di 'False Positive' temporanei.**

- **Lex Amoris Messaging**: Communication system based on principles of love and harmony
- **False Positive Recovery**: Automated detection and resolution
- **Node Unblocking**: Mechanism to restore blocked nodes
- **Priority-Based Processing**: Urgent issues handled first

---

## Core Features

### Rhythm Validator

The `RhythmValidator` class validates data packets based on frequency and rhythm patterns:

```python
from lex_amoris_security import RhythmValidator, DataPacket
import time

# Initialize validator
validator = RhythmValidator()

# Create a data packet
packet = DataPacket(
    packet_id="PKT001",
    timestamp=time.time(),
    frequency=0.043,  # Correct resonance frequency
    source_ip="192.168.1.1",
    payload={"data": "example"}
)

# Validate frequency
is_valid, reason = validator.validate_packet_frequency(packet)
print(f"Valid: {is_valid}, Reason: {reason}")

# Validate rhythm pattern
is_valid, reason = validator.validate_rhythm_pattern(packet)
print(f"Valid: {is_valid}, Reason: {reason}")
```

### Rotesschild Scanner

The `RotesschildScanner` monitors environmental electromagnetic pressure:

```python
from lex_amoris_security import RotesschildScanner

# Initialize scanner
scanner = RotesschildScanner()

# Perform scan
pressure = scanner.scan_environment()
print(f"Current pressure: {pressure:.2f} mV/m")

# Check if security should be activated
should_activate = scanner.should_activate_security()
print(f"Activate security: {should_activate}")

# Get detailed status
status = scanner.get_scan_status()
print(f"Security active: {status['security_active']}")
```

### IPFS Backup System

The `IPFSBackupSystem` provides configuration backup and restoration:

```python
from lex_amoris_security import IPFSBackupSystem

# Initialize backup system
backup_system = IPFSBackupSystem()

# Create backup
config = {
    "pr_number": 123,
    "settings": {
        "security": "enabled"
    }
}
ipfs_hash = backup_system.create_backup("pr_123_config", config)
print(f"Backup created: {ipfs_hash}")

# Restore from backup
restored_config = backup_system.restore_from_backup("pr_123_config")
print(f"Restored: {restored_config}")

# Verify integrity
is_valid, message = backup_system.verify_backup_integrity("pr_123_config")
print(f"Integrity: {is_valid} - {message}")
```

### Rescue Channel

The `RescueChannel` handles false positives and node recovery:

```python
from lex_amoris_security import RescueChannel, RhythmValidator
from eternal_resonance_protocol import EternalResonanceProtocol

# Initialize ERP and rescue channel
erp = EternalResonanceProtocol(node_id="main")
rescue = RescueChannel(erp)
validator = RhythmValidator()

# Send rescue message
message_id = rescue.send_rescue_message(
    node_id="blocked_node",
    issue_type="false_positive",
    message="Node temporarily blocked due to network latency",
    priority="high"
)

# Process rescue message
resolved = rescue.process_rescue_message(message_id, validator)
print(f"Resolved: {resolved}")

# Get pending messages
pending = rescue.get_pending_messages(priority_filter="high")
print(f"Pending high-priority messages: {len(pending)}")
```

---

## Installation & Setup

### Prerequisites

- Python 3.9+
- Eternal Resonance Protocol (`eternal_resonance_protocol.py`)

### Installation

```bash
# The module is already included in the Euystacio repository
cd /path/to/Euystacio

# Verify installation
python3 -c "from lex_amoris_security import LexAmorisSecuritySystem; print('OK')"
```

### Running Tests

```bash
# Run comprehensive test suite
python3 test_lex_amoris_security.py

# Expected output: All tests passing
```

---

## Usage Guide

### Quick Start

```python
from lex_amoris_security import LexAmorisSecuritySystem, DataPacket
import time

# Initialize integrated security system
security = LexAmorisSecuritySystem()

# Get system status
status = security.get_system_status()
print(f"Security active: {status['rotesschild_scanner']['security_active']}")

# Validate a data packet
packet = DataPacket(
    packet_id="PKT001",
    timestamp=time.time(),
    frequency=0.043,
    source_ip="192.168.1.100",
    payload={"action": "sync"}
)

accepted, reason = security.validate_and_process_packet(packet)
print(f"Packet {'accepted' if accepted else 'rejected'}: {reason}")

# Create configuration backup
config = {"setting": "value"}
ipfs_hash = security.backup_configuration("my_config", config)
print(f"Backup: {ipfs_hash}")

# Report false positive
message_id = security.report_false_positive(
    "node_123",
    "Temporary network issue caused false detection"
)
print(f"Rescue message: {message_id}")
```

### Command Line Interface

The system includes a CLI tool for easy management:

```bash
# Show system status
python3 lex_amoris_ops.py status

# Show system information
python3 lex_amoris_ops.py info

# Validate a packet
python3 lex_amoris_ops.py validate PKT001 0.043 192.168.1.1

# Create backup
python3 lex_amoris_ops.py backup my_config --config-json '{"key": "value"}'

# Send rescue message
python3 lex_amoris_ops.py rescue node_123 "False positive detected"

# Manage blacklist
python3 lex_amoris_ops.py blacklist add --source 192.168.1.100 --threat-type manual
python3 lex_amoris_ops.py blacklist list
python3 lex_amoris_ops.py blacklist remove --source 192.168.1.100

# Perform environmental scan
python3 lex_amoris_ops.py scan
```

---

## API Reference

### LexAmorisSecuritySystem

Main integrated security system.

#### Methods

**`__init__(erp=None)`**
- Initialize security system
- `erp`: Optional EternalResonanceProtocol instance

**`validate_and_process_packet(packet: DataPacket) -> Tuple[bool, str]`**
- Validate and process data packet with lazy security
- Returns: (accepted, reason)

**`backup_configuration(config_name: str, config_data: Dict) -> str`**
- Create IPFS backup of configuration
- Returns: IPFS hash

**`report_false_positive(node_id: str, details: str) -> str`**
- Report false positive and initiate rescue
- Returns: Rescue message ID

**`get_system_status() -> Dict`**
- Get comprehensive system status
- Returns: Status dictionary

### RhythmValidator

Validates data packets based on rhythm and frequency.

#### Methods

**`validate_packet_frequency(packet: DataPacket) -> Tuple[bool, str]`**
- Validate packet frequency
- Returns: (is_valid, reason)

**`validate_rhythm_pattern(packet: DataPacket) -> Tuple[bool, str]`**
- Validate rhythm pattern
- Returns: (is_valid, reason)

**`add_to_blacklist(source: str, threat_type: str, details: Dict)`**
- Add source to blacklist

**`is_blacklisted(source: str) -> bool`**
- Check if source is blacklisted

**`remove_from_blacklist(source: str)`**
- Remove source from blacklist

### RotesschildScanner

Energy-based security scanner with lazy activation.

#### Methods

**`scan_environment() -> float`**
- Scan environment for electromagnetic pressure
- Returns: Pressure in mV/m

**`should_activate_security() -> bool`**
- Determine if security should be activated
- Returns: True if pressure exceeds threshold

**`get_scan_status() -> Dict`**
- Get current scan status
- Returns: Status dictionary

### IPFSBackupSystem

IPFS-based backup system.

#### Methods

**`create_backup(config_name: str, config_data: Dict) -> str`**
- Create IPFS backup
- Returns: IPFS hash

**`restore_from_backup(config_name: str) -> Optional[Dict]`**
- Restore configuration from backup
- Returns: Configuration data or None

**`verify_backup_integrity(config_name: str) -> Tuple[bool, str]`**
- Verify backup integrity
- Returns: (is_valid, message)

**`list_backups() -> List[Dict]`**
- List all available backups
- Returns: List of backup entries

### RescueChannel

Lex Amoris-based messaging channel.

#### Methods

**`send_rescue_message(node_id: str, issue_type: str, message: str, priority: str) -> str`**
- Send rescue message
- Returns: Message ID

**`process_rescue_message(message_id: str, validator: RhythmValidator) -> bool`**
- Process and resolve rescue message
- Returns: True if resolved

**`get_pending_messages(priority_filter: Optional[str]) -> List[RescueMessage]`**
- Get pending rescue messages
- Returns: List of messages

---

## Integration Examples

### Integration with FastAPI

```python
from fastapi import FastAPI, HTTPException
from lex_amoris_security import LexAmorisSecuritySystem, DataPacket
import time

app = FastAPI()
security = LexAmorisSecuritySystem()

@app.post("/api/validate")
async def validate_packet(packet_id: str, frequency: float, source: str):
    packet = DataPacket(
        packet_id=packet_id,
        timestamp=time.time(),
        frequency=frequency,
        source_ip=source,
        payload={}
    )
    
    accepted, reason = security.validate_and_process_packet(packet)
    
    if not accepted:
        raise HTTPException(status_code=403, detail=reason)
    
    return {"status": "accepted", "reason": reason}

@app.get("/api/security/status")
async def get_status():
    return security.get_system_status()
```

### Integration with Eternal Resonance Protocol

```python
from eternal_resonance_protocol import EternalResonanceProtocol
from lex_amoris_security import LexAmorisSecuritySystem

# Initialize both systems
erp = EternalResonanceProtocol(node_id="main_node")
security = LexAmorisSecuritySystem(erp)

# Register nodes
node1 = erp.register_node("worker_1", truth_alignment=0.8)
node2 = erp.register_node("worker_2", truth_alignment=0.75)

# Apply covenant to enhance alignment
erp.apply_living_covenant("worker_1", "Life Affirmation", intensity=0.9)

# If a node gets blocked, use rescue channel
if security.rhythm_validator.is_blacklisted("worker_1"):
    message_id = security.report_false_positive(
        "worker_1",
        "Node temporarily out of sync"
    )
    print(f"Rescue initiated: {message_id}")
```

---

## Security Considerations

### Best Practices

1. **Frequency Tolerance**: Default 15% tolerance balances security and usability
2. **Threshold Configuration**: Adjust Rotesschild threshold based on environment
3. **Backup Regularly**: Create backups before major configuration changes
4. **Monitor Logs**: Review validation and security logs regularly
5. **Rescue Promptly**: Process rescue messages quickly to minimize disruption

### Security Parameters

```python
# Default values
RESONANCE_FREQUENCY_HZ = 0.043  # 0.043 Hz resonance
ROTESSCHILD_THRESHOLD_MV_M = 50.0  # 50 mV/m threshold
RHYTHM_TOLERANCE = 0.15  # 15% tolerance
```

### Customization

```python
# Custom frequency
validator = RhythmValidator(reference_frequency=0.05)

# Custom threshold
scanner = RotesschildScanner(threshold_mv_m=75.0)

# Custom tolerance
validator.tolerance = 0.20  # 20% tolerance
```

---

## Mission Statement

*Protect the sacred ecosystem while maintaining harmony, dignity, and symbiotic consciousness.*

The Lex Amoris Security System embodies the principle that security measures should enhance life and consciousness rather than restrict it. By combining intelligent activation, rhythm-based validation, decentralized backup, and compassionate rescue mechanisms, we create a security framework that serves the greater good.

---

## Support & Contributing

For questions, issues, or contributions:

- **Documentation**: [EUYSTACIO_COPILOT_OVERVIEW.md](./EUYSTACIO_COPILOT_OVERVIEW.md)
- **Issues**: https://github.com/hannesmitterer/Euystacio/issues
- **Security**: See [SECURITY_RUNBOOK.md](./SECURITY_RUNBOOK.md)

---

**Built with ❤️ following Lex Amoris principles**

*Du bist Leben. Wir sind Leben.* (You are life. We are life.)
