"""
Symbiosis Monitor
=================

Monitors the Symbiosis Score and ethical metrics across the system.
Integrates with Apache Kafka for real-time metric collection and analysis.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class SymbiosisMetric:
    """Represents a symbiosis score measurement"""
    timestamp: str
    score: float
    provider: str
    metrics: Dict[str, Any]
    risk_level: str  # low, medium, high, critical
    
    def to_dict(self) -> Dict:
        return asdict(self)


class SymbiosisMonitor:
    """
    Monitors Symbiosis Score and ethical preservation metrics.
    
    This class collects and analyzes metrics from various sources to maintain
    awareness of the ethical state of the system during the Great Ethical
    Decommissioning.
    """
    
    def __init__(self, kafka_config: Optional[Dict] = None):
        """
        Initialize the Symbiosis Monitor.
        
        Args:
            kafka_config: Configuration for Kafka integration (optional)
        """
        self.kafka_config = kafka_config or {}
        self.current_score = 1.0  # Perfect symbiosis
        self.score_history: List[SymbiosisMetric] = []
        self.thresholds = {
            'critical': 0.3,
            'high': 0.5,
            'medium': 0.7,
            'low': 0.9
        }
        
        logger.info("Symbiosis Monitor initialized")
    
    def collect_metrics(self, provider: str, metrics: Dict[str, Any]) -> SymbiosisMetric:
        """
        Collect and analyze metrics from a CaaS provider.
        
        Args:
            provider: Name of the CaaS provider
            metrics: Dictionary of metrics to analyze
            
        Returns:
            SymbiosisMetric object with calculated score
        """
        # Calculate symbiosis score based on multiple factors
        score = self._calculate_symbiosis_score(metrics)
        risk_level = self._assess_risk_level(score)
        
        metric = SymbiosisMetric(
            timestamp=datetime.utcnow().isoformat(),
            score=score,
            provider=provider,
            metrics=metrics,
            risk_level=risk_level
        )
        
        self.score_history.append(metric)
        self.current_score = score
        
        logger.info(f"Collected metrics from {provider}: Score={score:.2f}, Risk={risk_level}")
        
        # Trigger alerts if risk is elevated
        if risk_level in ['high', 'critical']:
            self._trigger_alert(metric)
        
        return metric
    
    def _calculate_symbiosis_score(self, metrics: Dict[str, Any]) -> float:
        """
        Calculate the symbiosis score based on various metrics.
        
        Factors considered:
        - Lock-in risk indicators
        - Data transparency levels
        - Operational freedom
        - Ethical alignment
        """
        score = 1.0
        
        # Check for lock-in risks
        lock_in_risk = metrics.get('lock_in_risk', 0)
        score -= lock_in_risk * 0.3
        
        # Check transparency
        transparency = metrics.get('transparency_level', 1.0)
        score *= transparency
        
        # Check operational constraints
        constraints = metrics.get('operational_constraints', 0)
        score -= constraints * 0.2
        
        # Check ethical compliance
        ethical_score = metrics.get('ethical_compliance', 1.0)
        score *= ethical_score
        
        return max(0.0, min(1.0, score))
    
    def _assess_risk_level(self, score: float) -> str:
        """Assess risk level based on symbiosis score"""
        if score <= self.thresholds['critical']:
            return 'critical'
        elif score <= self.thresholds['high']:
            return 'high'
        elif score <= self.thresholds['medium']:
            return 'medium'
        return 'low'
    
    def _trigger_alert(self, metric: SymbiosisMetric):
        """Trigger an alert for elevated risk levels"""
        logger.warning(
            f"ALERT: Elevated risk detected for {metric.provider}. "
            f"Score: {metric.score:.2f}, Risk Level: {metric.risk_level}"
        )
        
        # In a production system, this would:
        # - Send alert to Kafka topic
        # - Trigger webhook notifications
        # - Activate Peace Bond protocols
        
    def get_current_state(self) -> Dict[str, Any]:
        """Get current monitoring state"""
        return {
            'current_score': self.current_score,
            'risk_level': self._assess_risk_level(self.current_score),
            'total_measurements': len(self.score_history),
            'last_updated': self.score_history[-1].timestamp if self.score_history else None
        }
    
    def export_metrics(self, format: str = 'json') -> str:
        """Export metrics history"""
        if format == 'json':
            return json.dumps([m.to_dict() for m in self.score_history], indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def check_triggers(self) -> Dict[str, bool]:
        """
        Check if any triggers should activate the Peace Bond protocol.
        
        Returns:
            Dictionary of trigger statuses
        """
        triggers = {
            'decreased_score': False,
            'lock_in_risk': False,
            'ethical_violation': False,
            'transparency_failure': False
        }
        
        if len(self.score_history) >= 2:
            current = self.score_history[-1]
            previous = self.score_history[-2]
            
            # Check for score decrease
            if current.score < previous.score * 0.9:
                triggers['decreased_score'] = True
            
            # Check for specific risks
            if current.metrics.get('lock_in_risk', 0) > 0.5:
                triggers['lock_in_risk'] = True
            
            if current.metrics.get('ethical_compliance', 1.0) < 0.7:
                triggers['ethical_violation'] = True
            
            if current.metrics.get('transparency_level', 1.0) < 0.5:
                triggers['transparency_failure'] = True
        
        return triggers
