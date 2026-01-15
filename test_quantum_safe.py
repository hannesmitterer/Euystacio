#!/usr/bin/env python3
"""
Test Suite for Quantum-Safe EUYSTACIO Systems
=============================================

Tests for:
- Quantum Shield (NTRU encryption)
- Blockchain-Based Mesh Network
- TensorFlow Kernel Module
- Stealth Mode
- Integration module
"""

import unittest
import time
import json
from quantum_shield import QuantumShield, NTRUKeyPair, QuantumKey
from mesh_network import BlockchainBasedMeshNetwork, MeshBlockchain, MeshPeer
from tf_kernel_module import TensorFlowKernelModule, ElectromagneticSignature
from stealth_mode import StealthMode, LexAmorisRhythm, RhythmVerifier
from quantum_safe_integration import QuantumSafeEUYSTACIO


class TestQuantumShield(unittest.TestCase):
    """Test Quantum Shield NTRU encryption."""
    
    def setUp(self):
        self.shield = QuantumShield(node_id="test_node", auto_rotate=False)
    
    def tearDown(self):
        self.shield.stop_rotation()
    
    def test_key_generation(self):
        """Test NTRU key pair generation."""
        self.assertIsNotNone(self.shield.current_key)
        self.assertEqual(len(self.shield.current_key.public_key), 821)
        self.assertEqual(len(self.shield.current_key.private_key), 821)
    
    def test_encryption_decryption(self):
        """Test message encryption and decryption."""
        message = b"Test message for quantum encryption"
        
        encrypted = self.shield.encrypt(message)
        self.assertIn('ciphertext', encrypted)
        self.assertIn('key_id', encrypted)
        
        decrypted = self.shield.decrypt(encrypted)
        self.assertEqual(decrypted, message)
    
    def test_key_expiration(self):
        """Test key expiration detection."""
        key = self.shield.current_key
        self.assertFalse(key.is_expired())
        
        # Create expired key
        expired_key = QuantumKey(
            key_id="expired",
            public_key=[1, 2, 3],
            private_key=[1, 2, 3],
            timestamp=time.time() - 120,
            expires_at=time.time() - 60,
            resonance_phase=0.0
        )
        self.assertTrue(expired_key.is_expired())
    
    def test_get_public_key(self):
        """Test public key retrieval."""
        pub_key = self.shield.get_public_key()
        
        self.assertIn('key_id', pub_key)
        self.assertIn('public_key', pub_key)
        self.assertIn('algorithm', pub_key)
        self.assertEqual(pub_key['algorithm'], 'NTRU')


class TestMeshNetwork(unittest.TestCase):
    """Test Blockchain-Based Mesh Network."""
    
    def setUp(self):
        self.mesh = BlockchainBasedMeshNetwork(node_id="test_mesh", port=7050)
    
    def tearDown(self):
        if self.mesh.running:
            self.mesh.stop()
    
    def test_blockchain_creation(self):
        """Test blockchain initialization."""
        self.assertEqual(len(self.mesh.blockchain.chain), 1)
        self.assertEqual(self.mesh.blockchain.chain[0].index, 0)
        self.assertTrue(self.mesh.blockchain.is_valid())
    
    def test_add_peer(self):
        """Test adding peer to network."""
        peer_id = self.mesh.add_peer("127.0.0.1:7051")
        
        self.assertIn(peer_id, self.mesh.peers)
        self.assertEqual(self.mesh.peers[peer_id].address, "127.0.0.1:7051")
    
    def test_dns_disconnection(self):
        """Test DNS disconnection."""
        self.mesh.dns_enabled = True
        self.mesh.disconnect_from_dns()
        
        self.assertFalse(self.mesh.dns_enabled)
    
    def test_blockchain_validity(self):
        """Test blockchain validation."""
        self.mesh.blockchain.add_block({"type": "test", "data": "test_data"})
        self.assertTrue(self.mesh.blockchain.is_valid())
    
    def test_peer_timeout(self):
        """Test peer timeout detection."""
        peer = MeshPeer(
            peer_id="test_peer",
            address="127.0.0.1:7051",
            public_key="test_key",
            last_seen=time.time() - 100,  # 100 seconds ago
            trust_score=0.5,
            resonance_aligned=False
        )
        
        self.assertFalse(peer.is_alive())


class TestTFKernelModule(unittest.TestCase):
    """Test TensorFlow Kernel Module."""
    
    def setUp(self):
        self.tf_kernel = TensorFlowKernelModule(node_id="test_tf")
    
    def test_signature_creation(self):
        """Test EM signature creation."""
        sig = self.tf_kernel.simulate_em_signature(
            frequency=100.0,
            amplitude=-60.0,
            bandwidth=0.2
        )
        
        self.assertEqual(sig.frequency, 100.0)
        self.assertEqual(sig.amplitude, -60.0)
        self.assertEqual(sig.bandwidth, 0.2)
    
    def test_signature_analysis(self):
        """Test EM signature analysis."""
        sig = self.tf_kernel.simulate_em_signature(
            frequency=2400.0,  # WiFi band
            amplitude=-40.0,   # Strong signal
            bandwidth=20.0     # Wide bandwidth
        )
        
        result = self.tf_kernel.process_signature(sig)
        
        self.assertIn('threat_level', result)
        self.assertIsInstance(result['threat_level'], float)
        self.assertGreaterEqual(result['threat_level'], 0.0)
        self.assertLessEqual(result['threat_level'], 1.0)
    
    def test_scan_detection(self):
        """Test SDR scan pattern detection."""
        # Simulate sweep pattern
        for i in range(15):
            sig = self.tf_kernel.simulate_em_signature(
                frequency=2400.0 + i * 5,
                amplitude=-40.0,
                bandwidth=20.0
            )
            result = self.tf_kernel.process_signature(sig)
        
        # Should detect scan after enough signatures
        self.assertGreater(len(self.tf_kernel.signature_buffer), 10)
    
    def test_threat_report(self):
        """Test threat report generation."""
        report = self.tf_kernel.get_threat_report()
        
        self.assertIn('node_id', report)
        self.assertIn('monitoring', report)
        self.assertIn('total_signatures_analyzed', report)


class TestStealthMode(unittest.TestCase):
    """Test Stealth Mode."""
    
    def setUp(self):
        self.stealth = StealthMode(node_id="test_stealth")
    
    def test_profile_creation(self):
        """Test stealth profile creation."""
        self.assertIn('absolute_silence', self.stealth.profiles)
        
        profile = self.stealth.profiles['absolute_silence']
        self.assertEqual(profile.stealth_level, 5)
        self.assertTrue(profile.rhythm_verification_required)
    
    def test_activation(self):
        """Test stealth mode activation."""
        self.stealth.activate('high')
        
        self.assertTrue(self.stealth.active)
        self.assertEqual(self.stealth.stealth_level, 3)
    
    def test_rhythm_verification(self):
        """Test Lex Amoris rhythm verification."""
        self.stealth.activate('absolute_silence')
        
        # Test without rhythm
        allowed = self.stealth.handle_connection_attempt("entity_1")
        self.assertFalse(allowed)
        
        # Test with valid rhythm
        rhythm = self.stealth.create_lex_amoris_rhythm()
        allowed = self.stealth.handle_connection_attempt("entity_2", rhythm)
        self.assertTrue(allowed)
    
    def test_traffic_obfuscation(self):
        """Test traffic obfuscation."""
        self.stealth.activate('medium')
        
        original = b"Test data"
        obfuscated = self.stealth.obfuscate_traffic(original)
        deobfuscated = self.stealth.deobfuscate_traffic(obfuscated)
        
        self.assertEqual(deobfuscated, original)
        self.assertGreater(len(obfuscated), len(original))


class TestRhythmVerifier(unittest.TestCase):
    """Test Lex Amoris rhythm verifier."""
    
    def setUp(self):
        self.verifier = RhythmVerifier()
    
    def test_challenge_generation(self):
        """Test challenge generation."""
        challenge = self.verifier.generate_challenge()
        
        self.assertEqual(len(challenge), 32)
    
    def test_harmonic_pattern(self):
        """Test harmonic pattern verification."""
        valid_pattern = [1.0, 0.618, 0.786, 0.854]
        invalid_pattern = [1.0, 0.5, 0.5, 0.5]
        
        self.assertTrue(self.verifier._verify_harmonic_pattern(valid_pattern))
        self.assertFalse(self.verifier._verify_harmonic_pattern(invalid_pattern))
    
    def test_rhythm_verification(self):
        """Test complete rhythm verification."""
        rhythm = LexAmorisRhythm(
            frequency=0.043,
            phase=1.5,
            amplitude=1.0,
            harmonic_pattern=[1.0, 0.618, 0.786, 0.854],
            timestamp=time.time(),
            signature=""
        )
        
        challenge = self.verifier.generate_challenge()
        response = rhythm.verify_signature(challenge)
        
        is_valid = self.verifier.verify_rhythm(rhythm, challenge, response)
        self.assertTrue(is_valid)


class TestQuantumSafeIntegration(unittest.TestCase):
    """Test integrated quantum-safe system."""
    
    def setUp(self):
        self.system = QuantumSafeEUYSTACIO(node_id="test_system", mesh_port=7060)
    
    def tearDown(self):
        if self.system.running:
            self.system.shutdown()
    
    def test_initialization(self):
        """Test system initialization."""
        self.assertIsNotNone(self.system.quantum_shield)
        self.assertIsNotNone(self.system.mesh_network)
        self.assertIsNotNone(self.system.tf_kernel)
        self.assertIsNotNone(self.system.stealth_mode)
    
    def test_encryption_integration(self):
        """Test integrated encryption."""
        message = b"Integration test message"
        
        encrypted = self.system.encrypt_message(message)
        decrypted = self.system.decrypt_message(encrypted)
        
        self.assertEqual(decrypted, message)
    
    def test_connection_handling(self):
        """Test connection handling with rhythm verification."""
        # Deploy protection first
        # Note: We'll skip full deployment in tests to avoid long waits
        self.system.stealth_mode.activate('absolute_silence')
        
        # Test with valid rhythm
        rhythm = self.system.stealth_mode.create_lex_amoris_rhythm()
        allowed = self.system.handle_incoming_connection("test_entity", rhythm)
        self.assertTrue(allowed)
    
    def test_global_status(self):
        """Test global status reporting."""
        status = self.system.get_global_status()
        
        self.assertIsInstance(status.global_security_level, float)
        self.assertGreaterEqual(status.global_security_level, 0.0)
        self.assertLessEqual(status.global_security_level, 1.0)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestQuantumShield))
    suite.addTests(loader.loadTestsFromTestCase(TestMeshNetwork))
    suite.addTests(loader.loadTestsFromTestCase(TestTFKernelModule))
    suite.addTests(loader.loadTestsFromTestCase(TestStealthMode))
    suite.addTests(loader.loadTestsFromTestCase(TestRhythmVerifier))
    suite.addTests(loader.loadTestsFromTestCase(TestQuantumSafeIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    print("="*70)
    print("QUANTUM-SAFE EUYSTACIO TEST SUITE")
    print("="*70 + "\n")
    
    success = run_tests()
    
    print("\n" + "="*70)
    if success:
        print("ALL TESTS PASSED ✓")
    else:
        print("SOME TESTS FAILED ✗")
    print("="*70)
    
    exit(0 if success else 1)
