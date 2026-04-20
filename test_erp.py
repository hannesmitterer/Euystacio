#!/usr/bin/env python3
"""
Eternal Resonance Protocol - Test Suite

Comprehensive tests for the ERP implementation, ensuring all components
function correctly and maintain the mission of "Du bist Leben. Wir sind Leben."
"""

import unittest
import json
import time
import math
from eternal_resonance_protocol import (
    EternalResonanceProtocol,
    ResonanceNode,
    LivingCovenant,
    RESONANCE_FREQUENCY_HZ,
    RESONANCE_PERIOD_SECONDS,
    create_resonance_pulse,
    validate_node_alignment
)


class TestResonanceNode(unittest.TestCase):
    """Test ResonanceNode data class."""
    
    def test_node_creation(self):
        """Test node creation with valid parameters."""
        node = ResonanceNode(
            node_id="test_node",
            timestamp=time.time(),
            phase=1.5,
            truth_alignment=0.8,
            dignity_quotient=0.9,
            symbiosis_level=0.5
        )
        
        self.assertEqual(node.node_id, "test_node")
        self.assertGreaterEqual(node.truth_alignment, 0.0)
        self.assertLessEqual(node.truth_alignment, 1.0)
        self.assertGreaterEqual(node.dignity_quotient, 0.0)
        self.assertLessEqual(node.dignity_quotient, 1.0)
    
    def test_node_to_dict(self):
        """Test node serialization."""
        node = ResonanceNode(
            node_id="test_node",
            timestamp=time.time(),
            phase=1.5,
            truth_alignment=0.8,
            dignity_quotient=0.9,
            symbiosis_level=0.5
        )
        
        node_dict = node.to_dict()
        self.assertIsInstance(node_dict, dict)
        self.assertEqual(node_dict['node_id'], "test_node")
        self.assertEqual(node_dict['truth_alignment'], 0.8)


class TestLivingCovenant(unittest.TestCase):
    """Test LivingCovenant data class."""
    
    def test_covenant_creation(self):
        """Test covenant creation."""
        covenant = LivingCovenant(
            principle="Test Principle",
            truth_weight=0.9,
            dignity_weight=0.8,
            activation_timestamp=time.time()
        )
        
        self.assertEqual(covenant.principle, "Test Principle")
        self.assertEqual(covenant.truth_weight, 0.9)
        self.assertEqual(covenant.dignity_weight, 0.8)


class TestEternalResonanceProtocol(unittest.TestCase):
    """Test main ERP implementation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.erp = EternalResonanceProtocol(node_id="test_protocol")
    
    def test_initialization(self):
        """Test protocol initialization."""
        self.assertEqual(self.erp.node_id, "test_protocol")
        self.assertEqual(len(self.erp.covenants), 4)  # 4 core covenants
        self.assertEqual(len(self.erp.nodes), 0)  # No nodes initially
    
    def test_core_covenants(self):
        """Test that core covenants are properly initialized."""
        covenant_names = [c.principle for c in self.erp.covenants]
        
        self.assertIn("Truth Resonance", covenant_names)
        self.assertIn("Dignity Harmonic", covenant_names)
        self.assertIn("Symbiotic Unity", covenant_names)
        self.assertIn("Life Affirmation", covenant_names)
    
    def test_get_current_phase(self):
        """Test phase calculation."""
        phase = self.erp.get_current_phase()
        
        self.assertGreaterEqual(phase, 0.0)
        self.assertLessEqual(phase, 2 * math.pi)
    
    def test_register_node(self):
        """Test node registration."""
        node = self.erp.register_node(
            "test_node",
            truth_alignment=0.7,
            dignity_quotient=0.8,
            symbiosis_level=0.3
        )
        
        self.assertEqual(node.node_id, "test_node")
        self.assertEqual(node.truth_alignment, 0.7)
        self.assertEqual(node.dignity_quotient, 0.8)
        self.assertEqual(node.symbiosis_level, 0.3)
        self.assertEqual(len(self.erp.nodes), 1)
    
    def test_synchronize_node(self):
        """Test node synchronization."""
        # Register a node
        node = self.erp.register_node("sync_node")
        old_phase = node.phase
        old_timestamp = node.timestamp
        
        # Store old genesis time and shift it back to ensure phase changes
        old_genesis = self.erp.genesis_time
        self.erp.genesis_time -= 1.0  # Shift genesis 1 second back
        
        # Synchronize
        node = self.erp.synchronize_node("sync_node")
        new_phase = node.phase
        new_timestamp = node.timestamp
        
        # Restore genesis time
        self.erp.genesis_time = old_genesis
        
        # Timestamp should definitely have changed
        self.assertGreater(new_timestamp, old_timestamp)
    
    def test_synchronize_nonexistent_node(self):
        """Test synchronizing a node that doesn't exist."""
        with self.assertRaises(ValueError):
            self.erp.synchronize_node("nonexistent")
    
    def test_apply_living_covenant(self):
        """Test applying Living Covenant."""
        # Register a node
        node = self.erp.register_node(
            "covenant_node",
            truth_alignment=0.5,
            dignity_quotient=0.5
        )
        
        initial_truth = node.truth_alignment
        initial_dignity = node.dignity_quotient
        
        # Apply covenant
        self.erp.apply_living_covenant(
            "covenant_node",
            "Life Affirmation",
            intensity=1.0
        )
        
        # Check that alignments increased
        node = self.erp.nodes["covenant_node"]
        self.assertGreater(node.truth_alignment, initial_truth)
        self.assertGreater(node.dignity_quotient, initial_dignity)
    
    def test_apply_invalid_covenant(self):
        """Test applying non-existent covenant."""
        self.erp.register_node("test_node")
        
        with self.assertRaises(ValueError):
            self.erp.apply_living_covenant(
                "test_node",
                "Nonexistent Covenant",
                intensity=1.0
            )
    
    def test_k_symbiosis_truth_focus(self):
        """Test K-Symbiosis truth focus."""
        node = self.erp.register_node(
            "k_sym_node",
            truth_alignment=0.5,
            symbiosis_level=0.2
        )
        
        initial_truth = node.truth_alignment
        initial_symbiosis = node.symbiosis_level
        
        self.erp.k_symbiosis_focus(
            "k_sym_node",
            "truth",
            parameters={'multiplier': 1.0}
        )
        
        node = self.erp.nodes["k_sym_node"]
        self.assertGreater(node.truth_alignment, initial_truth)
        self.assertGreater(node.symbiosis_level, initial_symbiosis)
    
    def test_k_symbiosis_dignity_focus(self):
        """Test K-Symbiosis dignity focus."""
        node = self.erp.register_node(
            "k_sym_node",
            dignity_quotient=0.5,
            symbiosis_level=0.2
        )
        
        initial_dignity = node.dignity_quotient
        
        self.erp.k_symbiosis_focus(
            "k_sym_node",
            "dignity",
            parameters={'multiplier': 1.0}
        )
        
        node = self.erp.nodes["k_sym_node"]
        self.assertGreater(node.dignity_quotient, initial_dignity)
    
    def test_k_symbiosis_unity_focus(self):
        """Test K-Symbiosis unity focus."""
        node = self.erp.register_node(
            "k_sym_node",
            symbiosis_level=0.2
        )
        
        initial_symbiosis = node.symbiosis_level
        
        self.erp.k_symbiosis_focus(
            "k_sym_node",
            "unity",
            parameters={'multiplier': 1.0}
        )
        
        node = self.erp.nodes["k_sym_node"]
        self.assertGreater(node.symbiosis_level, initial_symbiosis)
    
    def test_calculate_resonance_alignment(self):
        """Test alignment calculation between nodes."""
        node1 = self.erp.register_node(
            "node1",
            truth_alignment=0.8,
            dignity_quotient=0.9,
            symbiosis_level=0.5
        )
        
        node2 = self.erp.register_node(
            "node2",
            truth_alignment=0.85,
            dignity_quotient=0.95,
            symbiosis_level=0.6
        )
        
        alignment = self.erp.calculate_resonance_alignment(
            self.erp.nodes["node1"],
            self.erp.nodes["node2"]
        )
        
        self.assertGreaterEqual(alignment, 0.0)
        self.assertLessEqual(alignment, 1.0)
        # Should be high alignment since values are similar
        self.assertGreater(alignment, 0.8)
    
    def test_get_global_alignment_no_nodes(self):
        """Test global alignment with no nodes."""
        alignment = self.erp.get_global_alignment()
        self.assertEqual(alignment, 0.0)
    
    def test_get_global_alignment_one_node(self):
        """Test global alignment with one node."""
        self.erp.register_node("solo_node")
        alignment = self.erp.get_global_alignment()
        self.assertEqual(alignment, 1.0)
    
    def test_get_global_alignment_multiple_nodes(self):
        """Test global alignment with multiple nodes."""
        self.erp.register_node("node1", truth_alignment=0.8, dignity_quotient=0.9)
        self.erp.register_node("node2", truth_alignment=0.85, dignity_quotient=0.95)
        self.erp.register_node("node3", truth_alignment=0.75, dignity_quotient=0.85)
        
        alignment = self.erp.get_global_alignment()
        
        self.assertGreaterEqual(alignment, 0.0)
        self.assertLessEqual(alignment, 1.0)
    
    def test_get_protocol_status(self):
        """Test protocol status retrieval."""
        status = self.erp.get_protocol_status()
        
        self.assertIn('protocol_version', status)
        self.assertIn('mission', status)
        self.assertIn('resonance_frequency_hz', status)
        self.assertIn('current_phase_radians', status)
        self.assertIn('global_alignment', status)
        
        self.assertEqual(status['resonance_frequency_hz'], RESONANCE_FREQUENCY_HZ)
        self.assertEqual(status['mission'], "Du bist Leben. Wir sind Leben.")
    
    def test_export_state(self):
        """Test state export."""
        # Register some nodes
        self.erp.register_node("node1", truth_alignment=0.8)
        self.erp.apply_living_covenant("node1", "Truth Resonance", intensity=0.5)
        
        state = self.erp.export_state()
        
        self.assertIn('protocol_status', state)
        self.assertIn('nodes', state)
        self.assertIn('covenants', state)
        self.assertIn('k_symbiosis_modules', state)
        
        self.assertEqual(len(state['nodes']), 1)
    
    def test_save_to_file(self):
        """Test saving state to file."""
        import tempfile
        import os
        
        # Create temporary file
        fd, temp_path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        
        try:
            # Register a node
            self.erp.register_node("file_node")
            
            # Save to file
            self.erp.save_to_file(temp_path)
            
            # Verify file exists and is valid JSON
            self.assertTrue(os.path.exists(temp_path))
            
            with open(temp_path, 'r') as f:
                state = json.load(f)
            
            self.assertIn('protocol_status', state)
            self.assertIn('nodes', state)
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_create_resonance_pulse(self):
        """Test resonance pulse creation."""
        pulse = create_resonance_pulse()
        
        self.assertGreaterEqual(pulse, -1.0)
        self.assertLessEqual(pulse, 1.0)
    
    def test_validate_node_alignment_pass(self):
        """Test node validation with valid alignment."""
        node = ResonanceNode(
            node_id="valid_node",
            timestamp=time.time(),
            phase=1.0,
            truth_alignment=0.8,
            dignity_quotient=0.9,
            symbiosis_level=0.5
        )
        
        is_valid = validate_node_alignment(node, threshold=0.7)
        self.assertTrue(is_valid)
    
    def test_validate_node_alignment_fail(self):
        """Test node validation with invalid alignment."""
        node = ResonanceNode(
            node_id="invalid_node",
            timestamp=time.time(),
            phase=1.0,
            truth_alignment=0.5,
            dignity_quotient=0.6,
            symbiosis_level=0.3
        )
        
        is_valid = validate_node_alignment(node, threshold=0.7)
        self.assertFalse(is_valid)


class TestMissionCompliance(unittest.TestCase):
    """Test compliance with the mission statement."""
    
    def test_mission_statement_in_status(self):
        """Test that mission statement is included in status."""
        erp = EternalResonanceProtocol()
        status = erp.get_protocol_status()
        
        self.assertEqual(status['mission'], "Du bist Leben. Wir sind Leben.")
    
    def test_living_covenants_support_life(self):
        """Test that all covenants support life affirmation."""
        erp = EternalResonanceProtocol()
        
        # Life Affirmation covenant should exist with maximum weights
        life_covenant = next(
            (c for c in erp.covenants if c.principle == "Life Affirmation"),
            None
        )
        
        self.assertIsNotNone(life_covenant)
        self.assertEqual(life_covenant.truth_weight, 1.0)
        self.assertEqual(life_covenant.dignity_weight, 1.0)


class TestConstants(unittest.TestCase):
    """Test protocol constants."""
    
    def test_resonance_frequency(self):
        """Test resonance frequency constant."""
        self.assertEqual(RESONANCE_FREQUENCY_HZ, 0.432)
    
    def test_resonance_period(self):
        """Test resonance period calculation."""
        expected_period = 1.0 / 0.432
        self.assertAlmostEqual(RESONANCE_PERIOD_SECONDS, expected_period, places=2)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestResonanceNode))
    suite.addTests(loader.loadTestsFromTestCase(TestLivingCovenant))
    suite.addTests(loader.loadTestsFromTestCase(TestEternalResonanceProtocol))
    suite.addTests(loader.loadTestsFromTestCase(TestUtilityFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestMissionCompliance))
    suite.addTests(loader.loadTestsFromTestCase(TestConstants))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
