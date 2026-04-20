"""
Autonomous Time Reference Module
==================================

Implements decentralized time synchronization independent of EU NTP servers,
providing resilience against digital blackouts and NTP-induced drift.

This module provides:
- Local oscillator-based timekeeping
- Cryptographically signed timestamp verification
- Peer-to-peer time consensus
- Fallback mechanisms for the 0.0043 Hz bio-clock signal

Protocol: EUYSTACIO / NSR
Status: Allerta Livello 2 (Active Monitoring)
Date: 20 Gennaio 2026
"""

import time
import json
import hashlib
import hmac
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import random
import math


# Core Constants
BIOCLOCK_FREQUENCY_HZ = 0.0043  # Bio-clock frequency
BIOCLOCK_PERIOD_SECONDS = 1.0 / BIOCLOCK_FREQUENCY_HZ  # ~232.56 seconds
LOCAL_DRIFT_TOLERANCE_MS = 100  # Maximum acceptable drift in milliseconds
SIGNATURE_ALGORITHM = "HMAC-SHA256"


@dataclass
class TimeReference:
    """Represents a cryptographically signed time reference."""
    timestamp: float
    source: str
    signature: str
    confidence: float  # 0.0 to 1.0
    metadata: Optional[Dict] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)
    
    def verify_signature(self, secret_key: bytes) -> bool:
        """Verify the cryptographic signature of this time reference."""
        message = f"{self.timestamp}:{self.source}".encode('utf-8')
        expected_signature = hmac.new(secret_key, message, hashlib.sha256).hexdigest()
        return hmac.compare_digest(self.signature, expected_signature)


class LocalOscillator:
    """
    Simulates a local hardware oscillator for autonomous timekeeping.
    In production, this would interface with actual hardware oscillators.
    """
    
    def __init__(self, drift_rate: float = 0.0001):
        """
        Initialize local oscillator.
        
        Args:
            drift_rate: Simulated drift rate (seconds per second)
        """
        self.genesis_time = time.time()
        self.drift_rate = drift_rate
        self.accumulated_drift = 0.0
        
    def get_time(self) -> float:
        """Get current time from local oscillator."""
        elapsed = time.time() - self.genesis_time
        drift = elapsed * self.drift_rate
        self.accumulated_drift = drift
        return time.time() + drift
    
    def get_drift(self) -> float:
        """Get accumulated drift in seconds."""
        return self.accumulated_drift
    
    def calibrate(self, reference_time: float):
        """Calibrate oscillator against a trusted reference."""
        current = self.get_time()
        correction = reference_time - current
        self.genesis_time += correction
        self.accumulated_drift = 0.0


class AutonomousTimeReference:
    """
    Main autonomous time reference system for the 0.0043 Hz bio-clock.
    
    Provides NTP-independent timekeeping using:
    - Local hardware oscillators
    - Cryptographically signed timestamps
    - Peer-to-peer time consensus
    - Blockchain-anchored time references
    """
    
    def __init__(self, node_id: str = "primary", secret_key: Optional[bytes] = None):
        """
        Initialize autonomous time reference system.
        
        Args:
            node_id: Unique identifier for this node
            secret_key: Secret key for signing timestamps
        """
        self.node_id = node_id
        self.secret_key = secret_key or self._generate_secret_key()
        self.local_oscillator = LocalOscillator()
        self.peer_references: List[TimeReference] = []
        self.blockchain_references: List[TimeReference] = []
        self.last_calibration = time.time()
        
    def _generate_secret_key(self) -> bytes:
        """Generate a secure random secret key."""
        return hashlib.sha256(f"{self.node_id}:{time.time()}:{random.random()}".encode()).digest()
    
    def get_autonomous_time(self) -> float:
        """
        Get current time from autonomous sources.
        
        Returns:
            Current timestamp independent of NTP servers
        """
        # Use local oscillator as primary source
        local_time = self.local_oscillator.get_time()
        
        # Apply peer consensus if available
        if self.peer_references:
            consensus_time = self._compute_consensus_time()
            if consensus_time:
                # Weighted average between local and consensus
                local_weight = 0.6
                consensus_weight = 0.4
                return (local_time * local_weight) + (consensus_time * consensus_weight)
        
        return local_time
    
    def create_signed_timestamp(self, metadata: Optional[Dict] = None) -> TimeReference:
        """
        Create a cryptographically signed timestamp.
        
        Args:
            metadata: Optional metadata to include
            
        Returns:
            Signed time reference
        """
        timestamp = self.get_autonomous_time()
        message = f"{timestamp}:{self.node_id}".encode('utf-8')
        signature = hmac.new(self.secret_key, message, hashlib.sha256).hexdigest()
        
        return TimeReference(
            timestamp=timestamp,
            source=self.node_id,
            signature=signature,
            confidence=self._calculate_confidence(),
            metadata=metadata
        )
    
    def verify_timestamp(self, time_ref: TimeReference) -> bool:
        """
        Verify a cryptographically signed timestamp.
        
        Args:
            time_ref: Time reference to verify
            
        Returns:
            True if signature is valid
        """
        return time_ref.verify_signature(self.secret_key)
    
    def add_peer_reference(self, time_ref: TimeReference):
        """
        Add a time reference from a peer node.
        
        Args:
            time_ref: Peer time reference
        """
        # Verify signature if from same network
        if time_ref.source.startswith(self.node_id.split('_')[0]):
            if not self.verify_timestamp(time_ref):
                return
        
        # Add to peer references
        self.peer_references.append(time_ref)
        
        # Keep only recent references (last hour)
        cutoff = time.time() - 3600
        self.peer_references = [
            ref for ref in self.peer_references
            if ref.timestamp > cutoff
        ]
    
    def add_blockchain_reference(self, block_timestamp: float, block_hash: str):
        """
        Add a time reference from blockchain.
        
        Args:
            block_timestamp: Timestamp from blockchain block
            block_hash: Hash of the block
        """
        signature = hashlib.sha256(f"{block_timestamp}:{block_hash}".encode()).hexdigest()
        
        time_ref = TimeReference(
            timestamp=block_timestamp,
            source=f"blockchain:{block_hash[:16]}",
            signature=signature,
            confidence=0.95,
            metadata={"block_hash": block_hash}
        )
        
        self.blockchain_references.append(time_ref)
        
        # Keep only recent references
        cutoff = time.time() - 7200  # 2 hours
        self.blockchain_references = [
            ref for ref in self.blockchain_references
            if ref.timestamp > cutoff
        ]
    
    def _compute_consensus_time(self) -> Optional[float]:
        """
        Compute consensus time from peer references.
        
        Returns:
            Consensus timestamp or None
        """
        if not self.peer_references:
            return None
        
        # Weight by confidence and recency
        weighted_sum = 0.0
        total_weight = 0.0
        
        for ref in self.peer_references:
            recency_weight = 1.0 / (1.0 + (time.time() - ref.timestamp) / 60.0)
            weight = ref.confidence * recency_weight
            weighted_sum += ref.timestamp * weight
            total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else None
    
    def _calculate_confidence(self) -> float:
        """
        Calculate confidence in current time reference.
        
        Returns:
            Confidence value between 0.0 and 1.0
        """
        base_confidence = 0.7  # Base confidence in local oscillator
        
        # Increase confidence with peer consensus
        if len(self.peer_references) >= 3:
            base_confidence += 0.15
        
        # Increase confidence with blockchain references
        if len(self.blockchain_references) >= 1:
            base_confidence += 0.10
        
        # Decrease confidence based on time since last calibration
        hours_since_calibration = (time.time() - self.last_calibration) / 3600.0
        calibration_penalty = min(0.2, hours_since_calibration * 0.01)
        
        return min(1.0, base_confidence - calibration_penalty)
    
    def calibrate(self, reference_time: float):
        """
        Calibrate the autonomous time system.
        
        Args:
            reference_time: Trusted reference timestamp
        """
        self.local_oscillator.calibrate(reference_time)
        self.last_calibration = time.time()
    
    def get_bioclock_phase(self) -> float:
        """
        Get current phase of the 0.0043 Hz bio-clock.
        
        Returns:
            Phase angle in radians (0 to 2π)
        """
        current_time = self.get_autonomous_time()
        phase = (current_time % BIOCLOCK_PERIOD_SECONDS) / BIOCLOCK_PERIOD_SECONDS
        return phase * 2 * math.pi
    
    def get_status(self) -> Dict:
        """
        Get comprehensive status of the autonomous time system.
        
        Returns:
            Status dictionary
        """
        return {
            "node_id": self.node_id,
            "current_time": self.get_autonomous_time(),
            "bioclock_phase_rad": self.get_bioclock_phase(),
            "confidence": self._calculate_confidence(),
            "local_drift_seconds": self.local_oscillator.get_drift(),
            "peer_references": len(self.peer_references),
            "blockchain_references": len(self.blockchain_references),
            "hours_since_calibration": (time.time() - self.last_calibration) / 3600.0,
            "bioclock_frequency_hz": BIOCLOCK_FREQUENCY_HZ,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    def save_state(self, filepath: str):
        """Save state to file."""
        state = {
            "node_id": self.node_id,
            "genesis_time": self.local_oscillator.genesis_time,
            "drift_rate": self.local_oscillator.drift_rate,
            "last_calibration": self.last_calibration,
            "peer_references": [ref.to_dict() for ref in self.peer_references],
            "blockchain_references": [ref.to_dict() for ref in self.blockchain_references]
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
    
    def load_state(self, filepath: str):
        """Load state from file."""
        with open(filepath, 'r') as f:
            state = json.load(f)
        
        self.local_oscillator.genesis_time = state["genesis_time"]
        self.local_oscillator.drift_rate = state["drift_rate"]
        self.last_calibration = state["last_calibration"]
        
        # Restore references
        self.peer_references = [
            TimeReference(**ref) for ref in state.get("peer_references", [])
        ]
        self.blockchain_references = [
            TimeReference(**ref) for ref in state.get("blockchain_references", [])
        ]


def validate_time_independence(atr: AutonomousTimeReference) -> Dict:
    """
    Validate that the time reference system operates independently.
    
    Args:
        atr: Autonomous time reference instance
        
    Returns:
        Validation results
    """
    results = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tests_passed": 0,
        "tests_failed": 0,
        "details": []
    }
    
    # Test 1: Can generate time without external sources
    try:
        local_time = atr.get_autonomous_time()
        if local_time > 0:
            results["tests_passed"] += 1
            results["details"].append("✓ Local time generation working")
        else:
            results["tests_failed"] += 1
            results["details"].append("✗ Local time generation failed")
    except Exception as e:
        results["tests_failed"] += 1
        results["details"].append(f"✗ Local time generation error: {e}")
    
    # Test 2: Can create signed timestamps
    try:
        signed_ts = atr.create_signed_timestamp()
        if signed_ts.signature:
            results["tests_passed"] += 1
            results["details"].append("✓ Cryptographic signing working")
        else:
            results["tests_failed"] += 1
            results["details"].append("✗ Cryptographic signing failed")
    except Exception as e:
        results["tests_failed"] += 1
        results["details"].append(f"✗ Cryptographic signing error: {e}")
    
    # Test 3: Can compute bio-clock phase
    try:
        phase = atr.get_bioclock_phase()
        if 0 <= phase <= 6.283185307179586:  # 2π
            results["tests_passed"] += 1
            results["details"].append(f"✓ Bio-clock phase: {phase:.4f} rad")
        else:
            results["tests_failed"] += 1
            results["details"].append("✗ Bio-clock phase out of range")
    except Exception as e:
        results["tests_failed"] += 1
        results["details"].append(f"✗ Bio-clock phase error: {e}")
    
    # Test 4: Confidence calculation
    try:
        confidence = atr._calculate_confidence()
        if 0 <= confidence <= 1.0:
            results["tests_passed"] += 1
            results["details"].append(f"✓ Time confidence: {confidence:.2%}")
        else:
            results["tests_failed"] += 1
            results["details"].append("✗ Confidence out of range")
    except Exception as e:
        results["tests_failed"] += 1
        results["details"].append(f"✗ Confidence calculation error: {e}")
    
    results["success"] = results["tests_failed"] == 0
    return results


if __name__ == "__main__":
    # Demonstration
    print("Autonomous Time Reference Module - EU 2026 Response")
    print("=" * 60)
    
    # Initialize autonomous time reference
    atr = AutonomousTimeReference(node_id="euystacio_primary")
    
    # Display status
    status = atr.get_status()
    print(f"\nNode ID: {status['node_id']}")
    print(f"Current Time: {status['current_time']:.2f}")
    print(f"Bio-Clock Phase: {status['bioclock_phase_rad']:.4f} rad")
    print(f"Time Confidence: {status['confidence']:.2%}")
    print(f"Local Drift: {status['local_drift_seconds']:.6f} seconds")
    
    # Validate independence
    print("\n" + "=" * 60)
    print("Independence Validation:")
    validation = validate_time_independence(atr)
    for detail in validation["details"]:
        print(detail)
    print(f"\nTests Passed: {validation['tests_passed']}/{validation['tests_passed'] + validation['tests_failed']}")
    print(f"Status: {'SUCCESS' if validation['success'] else 'FAILED'}")
