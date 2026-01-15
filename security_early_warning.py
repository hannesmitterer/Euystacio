#!/usr/bin/env python3
"""
TensorFlow-Based Early Warning System
Scenario A: Spionage und Datenextraktion

Implements an AI-powered anomaly detection system for protocol and 
frequency deviations using TensorFlow-inspired architecture.
"""

import time
import math
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from collections import deque
import json


@dataclass
class AnomalyDetection:
    """Represents an anomaly detection event."""
    timestamp: float
    anomaly_type: str
    severity: float  # 0.0 to 1.0
    confidence: float  # 0.0 to 1.0
    details: Dict
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'timestamp': self.timestamp,
            'anomaly_type': self.anomaly_type,
            'severity': self.severity,
            'confidence': self.confidence,
            'details': self.details
        }


class ProtocolAnomalyDetector:
    """
    Detects anomalies in protocol behavior.
    
    Uses statistical analysis and pattern recognition to identify
    deviations from normal protocol operation.
    """
    
    def __init__(self, window_size: int = 100):
        """
        Initialize protocol anomaly detector.
        
        Args:
            window_size: Number of samples to keep in sliding window
        """
        self.window_size = window_size
        self.latency_window = deque(maxlen=window_size)
        self.packet_size_window = deque(maxlen=window_size)
        self.error_rate_window = deque(maxlen=window_size)
        self.detections = []
        
    def add_sample(self, latency_ms: float, packet_size_bytes: int, 
                   error_rate: float):
        """
        Add protocol sample for analysis.
        
        Args:
            latency_ms: Protocol latency in milliseconds
            packet_size_bytes: Packet size in bytes
            error_rate: Error rate (0.0 to 1.0)
        """
        self.latency_window.append(latency_ms)
        self.packet_size_window.append(packet_size_bytes)
        self.error_rate_window.append(error_rate)
    
    def _calculate_zscore(self, value: float, window: deque) -> float:
        """
        Calculate Z-score for anomaly detection.
        
        Args:
            value: Current value
            window: Historical window
            
        Returns:
            Z-score
        """
        if len(window) < 2:
            return 0.0
        
        mean = sum(window) / len(window)
        variance = sum((x - mean) ** 2 for x in window) / len(window)
        std_dev = math.sqrt(variance)
        
        if std_dev == 0:
            return 0.0
        
        return abs(value - mean) / std_dev
    
    def detect_anomalies(self, threshold: float = 3.0) -> List[AnomalyDetection]:
        """
        Detect protocol anomalies.
        
        Args:
            threshold: Z-score threshold for anomaly detection
            
        Returns:
            List of detected anomalies
        """
        anomalies = []
        current_time = time.time()
        
        # Check latency anomalies
        if len(self.latency_window) >= 10:
            latest_latency = self.latency_window[-1]
            z_score = self._calculate_zscore(latest_latency, self.latency_window)
            
            if z_score > threshold:
                anomalies.append(AnomalyDetection(
                    timestamp=current_time,
                    anomaly_type='latency_spike',
                    severity=min(1.0, z_score / 10.0),
                    confidence=min(1.0, z_score / threshold),
                    details={
                        'latency_ms': latest_latency,
                        'z_score': z_score,
                        'mean_latency': sum(self.latency_window) / len(self.latency_window)
                    }
                ))
        
        # Check packet size anomalies
        if len(self.packet_size_window) >= 10:
            latest_size = self.packet_size_window[-1]
            z_score = self._calculate_zscore(latest_size, self.packet_size_window)
            
            if z_score > threshold:
                anomalies.append(AnomalyDetection(
                    timestamp=current_time,
                    anomaly_type='packet_size_anomaly',
                    severity=min(1.0, z_score / 10.0),
                    confidence=min(1.0, z_score / threshold),
                    details={
                        'packet_size': latest_size,
                        'z_score': z_score
                    }
                ))
        
        # Check error rate anomalies
        if len(self.error_rate_window) >= 10:
            latest_error = self.error_rate_window[-1]
            mean_error = sum(self.error_rate_window) / len(self.error_rate_window)
            
            if latest_error > mean_error * 2.0 and latest_error > 0.05:
                anomalies.append(AnomalyDetection(
                    timestamp=current_time,
                    anomaly_type='elevated_error_rate',
                    severity=min(1.0, latest_error * 5.0),
                    confidence=0.9,
                    details={
                        'error_rate': latest_error,
                        'mean_error_rate': mean_error
                    }
                ))
        
        self.detections.extend(anomalies)
        return anomalies


class FrequencyAnomalyDetector:
    """
    Detects anomalies in frequency spectrum.
    
    Identifies unexpected frequency deviations and potential interference.
    """
    
    def __init__(self, expected_frequency: float, tolerance_mhz: float = 1.0):
        """
        Initialize frequency anomaly detector.
        
        Args:
            expected_frequency: Expected frequency in MHz
            tolerance_mhz: Frequency tolerance in MHz
        """
        self.expected_frequency = expected_frequency
        self.tolerance_mhz = tolerance_mhz
        self.frequency_samples = deque(maxlen=100)
        self.power_samples = deque(maxlen=100)
        self.detections = []
    
    def add_spectrum_sample(self, frequency_mhz: float, power_dbm: float):
        """
        Add frequency spectrum sample.
        
        Args:
            frequency_mhz: Measured frequency in MHz
            power_dbm: Signal power in dBm
        """
        self.frequency_samples.append(frequency_mhz)
        self.power_samples.append(power_dbm)
    
    def detect_anomalies(self) -> List[AnomalyDetection]:
        """
        Detect frequency anomalies.
        
        Returns:
            List of detected anomalies
        """
        anomalies = []
        current_time = time.time()
        
        if not self.frequency_samples:
            return anomalies
        
        latest_freq = self.frequency_samples[-1]
        latest_power = self.power_samples[-1]
        
        # Check frequency deviation
        deviation = abs(latest_freq - self.expected_frequency)
        if deviation > self.tolerance_mhz:
            anomalies.append(AnomalyDetection(
                timestamp=current_time,
                anomaly_type='frequency_deviation',
                severity=min(1.0, deviation / (self.tolerance_mhz * 5.0)),
                confidence=0.95,
                details={
                    'expected_mhz': self.expected_frequency,
                    'measured_mhz': latest_freq,
                    'deviation_mhz': deviation
                }
            ))
        
        # Check for unexpected signal power
        if len(self.power_samples) >= 10:
            mean_power = sum(self.power_samples) / len(self.power_samples)
            power_diff = abs(latest_power - mean_power)
            
            if power_diff > 10.0:  # 10 dB deviation
                anomalies.append(AnomalyDetection(
                    timestamp=current_time,
                    anomaly_type='power_anomaly',
                    severity=min(1.0, power_diff / 30.0),
                    confidence=0.85,
                    details={
                        'power_dbm': latest_power,
                        'mean_power_dbm': mean_power,
                        'deviation_db': power_diff
                    }
                ))
        
        self.detections.extend(anomalies)
        return anomalies


class NeuralAnomalyClassifier:
    """
    Simplified neural network-inspired anomaly classifier.
    
    Uses multi-layer perceptron-like architecture for classifying
    anomaly patterns. In production, use actual TensorFlow/PyTorch.
    """
    
    def __init__(self, input_size: int = 5):
        """
        Initialize neural classifier.
        
        Args:
            input_size: Number of input features
        """
        self.input_size = input_size
        self.weights = [[0.5 for _ in range(input_size)] for _ in range(3)]
        self.trained = False
    
    def _sigmoid(self, x: float) -> float:
        """Sigmoid activation function."""
        return 1.0 / (1.0 + math.exp(-x))
    
    def predict(self, features: List[float]) -> Tuple[str, float]:
        """
        Predict anomaly classification.
        
        Args:
            features: Input feature vector
            
        Returns:
            Tuple of (anomaly_class, confidence)
        """
        if len(features) != self.input_size:
            raise ValueError(f"Expected {self.input_size} features, got {len(features)}")
        
        # Simple feedforward (simplified)
        hidden = [self._sigmoid(sum(f * w for f, w in zip(features, weights)))
                  for weights in self.weights]
        
        output = sum(hidden) / len(hidden)
        
        # Classify based on output
        if output > 0.75:
            return ('critical', output)
        elif output > 0.5:
            return ('warning', output)
        else:
            return ('normal', 1.0 - output)
    
    def extract_features(self, anomaly: AnomalyDetection) -> List[float]:
        """
        Extract features from anomaly for classification.
        
        Args:
            anomaly: Anomaly detection event
            
        Returns:
            Feature vector
        """
        # Normalize features to 0-1 range
        features = [
            anomaly.severity,
            anomaly.confidence,
            1.0 if anomaly.anomaly_type.startswith('latency') else 0.0,
            1.0 if anomaly.anomaly_type.startswith('frequency') else 0.0,
            1.0 if anomaly.anomaly_type.startswith('power') else 0.0
        ]
        return features


class EarlyWarningSystem:
    """
    Comprehensive early warning system coordinating multiple detectors.
    
    Integrates protocol and frequency anomaly detection with neural
    classification for comprehensive threat detection.
    """
    
    def __init__(self):
        """Initialize early warning system."""
        self.protocol_detector = ProtocolAnomalyDetector()
        self.frequency_detector = FrequencyAnomalyDetector(2400.0)
        self.classifier = NeuralAnomalyClassifier()
        self.all_detections = []
        self.alert_count = 0
        self.started = False
        self.start_time = None
    
    def start(self):
        """Start the early warning system."""
        self.started = True
        self.start_time = time.time()
    
    def stop(self):
        """Stop the early warning system."""
        self.started = False
    
    def add_protocol_sample(self, latency_ms: float, packet_size_bytes: int,
                           error_rate: float):
        """Add protocol telemetry sample."""
        if self.started:
            self.protocol_detector.add_sample(latency_ms, packet_size_bytes, error_rate)
    
    def add_frequency_sample(self, frequency_mhz: float, power_dbm: float):
        """Add frequency spectrum sample."""
        if self.started:
            self.frequency_detector.add_spectrum_sample(frequency_mhz, power_dbm)
    
    def check_for_threats(self) -> List[Dict]:
        """
        Check for security threats.
        
        Returns:
            List of classified threats
        """
        if not self.started:
            return []
        
        threats = []
        
        # Detect protocol anomalies
        protocol_anomalies = self.protocol_detector.detect_anomalies()
        
        # Detect frequency anomalies
        frequency_anomalies = self.frequency_detector.detect_anomalies()
        
        # Classify all anomalies
        all_anomalies = protocol_anomalies + frequency_anomalies
        
        for anomaly in all_anomalies:
            features = self.classifier.extract_features(anomaly)
            threat_class, confidence = self.classifier.predict(features)
            
            threat = {
                'timestamp': anomaly.timestamp,
                'type': anomaly.anomaly_type,
                'classification': threat_class,
                'severity': anomaly.severity,
                'confidence': confidence,
                'details': anomaly.details
            }
            
            threats.append(threat)
            self.all_detections.append(anomaly)
            
            if threat_class in ['critical', 'warning']:
                self.alert_count += 1
        
        return threats
    
    def get_statistics(self) -> Dict:
        """Get early warning system statistics."""
        return {
            'active': self.started,
            'uptime_seconds': time.time() - self.start_time if self.start_time else 0,
            'total_detections': len(self.all_detections),
            'alert_count': self.alert_count,
            'protocol_samples': len(self.protocol_detector.latency_window),
            'frequency_samples': len(self.frequency_detector.frequency_samples)
        }


if __name__ == '__main__':
    print("=== TensorFlow-Based Early Warning System Demo ===")
    print()
    
    # Initialize system
    ews = EarlyWarningSystem()
    ews.start()
    
    print("Early Warning System started...")
    
    # Simulate normal operation
    for i in range(20):
        ews.add_protocol_sample(
            latency_ms=10.0 + (i % 5),
            packet_size_bytes=1500 + (i % 100),
            error_rate=0.01
        )
        ews.add_frequency_sample(
            frequency_mhz=2400.0 + (i % 3) * 0.1,
            power_dbm=-50.0
        )
    
    # Simulate anomaly
    ews.add_protocol_sample(latency_ms=100.0, packet_size_bytes=5000, error_rate=0.15)
    ews.add_frequency_sample(frequency_mhz=2405.0, power_dbm=-30.0)
    
    # Check for threats
    threats = ews.check_for_threats()
    
    stats = ews.get_statistics()
    print(f"System Active: {stats['active']}")
    print(f"Total Detections: {stats['total_detections']}")
    print(f"Alert Count: {stats['alert_count']}")
    print(f"Threats Detected: {len(threats)}")
    
    if threats:
        print("\nDetected Threats:")
        for threat in threats:
            print(f"  - {threat['type']}: {threat['classification']} "
                  f"(severity: {threat['severity']:.2f}, confidence: {threat['confidence']:.2f})")
    
    print()
    print("✓ Early warning system operational")
