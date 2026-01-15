#!/usr/bin/env python3
"""
Security Module Test Suite

Comprehensive tests for all security enhancement modules.
"""

import unittest
import time
import hashlib
from security_quantum_crypto import QuantumSafeCrypto, NTRUKeyPair
from security_em_hardening import (
    AdaptiveFrequencyHopping, FaradayProtection, EMHardeningCoordinator
)
from security_early_warning import (
    ProtocolAnomalyDetector, FrequencyAnomalyDetector, EarlyWarningSystem
)
from security_blockchain_validator import (
    BlockchainChain, ForkConsensusValidator
)
from security_data_poisoning import (
    DataSample, DataPoisoningDetector, DataSanitizer
)
from security_geozone_filter import (
    GeoZoneFilter, GeoLocation, ConnectionAttempt
)
from security_mesh_network import MeshNetworkTopology, NodeStatus
from security_coordinator import SecurityCoordinator


class TestQuantumCrypto(unittest.TestCase):
    """Test quantum-safe cryptography."""
    
    def test_keypair_generation(self):
        """Test NTRU key pair generation."""
        crypto = QuantumSafeCrypto('ntru_hps_2048_509')
        keypair = crypto.generate_keypair()
        
        self.assertIsInstance(keypair, NTRUKeyPair)
        self.assertIsNotNone(keypair.public_key)
        self.assertIsNotNone(keypair.private_key)
        self.assertEqual(keypair.parameter_set, 'ntru_hps_2048_509')
    
    def test_encryption_decryption(self):
        """Test encryption and decryption."""
        crypto = QuantumSafeCrypto('ntru_hps_2048_509')
        keypair = crypto.generate_keypair()
        
        message = b"Test message"
        ciphertext = crypto.encrypt(message, keypair.public_key)
        
        self.assertIsInstance(ciphertext, str)
        self.assertGreater(len(ciphertext), 0)
    
    def test_security_level(self):
        """Test security level reporting."""
        crypto = QuantumSafeCrypto('ntru_hps_2048_509')
        level = crypto.get_security_level()
        
        self.assertEqual(level, 128)


class TestEMHardening(unittest.TestCase):
    """Test electromagnetic hardening."""
    
    def test_frequency_hopping_init(self):
        """Test frequency hopping initialization."""
        fh = AdaptiveFrequencyHopping()
        
        self.assertEqual(len(fh.channels), 79)
        self.assertEqual(fh.base_frequency, 2400.0)
    
    def test_hop_sequence_generation(self):
        """Test hop sequence generation."""
        fh = AdaptiveFrequencyHopping()
        sequence = fh.generate_hop_sequence("test_seed")
        
        self.assertEqual(len(sequence), 79)
        self.assertEqual(len(set(sequence)), 79)  # All unique
    
    def test_channel_hopping(self):
        """Test frequency hopping."""
        fh = AdaptiveFrequencyHopping()
        fh.generate_hop_sequence()
        
        channel1 = fh.hop_to_next_channel()
        channel2 = fh.hop_to_next_channel()
        
        self.assertNotEqual(channel1.frequency_mhz, channel2.frequency_mhz)
    
    def test_faraday_protection(self):
        """Test Faraday protection."""
        faraday = FaradayProtection('high')
        
        self.assertEqual(faraday.attenuation_db, 90)
        effectiveness = faraday.get_effectiveness()
        self.assertGreater(effectiveness, 99.9)


class TestEarlyWarning(unittest.TestCase):
    """Test early warning system."""
    
    def test_protocol_detector(self):
        """Test protocol anomaly detection."""
        detector = ProtocolAnomalyDetector()
        
        # Add normal samples
        for i in range(20):
            detector.add_sample(10.0, 1500, 0.01)
        
        # Add anomalous sample
        detector.add_sample(100.0, 5000, 0.5)
        
        anomalies = detector.detect_anomalies()
        self.assertGreater(len(anomalies), 0)
    
    def test_frequency_detector(self):
        """Test frequency anomaly detection."""
        detector = FrequencyAnomalyDetector(2400.0, tolerance_mhz=1.0)
        
        # Normal sample
        detector.add_spectrum_sample(2400.5, -50.0)
        anomalies1 = detector.detect_anomalies()
        self.assertEqual(len(anomalies1), 0)
        
        # Anomalous sample
        detector.add_spectrum_sample(2410.0, -30.0)
        anomalies2 = detector.detect_anomalies()
        self.assertGreater(len(anomalies2), 0)
    
    def test_early_warning_system(self):
        """Test integrated early warning system."""
        ews = EarlyWarningSystem()
        ews.start()
        
        # Add samples
        for i in range(10):
            ews.add_protocol_sample(10.0, 1500, 0.01)
        
        stats = ews.get_statistics()
        self.assertTrue(stats['active'])
        self.assertEqual(stats['protocol_samples'], 10)


class TestBlockchainValidator(unittest.TestCase):
    """Test blockchain fork validation."""
    
    def test_chain_creation(self):
        """Test blockchain chain creation."""
        chain = BlockchainChain("test_chain")
        
        self.assertEqual(len(chain.headers), 1)  # Genesis block
        self.assertEqual(chain.headers[0].height, 0)
    
    def test_block_addition(self):
        """Test adding blocks."""
        chain = BlockchainChain("test_chain")
        
        merkle = hashlib.sha256(b"transactions").hexdigest()
        header = chain.add_header(merkle, nonce=100)
        
        self.assertEqual(header.height, 1)
        self.assertEqual(header.previous_hash, chain.headers[0].hash)
    
    def test_fork_detection(self):
        """Test fork detection."""
        validator = ForkConsensusValidator()
        
        # Create two chains
        chain1 = validator.register_chain("chain1")
        chain2 = validator.register_chain("chain2")
        
        # Add same blocks to both
        for i in range(3):
            merkle = hashlib.sha256(f"tx_{i}".encode()).hexdigest()
            chain1.add_header(merkle, i * 100)
            chain2.add_header(merkle, i * 100)
        
        # Fork divergence
        chain1.add_header(hashlib.sha256(b"fork1").hexdigest(), 300)
        chain2.add_header(hashlib.sha256(b"fork2").hexdigest(), 400)
        
        forks = validator.detect_forks()
        self.assertGreater(len(forks), 0)


class TestDataPoisoning(unittest.TestCase):
    """Test data poisoning detection."""
    
    def test_detector_init(self):
        """Test detector initialization."""
        detector = DataPoisoningDetector(feature_dimension=5)
        
        self.assertEqual(detector.feature_dimension, 5)
        self.assertEqual(len(detector.clean_samples), 0)
    
    def test_clean_sample_addition(self):
        """Test adding clean samples."""
        detector = DataPoisoningDetector(feature_dimension=5)
        
        sample = DataSample(
            sample_id="clean_1",
            features=[0.5, 0.5, 0.5, 0.5, 0.5],
            label="normal",
            timestamp=time.time(),
            source="trusted"
        )
        
        detection = detector.add_sample(sample)
        self.assertIsNone(detection)
        self.assertEqual(len(detector.clean_samples), 1)
    
    def test_poisoned_sample_detection(self):
        """Test poisoned sample detection."""
        detector = DataPoisoningDetector(feature_dimension=5)
        
        # Add clean samples
        for i in range(20):
            sample = DataSample(
                sample_id=f"clean_{i}",
                features=[0.5, 0.5, 0.5, 0.5, 0.5],
                label="normal",
                timestamp=time.time(),
                source="trusted"
            )
            detector.add_sample(sample)
        
        # Add poisoned sample
        poisoned = DataSample(
            sample_id="poisoned",
            features=[10.0, 10.0, 10.0, 10.0, 10.0],
            label="attack",
            timestamp=time.time(),
            source="untrusted"
        )
        
        detection = detector.add_sample(poisoned)
        self.assertIsNotNone(detection)


class TestGeoZoneFilter(unittest.TestCase):
    """Test geo-zone filtering."""
    
    def test_filter_initialization(self):
        """Test filter initialization with default zones."""
        geo_filter = GeoZoneFilter()
        
        self.assertGreater(len(geo_filter.zones), 0)
    
    def test_allowed_connection(self):
        """Test allowing legitimate connection."""
        geo_filter = GeoZoneFilter()
        
        attempt = ConnectionAttempt(
            ip_address="192.168.1.1",
            location=GeoLocation(48.8566, 2.3522, 'FR', 'EU'),
            timestamp=time.time(),
            user_agent="Mozilla/5.0",
            request_type="GET"
        )
        
        allowed, reason = geo_filter.evaluate_connection(attempt)
        self.assertTrue(allowed)
    
    def test_blocked_connection(self):
        """Test blocking suspicious connection."""
        geo_filter = GeoZoneFilter()
        
        attempt = ConnectionAttempt(
            ip_address="10.0.0.1",
            location=GeoLocation(0.0, 0.0, 'ZZ', 'Unknown'),
            timestamp=time.time(),
            user_agent="Scanner",
            request_type="POST"
        )
        
        allowed, reason = geo_filter.evaluate_connection(attempt)
        self.assertFalse(allowed)


class TestMeshNetwork(unittest.TestCase):
    """Test mesh network architecture."""
    
    def test_network_initialization(self):
        """Test mesh network initialization."""
        mesh = MeshNetworkTopology('local_node')
        
        self.assertEqual(mesh.local_node_id, 'local_node')
        self.assertIn('local_node', mesh.nodes)
    
    def test_peer_addition(self):
        """Test adding peers."""
        mesh = MeshNetworkTopology('local_node')
        
        peer = mesh.add_peer(
            'peer1',
            'mesh://peer1',
            hashlib.sha256(b'key1').hexdigest()
        )
        
        self.assertEqual(peer.node_id, 'peer1')
        self.assertIn('peer1', mesh.nodes)
    
    def test_route_finding(self):
        """Test route finding."""
        mesh = MeshNetworkTopology('local_node')
        
        # Add peers
        mesh.add_peer('peer1', 'mesh://peer1', hashlib.sha256(b'k1').hexdigest())
        mesh.add_peer('peer2', 'mesh://peer2', hashlib.sha256(b'k2').hexdigest())
        
        # Connect peers
        mesh.connect_peers('peer1', 'peer2')
        
        # Find routes
        routes = mesh.find_routes('peer2')
        
        self.assertGreater(len(routes), 0)


class TestSecurityCoordinator(unittest.TestCase):
    """Test security coordinator integration."""
    
    def test_coordinator_initialization(self):
        """Test coordinator initialization."""
        coordinator = SecurityCoordinator('test_node')
        coordinator.initialize()
        
        self.assertTrue(coordinator.active)
        self.assertIsNotNone(coordinator.key_pair)
    
    def test_encryption_integration(self):
        """Test encryption through coordinator."""
        coordinator = SecurityCoordinator('test_node')
        coordinator.initialize()
        
        message = "Test message"
        encrypted = coordinator.encrypt_message(
            message,
            coordinator.key_pair.public_key
        )
        
        self.assertIsInstance(encrypted, str)
        self.assertGreater(len(encrypted), 0)
    
    def test_status_reporting(self):
        """Test status reporting."""
        coordinator = SecurityCoordinator('test_node')
        coordinator.initialize()
        
        status = coordinator.get_comprehensive_status()
        
        self.assertTrue(status.active)
        self.assertIn(status.threat_level, ['safe', 'low', 'medium', 'high', 'critical'])


def run_tests():
    """Run all security tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestQuantumCrypto))
    suite.addTests(loader.loadTestsFromTestCase(TestEMHardening))
    suite.addTests(loader.loadTestsFromTestCase(TestEarlyWarning))
    suite.addTests(loader.loadTestsFromTestCase(TestBlockchainValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestDataPoisoning))
    suite.addTests(loader.loadTestsFromTestCase(TestGeoZoneFilter))
    suite.addTests(loader.loadTestsFromTestCase(TestMeshNetwork))
    suite.addTests(loader.loadTestsFromTestCase(TestSecurityCoordinator))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    print("=== Euystacio Security Module Test Suite ===")
    print()
    success = run_tests()
    exit(0 if success else 1)
