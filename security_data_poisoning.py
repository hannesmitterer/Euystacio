#!/usr/bin/env python3
"""
AI Data Poisoning Detector
Scenario B: Systemstörungen und Sabotage

Implements detection and mitigation of AI training data poisoning attacks
to ensure model integrity and prevent sabotage.
"""

import time
import math
import hashlib
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class DataSample:
    """Represents a training data sample."""
    sample_id: str
    features: List[float]
    label: str
    timestamp: float
    source: str
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'sample_id': self.sample_id,
            'label': self.label,
            'timestamp': self.timestamp,
            'source': self.source,
            'feature_count': len(self.features)
        }


@dataclass
class PoisoningDetection:
    """Represents a detected poisoning attempt."""
    sample_id: str
    detection_type: str
    confidence: float
    severity: float
    details: Dict
    timestamp: float
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'sample_id': self.sample_id,
            'detection_type': self.detection_type,
            'confidence': self.confidence,
            'severity': self.severity,
            'details': self.details,
            'timestamp': self.timestamp
        }


class DataPoisoningDetector:
    """
    Detects poisoning attempts in AI training data.
    
    Uses multiple techniques including statistical analysis, outlier detection,
    and label consistency checking.
    """
    
    def __init__(self, feature_dimension: int):
        """
        Initialize data poisoning detector.
        
        Args:
            feature_dimension: Dimensionality of feature vectors
        """
        self.feature_dimension = feature_dimension
        self.clean_samples: List[DataSample] = []
        self.suspicious_samples: List[DataSample] = []
        self.detections: List[PoisoningDetection] = []
        self.label_distribution = defaultdict(int)
        self.source_reputation = defaultdict(lambda: 1.0)
    
    def add_sample(self, sample: DataSample) -> Optional[PoisoningDetection]:
        """
        Add and analyze a data sample.
        
        Args:
            sample: Data sample to analyze
            
        Returns:
            PoisoningDetection if poisoning detected, None otherwise
        """
        if len(sample.features) != self.feature_dimension:
            raise ValueError(f"Expected {self.feature_dimension} features, "
                           f"got {len(sample.features)}")
        
        # Check for poisoning
        detection = self._check_for_poisoning(sample)
        
        if detection:
            self.suspicious_samples.append(sample)
            self.detections.append(detection)
            # Reduce source reputation
            self.source_reputation[sample.source] *= 0.9
        else:
            self.clean_samples.append(sample)
            self.label_distribution[sample.label] += 1
            # Slightly increase source reputation
            self.source_reputation[sample.source] = min(
                1.0,
                self.source_reputation[sample.source] * 1.01
            )
        
        return detection
    
    def _check_for_poisoning(self, sample: DataSample) -> Optional[PoisoningDetection]:
        """
        Check if sample shows signs of poisoning.
        
        Args:
            sample: Sample to check
            
        Returns:
            PoisoningDetection if poisoning detected
        """
        current_time = time.time()
        
        # Check 1: Outlier detection in feature space
        if len(self.clean_samples) >= 10:
            outlier_score = self._calculate_outlier_score(sample.features)
            
            if outlier_score > 3.0:  # 3 sigma threshold
                return PoisoningDetection(
                    sample_id=sample.sample_id,
                    detection_type='statistical_outlier',
                    confidence=min(1.0, outlier_score / 5.0),
                    severity=min(1.0, outlier_score / 10.0),
                    details={
                        'outlier_score': outlier_score,
                        'threshold': 3.0
                    },
                    timestamp=current_time
                )
        
        # Check 2: Label distribution anomaly
        label_anomaly = self._check_label_anomaly(sample.label)
        if label_anomaly > 0.8:
            return PoisoningDetection(
                sample_id=sample.sample_id,
                detection_type='label_distribution_anomaly',
                confidence=label_anomaly,
                severity=0.6,
                details={
                    'label': sample.label,
                    'anomaly_score': label_anomaly
                },
                timestamp=current_time
            )
        
        # Check 3: Source reputation
        source_reputation = self.source_reputation[sample.source]
        if source_reputation < 0.3:
            return PoisoningDetection(
                sample_id=sample.sample_id,
                detection_type='low_source_reputation',
                confidence=0.7,
                severity=0.5,
                details={
                    'source': sample.source,
                    'reputation': source_reputation
                },
                timestamp=current_time
            )
        
        # Check 4: Feature value range check
        range_violation = self._check_feature_ranges(sample.features)
        if range_violation:
            return PoisoningDetection(
                sample_id=sample.sample_id,
                detection_type='feature_range_violation',
                confidence=0.9,
                severity=0.8,
                details=range_violation,
                timestamp=current_time
            )
        
        return None
    
    def _calculate_outlier_score(self, features: List[float]) -> float:
        """
        Calculate outlier score using Mahalanobis-like distance.
        
        Args:
            features: Feature vector
            
        Returns:
            Outlier score (higher = more anomalous)
        """
        if not self.clean_samples:
            return 0.0
        
        # Calculate mean and std for each feature
        n_features = len(features)
        means = [0.0] * n_features
        stds = [0.0] * n_features
        
        # Calculate means
        for sample in self.clean_samples:
            for i, val in enumerate(sample.features):
                means[i] += val
        
        n_samples = len(self.clean_samples)
        means = [m / n_samples for m in means]
        
        # Calculate standard deviations
        for sample in self.clean_samples:
            for i, val in enumerate(sample.features):
                stds[i] += (val - means[i]) ** 2
        
        stds = [math.sqrt(s / n_samples) if s > 0 else 0.01 for s in stds]  # Use small epsilon instead of 1.0
        
        # Calculate normalized distance
        distance = 0.0
        for i, (val, mean, std) in enumerate(zip(features, means, stds)):
            normalized_diff = abs(val - mean) / std if std > 0 else 0
            distance += normalized_diff ** 2
        
        return math.sqrt(distance / n_features)
    
    def _check_label_anomaly(self, label: str) -> float:
        """
        Check if label represents an anomalous distribution shift.
        
        Args:
            label: Sample label
            
        Returns:
            Anomaly score (0-1)
        """
        if not self.label_distribution:
            return 0.0
        
        total_samples = sum(self.label_distribution.values())
        label_count = self.label_distribution.get(label, 0)
        
        # Expected uniform distribution
        num_labels = len(self.label_distribution)
        expected_count = total_samples / num_labels if num_labels > 0 else 0
        
        if expected_count == 0:
            return 0.0
        
        # Check if this label is significantly underrepresented
        ratio = label_count / expected_count if expected_count > 0 else 0
        
        # Anomaly if significantly different from expected
        if ratio < 0.1 and total_samples > 50:
            return 0.9
        elif ratio < 0.3 and total_samples > 20:
            return 0.6
        
        return 0.0
    
    def _check_feature_ranges(self, features: List[float]) -> Optional[Dict]:
        """
        Check if features violate expected ranges.
        
        Args:
            features: Feature vector
            
        Returns:
            Violation details if found
        """
        # Check for extreme values
        for i, val in enumerate(features):
            if abs(val) > 1e6:  # Unreasonably large
                return {
                    'feature_index': i,
                    'value': val,
                    'reason': 'extreme_value'
                }
            
            if math.isnan(val) or math.isinf(val):
                return {
                    'feature_index': i,
                    'value': str(val),
                    'reason': 'invalid_value'
                }
        
        return None
    
    def filter_clean_dataset(self) -> List[DataSample]:
        """
        Get filtered dataset with suspicious samples removed.
        
        Returns:
            List of clean samples
        """
        return self.clean_samples.copy()
    
    def get_poisoning_rate(self) -> float:
        """
        Calculate poisoning rate in observed data.
        
        Returns:
            Poisoning rate (0-1)
        """
        total = len(self.clean_samples) + len(self.suspicious_samples)
        if total == 0:
            return 0.0
        
        return len(self.suspicious_samples) / total
    
    def get_statistics(self) -> Dict:
        """Get detector statistics."""
        return {
            'total_samples': len(self.clean_samples) + len(self.suspicious_samples),
            'clean_samples': len(self.clean_samples),
            'suspicious_samples': len(self.suspicious_samples),
            'poisoning_rate': self.get_poisoning_rate(),
            'detections_by_type': self._count_detections_by_type(),
            'source_reputations': dict(self.source_reputation)
        }
    
    def _count_detections_by_type(self) -> Dict[str, int]:
        """Count detections by type."""
        counts = defaultdict(int)
        for detection in self.detections:
            counts[detection.detection_type] += 1
        return dict(counts)


class DataSanitizer:
    """
    Sanitizes and validates training data before use.
    
    Works with DataPoisoningDetector to clean datasets.
    """
    
    def __init__(self, detector: DataPoisoningDetector):
        """
        Initialize data sanitizer.
        
        Args:
            detector: Associated poisoning detector
        """
        self.detector = detector
        self.sanitized_count = 0
        self.rejected_count = 0
    
    def sanitize_sample(self, sample: DataSample) -> Optional[DataSample]:
        """
        Sanitize a data sample.
        
        Args:
            sample: Sample to sanitize
            
        Returns:
            Sanitized sample or None if rejected
        """
        detection = self.detector.add_sample(sample)
        
        if detection:
            # Reject high-confidence poisoning
            if detection.confidence > 0.8:
                self.rejected_count += 1
                return None
            
            # Attempt to sanitize low-confidence detections
            if detection.confidence < 0.5:
                self.sanitized_count += 1
                return sample
        
        return sample
    
    def sanitize_batch(self, samples: List[DataSample]) -> List[DataSample]:
        """
        Sanitize a batch of samples.
        
        Args:
            samples: Batch of samples
            
        Returns:
            List of clean samples
        """
        clean_batch = []
        
        for sample in samples:
            sanitized = self.sanitize_sample(sample)
            if sanitized:
                clean_batch.append(sanitized)
        
        return clean_batch
    
    def get_statistics(self) -> Dict:
        """Get sanitization statistics."""
        return {
            'sanitized_count': self.sanitized_count,
            'rejected_count': self.rejected_count,
            'detector_stats': self.detector.get_statistics()
        }


if __name__ == '__main__':
    print("=== AI Data Poisoning Detector Demo ===")
    print()
    
    # Initialize detector
    detector = DataPoisoningDetector(feature_dimension=5)
    sanitizer = DataSanitizer(detector)
    
    # Add clean samples
    print("Adding clean training samples...")
    for i in range(50):
        sample = DataSample(
            sample_id=f"clean_{i}",
            features=[0.5 + i * 0.01, 0.3, 0.7, 0.2, 0.9],
            label='normal',
            timestamp=time.time(),
            source='trusted_source'
        )
        sanitizer.sanitize_sample(sample)
    
    # Add poisoned samples
    print("Adding potentially poisoned samples...")
    
    # Outlier
    poisoned1 = DataSample(
        sample_id="poisoned_outlier",
        features=[10.0, 10.0, 10.0, 10.0, 10.0],  # Extreme values
        label='normal',
        timestamp=time.time(),
        source='untrusted_source'
    )
    result1 = sanitizer.sanitize_sample(poisoned1)
    
    # Invalid value
    poisoned2 = DataSample(
        sample_id="poisoned_invalid",
        features=[float('nan'), 0.5, 0.5, 0.5, 0.5],
        label='attack',
        timestamp=time.time(),
        source='untrusted_source'
    )
    result2 = sanitizer.sanitize_sample(poisoned2)
    
    # Get statistics
    stats = sanitizer.get_statistics()
    detector_stats = stats['detector_stats']
    
    print(f"\nTotal Samples Processed: {detector_stats['total_samples']}")
    print(f"Clean Samples: {detector_stats['clean_samples']}")
    print(f"Suspicious Samples: {detector_stats['suspicious_samples']}")
    print(f"Poisoning Rate: {detector_stats['poisoning_rate']:.2%}")
    print(f"Sanitized: {stats['sanitized_count']}")
    print(f"Rejected: {stats['rejected_count']}")
    
    if detector_stats['detections_by_type']:
        print("\nDetections by Type:")
        for det_type, count in detector_stats['detections_by_type'].items():
            print(f"  {det_type}: {count}")
    
    print()
    print("✓ Data poisoning detection operational")
