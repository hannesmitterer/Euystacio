#!/usr/bin/env python3
"""
Blacklist Manager - Test Suite

Comprehensive tests for the blacklist manager and its integration with the
Eternal Resonance Protocol.
"""

import unittest
import json
import time
import os
import tempfile
from blacklist_manager import (
    BlacklistManager,
    BlacklistEntry,
    ThreatCategory,
    ThreatSeverity,
    validate_entity_against_blacklist
)


class TestBlacklistEntry(unittest.TestCase):
    """Test BlacklistEntry data class."""
    
    def test_entry_creation(self):
        """Test entry creation with valid parameters."""
        entry = BlacklistEntry(
            entity_id="test_node_001",
            entity_type="node",
            category=ThreatCategory.MALICIOUS_NODE.value,
            severity=ThreatSeverity.HIGH.value,
            reason="Test reason",
            blocked_at=time.time(),
            blocked_by="test_system"
        )
        
        self.assertEqual(entry.entity_id, "test_node_001")
        self.assertEqual(entry.entity_type, "node")
        self.assertEqual(entry.category, ThreatCategory.MALICIOUS_NODE.value)
        self.assertEqual(entry.severity, ThreatSeverity.HIGH.value)
    
    def test_entry_to_dict(self):
        """Test entry serialization."""
        entry = BlacklistEntry(
            entity_id="test_node_001",
            entity_type="node",
            category=ThreatCategory.MALICIOUS_NODE.value,
            severity=ThreatSeverity.HIGH.value,
            reason="Test reason",
            blocked_at=time.time(),
            blocked_by="test_system"
        )
        
        entry_dict = entry.to_dict()
        self.assertIsInstance(entry_dict, dict)
        self.assertEqual(entry_dict['entity_id'], "test_node_001")
    
    def test_entry_expiration(self):
        """Test entry expiration logic."""
        # Permanent entry
        permanent = BlacklistEntry(
            entity_id="permanent_node",
            entity_type="node",
            category=ThreatCategory.MALICIOUS_NODE.value,
            severity=ThreatSeverity.CRITICAL.value,
            reason="Permanent ban",
            blocked_at=time.time(),
            blocked_by="admin",
            expires_at=None
        )
        self.assertFalse(permanent.is_expired())
        
        # Expired entry
        expired = BlacklistEntry(
            entity_id="temp_node",
            entity_type="node",
            category=ThreatCategory.SUSPICIOUS_ENTITY.value,
            severity=ThreatSeverity.LOW.value,
            reason="Temporary ban",
            blocked_at=time.time() - 1000,
            blocked_by="system",
            expires_at=time.time() - 500
        )
        self.assertTrue(expired.is_expired())
        
        # Not expired entry
        not_expired = BlacklistEntry(
            entity_id="future_node",
            entity_type="node",
            category=ThreatCategory.SUSPICIOUS_ENTITY.value,
            severity=ThreatSeverity.LOW.value,
            reason="Future expiration",
            blocked_at=time.time(),
            blocked_by="system",
            expires_at=time.time() + 1000
        )
        self.assertFalse(not_expired.is_expired())


class TestBlacklistManager(unittest.TestCase):
    """Test BlacklistManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary file for testing
        self.temp_fd, self.temp_path = tempfile.mkstemp(suffix='.json')
        os.close(self.temp_fd)
        self.manager = BlacklistManager(storage_path=self.temp_path)
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_path):
            os.remove(self.temp_path)
    
    def test_initialization(self):
        """Test manager initialization."""
        self.assertEqual(self.manager.storage_path, self.temp_path)
        self.assertEqual(len(self.manager.blacklist), 0)
    
    def test_add_entry(self):
        """Test adding an entry to the blacklist."""
        entry = self.manager.add_entry(
            entity_id="malicious_node",
            entity_type="node",
            category=ThreatCategory.MALICIOUS_NODE,
            severity=ThreatSeverity.HIGH,
            reason="Test malicious activity",
            blocked_by="test_admin"
        )
        
        self.assertEqual(entry.entity_id, "malicious_node")
        self.assertEqual(len(self.manager.blacklist), 1)
        self.assertIn("malicious_node", self.manager.blacklist)
    
    def test_remove_entry(self):
        """Test removing an entry from the blacklist."""
        # Add entry
        self.manager.add_entry(
            entity_id="temp_node",
            entity_type="node",
            category=ThreatCategory.SUSPICIOUS_ENTITY,
            severity=ThreatSeverity.MEDIUM,
            reason="Temporary block",
            blocked_by="system"
        )
        
        # Remove entry
        result = self.manager.remove_entry("temp_node")
        self.assertTrue(result)
        self.assertEqual(len(self.manager.blacklist), 0)
        
        # Try to remove non-existent entry
        result = self.manager.remove_entry("nonexistent")
        self.assertFalse(result)
    
    def test_is_blacklisted(self):
        """Test checking if entity is blacklisted."""
        # Add entry
        self.manager.add_entry(
            entity_id="blocked_node",
            entity_type="node",
            category=ThreatCategory.ATTACK_ATTEMPT,
            severity=ThreatSeverity.CRITICAL,
            reason="Attack detected",
            blocked_by="security"
        )
        
        # Check blacklisted
        self.assertTrue(self.manager.is_blacklisted("blocked_node"))
        self.assertFalse(self.manager.is_blacklisted("clean_node"))
    
    def test_is_blacklisted_with_expiration(self):
        """Test blacklist check with expired entries."""
        # Add expired entry
        self.manager.add_entry(
            entity_id="expired_node",
            entity_type="node",
            category=ThreatCategory.SUSPICIOUS_ENTITY,
            severity=ThreatSeverity.LOW,
            reason="Temporary block",
            blocked_by="system",
            expires_at=time.time() - 100  # Already expired
        )
        
        # Should return False and auto-remove
        self.assertFalse(self.manager.is_blacklisted("expired_node"))
        self.assertNotIn("expired_node", self.manager.blacklist)
    
    def test_get_entry(self):
        """Test getting a blacklist entry."""
        # Add entry
        added_entry = self.manager.add_entry(
            entity_id="test_node",
            entity_type="node",
            category=ThreatCategory.PROTOCOL_VIOLATION,
            severity=ThreatSeverity.MEDIUM,
            reason="Protocol violation",
            blocked_by="monitor"
        )
        
        # Get entry
        entry = self.manager.get_entry("test_node")
        self.assertIsNotNone(entry)
        self.assertEqual(entry.entity_id, "test_node")
        
        # Try to get non-existent entry
        entry = self.manager.get_entry("nonexistent")
        self.assertIsNone(entry)
    
    def test_get_all_entries(self):
        """Test getting all entries with filtering."""
        # Add multiple entries
        self.manager.add_entry(
            entity_id="node1",
            entity_type="node",
            category=ThreatCategory.MALICIOUS_NODE,
            severity=ThreatSeverity.CRITICAL,
            reason="Malicious",
            blocked_by="admin"
        )
        
        self.manager.add_entry(
            entity_id="node2",
            entity_type="node",
            category=ThreatCategory.SUSPICIOUS_ENTITY,
            severity=ThreatSeverity.HIGH,
            reason="Suspicious",
            blocked_by="admin"
        )
        
        self.manager.add_entry(
            entity_id="agent1",
            entity_type="agent",
            category=ThreatCategory.ATTACK_ATTEMPT,
            severity=ThreatSeverity.CRITICAL,
            reason="Attack",
            blocked_by="system"
        )
        
        # Get all entries
        all_entries = self.manager.get_all_entries()
        self.assertEqual(len(all_entries), 3)
        
        # Filter by entity type
        node_entries = self.manager.get_all_entries(entity_type="node")
        self.assertEqual(len(node_entries), 2)
        
        # Filter by category
        malicious_entries = self.manager.get_all_entries(
            category=ThreatCategory.MALICIOUS_NODE
        )
        self.assertEqual(len(malicious_entries), 1)
        
        # Filter by severity
        critical_entries = self.manager.get_all_entries(
            severity=ThreatSeverity.CRITICAL
        )
        self.assertEqual(len(critical_entries), 2)
    
    def test_get_statistics(self):
        """Test getting blacklist statistics."""
        # Add entries
        self.manager.add_entry(
            entity_id="node1",
            entity_type="node",
            category=ThreatCategory.MALICIOUS_NODE,
            severity=ThreatSeverity.CRITICAL,
            reason="Test",
            blocked_by="admin"
        )
        
        self.manager.add_entry(
            entity_id="node2",
            entity_type="node",
            category=ThreatCategory.SUSPICIOUS_ENTITY,
            severity=ThreatSeverity.HIGH,
            reason="Test",
            blocked_by="admin",
            expires_at=time.time() + 1000
        )
        
        stats = self.manager.get_statistics()
        
        self.assertEqual(stats['total_entries'], 2)
        self.assertEqual(stats['permanent_entries'], 1)
        self.assertEqual(stats['temporary_entries'], 1)
        self.assertIn('by_category', stats)
        self.assertIn('by_severity', stats)
        self.assertIn('by_type', stats)
    
    def test_persistence(self):
        """Test saving and loading from file."""
        # Add entries
        self.manager.add_entry(
            entity_id="persistent_node",
            entity_type="node",
            category=ThreatCategory.DATA_THEFT,
            severity=ThreatSeverity.CRITICAL,
            reason="Data theft detected",
            blocked_by="security"
        )
        
        # Create new manager with same file
        new_manager = BlacklistManager(storage_path=self.temp_path)
        
        # Check entry was loaded
        self.assertEqual(len(new_manager.blacklist), 1)
        self.assertTrue(new_manager.is_blacklisted("persistent_node"))
    
    def test_export_state(self):
        """Test exporting blacklist state."""
        # Add entry
        self.manager.add_entry(
            entity_id="export_node",
            entity_type="node",
            category=ThreatCategory.INTEGRITY_BREACH,
            severity=ThreatSeverity.HIGH,
            reason="Integrity breach",
            blocked_by="monitor"
        )
        
        state = self.manager.export_state()
        
        self.assertIn('blacklist_version', state)
        self.assertIn('storage_path', state)
        self.assertIn('statistics', state)
        self.assertIn('entries', state)
        self.assertEqual(len(state['entries']), 1)


class TestValidation(unittest.TestCase):
    """Test validation functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_fd, self.temp_path = tempfile.mkstemp(suffix='.json')
        os.close(self.temp_fd)
        self.manager = BlacklistManager(storage_path=self.temp_path)
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_path):
            os.remove(self.temp_path)
    
    def test_validate_clean_entity(self):
        """Test validation of non-blacklisted entity."""
        result = validate_entity_against_blacklist(
            "clean_node",
            self.manager,
            raise_on_blocked=False
        )
        self.assertTrue(result)
    
    def test_validate_blacklisted_entity_no_raise(self):
        """Test validation of blacklisted entity without raising."""
        # Add to blacklist
        self.manager.add_entry(
            entity_id="blocked_node",
            entity_type="node",
            category=ThreatCategory.MALICIOUS_NODE,
            severity=ThreatSeverity.HIGH,
            reason="Blocked",
            blocked_by="admin"
        )
        
        result = validate_entity_against_blacklist(
            "blocked_node",
            self.manager,
            raise_on_blocked=False
        )
        self.assertFalse(result)
    
    def test_validate_blacklisted_entity_with_raise(self):
        """Test validation of blacklisted entity with raising."""
        # Add to blacklist
        self.manager.add_entry(
            entity_id="blocked_node",
            entity_type="node",
            category=ThreatCategory.ATTACK_ATTEMPT,
            severity=ThreatSeverity.CRITICAL,
            reason="Attack detected",
            blocked_by="security"
        )
        
        with self.assertRaises(ValueError) as context:
            validate_entity_against_blacklist(
                "blocked_node",
                self.manager,
                raise_on_blocked=True
            )
        
        self.assertIn("blacklisted", str(context.exception))
        self.assertIn("Attack detected", str(context.exception))


class TestThreatCategories(unittest.TestCase):
    """Test threat category and severity enums."""
    
    def test_threat_categories(self):
        """Test all threat categories are defined."""
        categories = [
            ThreatCategory.MALICIOUS_NODE,
            ThreatCategory.SUSPICIOUS_ENTITY,
            ThreatCategory.ATTACK_ATTEMPT,
            ThreatCategory.DATA_THEFT,
            ThreatCategory.PROTOCOL_VIOLATION,
            ThreatCategory.INTEGRITY_BREACH
        ]
        
        self.assertEqual(len(categories), 6)
        
        for cat in categories:
            self.assertIsInstance(cat.value, str)
    
    def test_threat_severities(self):
        """Test all severity levels are defined."""
        severities = [
            ThreatSeverity.LOW,
            ThreatSeverity.MEDIUM,
            ThreatSeverity.HIGH,
            ThreatSeverity.CRITICAL
        ]
        
        self.assertEqual(len(severities), 4)
        
        for sev in severities:
            self.assertIsInstance(sev.value, str)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestBlacklistEntry))
    suite.addTests(loader.loadTestsFromTestCase(TestBlacklistManager))
    suite.addTests(loader.loadTestsFromTestCase(TestValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestThreatCategories))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
