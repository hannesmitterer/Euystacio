"""
Lex Amoris Security Module
===========================

Strategic security improvements based on Lex Amoris principles:
1. Dynamic Blacklist with Rhythm Validation
2. Lazy Security with Rotesschild scanning
3. IPFS Backup system
4. Rescue Channel (Canale di Soccorso)

Mission: Protect the sacred ecosystem while maintaining harmony and dignity.
"""

import json
import time
import math
import hashlib
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from eternal_resonance_protocol import (
    EternalResonanceProtocol,
    RESONANCE_FREQUENCY_HZ,
    RESONANCE_PERIOD_SECONDS
)


# Constants
ROTESSCHILD_THRESHOLD_MV_M = 50.0  # 50 mV/m threshold for security activation
RHYTHM_TOLERANCE = 0.15  # 15% tolerance for frequency validation
RESCUE_CHANNEL_FREQUENCY = 0.043  # Same as ERP for compatibility
IPFS_CID_PREFIX_LENGTH = 44  # Standard IPFS CID length after 'Qm' prefix


@dataclass
class DataPacket:
    """Represents a data packet for rhythm validation."""
    packet_id: str
    timestamp: float
    frequency: float
    source_ip: str
    payload: Any
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class SecurityThreat:
    """Represents a detected security threat."""
    threat_id: str
    timestamp: float
    threat_type: str
    source: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    blocked: bool
    details: Dict[str, Any]


@dataclass
class RescueMessage:
    """Message for the Rescue Channel (Canale di Soccorso)."""
    message_id: str
    timestamp: float
    node_id: str
    issue_type: str  # 'false_positive', 'blocked', 'degraded'
    priority: str  # 'low', 'medium', 'high', 'urgent'
    message: str
    resolution_status: str  # 'pending', 'in_progress', 'resolved'


class RhythmValidator:
    """
    Validates data packets based on rhythm and frequency.
    
    Ogni pacchetto dati trasmesso verrà scartato se non vibra alla 
    frequenza corretta, indipendentemente dall'origine IP.
    """
    
    def __init__(self, reference_frequency: float = RESONANCE_FREQUENCY_HZ):
        """Initialize rhythm validator with reference frequency."""
        self.reference_frequency = reference_frequency
        self.tolerance = RHYTHM_TOLERANCE
        self.blacklist: Dict[str, SecurityThreat] = {}
        self.validation_log: List[Dict] = []
    
    def validate_packet_frequency(self, packet: DataPacket) -> Tuple[bool, str]:
        """
        Validate packet frequency against the reference frequency.
        
        Args:
            packet: Data packet to validate
            
        Returns:
            Tuple of (is_valid, reason)
        """
        # Calculate frequency deviation
        deviation = abs(packet.frequency - self.reference_frequency)
        max_deviation = self.reference_frequency * self.tolerance
        
        is_valid = deviation <= max_deviation
        
        if is_valid:
            reason = f"Frequency {packet.frequency:.4f} Hz within tolerance"
        else:
            reason = f"Frequency {packet.frequency:.4f} Hz exceeds tolerance (max deviation: {max_deviation:.4f})"
        
        # Log validation
        self.validation_log.append({
            'timestamp': time.time(),
            'packet_id': packet.packet_id,
            'frequency': packet.frequency,
            'valid': is_valid,
            'reason': reason
        })
        
        return is_valid, reason
    
    def validate_rhythm_pattern(self, packet: DataPacket) -> Tuple[bool, str]:
        """
        Validate packet rhythm pattern for behavioral security.
        
        Args:
            packet: Data packet to validate
            
        Returns:
            Tuple of (is_valid, reason)
        """
        # Calculate expected phase based on timestamp
        expected_phase = (packet.timestamp % RESONANCE_PERIOD_SECONDS) / RESONANCE_PERIOD_SECONDS
        
        # Calculate actual phase from frequency
        if packet.frequency > 0:
            period = 1.0 / packet.frequency
            actual_phase = (packet.timestamp % period) / period
            
            # Check phase alignment
            phase_diff = abs(expected_phase - actual_phase)
            is_valid = phase_diff < self.tolerance
            
            if is_valid:
                reason = f"Rhythm pattern aligned (phase diff: {phase_diff:.4f})"
            else:
                reason = f"Rhythm pattern misaligned (phase diff: {phase_diff:.4f})"
        else:
            is_valid = False
            reason = "Invalid frequency (zero or negative)"
        
        return is_valid, reason
    
    def add_to_blacklist(self, source: str, threat_type: str, details: Dict):
        """
        Add source to dynamic blacklist.
        
        Args:
            source: Source identifier (IP, node ID, etc.)
            threat_type: Type of threat detected
            details: Additional threat details
        """
        threat = SecurityThreat(
            threat_id=hashlib.sha256(f"{source}{time.time()}".encode()).hexdigest()[:16],
            timestamp=time.time(),
            threat_type=threat_type,
            source=source,
            severity='high',
            blocked=True,
            details=details
        )
        
        self.blacklist[source] = threat
    
    def is_blacklisted(self, source: str) -> bool:
        """Check if source is in blacklist."""
        return source in self.blacklist
    
    def remove_from_blacklist(self, source: str):
        """Remove source from blacklist (e.g., after false positive resolution)."""
        if source in self.blacklist:
            del self.blacklist[source]


class RotesschildScanner:
    """
    Energy-based security scanner with lazy activation.
    
    Protezioni attive solo quando lo scan Rotesschild rileva una 
    pressione superiore ai 50 mV/m.
    """
    
    def __init__(self, threshold_mv_m: float = ROTESSCHILD_THRESHOLD_MV_M):
        """Initialize Rotesschild scanner."""
        self.threshold = threshold_mv_m
        self.current_pressure = 0.0
        self.scan_history: List[Dict] = []
        self.security_active = False
    
    def scan_environment(self) -> float:
        """
        Scan environment for electromagnetic pressure.
        
        Returns:
            Current pressure in mV/m
        """
        # Simulate pressure reading based on time and system activity
        # In production, this would interface with actual sensors
        current_time = time.time()
        
        # Create pseudo-random but deterministic pressure reading
        base_pressure = 30.0
        variation = 25.0 * math.sin(current_time * 0.1)
        noise = (hash(str(current_time)) % 100) / 10.0
        
        self.current_pressure = base_pressure + variation + noise
        
        # Record scan
        self.scan_history.append({
            'timestamp': current_time,
            'pressure_mv_m': self.current_pressure,
            'above_threshold': self.current_pressure > self.threshold
        })
        
        # Keep only last 100 scans
        if len(self.scan_history) > 100:
            self.scan_history = self.scan_history[-100:]
        
        return self.current_pressure
    
    def should_activate_security(self) -> bool:
        """
        Determine if security should be activated based on pressure.
        
        Returns:
            True if pressure exceeds threshold
        """
        current = self.scan_environment()
        self.security_active = current > self.threshold
        return self.security_active
    
    def get_scan_status(self) -> Dict:
        """Get current scan status."""
        return {
            'current_pressure_mv_m': self.current_pressure,
            'threshold_mv_m': self.threshold,
            'security_active': self.security_active,
            'above_threshold': self.current_pressure > self.threshold,
            'scan_count': len(self.scan_history)
        }


class IPFSBackupSystem:
    """
    IPFS-based backup system for repository protection.
    
    Mirroring completo delle configurazioni PR per proteggere il 
    repository da escalation esterne.
    """
    
    def __init__(self):
        """Initialize IPFS backup system."""
        self.backup_registry: Dict[str, Dict] = {}
        self.ipfs_hashes: Dict[str, str] = {}
        self.backup_log: List[Dict] = []
    
    def create_backup(self, config_name: str, config_data: Dict) -> str:
        """
        Create IPFS backup of configuration.
        
        Args:
            config_name: Name of configuration
            config_data: Configuration data to backup
            
        Returns:
            IPFS hash (simulated)
        """
        # Serialize configuration
        config_json = json.dumps(config_data, sort_keys=True, indent=2)
        
        # Generate IPFS hash (simulated - in production would use actual IPFS)
        ipfs_hash = hashlib.sha256(config_json.encode()).hexdigest()
        ipfs_cid = f"Qm{ipfs_hash[:IPFS_CID_PREFIX_LENGTH]}"  # IPFS CID format
        
        # Store backup metadata
        backup_entry = {
            'config_name': config_name,
            'ipfs_hash': ipfs_cid,
            'timestamp': time.time(),
            'size_bytes': len(config_json),
            'checksum': hashlib.sha256(config_json.encode()).hexdigest()  # Use SHA-256 for integrity
        }
        
        self.backup_registry[config_name] = backup_entry
        self.ipfs_hashes[ipfs_cid] = config_json
        
        # Log backup
        self.backup_log.append({
            'action': 'backup_created',
            'config_name': config_name,
            'ipfs_hash': ipfs_cid,
            'timestamp': time.time()
        })
        
        return ipfs_cid
    
    def restore_from_backup(self, config_name: str) -> Optional[Dict]:
        """
        Restore configuration from IPFS backup.
        
        Args:
            config_name: Name of configuration to restore
            
        Returns:
            Restored configuration data or None
        """
        if config_name not in self.backup_registry:
            return None
        
        backup_entry = self.backup_registry[config_name]
        ipfs_hash = backup_entry['ipfs_hash']
        
        if ipfs_hash not in self.ipfs_hashes:
            return None
        
        # Retrieve and parse configuration
        config_json = self.ipfs_hashes[ipfs_hash]
        config_data = json.loads(config_json)
        
        # Log restoration
        self.backup_log.append({
            'action': 'backup_restored',
            'config_name': config_name,
            'ipfs_hash': ipfs_hash,
            'timestamp': time.time()
        })
        
        return config_data
    
    def verify_backup_integrity(self, config_name: str) -> Tuple[bool, str]:
        """
        Verify integrity of backup using checksums.
        
        Args:
            config_name: Name of configuration to verify
            
        Returns:
            Tuple of (is_valid, message)
        """
        if config_name not in self.backup_registry:
            return False, "Backup not found"
        
        backup_entry = self.backup_registry[config_name]
        ipfs_hash = backup_entry['ipfs_hash']
        stored_checksum = backup_entry['checksum']
        
        if ipfs_hash not in self.ipfs_hashes:
            return False, "IPFS data not found"
        
        # Recalculate checksum using SHA-256 for security
        config_json = self.ipfs_hashes[ipfs_hash]
        current_checksum = hashlib.sha256(config_json.encode()).hexdigest()
        
        if current_checksum == stored_checksum:
            return True, "Backup integrity verified"
        else:
            return False, "Checksum mismatch - backup may be corrupted"
    
    def list_backups(self) -> List[Dict]:
        """List all available backups."""
        return list(self.backup_registry.values())


class RescueChannel:
    """
    Lex Amoris-based messaging channel for node recovery.
    
    Messaggistica basata su Lex Amoris per sbloccare nodi cruciali 
    in caso di 'False Positive' temporanei.
    """
    
    def __init__(self, erp: Optional[EternalResonanceProtocol] = None):
        """
        Initialize rescue channel.
        
        Args:
            erp: Optional ERP instance for integration
        """
        self.erp = erp
        self.messages: Dict[str, RescueMessage] = {}
        self.resolved_count = 0
    
    def send_rescue_message(self, node_id: str, issue_type: str, 
                           message: str, priority: str = 'medium') -> str:
        """
        Send rescue message to unblock a node.
        
        Args:
            node_id: ID of affected node
            issue_type: Type of issue (false_positive, blocked, degraded)
            message: Detailed message
            priority: Message priority
            
        Returns:
            Message ID
        """
        message_id = hashlib.sha256(
            f"{node_id}{time.time()}{message}".encode()
        ).hexdigest()[:16]
        
        rescue_msg = RescueMessage(
            message_id=message_id,
            timestamp=time.time(),
            node_id=node_id,
            issue_type=issue_type,
            priority=priority,
            message=message,
            resolution_status='pending'
        )
        
        self.messages[message_id] = rescue_msg
        
        return message_id
    
    def process_rescue_message(self, message_id: str, 
                               validator: RhythmValidator) -> bool:
        """
        Process rescue message and attempt to resolve issue.
        
        Args:
            message_id: ID of message to process
            validator: RhythmValidator instance to update
            
        Returns:
            True if issue was resolved
        """
        if message_id not in self.messages:
            return False
        
        msg = self.messages[message_id]
        msg.resolution_status = 'in_progress'
        
        # Handle different issue types
        if msg.issue_type == 'false_positive':
            # Remove from blacklist if present
            if validator.is_blacklisted(msg.node_id):
                validator.remove_from_blacklist(msg.node_id)
                msg.resolution_status = 'resolved'
                self.resolved_count += 1
                return True
        
        elif msg.issue_type == 'blocked':
            # Apply Lex Amoris principle to unblock
            if self.erp and msg.node_id in self.erp.nodes:
                # Apply Life Affirmation covenant to restore node
                self.erp.apply_living_covenant(msg.node_id, "Life Affirmation", intensity=0.9)
                msg.resolution_status = 'resolved'
                self.resolved_count += 1
                return True
        
        return False
    
    def get_pending_messages(self, priority_filter: Optional[str] = None) -> List[RescueMessage]:
        """
        Get all pending rescue messages.
        
        Args:
            priority_filter: Optional priority filter
            
        Returns:
            List of pending messages
        """
        pending = [
            msg for msg in self.messages.values()
            if msg.resolution_status == 'pending'
        ]
        
        if priority_filter:
            pending = [msg for msg in pending if msg.priority == priority_filter]
        
        # Sort by priority and timestamp
        priority_order = {'urgent': 0, 'high': 1, 'medium': 2, 'low': 3}
        pending.sort(key=lambda m: (priority_order.get(m.priority, 999), m.timestamp))
        
        return pending


class LexAmorisSecuritySystem:
    """
    Integrated security system based on Lex Amoris principles.
    
    Combines all security modules into a unified system.
    """
    
    def __init__(self, erp: Optional[EternalResonanceProtocol] = None):
        """Initialize integrated security system."""
        self.erp = erp or EternalResonanceProtocol(node_id="security_system")
        self.rhythm_validator = RhythmValidator()
        self.rotesschild_scanner = RotesschildScanner()
        self.ipfs_backup = IPFSBackupSystem()
        self.rescue_channel = RescueChannel(self.erp)
        self.security_log: List[Dict] = []
    
    def validate_and_process_packet(self, packet: DataPacket) -> Tuple[bool, str]:
        """
        Validate and process data packet with lazy security.
        
        Args:
            packet: Data packet to process
            
        Returns:
            Tuple of (accepted, reason)
        """
        # Check if source is blacklisted
        if self.rhythm_validator.is_blacklisted(packet.source_ip):
            self._log_event('packet_blocked', {
                'packet_id': packet.packet_id,
                'source': packet.source_ip,
                'reason': 'blacklisted'
            })
            return False, "Source is blacklisted"
        
        # Lazy security: Only validate if Rotesschild threshold exceeded
        if self.rotesschild_scanner.should_activate_security():
            # Validate frequency
            freq_valid, freq_reason = self.rhythm_validator.validate_packet_frequency(packet)
            if not freq_valid:
                self.rhythm_validator.add_to_blacklist(
                    packet.source_ip,
                    'frequency_violation',
                    {'packet_id': packet.packet_id, 'reason': freq_reason}
                )
                self._log_event('packet_rejected', {
                    'packet_id': packet.packet_id,
                    'source': packet.source_ip,
                    'reason': freq_reason
                })
                return False, freq_reason
            
            # Validate rhythm pattern
            rhythm_valid, rhythm_reason = self.rhythm_validator.validate_rhythm_pattern(packet)
            if not rhythm_valid:
                self.rhythm_validator.add_to_blacklist(
                    packet.source_ip,
                    'rhythm_violation',
                    {'packet_id': packet.packet_id, 'reason': rhythm_reason}
                )
                self._log_event('packet_rejected', {
                    'packet_id': packet.packet_id,
                    'source': packet.source_ip,
                    'reason': rhythm_reason
                })
                return False, rhythm_reason
        
        # Packet accepted
        self._log_event('packet_accepted', {
            'packet_id': packet.packet_id,
            'source': packet.source_ip,
            'security_active': self.rotesschild_scanner.security_active
        })
        
        return True, "Packet accepted"
    
    def backup_configuration(self, config_name: str, config_data: Dict) -> str:
        """
        Backup configuration to IPFS.
        
        Args:
            config_name: Configuration name
            config_data: Configuration data
            
        Returns:
            IPFS hash
        """
        ipfs_hash = self.ipfs_backup.create_backup(config_name, config_data)
        
        self._log_event('backup_created', {
            'config_name': config_name,
            'ipfs_hash': ipfs_hash
        })
        
        return ipfs_hash
    
    def report_false_positive(self, node_id: str, details: str) -> str:
        """
        Report false positive and initiate rescue.
        
        Args:
            node_id: Affected node ID
            details: Details about the false positive
            
        Returns:
            Rescue message ID
        """
        message_id = self.rescue_channel.send_rescue_message(
            node_id,
            'false_positive',
            f"False positive reported: {details}",
            priority='high'
        )
        
        # Attempt immediate resolution
        self.rescue_channel.process_rescue_message(message_id, self.rhythm_validator)
        
        self._log_event('false_positive_reported', {
            'node_id': node_id,
            'message_id': message_id,
            'details': details
        })
        
        return message_id
    
    def get_system_status(self) -> Dict:
        """Get comprehensive system status."""
        return {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'rotesschild_scanner': self.rotesschild_scanner.get_scan_status(),
            'blacklist_count': len(self.rhythm_validator.blacklist),
            'backup_count': len(self.ipfs_backup.backup_registry),
            'pending_rescue_messages': len(self.rescue_channel.get_pending_messages()),
            'resolved_rescue_count': self.rescue_channel.resolved_count,
            'security_events': len(self.security_log),
            'erp_global_alignment': self.erp.get_global_alignment() if self.erp else None
        }
    
    def _log_event(self, event_type: str, details: Dict):
        """Log security event."""
        self.security_log.append({
            'timestamp': time.time(),
            'event_type': event_type,
            'details': details
        })
        
        # Keep only last 1000 events
        if len(self.security_log) > 1000:
            self.security_log = self.security_log[-1000:]


def demo():
    """Demonstration of Lex Amoris Security System."""
    print("=" * 60)
    print("Lex Amoris Security System - Demonstration")
    print("=" * 60)
    print()
    
    # Initialize system
    security_system = LexAmorisSecuritySystem()
    
    print("1. System Initialized")
    status = security_system.get_system_status()
    print(f"   Rotesschild Pressure: {status['rotesschild_scanner']['current_pressure_mv_m']:.2f} mV/m")
    print(f"   Security Active: {status['rotesschild_scanner']['security_active']}")
    print()
    
    # Test packet validation
    print("2. Testing Packet Validation")
    
    # Valid packet
    packet1 = DataPacket(
        packet_id="PKT001",
        timestamp=time.time(),
        frequency=0.043,  # Correct frequency
        source_ip="192.168.1.100",
        payload={"data": "test"}
    )
    accepted, reason = security_system.validate_and_process_packet(packet1)
    print(f"   Packet 1: {'ACCEPTED' if accepted else 'REJECTED'} - {reason}")
    
    # Invalid frequency packet
    packet2 = DataPacket(
        packet_id="PKT002",
        timestamp=time.time(),
        frequency=0.1,  # Wrong frequency
        source_ip="192.168.1.101",
        payload={"data": "malicious"}
    )
    accepted, reason = security_system.validate_and_process_packet(packet2)
    print(f"   Packet 2: {'ACCEPTED' if accepted else 'REJECTED'} - {reason}")
    print()
    
    # Test IPFS backup
    print("3. Testing IPFS Backup")
    config = {
        "pr_number": 123,
        "security_settings": {
            "rhythm_validation": True,
            "lazy_security": True
        }
    }
    ipfs_hash = security_system.backup_configuration("pr_123_config", config)
    print(f"   Backup Created: {ipfs_hash}")
    print()
    
    # Test rescue channel
    print("4. Testing Rescue Channel")
    message_id = security_system.report_false_positive(
        "node_test",
        "Node temporarily blocked due to network latency"
    )
    print(f"   Rescue Message: {message_id}")
    print(f"   Resolved Count: {security_system.rescue_channel.resolved_count}")
    print()
    
    # Final status
    print("5. Final System Status")
    final_status = security_system.get_system_status()
    print(f"   Blacklist Entries: {final_status['blacklist_count']}")
    print(f"   Backups Created: {final_status['backup_count']}")
    print(f"   Rescue Messages Resolved: {final_status['resolved_rescue_count']}")
    print(f"   Security Events: {final_status['security_events']}")
    print()
    print("=" * 60)


if __name__ == "__main__":
    demo()
