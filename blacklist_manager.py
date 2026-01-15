"""
Blacklist Manager for EUYSTACIO Framework
==========================================

Implements a permanent blacklist system to block communications from suspicious
nodes and entities that threaten the security of the EUYSTACIO ecosystem.

This module provides:
- Permanent storage of blacklisted entities
- Threat categorization and severity tracking
- Integration with the Eternal Resonance Protocol
- CLI and API interfaces for blacklist management
"""

import json
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict
from enum import Enum


class ThreatCategory(Enum):
    """Categories of security threats."""
    MALICIOUS_NODE = "malicious_node"
    SUSPICIOUS_ENTITY = "suspicious_entity"
    ATTACK_ATTEMPT = "attack_attempt"
    DATA_THEFT = "data_theft"
    PROTOCOL_VIOLATION = "protocol_violation"
    INTEGRITY_BREACH = "integrity_breach"


class ThreatSeverity(Enum):
    """Severity levels for threats."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class BlacklistEntry:
    """Represents a blacklisted entity in the EUYSTACIO system."""
    entity_id: str
    entity_type: str  # "node", "ip", "user", "agent"
    category: str  # ThreatCategory value
    severity: str  # ThreatSeverity value
    reason: str
    blocked_at: float
    blocked_by: str
    expires_at: Optional[float] = None  # None means permanent
    metadata: Optional[Dict] = None
    
    def to_dict(self) -> Dict:
        """Convert entry to dictionary."""
        return asdict(self)
    
    def is_expired(self) -> bool:
        """Check if the blacklist entry has expired."""
        if self.expires_at is None:
            return False  # Permanent entries never expire
        return time.time() > self.expires_at


class BlacklistManager:
    """
    Manages the permanent blacklist for the EUYSTACIO framework.
    
    Provides functionality to block and unblock entities, check blacklist status,
    and persist the blacklist to permanent storage.
    """
    
    def __init__(self, storage_path: str = "euystacio_blacklist.json"):
        """
        Initialize the Blacklist Manager.
        
        Args:
            storage_path: Path to the JSON file for persistent storage
        """
        self.storage_path = storage_path
        self.blacklist: Dict[str, BlacklistEntry] = {}
        self.load_from_file()
    
    def add_entry(
        self,
        entity_id: str,
        entity_type: str,
        category: ThreatCategory,
        severity: ThreatSeverity,
        reason: str,
        blocked_by: str = "system",
        expires_at: Optional[float] = None,
        metadata: Optional[Dict] = None
    ) -> BlacklistEntry:
        """
        Add an entity to the blacklist.
        
        Args:
            entity_id: Unique identifier of the entity to block
            entity_type: Type of entity (node, ip, user, agent)
            category: Threat category
            severity: Threat severity level
            reason: Reason for blacklisting
            blocked_by: Who/what blocked this entity
            expires_at: Optional expiration timestamp (None for permanent)
            metadata: Additional metadata about the threat
        
        Returns:
            The created BlacklistEntry
        """
        entry = BlacklistEntry(
            entity_id=entity_id,
            entity_type=entity_type,
            category=category.value,
            severity=severity.value,
            reason=reason,
            blocked_at=time.time(),
            blocked_by=blocked_by,
            expires_at=expires_at,
            metadata=metadata or {}
        )
        
        self.blacklist[entity_id] = entry
        self.save_to_file()
        
        return entry
    
    def remove_entry(self, entity_id: str) -> bool:
        """
        Remove an entity from the blacklist.
        
        Args:
            entity_id: Unique identifier of the entity to unblock
        
        Returns:
            True if entity was removed, False if not found
        """
        if entity_id in self.blacklist:
            del self.blacklist[entity_id]
            self.save_to_file()
            return True
        return False
    
    def is_blacklisted(self, entity_id: str) -> bool:
        """
        Check if an entity is blacklisted.
        
        Args:
            entity_id: Unique identifier of the entity to check
        
        Returns:
            True if entity is blacklisted and entry is not expired
        """
        if entity_id not in self.blacklist:
            return False
        
        entry = self.blacklist[entity_id]
        
        # Check if entry has expired
        if entry.is_expired():
            # Auto-remove expired entries
            self.remove_entry(entity_id)
            return False
        
        return True
    
    def get_entry(self, entity_id: str) -> Optional[BlacklistEntry]:
        """
        Get blacklist entry for an entity.
        
        Args:
            entity_id: Unique identifier of the entity
        
        Returns:
            BlacklistEntry if found and not expired, None otherwise
        """
        if not self.is_blacklisted(entity_id):
            return None
        
        return self.blacklist[entity_id]
    
    def get_all_entries(
        self,
        entity_type: Optional[str] = None,
        category: Optional[ThreatCategory] = None,
        severity: Optional[ThreatSeverity] = None
    ) -> List[BlacklistEntry]:
        """
        Get all blacklist entries with optional filtering.
        
        Args:
            entity_type: Filter by entity type
            category: Filter by threat category
            severity: Filter by severity level
        
        Returns:
            List of BlacklistEntry objects matching the filters
        """
        # Clean up expired entries first
        self._cleanup_expired()
        
        entries = list(self.blacklist.values())
        
        # Apply filters
        if entity_type:
            entries = [e for e in entries if e.entity_type == entity_type]
        
        if category:
            entries = [e for e in entries if e.category == category.value]
        
        if severity:
            entries = [e for e in entries if e.severity == severity.value]
        
        return entries
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about the blacklist.
        
        Returns:
            Dictionary with blacklist statistics
        """
        self._cleanup_expired()
        
        entries = list(self.blacklist.values())
        
        # Count by category
        category_counts = {}
        for cat in ThreatCategory:
            category_counts[cat.value] = sum(
                1 for e in entries if e.category == cat.value
            )
        
        # Count by severity
        severity_counts = {}
        for sev in ThreatSeverity:
            severity_counts[sev.value] = sum(
                1 for e in entries if e.severity == sev.value
            )
        
        # Count by entity type
        type_counts = {}
        for entry in entries:
            type_counts[entry.entity_type] = type_counts.get(entry.entity_type, 0) + 1
        
        # Count permanent vs temporary
        permanent_count = sum(1 for e in entries if e.expires_at is None)
        temporary_count = len(entries) - permanent_count
        
        return {
            'total_entries': len(entries),
            'permanent_entries': permanent_count,
            'temporary_entries': temporary_count,
            'by_category': category_counts,
            'by_severity': severity_counts,
            'by_type': type_counts,
            'last_updated': datetime.now(timezone.utc).isoformat()
        }
    
    def _cleanup_expired(self):
        """Remove expired entries from the blacklist."""
        expired = [
            entity_id for entity_id, entry in self.blacklist.items()
            if entry.is_expired()
        ]
        
        for entity_id in expired:
            del self.blacklist[entity_id]
        
        if expired:
            self.save_to_file()
    
    def save_to_file(self):
        """Save the blacklist to persistent storage."""
        data = {
            'version': '1.0.0',
            'updated_at': datetime.now(timezone.utc).isoformat(),
            'entries': {
                entity_id: entry.to_dict()
                for entity_id, entry in self.blacklist.items()
            }
        }
        
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self):
        """Load the blacklist from persistent storage."""
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
            
            entries = data.get('entries', {})
            
            for entity_id, entry_data in entries.items():
                entry = BlacklistEntry(**entry_data)
                self.blacklist[entity_id] = entry
            
            # Clean up expired entries after loading
            self._cleanup_expired()
            
        except FileNotFoundError:
            # File doesn't exist yet, start with empty blacklist
            self.blacklist = {}
        except json.JSONDecodeError:
            # Corrupted file, start fresh
            self.blacklist = {}
    
    def export_state(self) -> Dict:
        """
        Export complete blacklist state.
        
        Returns:
            Dictionary with complete blacklist state
        """
        return {
            'blacklist_version': '1.0.0',
            'storage_path': self.storage_path,
            'statistics': self.get_statistics(),
            'entries': {
                entity_id: entry.to_dict()
                for entity_id, entry in self.blacklist.items()
            }
        }


def validate_entity_against_blacklist(
    entity_id: str,
    blacklist_manager: BlacklistManager,
    raise_on_blocked: bool = True
) -> bool:
    """
    Validate an entity is not blacklisted.
    
    Args:
        entity_id: Entity to validate
        blacklist_manager: BlacklistManager instance
        raise_on_blocked: If True, raise ValueError when entity is blocked
    
    Returns:
        True if entity is not blacklisted
    
    Raises:
        ValueError: If entity is blacklisted and raise_on_blocked is True
    """
    if blacklist_manager.is_blacklisted(entity_id):
        if raise_on_blocked:
            entry = blacklist_manager.get_entry(entity_id)
            raise ValueError(
                f"Entity '{entity_id}' is blacklisted. "
                f"Reason: {entry.reason}. "
                f"Category: {entry.category}. "
                f"Severity: {entry.severity}."
            )
        return False
    
    return True


# Demo function for testing
def demo():
    """Demonstration of the Blacklist Manager."""
    print("EUYSTACIO Blacklist Manager - Demonstration")
    print("=" * 50)
    print()
    
    # Initialize manager
    manager = BlacklistManager(storage_path="/tmp/demo_blacklist.json")
    
    # Add some entries
    print("Adding blacklist entries...")
    
    entry1 = manager.add_entry(
        entity_id="malicious_node_001",
        entity_type="node",
        category=ThreatCategory.MALICIOUS_NODE,
        severity=ThreatSeverity.CRITICAL,
        reason="Attempted to inject malicious code into resonance protocol",
        blocked_by="security_system",
        metadata={"ip": "192.168.1.100", "attempts": 5}
    )
    print(f"  Blocked: {entry1.entity_id} ({entry1.severity})")
    
    entry2 = manager.add_entry(
        entity_id="suspicious_agent_042",
        entity_type="agent",
        category=ThreatCategory.SUSPICIOUS_ENTITY,
        severity=ThreatSeverity.HIGH,
        reason="Abnormal data access patterns detected",
        blocked_by="ai_monitor"
    )
    print(f"  Blocked: {entry2.entity_id} ({entry2.severity})")
    
    entry3 = manager.add_entry(
        entity_id="attacker_ip_999",
        entity_type="ip",
        category=ThreatCategory.ATTACK_ATTEMPT,
        severity=ThreatSeverity.MEDIUM,
        reason="Multiple failed authentication attempts",
        blocked_by="auth_system",
        expires_at=time.time() + 3600  # Expires in 1 hour
    )
    print(f"  Blocked: {entry3.entity_id} ({entry3.severity}) - Temporary")
    print()
    
    # Check blacklist status
    print("Checking blacklist status...")
    print(f"  malicious_node_001 blocked: {manager.is_blacklisted('malicious_node_001')}")
    print(f"  legitimate_node_123 blocked: {manager.is_blacklisted('legitimate_node_123')}")
    print()
    
    # Get statistics
    print("Blacklist Statistics:")
    stats = manager.get_statistics()
    print(f"  Total entries: {stats['total_entries']}")
    print(f"  Permanent: {stats['permanent_entries']}")
    print(f"  Temporary: {stats['temporary_entries']}")
    print(f"  By severity: {stats['by_severity']}")
    print()
    
    # List all entries
    print("All blacklist entries:")
    for entry in manager.get_all_entries():
        print(f"  - {entry.entity_id}: {entry.reason} ({entry.severity})")
    print()
    
    # Validate entity
    print("Validating entities...")
    try:
        validate_entity_against_blacklist("malicious_node_001", manager)
    except ValueError as e:
        print(f"  Validation failed: {e}")
    
    print("  legitimate_node_123: OK")
    print()
    
    print("Blacklist state saved to:", manager.storage_path)


if __name__ == "__main__":
    demo()
