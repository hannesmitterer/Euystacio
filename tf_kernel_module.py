#!/usr/bin/env python3
"""
TensorFlow Kernel Module - Predictive AI Threat Detection
=========================================================

Implements AI-powered predictive analysis for electromagnetic fingerprints
and SDR (Software Defined Radio) scanning attempt detection.

Features:
- Electromagnetic signature analysis
- Anomaly detection in network patterns
- SDR scanning attempt mapping
- Real-time threat prediction
- Adaptive learning from attack patterns

Mission: Protect the Resonance School from electromagnetic surveillance and scanning attempts
"""

import os
import time
import json
import numpy as np
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, asdict
from collections import deque


# TensorFlow is optional - gracefully handle if not installed
try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("[TF Module] TensorFlow not installed - using simplified detection")


# Detection parameters
SIGNATURE_WINDOW_SIZE = 100  # Number of samples in detection window
ANOMALY_THRESHOLD = 0.75  # Threshold for anomaly detection (0-1)
SDR_FREQUENCY_BANDS = [
    (88.0, 108.0),    # FM Radio
    (400.0, 512.0),   # UHF
    (2400.0, 2500.0), # ISM band (WiFi, Bluetooth)
    (5000.0, 6000.0)  # 5 GHz WiFi
]


@dataclass
class ElectromagneticSignature:
    """Represents an electromagnetic signature detected in the environment."""
    timestamp: float
    frequency: float  # MHz
    amplitude: float  # dBm
    bandwidth: float  # MHz
    modulation: str
    source_angle: Optional[float] = None  # Degrees from north
    confidence: float = 0.0
    threat_level: float = 0.0
    
    def to_dict(self) -> Dict:
        """Convert signature to dictionary."""
        return asdict(self)


@dataclass
class SDRScanAttempt:
    """Represents a detected SDR scanning attempt."""
    timestamp: float
    scan_pattern: str  # "sweep", "hop", "fixed"
    frequency_range: Tuple[float, float]
    scan_rate: float  # scans per second
    source_estimate: Optional[Tuple[float, float]] = None  # lat, lon
    threat_score: float = 0.0
    blocked: bool = False
    
    def to_dict(self) -> Dict:
        """Convert scan attempt to dictionary."""
        return asdict(self)


class EMSignatureAnalyzer:
    """Analyzes electromagnetic signatures using AI pattern recognition."""
    
    def __init__(self):
        self.model: Optional[Any] = None
        self.signature_history = deque(maxlen=1000)
        
        if TF_AVAILABLE:
            self._build_model()
        else:
            print("[EM Analyzer] Operating in simplified mode without TensorFlow")
    
    def _build_model(self):
        """Build TensorFlow model for signature analysis."""
        if not TF_AVAILABLE:
            return
        
        # Simple neural network for anomaly detection
        # Input: [frequency, amplitude, bandwidth, time_features]
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(5,)),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')  # Anomaly score
        ])
        
        self.model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        print("[EM Analyzer] TensorFlow model initialized")
    
    def analyze_signature(self, signature: ElectromagneticSignature) -> float:
        """
        Analyze an electromagnetic signature for threats.
        
        Args:
            signature: EM signature to analyze
            
        Returns:
            Threat level (0.0 to 1.0)
        """
        self.signature_history.append(signature)
        
        if TF_AVAILABLE and self.model:
            # Use neural network for analysis
            features = self._extract_features(signature)
            prediction = self.model.predict(features, verbose=0)[0][0]
            return float(prediction)
        else:
            # Simplified rule-based analysis
            return self._rule_based_analysis(signature)
    
    def _extract_features(self, signature: ElectromagneticSignature) -> np.ndarray:
        """Extract features from signature for ML model."""
        # Normalize frequency (0-6000 MHz -> 0-1)
        freq_norm = signature.frequency / 6000.0
        
        # Normalize amplitude (-100 to 0 dBm -> 0-1)
        amp_norm = (signature.amplitude + 100) / 100.0
        
        # Normalize bandwidth
        bw_norm = signature.bandwidth / 100.0
        
        # Time features (hour of day, day of week)
        dt = datetime.fromtimestamp(signature.timestamp)
        hour_norm = dt.hour / 24.0
        day_norm = dt.weekday() / 7.0
        
        features = np.array([[freq_norm, amp_norm, bw_norm, hour_norm, day_norm]])
        return features
    
    def _rule_based_analysis(self, signature: ElectromagneticSignature) -> float:
        """Simple rule-based threat analysis (fallback when TF not available)."""
        threat_score = 0.0
        
        # Check for suspicious frequency bands
        for band_min, band_max in SDR_FREQUENCY_BANDS:
            if band_min <= signature.frequency <= band_max:
                threat_score += 0.2
        
        # High amplitude signals are more suspicious
        if signature.amplitude > -30:
            threat_score += 0.3
        
        # Wide bandwidth can indicate scanning
        if signature.bandwidth > 50:
            threat_score += 0.2
        
        # Unusual time patterns
        hour = datetime.fromtimestamp(signature.timestamp).hour
        if hour < 6 or hour > 22:
            threat_score += 0.2
        
        return min(1.0, threat_score)
    
    def train_on_data(self, signatures: List[ElectromagneticSignature], labels: List[float]):
        """
        Train the model on labeled signature data.
        
        Args:
            signatures: List of EM signatures
            labels: Corresponding threat labels (0.0 = benign, 1.0 = threat)
        """
        if not TF_AVAILABLE or not self.model:
            print("[EM Analyzer] Training requires TensorFlow")
            return
        
        # Extract features
        X = np.array([self._extract_features(sig)[0] for sig in signatures])
        y = np.array(labels)
        
        # Train model
        self.model.fit(X, y, epochs=10, batch_size=32, validation_split=0.2, verbose=1)
        print("[EM Analyzer] Model training completed")


class SDRScanDetector:
    """Detects and maps SDR scanning attempts."""
    
    def __init__(self):
        self.scan_history = deque(maxlen=500)
        self.active_scans: Dict[str, SDRScanAttempt] = {}
        self.blocked_sources: Set[str] = set()
    
    def detect_scan_pattern(self, signatures: List[ElectromagneticSignature]) -> Optional[SDRScanAttempt]:
        """
        Detect SDR scanning patterns from signature sequence.
        
        Args:
            signatures: Recent EM signatures
            
        Returns:
            Detected scan attempt or None
        """
        if len(signatures) < 10:
            return None
        
        # Analyze frequency pattern
        frequencies = [s.frequency for s in signatures]
        freq_min = min(frequencies)
        freq_max = max(frequencies)
        freq_range = freq_max - freq_min
        
        # Detect sweep pattern (gradually increasing/decreasing frequency)
        is_sweep = self._is_sweep_pattern(frequencies)
        
        # Detect hopping pattern (random frequency changes)
        is_hopping = self._is_hopping_pattern(frequencies)
        
        if is_sweep or is_hopping:
            # Calculate scan rate
            time_span = signatures[-1].timestamp - signatures[0].timestamp
            scan_rate = len(signatures) / time_span if time_span > 0 else 0
            
            pattern = "sweep" if is_sweep else "hop"
            
            scan = SDRScanAttempt(
                timestamp=time.time(),
                scan_pattern=pattern,
                frequency_range=(freq_min, freq_max),
                scan_rate=scan_rate,
                threat_score=0.8 if is_sweep else 0.6
            )
            
            self.scan_history.append(scan)
            return scan
        
        return None
    
    def _is_sweep_pattern(self, frequencies: List[float]) -> bool:
        """Check if frequencies follow a sweep pattern."""
        if len(frequencies) < 5:
            return False
        
        # Check if frequencies are monotonically increasing or decreasing
        diffs = [frequencies[i+1] - frequencies[i] for i in range(len(frequencies)-1)]
        
        # All positive (increasing) or all negative (decreasing)
        all_increasing = all(d > 0 for d in diffs)
        all_decreasing = all(d < 0 for d in diffs)
        
        return all_increasing or all_decreasing
    
    def _is_hopping_pattern(self, frequencies: List[float]) -> bool:
        """Check if frequencies follow a hopping pattern."""
        if len(frequencies) < 10:
            return False
        
        # Check for large, irregular frequency changes
        diffs = [abs(frequencies[i+1] - frequencies[i]) for i in range(len(frequencies)-1)]
        avg_diff = sum(diffs) / len(diffs)
        
        # Hopping shows large irregular jumps
        large_jumps = sum(1 for d in diffs if d > avg_diff * 2)
        
        return large_jumps > len(diffs) * 0.3
    
    def map_scan_source(self, scan: SDRScanAttempt, signatures: List[ElectromagneticSignature]) -> Optional[Tuple[float, float]]:
        """
        Estimate the geographic source of a scan attempt.
        
        This is a simplified triangulation based on signal angles.
        In production, requires multiple receivers with directional antennas.
        
        Args:
            scan: Detected scan attempt
            signatures: Related signatures
            
        Returns:
            Estimated (latitude, longitude) or None
        """
        # Simplified estimation
        # In production, implement proper triangulation
        
        angles = [s.source_angle for s in signatures if s.source_angle is not None]
        
        if len(angles) >= 3:
            # Simple averaging (not accurate, just for demonstration)
            avg_angle = sum(angles) / len(angles)
            
            # Placeholder coordinates
            # In production, use actual receiver location and triangulation
            estimated_lat = 47.0 + (avg_angle / 360.0)
            estimated_lon = 11.0 + (avg_angle / 360.0)
            
            scan.source_estimate = (estimated_lat, estimated_lon)
            return scan.source_estimate
        
        return None
    
    def block_source(self, source_id: str):
        """Block future scans from a detected source."""
        self.blocked_sources.add(source_id)
        print(f"[SDR Detector] Blocked source: {source_id}")


class TensorFlowKernelModule:
    """
    Main TF Kernel Module for predictive threat detection.
    """
    
    def __init__(self, node_id: str = "euystacio_main"):
        self.node_id = node_id
        self.em_analyzer = EMSignatureAnalyzer()
        self.sdr_detector = SDRScanDetector()
        self.signature_buffer = deque(maxlen=SIGNATURE_WINDOW_SIZE)
        self.threat_events: List[Dict[str, Any]] = []
        self.monitoring = False
    
    def start_monitoring(self):
        """Start continuous threat monitoring."""
        self.monitoring = True
        print(f"[TF Kernel] Monitoring started for {self.node_id}")
    
    def stop_monitoring(self):
        """Stop threat monitoring."""
        self.monitoring = False
        print(f"[TF Kernel] Monitoring stopped for {self.node_id}")
    
    def process_signature(self, signature: ElectromagneticSignature) -> Dict[str, Any]:
        """
        Process a new electromagnetic signature.
        
        Args:
            signature: EM signature to analyze
            
        Returns:
            Analysis results with threat assessment
        """
        # Analyze signature
        threat_level = self.em_analyzer.analyze_signature(signature)
        signature.threat_level = threat_level
        
        # Add to buffer
        self.signature_buffer.append(signature)
        
        # Check for scan patterns
        scan_detected = None
        if len(self.signature_buffer) >= 10:
            scan_detected = self.sdr_detector.detect_scan_pattern(
                list(self.signature_buffer)
            )
        
        # Record threat event if significant
        if threat_level > ANOMALY_THRESHOLD or scan_detected:
            event = {
                "timestamp": time.time(),
                "type": "scan_attempt" if scan_detected else "anomaly",
                "threat_level": threat_level,
                "signature": signature.to_dict(),
                "scan": scan_detected.to_dict() if scan_detected else None
            }
            self.threat_events.append(event)
            
            print(f"[TF Kernel] THREAT DETECTED: {event['type']} "
                  f"(level: {threat_level:.2f})")
        
        return {
            "threat_level": threat_level,
            "scan_detected": scan_detected is not None,
            "scan_details": scan_detected.to_dict() if scan_detected else None,
            "timestamp": time.time()
        }
    
    def simulate_em_signature(self, frequency: float, amplitude: float, 
                             bandwidth: float, modulation: str = "FM") -> ElectromagneticSignature:
        """
        Create a simulated EM signature (for testing).
        
        Args:
            frequency: Frequency in MHz
            amplitude: Amplitude in dBm
            bandwidth: Bandwidth in MHz
            modulation: Modulation type
            
        Returns:
            EM signature
        """
        return ElectromagneticSignature(
            timestamp=time.time(),
            frequency=frequency,
            amplitude=amplitude,
            bandwidth=bandwidth,
            modulation=modulation,
            confidence=0.9
        )
    
    def get_threat_report(self) -> Dict[str, Any]:
        """Generate a threat analysis report."""
        recent_threats = [e for e in self.threat_events 
                         if time.time() - e['timestamp'] < 3600]
        
        avg_threat_level = (
            sum(e['threat_level'] for e in recent_threats) / len(recent_threats)
            if recent_threats else 0.0
        )
        
        return {
            "node_id": self.node_id,
            "monitoring": self.monitoring,
            "total_signatures_analyzed": len(self.em_analyzer.signature_history),
            "recent_threat_events": len(recent_threats),
            "average_threat_level": avg_threat_level,
            "scan_attempts_detected": sum(1 for e in recent_threats 
                                         if e['type'] == 'scan_attempt'),
            "blocked_sources": len(self.sdr_detector.blocked_sources),
            "timestamp": time.time()
        }
    
    def save_threat_log(self, filepath: str):
        """Save threat events to file."""
        with open(filepath, 'w') as f:
            json.dump({
                "node_id": self.node_id,
                "threat_events": self.threat_events,
                "timestamp": time.time()
            }, f, indent=2)


# Example usage
if __name__ == "__main__":
    print("=== TensorFlow Kernel Module - Threat Detection Demo ===\n")
    
    if not TF_AVAILABLE:
        print("[WARNING] TensorFlow not available - using simplified detection\n")
    
    # Create TF kernel module
    tf_kernel = TensorFlowKernelModule(node_id="demo_node")
    tf_kernel.start_monitoring()
    
    print("Simulating electromagnetic signatures...\n")
    
    # Simulate normal signatures
    for i in range(5):
        sig = tf_kernel.simulate_em_signature(
            frequency=100.0 + i * 10,
            amplitude=-60.0,
            bandwidth=0.2,
            modulation="FM"
        )
        result = tf_kernel.process_signature(sig)
        print(f"Normal signal {i+1}: threat_level={result['threat_level']:.2f}")
    
    print("\nSimulating SDR scan sweep...\n")
    
    # Simulate scan sweep (gradually increasing frequency)
    for i in range(15):
        sig = tf_kernel.simulate_em_signature(
            frequency=2400.0 + i * 5,  # WiFi band sweep
            amplitude=-40.0,  # Strong signal
            bandwidth=20.0,   # Wide bandwidth
            modulation="OFDM"
        )
        result = tf_kernel.process_signature(sig)
        
        if result['scan_detected']:
            print(f"[!] SCAN DETECTED: {result['scan_details']['scan_pattern']} pattern")
    
    # Generate threat report
    print("\n" + "="*60)
    report = tf_kernel.get_threat_report()
    print("Threat Analysis Report:")
    for key, value in report.items():
        print(f"  {key}: {value}")
    
    tf_kernel.stop_monitoring()
    print("\nMonitoring stopped.")
