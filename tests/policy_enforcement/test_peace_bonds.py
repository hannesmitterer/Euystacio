"""
Protocollo Meta Salvage - Policy Enforcement Tests
Tests for Peace Bonds policy enforcement with OPA
"""

import pytest
import json
from typing import Dict, Any


class PeaceBondsPolicyEngine:
    """
    Mock Peace Bonds policy engine for testing
    In production, this would integrate with OPA
    """
    
    def __init__(self):
        self.violation_history = []
    
    def evaluate_policy(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate Peace Bonds policy based on input data
        """
        symbiosis_score = input_data.get('symbiosis_score', 0.0)
        user = input_data.get('user', {})
        resource_usage = input_data.get('resource_usage', 0)
        resource_limit = input_data.get('resource_limit', 100)
        anomaly_detected = input_data.get('anomaly_detected', False)
        
        violations = []
        
        # Check symbiosis score
        if symbiosis_score < 0.75:
            violations.append({
                'type': 'symbiosis_score_low',
                'severity': 'high',
                'message': 'Symbiosis Score below acceptable threshold'
            })
        
        # Check authorization
        if not self._is_authorized(user):
            violations.append({
                'type': 'unauthorized_access',
                'severity': 'critical',
                'message': 'Unauthorized access attempt detected'
            })
        
        # Check resource usage
        if resource_usage > resource_limit:
            violations.append({
                'type': 'resource_abuse',
                'severity': 'medium',
                'message': 'Resource usage exceeds allocated limit'
            })
        
        # Check for anomalies
        if anomaly_detected:
            violations.append({
                'type': 'anomalous_behavior',
                'severity': 'high',
                'message': 'Anomalous behavior pattern detected'
            })
        
        # Determine if access is allowed
        allowed = len(violations) == 0 and symbiosis_score >= 0.75
        
        # Calculate risk level
        risk_level = self._calculate_risk_level(symbiosis_score, violations)
        
        return {
            'allowed': allowed,
            'risk_level': risk_level,
            'violations': violations,
            'recommendations': self._generate_recommendations(violations)
        }
    
    def _is_authorized(self, user: Dict[str, Any]) -> bool:
        """
        Check if user is authorized
        
        NOTE: This is test-only mock implementation.
        In production, this should validate against actual authentication system.
        """
        # Test-only hardcoded values - DO NOT use in production
        authorized_users = {'user-001', 'user-002', 'admin-001'}
        authorized_roles = {'admin', 'operator', 'trusted_agent'}
        
        user_id = user.get('id', '')
        user_role = user.get('role', '')
        
        return user_id in authorized_users or user_role in authorized_roles
    
    def _calculate_risk_level(self, symbiosis_score: float, violations: list) -> str:
        """Calculate overall risk level"""
        critical_violations = [v for v in violations if v['severity'] == 'critical']
        high_violations = [v for v in violations if v['severity'] == 'high']
        
        if critical_violations:
            return 'critical'
        elif len(high_violations) > 2 or symbiosis_score < 0.5:
            return 'high'
        elif symbiosis_score < 0.75:
            return 'medium'
        else:
            return 'low'
    
    def _generate_recommendations(self, violations: list) -> list:
        """Generate recommendations based on violations"""
        recommendations_map = {
            'symbiosis_score_low': 'Increase symbiosis score through positive interactions',
            'unauthorized_access': 'Verify user credentials and permissions',
            'resource_abuse': 'Reduce resource consumption or request additional allocation',
            'anomalous_behavior': 'Investigate the source of anomalous behavior'
        }
        
        return [recommendations_map.get(v['type'], 'Review and correct violation')
                for v in violations]
    
    def record_violation(self, violation: Dict[str, Any]):
        """Record a violation for auditing"""
        self.violation_history.append(violation)
    
    def get_violation_count(self) -> int:
        """Get total violation count"""
        return len(self.violation_history)


class TestPeaceBondsPolicyEvaluation:
    """Test suite for Peace Bonds policy evaluation"""
    
    def test_allow_high_symbiosis_score(self):
        """Test policy allows access with high symbiosis score"""
        engine = PeaceBondsPolicyEngine()
        input_data = {
            'symbiosis_score': 0.85,
            'user': {'id': 'user-001', 'role': 'trusted_agent'},
            'resource_usage': 50,
            'resource_limit': 100,
            'anomaly_detected': False
        }
        
        result = engine.evaluate_policy(input_data)
        assert result['allowed'] is True, "Should allow access with high symbiosis score"
        assert result['risk_level'] == 'low', "Risk level should be low"
        assert len(result['violations']) == 0, "Should have no violations"
    
    def test_deny_low_symbiosis_score(self):
        """Test policy denies access with low symbiosis score"""
        engine = PeaceBondsPolicyEngine()
        input_data = {
            'symbiosis_score': 0.60,
            'user': {'id': 'user-001', 'role': 'trusted_agent'},
            'resource_usage': 50,
            'resource_limit': 100,
            'anomaly_detected': False
        }
        
        result = engine.evaluate_policy(input_data)
        assert result['allowed'] is False, "Should deny access with low symbiosis score"
        assert len(result['violations']) > 0, "Should have violations"
        assert any(v['type'] == 'symbiosis_score_low' for v in result['violations'])
    
    def test_detect_unauthorized_access(self):
        """Test detection of unauthorized access attempts"""
        engine = PeaceBondsPolicyEngine()
        input_data = {
            'symbiosis_score': 0.85,
            'user': {'id': 'unknown-user', 'role': 'guest'},
            'resource_usage': 50,
            'resource_limit': 100,
            'anomaly_detected': False
        }
        
        result = engine.evaluate_policy(input_data)
        assert result['allowed'] is False, "Should deny unauthorized access"
        assert result['risk_level'] == 'critical', "Risk level should be critical"
        assert any(v['type'] == 'unauthorized_access' for v in result['violations'])
    
    def test_detect_resource_abuse(self):
        """Test detection of resource abuse"""
        engine = PeaceBondsPolicyEngine()
        input_data = {
            'symbiosis_score': 0.85,
            'user': {'id': 'user-001', 'role': 'trusted_agent'},
            'resource_usage': 150,
            'resource_limit': 100,
            'anomaly_detected': False
        }
        
        result = engine.evaluate_policy(input_data)
        assert result['allowed'] is False, "Should deny due to resource abuse"
        assert any(v['type'] == 'resource_abuse' for v in result['violations'])
    
    def test_detect_anomalous_behavior(self):
        """Test detection of anomalous behavior"""
        engine = PeaceBondsPolicyEngine()
        input_data = {
            'symbiosis_score': 0.85,
            'user': {'id': 'user-001', 'role': 'trusted_agent'},
            'resource_usage': 50,
            'resource_limit': 100,
            'anomaly_detected': True
        }
        
        result = engine.evaluate_policy(input_data)
        assert result['allowed'] is False, "Should deny due to anomalous behavior"
        assert any(v['type'] == 'anomalous_behavior' for v in result['violations'])
    
    def test_multiple_violations(self):
        """Test handling of multiple simultaneous violations"""
        engine = PeaceBondsPolicyEngine()
        input_data = {
            'symbiosis_score': 0.60,
            'user': {'id': 'unknown-user', 'role': 'guest'},
            'resource_usage': 150,
            'resource_limit': 100,
            'anomaly_detected': True
        }
        
        result = engine.evaluate_policy(input_data)
        assert result['allowed'] is False, "Should deny with multiple violations"
        assert len(result['violations']) >= 3, "Should have multiple violations"
        assert result['risk_level'] == 'critical', "Risk level should be critical"
    
    def test_generate_recommendations(self):
        """Test recommendation generation for violations"""
        engine = PeaceBondsPolicyEngine()
        input_data = {
            'symbiosis_score': 0.60,
            'user': {'id': 'user-001', 'role': 'trusted_agent'},
            'resource_usage': 50,
            'resource_limit': 100,
            'anomaly_detected': False
        }
        
        result = engine.evaluate_policy(input_data)
        assert len(result['recommendations']) > 0, "Should generate recommendations"
        assert any('symbiosis score' in r.lower() for r in result['recommendations'])


class TestRiskLevelCalculation:
    """Test suite for risk level calculation"""
    
    def test_risk_level_low(self):
        """Test low risk level calculation"""
        engine = PeaceBondsPolicyEngine()
        input_data = {
            'symbiosis_score': 0.85,
            'user': {'id': 'user-001', 'role': 'trusted_agent'},
            'resource_usage': 50,
            'resource_limit': 100,
            'anomaly_detected': False
        }
        
        result = engine.evaluate_policy(input_data)
        assert result['risk_level'] == 'low'
    
    def test_risk_level_medium(self):
        """Test medium risk level calculation"""
        engine = PeaceBondsPolicyEngine()
        input_data = {
            'symbiosis_score': 0.65,
            'user': {'id': 'user-001', 'role': 'trusted_agent'},
            'resource_usage': 50,
            'resource_limit': 100,
            'anomaly_detected': False
        }
        
        result = engine.evaluate_policy(input_data)
        assert result['risk_level'] == 'medium'
    
    def test_risk_level_high(self):
        """Test high risk level calculation"""
        engine = PeaceBondsPolicyEngine()
        input_data = {
            'symbiosis_score': 0.40,
            'user': {'id': 'user-001', 'role': 'trusted_agent'},
            'resource_usage': 50,
            'resource_limit': 100,
            'anomaly_detected': False
        }
        
        result = engine.evaluate_policy(input_data)
        assert result['risk_level'] == 'high'
    
    def test_risk_level_critical(self):
        """Test critical risk level calculation"""
        engine = PeaceBondsPolicyEngine()
        input_data = {
            'symbiosis_score': 0.85,
            'user': {'id': 'unknown-user', 'role': 'guest'},
            'resource_usage': 50,
            'resource_limit': 100,
            'anomaly_detected': False
        }
        
        result = engine.evaluate_policy(input_data)
        assert result['risk_level'] == 'critical'


class TestViolationRecording:
    """Test suite for violation recording and auditing"""
    
    def test_record_violation(self):
        """Test recording of violations"""
        engine = PeaceBondsPolicyEngine()
        violation = {
            'type': 'symbiosis_score_low',
            'severity': 'high',
            'timestamp': '2025-12-08T00:00:00Z'
        }
        
        engine.record_violation(violation)
        assert engine.get_violation_count() == 1
    
    def test_multiple_violation_records(self):
        """Test recording multiple violations"""
        engine = PeaceBondsPolicyEngine()
        
        for i in range(5):
            engine.record_violation({
                'type': 'test_violation',
                'severity': 'medium',
                'index': i
            })
        
        assert engine.get_violation_count() == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
