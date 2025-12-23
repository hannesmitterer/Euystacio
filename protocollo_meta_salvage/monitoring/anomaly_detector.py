"""
Anomaly Detector
================

Detects anomalies in data flows using Apache Flink-style stream processing.
Identifies patterns that indicate ethical risks or system degradation.
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import deque

logger = logging.getLogger(__name__)


@dataclass
class Anomaly:
    """Represents a detected anomaly"""
    timestamp: str
    type: str
    severity: str  # low, medium, high, critical
    description: str
    metrics: Dict[str, Any]
    provider: str


class AnomalyDetector:
    """
    Detects anomalies in data flows and system behavior.
    
    Uses statistical analysis and pattern matching to identify
    deviations from expected ethical behavior.
    """
    
    def __init__(self, window_size: int = 100):
        """
        Initialize the Anomaly Detector.
        
        Args:
            window_size: Number of data points to keep in sliding window
        """
        self.window_size = window_size
        self.data_window: deque = deque(maxlen=window_size)
        self.detected_anomalies: List[Anomaly] = []
        self.baseline_metrics: Dict[str, float] = {}
        
        logger.info(f"Anomaly Detector initialized with window size {window_size}")
    
    def process_stream(self, data_point: Dict[str, Any]) -> Optional[Anomaly]:
        """
        Process a data point from the stream.
        
        Args:
            data_point: Dictionary containing metrics and metadata
            
        Returns:
            Anomaly object if anomaly detected, None otherwise
        """
        self.data_window.append(data_point)
        
        # Update baseline metrics
        self._update_baseline()
        
        # Check for various anomaly types
        anomaly = self._detect_anomalies(data_point)
        
        if anomaly:
            self.detected_anomalies.append(anomaly)
            logger.warning(f"Anomaly detected: {anomaly.type} - {anomaly.description}")
        
        return anomaly
    
    def _update_baseline(self):
        """Update baseline metrics from the sliding window"""
        if len(self.data_window) < 10:
            return
        
        # Calculate average metrics
        metrics_sum = {}
        for point in self.data_window:
            for key, value in point.get('metrics', {}).items():
                if isinstance(value, (int, float)):
                    metrics_sum[key] = metrics_sum.get(key, 0) + value
        
        for key, total in metrics_sum.items():
            self.baseline_metrics[key] = total / len(self.data_window)
    
    def _detect_anomalies(self, data_point: Dict[str, Any]) -> Optional[Anomaly]:
        """Detect anomalies in the data point"""
        metrics = data_point.get('metrics', {})
        provider = data_point.get('provider', 'unknown')
        
        # Check for throughput anomalies
        if 'throughput' in metrics and 'throughput' in self.baseline_metrics:
            current = metrics['throughput']
            baseline = self.baseline_metrics['throughput']
            
            if current > baseline * 2:
                return Anomaly(
                    timestamp=datetime.utcnow().isoformat(),
                    type='throughput_spike',
                    severity='high',
                    description=f'Throughput spike detected: {current:.2f} (baseline: {baseline:.2f})',
                    metrics=metrics,
                    provider=provider
                )
        
        # Check for error rate anomalies
        if 'error_rate' in metrics:
            if metrics['error_rate'] > 0.1:  # 10% error rate
                return Anomaly(
                    timestamp=datetime.utcnow().isoformat(),
                    type='high_error_rate',
                    severity='critical',
                    description=f'High error rate detected: {metrics["error_rate"]:.2%}',
                    metrics=metrics,
                    provider=provider
                )
        
        # Check for data quality degradation
        if 'data_quality' in metrics:
            if metrics['data_quality'] < 0.7:
                return Anomaly(
                    timestamp=datetime.utcnow().isoformat(),
                    type='data_quality_degradation',
                    severity='medium',
                    description=f'Data quality below threshold: {metrics["data_quality"]:.2f}',
                    metrics=metrics,
                    provider=provider
                )
        
        # Check for unexpected API patterns
        if 'api_calls' in metrics and 'api_calls' in self.baseline_metrics:
            current = metrics['api_calls']
            baseline = self.baseline_metrics['api_calls']
            
            if current > baseline * 3:
                return Anomaly(
                    timestamp=datetime.utcnow().isoformat(),
                    type='unusual_api_pattern',
                    severity='medium',
                    description=f'Unusual API call pattern: {current} calls (baseline: {baseline:.0f})',
                    metrics=metrics,
                    provider=provider
                )
        
        return None
    
    def get_recent_anomalies(self, hours: int = 24) -> List[Anomaly]:
        """Get anomalies detected in the last N hours"""
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        
        recent = []
        for anomaly in self.detected_anomalies:
            timestamp = datetime.fromisoformat(anomaly.timestamp)
            if timestamp > cutoff:
                recent.append(anomaly)
        
        return recent
    
    def get_anomaly_summary(self) -> Dict[str, Any]:
        """Get summary of detected anomalies"""
        type_counts = {}
        severity_counts = {}
        
        for anomaly in self.detected_anomalies:
            type_counts[anomaly.type] = type_counts.get(anomaly.type, 0) + 1
            severity_counts[anomaly.severity] = severity_counts.get(anomaly.severity, 0) + 1
        
        return {
            'total_anomalies': len(self.detected_anomalies),
            'by_type': type_counts,
            'by_severity': severity_counts,
            'recent_24h': len(self.get_recent_anomalies(24))
        }
