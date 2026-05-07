#!/usr/bin/env python3
"""
Lex Amoris Security System - Test Suite

Comprehensive tests for all security components:
- Rhythm Validator
- Rotesschild Scanner
- IPFS Backup System
- Rescue Channel
- Integrated Security System
"""

import unittest
import json
import time
from lex_amoris_security import (
    DataPacket,
    SecurityThreat,
    RescueMessage,
    RhythmValidator,
    RotesschildScanner,
    IPFSBackupSystem,
    RescueChannel,
    LexAmorisSecuritySystem,
    RESONANCE_FREQUENCY_HZ,
    ROTESSCHILD_THRESHOLD_MV_M,
    RHYTHM_TOLERANCE
)
from eternal_resonance_protocol import EternalResonanceProtocol


class TestDataPacket(unittest.TestCase):
    """Test DataPacket data class."""
    
    def test_packet_creation(self):
        """Test packet creation."""
        packet = DataPacket(
            packet_id="TEST001",
            timestamp=time.time(),
            frequency=0.043,
            source_ip="192.168.1.1",
            payload={"data": "test"}
        )
        
        self.assertEqual(packet.packet_id, "TEST001")
        self.assertEqual(packet.frequency, 0.043)
        self.assertEqual(packet.source_ip, "192.168.1.1")


class TestRhythmValidator(unittest.TestCase):
    """Test RhythmValidator functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator = RhythmValidator()
    
    def test_initialization(self):
        """Test validator initialization."""
        self.assertEqual(self.validator.reference_frequency, RESONANCE_FREQUENCY_HZ)
        self.assertEqual(self.validator.tolerance, RHYTHM_TOLERANCE)
        self.assertEqual(len(self.validator.blacklist), 0)
    
    def test_validate_correct_frequency(self):
        """Test validation with correct frequency."""
        packet = DataPacket(
            packet_id="VALID001",
            timestamp=time.time(),
            frequency=0.043,  # Exact match
            source_ip="192.168.1.1",
            payload={}
        )
        
        is_valid, reason = self.validator.validate_packet_frequency(packet)
        self.assertTrue(is_valid)
        self.assertIn("within tolerance", reason)
    
    def test_validate_frequency_within_tolerance(self):
        """Test validation with frequency within tolerance."""
        packet = DataPacket(
            packet_id="VALID002",
            timestamp=time.time(),
            frequency=0.045,  # Within 15% tolerance
            source_ip="192.168.1.1",
            payload={}
        )
        
        is_valid, reason = self.validator.validate_packet_frequency(packet)
        self.assertTrue(is_valid)
    
    def test_validate_frequency_outside_tolerance(self):
        """Test validation with frequency outside tolerance."""
        packet = DataPacket(
            packet_id="INVALID001",
            timestamp=time.time(),
            frequency=0.1,  # Way outside tolerance
            source_ip="192.168.1.1",
            payload={}
        )
        
        is_valid, reason = self.validator.validate_packet_frequency(packet)
        self.assertFalse(is_valid)
        self.assertIn("exceeds tolerance", reason)
    
    def test_validate_rhythm_pattern(self):
        """Test rhythm pattern validation."""
        packet = DataPacket(
            packet_id="RHYTHM001",
            timestamp=time.time(),
            frequency=0.043,
            source_ip="192.168.1.1",
            payload={}
        )
        
        is_valid, reason = self.validator.validate_rhythm_pattern(packet)
        # Should return a boolean and reason
        self.assertIsInstance(is_valid, bool)
        self.assertIsInstance(reason, str)
    
    def test_validate_rhythm_pattern_zero_frequency(self):
        """Test rhythm pattern validation with zero frequency."""
        packet = DataPacket(
            packet_id="ZERO001",
            timestamp=time.time(),
            frequency=0.0,
            source_ip="192.168.1.1",
            payload={}
        )
        
        is_valid, reason = self.validator.validate_rhythm_pattern(packet)
        self.assertFalse(is_valid)
        self.assertIn("Invalid frequency", reason)
    
    def test_add_to_blacklist(self):
        """Test adding source to blacklist."""
        self.validator.add_to_blacklist(
            "192.168.1.100",
            "frequency_violation",
            {"reason": "test"}
        )
        
        self.assertEqual(len(self.validator.blacklist), 1)
        self.assertTrue(self.validator.is_blacklisted("192.168.1.100"))
    
    def test_is_blacklisted(self):
        """Test blacklist checking."""
        self.assertFalse(self.validator.is_blacklisted("192.168.1.200"))
        
        self.validator.add_to_blacklist("192.168.1.200", "test", {})
        self.assertTrue(self.validator.is_blacklisted("192.168.1.200"))
    
    def test_remove_from_blacklist(self):
        """Test removing from blacklist."""
        self.validator.add_to_blacklist("192.168.1.150", "test", {})
        self.assertTrue(self.validator.is_blacklisted("192.168.1.150"))
        
        self.validator.remove_from_blacklist("192.168.1.150")
        self.assertFalse(self.validator.is_blacklisted("192.168.1.150"))
    
    def test_validation_logging(self):
        """Test that validations are logged."""
        initial_log_size = len(self.validator.validation_log)
        
        packet = DataPacket(
            packet_id="LOG001",
            timestamp=time.time(),
            frequency=0.043,
            source_ip="192.168.1.1",
            payload={}
        )
        
        self.validator.validate_packet_frequency(packet)
        
        self.assertEqual(len(self.validator.validation_log), initial_log_size + 1)


class TestRotesschildScanner(unittest.TestCase):
    """Test RotesschildScanner functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scanner = RotesschildScanner()
    
    def test_initialization(self):
        """Test scanner initialization."""
        self.assertEqual(self.scanner.threshold, ROTESSCHILD_THRESHOLD_MV_M)
        self.assertEqual(self.scanner.current_pressure, 0.0)
        self.assertFalse(self.scanner.security_active)
    
    def test_scan_environment(self):
        """Test environment scanning."""
        pressure = self.scanner.scan_environment()
        
        self.assertIsInstance(pressure, float)
        self.assertGreater(pressure, 0.0)
        self.assertEqual(self.scanner.current_pressure, pressure)
    
    def test_scan_history_logging(self):
        """Test that scans are logged."""
        initial_count = len(self.scanner.scan_history)
        
        self.scanner.scan_environment()
        
        self.assertEqual(len(self.scanner.scan_history), initial_count + 1)
    
    def test_scan_history_limit(self):
        """Test that scan history is limited to 100 entries."""
        # Perform many scans
        for _ in range(150):
            self.scanner.scan_environment()
        
        self.assertLessEqual(len(self.scanner.scan_history), 100)
    
    def test_should_activate_security(self):
        """Test security activation decision."""
        result = self.scanner.should_activate_security()
        
        self.assertIsInstance(result, bool)
        # Security should be active if pressure > threshold
        if self.scanner.current_pressure > self.scanner.threshold:
            self.assertTrue(result)
            self.assertTrue(self.scanner.security_active)
    
    def test_get_scan_status(self):
        """Test getting scan status."""
        self.scanner.scan_environment()
        status = self.scanner.get_scan_status()
        
        self.assertIn('current_pressure_mv_m', status)
        self.assertIn('threshold_mv_m', status)
        self.assertIn('security_active', status)
        self.assertIn('above_threshold', status)
        self.assertIn('scan_count', status)


class TestIPFSBackupSystem(unittest.TestCase):
    """Test IPFSBackupSystem functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.backup_system = IPFSBackupSystem()
    
    def test_initialization(self):
        """Test backup system initialization."""
        self.assertEqual(len(self.backup_system.backup_registry), 0)
        self.assertEqual(len(self.backup_system.ipfs_hashes), 0)
        self.assertEqual(len(self.backup_system.backup_log), 0)
    
    def test_create_backup(self):
        """Test creating a backup."""
        config_data = {
            "setting1": "value1",
            "setting2": 123
        }
        
        ipfs_hash = self.backup_system.create_backup("test_config", config_data)
        
        self.assertIsInstance(ipfs_hash, str)
        self.assertTrue(ipfs_hash.startswith("Qm"))
        self.assertEqual(len(self.backup_system.backup_registry), 1)
        self.assertIn("test_config", self.backup_system.backup_registry)
    
    def test_restore_from_backup(self):
        """Test restoring from backup."""
        original_config = {
            "key": "value",
            "number": 42
        }
        
        # Create backup
        ipfs_hash = self.backup_system.create_backup("restore_test", original_config)
        
        # Restore
        restored_config = self.backup_system.restore_from_backup("restore_test")
        
        self.assertIsNotNone(restored_config)
        self.assertEqual(restored_config, original_config)
    
    def test_restore_nonexistent_backup(self):
        """Test restoring a backup that doesn't exist."""
        result = self.backup_system.restore_from_backup("nonexistent")
        
        self.assertIsNone(result)
    
    def test_verify_backup_integrity(self):
        """Test backup integrity verification."""
        config_data = {"test": "data"}
        
        self.backup_system.create_backup("integrity_test", config_data)
        
        is_valid, message = self.backup_system.verify_backup_integrity("integrity_test")
        
        self.assertTrue(is_valid)
        self.assertIn("verified", message)
    
    def test_verify_nonexistent_backup(self):
        """Test verifying a backup that doesn't exist."""
        is_valid, message = self.backup_system.verify_backup_integrity("nonexistent")
        
        self.assertFalse(is_valid)
        self.assertIn("not found", message)
    
    def test_list_backups(self):
        """Test listing all backups."""
        # Create multiple backups
        self.backup_system.create_backup("backup1", {"data": 1})
        self.backup_system.create_backup("backup2", {"data": 2})
        self.backup_system.create_backup("backup3", {"data": 3})
        
        backups = self.backup_system.list_backups()
        
        self.assertEqual(len(backups), 3)
        self.assertIsInstance(backups, list)
    
    def test_backup_logging(self):
        """Test that backup operations are logged."""
        initial_log_size = len(self.backup_system.backup_log)
        
        self.backup_system.create_backup("log_test", {"data": "test"})
        
        self.assertGreater(len(self.backup_system.backup_log), initial_log_size)


class TestRescueChannel(unittest.TestCase):
    """Test RescueChannel functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.erp = EternalResonanceProtocol(node_id="test_erp")
        self.rescue_channel = RescueChannel(self.erp)
        self.validator = RhythmValidator()
    
    def test_initialization(self):
        """Test rescue channel initialization."""
        self.assertEqual(len(self.rescue_channel.messages), 0)
        self.assertEqual(self.rescue_channel.resolved_count, 0)
    
    def test_send_rescue_message(self):
        """Test sending rescue message."""
        message_id = self.rescue_channel.send_rescue_message(
            "node1",
            "false_positive",
            "Test rescue message",
            priority="high"
        )
        
        self.assertIsInstance(message_id, str)
        self.assertEqual(len(self.rescue_channel.messages), 1)
        self.assertIn(message_id, self.rescue_channel.messages)
    
    def test_rescue_message_content(self):
        """Test rescue message content."""
        message_id = self.rescue_channel.send_rescue_message(
            "node_test",
            "blocked",
            "Node is blocked",
            priority="urgent"
        )
        
        msg = self.rescue_channel.messages[message_id]
        
        self.assertEqual(msg.node_id, "node_test")
        self.assertEqual(msg.issue_type, "blocked")
        self.assertEqual(msg.priority, "urgent")
        self.assertEqual(msg.resolution_status, "pending")
    
    def test_process_false_positive(self):
        """Test processing false positive rescue message."""
        # Add node to blacklist
        self.validator.add_to_blacklist("blocked_node", "test", {})
        self.assertTrue(self.validator.is_blacklisted("blocked_node"))
        
        # Send rescue message
        message_id = self.rescue_channel.send_rescue_message(
            "blocked_node",
            "false_positive",
            "False positive detected"
        )
        
        # Process rescue
        resolved = self.rescue_channel.process_rescue_message(message_id, self.validator)
        
        self.assertTrue(resolved)
        self.assertFalse(self.validator.is_blacklisted("blocked_node"))
        self.assertEqual(self.rescue_channel.resolved_count, 1)
    
    def test_process_blocked_node(self):
        """Test processing blocked node rescue message."""
        # Register node in ERP
        self.erp.register_node("blocked_erp_node", truth_alignment=0.5)
        
        # Send rescue message
        message_id = self.rescue_channel.send_rescue_message(
            "blocked_erp_node",
            "blocked",
            "Node needs unblocking"
        )
        
        # Process rescue
        resolved = self.rescue_channel.process_rescue_message(message_id, self.validator)
        
        self.assertTrue(resolved)
        self.assertEqual(self.rescue_channel.resolved_count, 1)
        
        # Check that node alignment improved
        node = self.erp.nodes["blocked_erp_node"]
        self.assertGreater(node.truth_alignment, 0.5)
    
    def test_process_nonexistent_message(self):
        """Test processing non-existent message."""
        resolved = self.rescue_channel.process_rescue_message("fake_id", self.validator)
        
        self.assertFalse(resolved)
    
    def test_get_pending_messages(self):
        """Test getting pending messages."""
        # Send multiple messages
        self.rescue_channel.send_rescue_message("node1", "false_positive", "msg1", "high")
        self.rescue_channel.send_rescue_message("node2", "blocked", "msg2", "medium")
        self.rescue_channel.send_rescue_message("node3", "degraded", "msg3", "urgent")
        
        pending = self.rescue_channel.get_pending_messages()
        
        self.assertEqual(len(pending), 3)
        # Should be sorted by priority (urgent first)
        self.assertEqual(pending[0].priority, "urgent")
    
    def test_get_pending_messages_with_filter(self):
        """Test getting pending messages with priority filter."""
        self.rescue_channel.send_rescue_message("node1", "false_positive", "msg1", "high")
        self.rescue_channel.send_rescue_message("node2", "blocked", "msg2", "medium")
        self.rescue_channel.send_rescue_message("node3", "degraded", "msg3", "high")
        
        high_priority = self.rescue_channel.get_pending_messages(priority_filter="high")
        
        self.assertEqual(len(high_priority), 2)
        for msg in high_priority:
            self.assertEqual(msg.priority, "high")


class TestLexAmorisSecuritySystem(unittest.TestCase):
    """Test integrated LexAmorisSecuritySystem."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.security_system = LexAmorisSecuritySystem()
    
    def test_initialization(self):
        """Test security system initialization."""
        self.assertIsNotNone(self.security_system.erp)
        self.assertIsNotNone(self.security_system.rhythm_validator)
        self.assertIsNotNone(self.security_system.rotesschild_scanner)
        self.assertIsNotNone(self.security_system.ipfs_backup)
        self.assertIsNotNone(self.security_system.rescue_channel)
    
    def test_validate_and_process_valid_packet(self):
        """Test processing a valid packet."""
        packet = DataPacket(
            packet_id="VALID001",
            timestamp=time.time(),
            frequency=0.043,
            source_ip="192.168.1.1",
            payload={"data": "test"}
        )
        
        accepted, reason = self.security_system.validate_and_process_packet(packet)
        
        # May be accepted depending on Rotesschild threshold
        self.assertIsInstance(accepted, bool)
        self.assertIsInstance(reason, str)
    
    def test_validate_and_process_blacklisted_packet(self):
        """Test processing packet from blacklisted source."""
        # Add source to blacklist
        self.security_system.rhythm_validator.add_to_blacklist(
            "192.168.1.100",
            "test",
            {}
        )
        
        packet = DataPacket(
            packet_id="BLOCKED001",
            timestamp=time.time(),
            frequency=0.043,
            source_ip="192.168.1.100",
            payload={"data": "test"}
        )
        
        accepted, reason = self.security_system.validate_and_process_packet(packet)
        
        self.assertFalse(accepted)
        self.assertIn("blacklisted", reason)
    
    def test_backup_configuration(self):
        """Test configuration backup."""
        config = {
            "setting1": "value1",
            "setting2": 123
        }
        
        ipfs_hash = self.security_system.backup_configuration("test_config", config)
        
        self.assertIsInstance(ipfs_hash, str)
        self.assertTrue(ipfs_hash.startswith("Qm"))
    
    def test_report_false_positive(self):
        """Test reporting false positive."""
        # Add node to blacklist
        self.security_system.rhythm_validator.add_to_blacklist(
            "node_fp",
            "test",
            {}
        )
        
        # Report false positive
        message_id = self.security_system.report_false_positive(
            "node_fp",
            "Network latency caused false detection"
        )
        
        self.assertIsInstance(message_id, str)
        # Should be removed from blacklist
        self.assertFalse(self.security_system.rhythm_validator.is_blacklisted("node_fp"))
    
    def test_get_system_status(self):
        """Test getting system status."""
        status = self.security_system.get_system_status()
        
        self.assertIn('timestamp', status)
        self.assertIn('rotesschild_scanner', status)
        self.assertIn('blacklist_count', status)
        self.assertIn('backup_count', status)
        self.assertIn('pending_rescue_messages', status)
        self.assertIn('resolved_rescue_count', status)
        self.assertIn('security_events', status)
        self.assertIn('erp_global_alignment', status)
    
    def test_security_event_logging(self):
        """Test that security events are logged."""
        initial_log_size = len(self.security_system.security_log)
        
        packet = DataPacket(
            packet_id="LOG001",
            timestamp=time.time(),
            frequency=0.043,
            source_ip="192.168.1.1",
            payload={}
        )
        
        self.security_system.validate_and_process_packet(packet)
        
        # Should have logged at least one event
        self.assertGreater(len(self.security_system.security_log), initial_log_size)
    
    def test_security_log_size_limit(self):
        """Test that security log is limited to 1000 entries."""
        # Generate many events
        for i in range(1100):
            packet = DataPacket(
                packet_id=f"PKT{i:04d}",
                timestamp=time.time(),
                frequency=0.043,
                source_ip="192.168.1.1",
                payload={}
            )
            self.security_system.validate_and_process_packet(packet)
        
        self.assertLessEqual(len(self.security_system.security_log), 1000)


class TestConstants(unittest.TestCase):
    """Test module constants."""
    
    def test_rotesschild_threshold(self):
        """Test Rotesschild threshold constant."""
        self.assertEqual(ROTESSCHILD_THRESHOLD_MV_M, 50.0)
    
    def test_rhythm_tolerance(self):
        """Test rhythm tolerance constant."""
        self.assertEqual(RHYTHM_TOLERANCE, 0.15)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDataPacket))
    suite.addTests(loader.loadTestsFromTestCase(TestRhythmValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestRotesschildScanner))
    suite.addTests(loader.loadTestsFromTestCase(TestIPFSBackupSystem))
    suite.addTests(loader.loadTestsFromTestCase(TestRescueChannel))
    suite.addTests(loader.loadTestsFromTestCase(TestLexAmorisSecuritySystem))
    suite.addTests(loader.loadTestsFromTestCase(TestConstants))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
