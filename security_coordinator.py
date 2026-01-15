#!/usr/bin/env python3
"""
Security Coordinator Module

Integrates and orchestrates all security components for comprehensive
protection across all attack scenarios.
"""

import time
from typing import Dict, List, Optional
from dataclasses import dataclass

# Import all security modules
from security_quantum_crypto import QuantumSafeCrypto, NTRUKeyPair
from security_em_hardening import EMHardeningCoordinator
from security_early_warning import EarlyWarningSystem
from security_blockchain_validator import ForkConsensusValidator
from security_data_poisoning import DataPoisoningDetector, DataSanitizer
from security_geozone_filter import GeoZoneFilter, ConnectionAttempt, GeoLocation
from security_mesh_network import MeshNetworkTopology


@dataclass
class SecurityStatus:
    """Overall security system status."""
    active: bool
    threat_level: str  # 'safe', 'low', 'medium', 'high', 'critical'
    components_active: Dict[str, bool]
    alerts_count: int
    last_update: float
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'active': self.active,
            'threat_level': self.threat_level,
            'components_active': self.components_active,
            'alerts_count': self.alerts_count,
            'last_update': self.last_update
        }


class SecurityCoordinator:
    """
    Coordinates all security subsystems for comprehensive protection.
    
    Integrates:
    - Scenario A: Quantum crypto, EM hardening, early warning
    - Scenario B: Blockchain validation, data poisoning detection
    - Scenario C: Geo-zone filtering, mesh networking
    """
    
    def __init__(self, node_id: str = 'euystacio_main'):
        """
        Initialize security coordinator.
        
        Args:
            node_id: Unique identifier for this node
        """
        self.node_id = node_id
        self.active = False
        self.start_time: Optional[float] = None
        
        # Scenario A: Spionage und Datenextraktion
        self.quantum_crypto = QuantumSafeCrypto('ntru_hps_2048_509')
        self.em_hardening = EMHardeningCoordinator(shielding_level='high')
        self.early_warning = EarlyWarningSystem()
        
        # Scenario B: Systemstörungen und Sabotage
        self.blockchain_validator = ForkConsensusValidator()
        self.data_poisoning_detector = DataPoisoningDetector(feature_dimension=10)
        self.data_sanitizer = DataSanitizer(self.data_poisoning_detector)
        
        # Scenario C: Globale Angriffe und Koordination
        self.geozone_filter = GeoZoneFilter()
        self.mesh_network = MeshNetworkTopology(node_id)
        
        # Unified state
        self.key_pair: Optional[NTRUKeyPair] = None
        self.total_alerts = 0
        self.threat_level = 'safe'
    
    def initialize(self):
        """Initialize all security subsystems."""
        print("Initializing comprehensive security system...")
        
        # Generate quantum-safe keys
        self.key_pair = self.quantum_crypto.generate_keypair()
        print(f"✓ Quantum-safe keys generated (Security: {self.quantum_crypto.get_security_level()} bits)")
        
        # Start EM hardening
        self.em_hardening.start_protection(seed=f"{self.node_id}_em_seed")
        print("✓ Electromagnetic hardening active")
        
        # Start early warning system
        self.early_warning.start()
        print("✓ Early warning system online")
        
        # Register blockchain chain
        main_chain = self.blockchain_validator.register_chain("main_chain")
        print("✓ Blockchain validator initialized")
        
        # Initialize data poisoning detection
        print("✓ Data poisoning detector ready")
        
        # Geo-zone filter already initialized
        print("✓ Geo-zone filter configured")
        
        # Mesh network already initialized
        print("✓ Mesh network topology established")
        
        self.active = True
        self.start_time = time.time()
        print(f"\n✓ Security Coordinator '{self.node_id}' fully operational")
        print("Mission: Du bist Leben. Wir sind Leben.\n")
    
    def update(self):
        """Update all security subsystems (call regularly)."""
        if not self.active:
            return
        
        # Update EM hardening
        self.em_hardening.update()
        
        # Check early warning system
        threats = self.early_warning.check_for_threats()
        if threats:
            self.total_alerts += len(threats)
            self._handle_threats(threats)
        
        # Check mesh network health
        self.mesh_network.check_node_health()
        
        # Update threat level
        self._update_threat_level()
    
    def _handle_threats(self, threats: List[Dict]):
        """
        Handle detected threats.
        
        Args:
            threats: List of threat detections
        """
        for threat in threats:
            classification = threat.get('classification', 'unknown')
            
            if classification == 'critical':
                # Escalate to critical threat level
                self.threat_level = 'critical'
                
                # Trigger enhanced EM hardening
                self.em_hardening.freq_hopping.hop_to_next_channel()
                
            elif classification == 'warning':
                # Moderate threat response
                if self.threat_level in ['safe', 'low']:
                    self.threat_level = 'medium'
    
    def _update_threat_level(self):
        """Update overall threat level based on all subsystems."""
        # Aggregate threat indicators
        indicators = []
        
        # Early warning threats
        ews_stats = self.early_warning.get_statistics()
        if ews_stats['alert_count'] > 10:
            indicators.append('high')
        elif ews_stats['alert_count'] > 5:
            indicators.append('medium')
        
        # Geo-zone blocks
        geo_stats = self.geozone_filter.get_statistics()
        if geo_stats['block_rate'] > 0.5:  # >50% blocks
            indicators.append('high')
        elif geo_stats['block_rate'] > 0.2:  # >20% blocks
            indicators.append('medium')
        
        # Blockchain forks
        fork_summary = self.blockchain_validator.get_fork_summary()
        if fork_summary['by_severity'].get('critical', 0) > 0:
            indicators.append('critical')
        elif fork_summary['by_severity'].get('high', 0) > 0:
            indicators.append('high')
        
        # Data poisoning
        poisoning_rate = self.data_poisoning_detector.get_poisoning_rate()
        if poisoning_rate > 0.3:  # >30% poisoned
            indicators.append('high')
        elif poisoning_rate > 0.1:  # >10% poisoned
            indicators.append('medium')
        
        # Select highest threat level
        if 'critical' in indicators:
            self.threat_level = 'critical'
        elif 'high' in indicators:
            self.threat_level = 'high'
        elif 'medium' in indicators:
            self.threat_level = 'medium'
        elif 'low' in indicators:
            self.threat_level = 'low'
        else:
            self.threat_level = 'safe'
    
    def encrypt_message(self, message: str, recipient_public_key: str) -> str:
        """
        Encrypt message using quantum-safe cryptography.
        
        Args:
            message: Message to encrypt
            recipient_public_key: Recipient's public key
            
        Returns:
            Encrypted ciphertext
        """
        return self.quantum_crypto.encrypt(
            message.encode('utf-8'),
            recipient_public_key
        )
    
    def decrypt_message(self, ciphertext: str) -> str:
        """
        Decrypt message using quantum-safe cryptography.
        
        Args:
            ciphertext: Encrypted message
            
        Returns:
            Decrypted plaintext
        """
        if not self.key_pair:
            raise ValueError("Key pair not initialized")
        
        decrypted = self.quantum_crypto.decrypt(
            ciphertext,
            self.key_pair.private_key
        )
        return decrypted.decode('utf-8')
    
    def get_comprehensive_status(self) -> SecurityStatus:
        """
        Get comprehensive security status.
        
        Returns:
            SecurityStatus object
        """
        return SecurityStatus(
            active=self.active,
            threat_level=self.threat_level,
            components_active={
                'quantum_crypto': self.key_pair is not None,
                'em_hardening': self.em_hardening.active,
                'early_warning': self.early_warning.started,
                'blockchain_validator': len(self.blockchain_validator.chains) > 0,
                'data_poisoning': True,
                'geozone_filter': True,
                'mesh_network': self.mesh_network.nodes is not None
            },
            alerts_count=self.total_alerts,
            last_update=time.time()
        )
    
    def get_detailed_report(self) -> Dict:
        """
        Get detailed security report from all subsystems.
        
        Returns:
            Comprehensive report dictionary
        """
        return {
            'coordinator': {
                'node_id': self.node_id,
                'active': self.active,
                'uptime_seconds': time.time() - self.start_time if self.start_time else 0,
                'threat_level': self.threat_level,
                'total_alerts': self.total_alerts
            },
            'scenario_a': {
                'quantum_crypto': {
                    'security_level': self.quantum_crypto.get_security_level(),
                    'parameter_set': self.quantum_crypto.parameter_set,
                    'key_generated': self.key_pair is not None
                },
                'em_hardening': self.em_hardening.get_comprehensive_status(),
                'early_warning': self.early_warning.get_statistics()
            },
            'scenario_b': {
                'blockchain': self.blockchain_validator.get_consensus_status(),
                'fork_summary': self.blockchain_validator.get_fork_summary(),
                'data_poisoning': self.data_poisoning_detector.get_statistics()
            },
            'scenario_c': {
                'geozone': self.geozone_filter.get_statistics(),
                'mesh_network': self.mesh_network.get_network_statistics()
            }
        }
    
    def shutdown(self):
        """Shutdown all security subsystems gracefully."""
        print("Shutting down security coordinator...")
        
        self.em_hardening.stop_protection()
        self.early_warning.stop()
        self.active = False
        
        print("✓ Security coordinator shutdown complete")


if __name__ == '__main__':
    print("=== Euystacio Security Coordinator Demo ===")
    print()
    
    # Initialize coordinator
    coordinator = SecurityCoordinator('demo_node')
    coordinator.initialize()
    
    print("\n--- Running Security Operations ---\n")
    
    # Simulate some operations
    for i in range(5):
        time.sleep(0.1)
        coordinator.update()
    
    # Test encryption
    if coordinator.key_pair:
        message = "Du bist Leben. Wir sind Leben."
        print(f"Original Message: {message}")
        
        encrypted = coordinator.encrypt_message(
            message,
            coordinator.key_pair.public_key
        )
        print(f"Encrypted: {encrypted[:64]}...")
        
        decrypted = coordinator.decrypt_message(encrypted)
        print(f"Decrypted: {decrypted}")
        print()
    
    # Get comprehensive status
    status = coordinator.get_comprehensive_status()
    print("Security Status:")
    print(f"  Active: {status.active}")
    print(f"  Threat Level: {status.threat_level.upper()}")
    print(f"  Total Alerts: {status.alerts_count}")
    print()
    
    print("Component Status:")
    for component, active in status.components_active.items():
        status_str = "✓ ACTIVE" if active else "✗ INACTIVE"
        print(f"  {component}: {status_str}")
    
    print()
    
    # Get detailed report
    report = coordinator.get_detailed_report()
    print(f"Uptime: {report['coordinator']['uptime_seconds']:.2f}s")
    print(f"Security Level: {report['scenario_a']['quantum_crypto']['security_level']} bits")
    print(f"EM Security Score: {report['scenario_a']['em_hardening']['security_score']:.2f}/100")
    print(f"Network Nodes: {report['scenario_c']['mesh_network']['total_nodes']}")
    
    print()
    
    # Shutdown
    coordinator.shutdown()
    
    print()
    print("✓ Comprehensive security demonstration complete")
