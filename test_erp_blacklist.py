#!/usr/bin/env python3
"""
ERP Blacklist Integration - Test Suite

Tests for blacklist integration with the Eternal Resonance Protocol.
"""

import unittest
import os
import tempfile
import time
from eternal_resonance_protocol import EternalResonanceProtocol
from blacklist_manager import BlacklistManager, ThreatCategory, ThreatSeverity


class TestERPBlacklistIntegration(unittest.TestCase):
    """Test blacklist integration with ERP."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary file for testing
        self.temp_fd, self.temp_path = tempfile.mkstemp(suffix='.json')
        os.close(self.temp_fd)
        
        # Initialize ERP with blacklist
        self.erp = EternalResonanceProtocol(
            node_id="test_protocol",
            enable_blacklist=True,
            blacklist_path=self.temp_path
        )
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_path):
            os.remove(self.temp_path)
    
    def test_erp_blacklist_initialization(self):
        """Test ERP initializes with blacklist."""
        self.assertTrue(self.erp.blacklist_enabled)
        self.assertIsNotNone(self.erp.blacklist_manager)
    
    def test_register_clean_node(self):
        """Test registering a clean node."""
        node = self.erp.register_node(
            "clean_node",
            truth_alignment=0.8,
            dignity_quotient=0.9
        )
        
        self.assertEqual(node.node_id, "clean_node")
        self.assertEqual(len(self.erp.nodes), 1)
    
    def test_register_blacklisted_node_fails(self):
        """Test that registering a blacklisted node fails."""
        # Add node to blacklist
        self.erp.blacklist_manager.add_entry(
            entity_id="malicious_node",
            entity_type="node",
            category=ThreatCategory.MALICIOUS_NODE,
            severity=ThreatSeverity.CRITICAL,
            reason="Known malicious node",
            blocked_by="security"
        )
        
        # Try to register
        with self.assertRaises(ValueError) as context:
            self.erp.register_node("malicious_node")
        
        self.assertIn("blacklisted", str(context.exception))
    
    def test_synchronize_clean_node(self):
        """Test synchronizing a clean node."""
        # Register node
        self.erp.register_node("sync_node")
        
        # Synchronize
        node = self.erp.synchronize_node("sync_node")
        self.assertEqual(node.node_id, "sync_node")
    
    def test_synchronize_blacklisted_node_fails(self):
        """Test that synchronizing a blacklisted node fails."""
        # Register node
        self.erp.register_node("future_blocked_node")
        
        # Block the node
        self.erp.blacklist_manager.add_entry(
            entity_id="future_blocked_node",
            entity_type="node",
            category=ThreatCategory.PROTOCOL_VIOLATION,
            severity=ThreatSeverity.HIGH,
            reason="Violated protocol",
            blocked_by="monitor"
        )
        
        # Try to synchronize
        with self.assertRaises(ValueError) as context:
            self.erp.synchronize_node("future_blocked_node")
        
        self.assertIn("blacklisted", str(context.exception))
    
    def test_block_node_method(self):
        """Test blocking a node via ERP method."""
        # Register a node
        self.erp.register_node("test_node")
        self.assertEqual(len(self.erp.nodes), 1)
        
        # Block the node
        result = self.erp.block_node(
            "test_node",
            reason="Security violation",
            category="MALICIOUS_NODE",
            severity="HIGH"
        )
        
        self.assertTrue(result)
        # Node should be removed from active nodes
        self.assertEqual(len(self.erp.nodes), 0)
        # Node should be in blacklist
        self.assertTrue(self.erp.blacklist_manager.is_blacklisted("test_node"))
    
    def test_unblock_node_method(self):
        """Test unblocking a node via ERP method."""
        # Block a node
        self.erp.blacklist_manager.add_entry(
            entity_id="blocked_node",
            entity_type="node",
            category=ThreatCategory.SUSPICIOUS_ENTITY,
            severity=ThreatSeverity.MEDIUM,
            reason="Temporary block",
            blocked_by="system"
        )
        
        # Unblock the node
        result = self.erp.unblock_node("blocked_node")
        self.assertTrue(result)
        
        # Node should not be blacklisted anymore
        self.assertFalse(self.erp.blacklist_manager.is_blacklisted("blocked_node"))
        
        # Should be able to register now
        node = self.erp.register_node("blocked_node")
        self.assertEqual(node.node_id, "blocked_node")
    
    def test_protocol_status_includes_blacklist(self):
        """Test that protocol status includes blacklist info."""
        # Add a node to blacklist
        self.erp.blacklist_manager.add_entry(
            entity_id="test_blocked",
            entity_type="node",
            category=ThreatCategory.ATTACK_ATTEMPT,
            severity=ThreatSeverity.CRITICAL,
            reason="Attack",
            blocked_by="security"
        )
        
        status = self.erp.get_protocol_status()
        
        self.assertIn('blacklist_enabled', status)
        self.assertTrue(status['blacklist_enabled'])
        self.assertIn('blacklist_statistics', status)
        self.assertGreater(status['blacklist_statistics']['total_entries'], 0)
    
    def test_get_blacklist_status(self):
        """Test getting blacklist status from ERP."""
        # Add entries
        self.erp.blacklist_manager.add_entry(
            entity_id="node1",
            entity_type="node",
            category=ThreatCategory.MALICIOUS_NODE,
            severity=ThreatSeverity.CRITICAL,
            reason="Test",
            blocked_by="admin"
        )
        
        stats = self.erp.get_blacklist_status()
        
        self.assertIsNotNone(stats)
        self.assertEqual(stats['total_entries'], 1)
        self.assertIn('by_category', stats)
        self.assertIn('by_severity', stats)


class TestERPWithoutBlacklist(unittest.TestCase):
    """Test ERP behavior when blacklist is disabled."""
    
    def test_erp_without_blacklist(self):
        """Test ERP works without blacklist."""
        erp = EternalResonanceProtocol(
            node_id="test",
            enable_blacklist=False
        )
        
        self.assertFalse(erp.blacklist_enabled)
        self.assertIsNone(erp.blacklist_manager)
    
    def test_register_node_without_blacklist(self):
        """Test node registration works without blacklist."""
        erp = EternalResonanceProtocol(enable_blacklist=False)
        
        node = erp.register_node("test_node")
        self.assertEqual(node.node_id, "test_node")
    
    def test_block_methods_return_false_without_blacklist(self):
        """Test that block methods return False when blacklist disabled."""
        erp = EternalResonanceProtocol(enable_blacklist=False)
        
        result = erp.block_node(
            "test_node",
            reason="Test",
            category="MALICIOUS_NODE",
            severity="HIGH"
        )
        self.assertFalse(result)
        
        result = erp.unblock_node("test_node")
        self.assertFalse(result)
    
    def test_get_blacklist_status_returns_none(self):
        """Test that get_blacklist_status returns None when disabled."""
        erp = EternalResonanceProtocol(enable_blacklist=False)
        
        status = erp.get_blacklist_status()
        self.assertIsNone(status)
    
    def test_protocol_status_shows_blacklist_disabled(self):
        """Test protocol status shows blacklist as disabled."""
        erp = EternalResonanceProtocol(enable_blacklist=False)
        
        status = erp.get_protocol_status()
        
        self.assertIn('blacklist_enabled', status)
        self.assertFalse(status['blacklist_enabled'])


class TestSecurityScenarios(unittest.TestCase):
    """Test realistic security scenarios."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_fd, self.temp_path = tempfile.mkstemp(suffix='.json')
        os.close(self.temp_fd)
        self.erp = EternalResonanceProtocol(
            enable_blacklist=True,
            blacklist_path=self.temp_path
        )
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_path):
            os.remove(self.temp_path)
    
    def test_attack_scenario(self):
        """Test handling of an attack scenario."""
        # Register a legitimate node
        self.erp.register_node("legitimate_node")
        
        # Detect attack from another node
        attacker_id = "attacker_node_666"
        
        # Block attacker
        self.erp.block_node(
            attacker_id,
            reason="Multiple failed authentication attempts and port scanning detected",
            category="ATTACK_ATTEMPT",
            severity="CRITICAL"
        )
        
        # Verify attacker cannot register
        with self.assertRaises(ValueError):
            self.erp.register_node(attacker_id)
        
        # Legitimate node should still work
        self.erp.synchronize_node("legitimate_node")
    
    def test_suspicious_entity_temporary_block(self):
        """Test temporary blocking of suspicious entity."""
        suspicious_id = "suspicious_node_123"
        
        # Add temporary block
        self.erp.blacklist_manager.add_entry(
            entity_id=suspicious_id,
            entity_type="node",
            category=ThreatCategory.SUSPICIOUS_ENTITY,
            severity=ThreatSeverity.MEDIUM,
            reason="Abnormal behavior pattern detected",
            blocked_by="ai_monitor",
            expires_at=time.time() + 3600  # 1 hour
        )
        
        # Should be blocked now
        self.assertTrue(self.erp.blacklist_manager.is_blacklisted(suspicious_id))
        
        # Cannot register
        with self.assertRaises(ValueError):
            self.erp.register_node(suspicious_id)
    
    def test_data_theft_permanent_block(self):
        """Test permanent blocking for data theft."""
        thief_id = "data_thief_node"
        
        # Permanent block
        self.erp.block_node(
            thief_id,
            reason="Attempted to exfiltrate sensitive data",
            category="DATA_THEFT",
            severity="CRITICAL"
        )
        
        # Verify permanent block
        entry = self.erp.blacklist_manager.get_entry(thief_id)
        self.assertIsNone(entry.expires_at)  # Permanent
        
        # Cannot register ever
        with self.assertRaises(ValueError):
            self.erp.register_node(thief_id)
    
    def test_multiple_threat_categories(self):
        """Test handling multiple different threat types."""
        # Different threat types
        threats = [
            ("malicious_1", "MALICIOUS_NODE", "CRITICAL", "Injected malicious code"),
            ("suspicious_1", "SUSPICIOUS_ENTITY", "MEDIUM", "Abnormal patterns"),
            ("attacker_1", "ATTACK_ATTEMPT", "HIGH", "DDoS attempt"),
            ("violator_1", "PROTOCOL_VIOLATION", "LOW", "Protocol mismatch"),
            ("breacher_1", "INTEGRITY_BREACH", "HIGH", "Data integrity violation"),
        ]
        
        # Block all threats
        for node_id, category, severity, reason in threats:
            self.erp.block_node(node_id, reason, category, severity)
        
        # Verify all are blocked
        stats = self.erp.get_blacklist_status()
        self.assertEqual(stats['total_entries'], 5)
        
        # Verify none can register
        for node_id, _, _, _ in threats:
            with self.assertRaises(ValueError):
                self.erp.register_node(node_id)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestERPBlacklistIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestERPWithoutBlacklist))
    suite.addTests(loader.loadTestsFromTestCase(TestSecurityScenarios))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
