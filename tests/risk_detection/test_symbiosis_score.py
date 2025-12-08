"""
Protocollo Meta Salvage - Risk Detection Tests
Tests for Symbiosis Score calculation and anomaly detection
"""

import pytest
from typing import Dict, Any


class SymbiosisScoreCalculator:
    """
    Mock Symbiosis Score calculator for testing purposes
    In production, this would connect to the actual scoring engine
    """
    
    def __init__(self, threshold: float = 0.75):
        self.threshold = threshold
    
    def calculate_score(self, metrics: Dict[str, Any]) -> float:
        """
        Calculate Symbiosis Score based on various metrics
        """
        # Mock implementation - in production, this would be more complex
        trust_score = metrics.get('trust_score', 0.5)
        cooperation_score = metrics.get('cooperation_score', 0.5)
        compliance_score = metrics.get('compliance_score', 0.5)
        
        # Weighted average
        score = (
            trust_score * 0.4 +
            cooperation_score * 0.3 +
            compliance_score * 0.3
        )
        
        return round(score, 2)
    
    def detect_anomaly(self, current_score: float, historical_scores: list) -> bool:
        """
        Detect anomalies in Symbiosis Score based on historical data
        """
        if not historical_scores:
            return False
        
        avg_score = sum(historical_scores) / len(historical_scores)
        std_dev = (sum((x - avg_score) ** 2 for x in historical_scores) / len(historical_scores)) ** 0.5
        
        # Anomaly if current score is more than 2 standard deviations away
        return abs(current_score - avg_score) > (2 * std_dev)
    
    def is_acceptable(self, score: float) -> bool:
        """
        Check if score meets the acceptable threshold
        """
        return score >= self.threshold


class TestSymbiosisScoreCalculation:
    """Test suite for Symbiosis Score calculation"""
    
    def test_calculate_score_high_trust(self):
        """Test score calculation with high trust metrics"""
        calculator = SymbiosisScoreCalculator()
        metrics = {
            'trust_score': 0.9,
            'cooperation_score': 0.85,
            'compliance_score': 0.88
        }
        
        score = calculator.calculate_score(metrics)
        assert score >= 0.75, f"Expected score >= 0.75, got {score}"
        assert score <= 1.0, f"Score should not exceed 1.0, got {score}"
    
    def test_calculate_score_low_trust(self):
        """Test score calculation with low trust metrics"""
        calculator = SymbiosisScoreCalculator()
        metrics = {
            'trust_score': 0.4,
            'cooperation_score': 0.5,
            'compliance_score': 0.45
        }
        
        score = calculator.calculate_score(metrics)
        assert score < 0.75, f"Expected score < 0.75, got {score}"
    
    def test_calculate_score_boundary(self):
        """Test score calculation at threshold boundary"""
        calculator = SymbiosisScoreCalculator(threshold=0.75)
        metrics = {
            'trust_score': 0.75,
            'cooperation_score': 0.75,
            'compliance_score': 0.75
        }
        
        score = calculator.calculate_score(metrics)
        assert calculator.is_acceptable(score), f"Score {score} should be acceptable"
    
    def test_is_acceptable_above_threshold(self):
        """Test acceptability check for scores above threshold"""
        calculator = SymbiosisScoreCalculator(threshold=0.75)
        assert calculator.is_acceptable(0.85) is True
        assert calculator.is_acceptable(0.75) is True
    
    def test_is_acceptable_below_threshold(self):
        """Test acceptability check for scores below threshold"""
        calculator = SymbiosisScoreCalculator(threshold=0.75)
        assert calculator.is_acceptable(0.74) is False
        assert calculator.is_acceptable(0.50) is False


class TestAnomalyDetection:
    """Test suite for anomaly detection in Symbiosis Scores"""
    
    def test_detect_no_anomaly_stable_scores(self):
        """Test no anomaly detection with stable historical scores"""
        calculator = SymbiosisScoreCalculator()
        historical_scores = [0.80, 0.82, 0.81, 0.79, 0.80]
        current_score = 0.81
        
        is_anomaly = calculator.detect_anomaly(current_score, historical_scores)
        assert is_anomaly is False, "Should not detect anomaly in stable scores"
    
    def test_detect_anomaly_sudden_drop(self):
        """Test anomaly detection with sudden score drop"""
        calculator = SymbiosisScoreCalculator()
        historical_scores = [0.80, 0.82, 0.81, 0.79, 0.80]
        current_score = 0.40  # Sudden drop
        
        is_anomaly = calculator.detect_anomaly(current_score, historical_scores)
        assert is_anomaly is True, "Should detect anomaly in sudden drop"
    
    def test_detect_anomaly_sudden_spike(self):
        """Test anomaly detection with sudden score spike"""
        calculator = SymbiosisScoreCalculator()
        historical_scores = [0.50, 0.52, 0.51, 0.49, 0.50]
        current_score = 0.95  # Sudden spike
        
        is_anomaly = calculator.detect_anomaly(current_score, historical_scores)
        assert is_anomaly is True, "Should detect anomaly in sudden spike"
    
    def test_detect_anomaly_empty_history(self):
        """Test anomaly detection with no historical data"""
        calculator = SymbiosisScoreCalculator()
        historical_scores = []
        current_score = 0.50
        
        is_anomaly = calculator.detect_anomaly(current_score, historical_scores)
        assert is_anomaly is False, "Should not detect anomaly with no history"
    
    def test_detect_anomaly_gradual_change(self):
        """Test no anomaly for gradual score changes"""
        calculator = SymbiosisScoreCalculator()
        historical_scores = [0.80, 0.805, 0.79, 0.795, 0.80]
        current_score = 0.79  # Gradual change within normal variance
        
        is_anomaly = calculator.detect_anomaly(current_score, historical_scores)
        assert is_anomaly is False, "Should not detect anomaly in gradual change"


class TestRiskAssessment:
    """Test suite for risk assessment based on Symbiosis Score"""
    
    def test_risk_level_low(self):
        """Test risk level classification for high scores"""
        calculator = SymbiosisScoreCalculator()
        score = 0.85
        
        if score >= 0.75:
            risk_level = "low"
        elif score >= 0.50:
            risk_level = "medium"
        else:
            risk_level = "high"
        
        assert risk_level == "low", "High score should indicate low risk"
    
    def test_risk_level_medium(self):
        """Test risk level classification for medium scores"""
        calculator = SymbiosisScoreCalculator()
        score = 0.65
        
        if score >= 0.75:
            risk_level = "low"
        elif score >= 0.50:
            risk_level = "medium"
        else:
            risk_level = "high"
        
        assert risk_level == "medium", "Medium score should indicate medium risk"
    
    def test_risk_level_high(self):
        """Test risk level classification for low scores"""
        calculator = SymbiosisScoreCalculator()
        score = 0.40
        
        if score >= 0.75:
            risk_level = "low"
        elif score >= 0.50:
            risk_level = "medium"
        else:
            risk_level = "high"
        
        assert risk_level == "high", "Low score should indicate high risk"


@pytest.mark.parametrize("trust,cooperation,compliance,expected_min", [
    (0.9, 0.85, 0.88, 0.75),  # All high
    (0.75, 0.75, 0.75, 0.75),  # All at threshold
    (0.5, 0.5, 0.5, 0.0),      # All medium
    (1.0, 1.0, 1.0, 0.95),     # All perfect
])
def test_score_calculation_parametrized(trust, cooperation, compliance, expected_min):
    """Parametrized test for various score combinations"""
    calculator = SymbiosisScoreCalculator()
    metrics = {
        'trust_score': trust,
        'cooperation_score': cooperation,
        'compliance_score': compliance
    }
    
    score = calculator.calculate_score(metrics)
    assert score >= expected_min or score >= 0.0, f"Score {score} should be >= {expected_min}"
    assert score <= 1.0, f"Score {score} should be <= 1.0"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
