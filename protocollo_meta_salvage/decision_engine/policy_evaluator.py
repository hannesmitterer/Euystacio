"""
Policy Evaluator
================

Evaluates policies in the style of Open Policy Agent (OPA).
Determines which policies apply and what actions should be taken.
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class Policy:
    """Represents an operational policy"""
    policy_id: str
    name: str
    description: str
    rules: List[Dict[str, Any]]
    actions: List[str]
    priority: int = 0
    enabled: bool = True


class PolicyEvaluator:
    """
    Evaluates policies to determine operational constraints.
    
    Inspired by Open Policy Agent (OPA), this evaluator applies
    declarative policies to make autonomous decisions about
    Peace Bond enforcement.
    """
    
    def __init__(self):
        """Initialize the Policy Evaluator"""
        self.policies: Dict[str, Policy] = {}
        self.evaluation_history: List[Dict[str, Any]] = []
        
        # Load default policies
        self._load_default_policies()
        
        logger.info("Policy Evaluator initialized")
    
    def _load_default_policies(self):
        """Load default operational policies"""
        
        # Throughput limitation policy
        throughput_policy = Policy(
            policy_id='pol_throughput_limit',
            name='Throughput Limitation',
            description='Limit throughput when lock-in risk is detected',
            rules=[
                {'condition': 'lock_in_risk > 0.5', 'threshold': 0.5},
                {'condition': 'symbiosis_score < 0.7', 'threshold': 0.7}
            ],
            actions=['limit_throughput', 'enable_monitoring'],
            priority=10
        )
        
        # Data portability policy
        portability_policy = Policy(
            policy_id='pol_data_portability',
            name='Data Portability Enforcement',
            description='Ensure data can be exported at any time',
            rules=[
                {'condition': 'lock_in_risk > 0.3', 'threshold': 0.3}
            ],
            actions=['enable_data_export', 'test_portability', 'document_format'],
            priority=20
        )
        
        # Transparency policy
        transparency_policy = Policy(
            policy_id='pol_transparency',
            name='Transparency Requirements',
            description='Enforce transparency and audit logging',
            rules=[
                {'condition': 'transparency_level < 0.8', 'threshold': 0.8}
            ],
            actions=['enable_audit_log', 'require_api_documentation', 'metadata_sharing'],
            priority=15
        )
        
        # Redundancy policy
        redundancy_policy = Policy(
            policy_id='pol_redundancy',
            name='Provider Redundancy',
            description='Maintain alternative providers for critical services',
            rules=[
                {'condition': 'symbiosis_score < 0.5', 'threshold': 0.5},
                {'condition': 'lock_in_risk > 0.6', 'threshold': 0.6}
            ],
            actions=['identify_alternatives', 'setup_redundancy', 'test_failover'],
            priority=25
        )
        
        # Ethical compliance policy
        ethical_policy = Policy(
            policy_id='pol_ethical_compliance',
            name='Ethical Compliance',
            description='Ensure ethical standards are maintained',
            rules=[
                {'condition': 'ethical_compliance < 0.7', 'threshold': 0.7}
            ],
            actions=['activate_ethical_review', 'restrict_operations', 'escalate_concern'],
            priority=30
        )
        
        for policy in [throughput_policy, portability_policy, transparency_policy, 
                       redundancy_policy, ethical_policy]:
            self.policies[policy.policy_id] = policy
    
    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate all policies against the current context.
        
        Args:
            context: Current system state and metrics
            
        Returns:
            Dictionary containing applicable policies and required actions
        """
        applicable_policies = []
        required_actions = set()
        
        # Sort policies by priority
        sorted_policies = sorted(
            self.policies.values(), 
            key=lambda p: p.priority, 
            reverse=True
        )
        
        for policy in sorted_policies:
            if not policy.enabled:
                continue
            
            if self._evaluate_policy(policy, context):
                applicable_policies.append(policy.policy_id)
                required_actions.update(policy.actions)
        
        result = {
            'timestamp': datetime.utcnow().isoformat(),
            'applicable_policies': applicable_policies,
            'required_actions': list(required_actions),
            'context': context
        }
        
        self.evaluation_history.append(result)
        
        if applicable_policies:
            logger.info(f"Policies triggered: {', '.join(applicable_policies)}")
        
        return result
    
    def _evaluate_policy(self, policy: Policy, context: Dict[str, Any]) -> bool:
        """Evaluate if a policy applies to the current context"""
        
        for rule in policy.rules:
            condition = rule['condition']
            threshold = rule['threshold']
            
            if self._evaluate_rule(condition, threshold, context):
                return True
        
        return False
    
    def _evaluate_rule(self, condition: str, threshold: float, context: Dict[str, Any]) -> bool:
        """Evaluate a single rule condition"""
        
        # Parse condition string
        if 'lock_in_risk >' in condition:
            return context.get('lock_in_risk', 0) > threshold
        
        elif 'symbiosis_score <' in condition:
            return context.get('symbiosis_score', 1.0) < threshold
        
        elif 'transparency_level <' in condition:
            return context.get('transparency_level', 1.0) < threshold
        
        elif 'ethical_compliance <' in condition:
            return context.get('ethical_compliance', 1.0) < threshold
        
        return False
    
    def add_policy(self, policy: Policy):
        """Add a new policy"""
        self.policies[policy.policy_id] = policy
        logger.info(f"Policy added: {policy.name}")
    
    def remove_policy(self, policy_id: str):
        """Remove a policy"""
        if policy_id in self.policies:
            del self.policies[policy_id]
            logger.info(f"Policy removed: {policy_id}")
    
    def enable_policy(self, policy_id: str):
        """Enable a policy"""
        if policy_id in self.policies:
            self.policies[policy_id].enabled = True
            logger.info(f"Policy enabled: {policy_id}")
    
    def disable_policy(self, policy_id: str):
        """Disable a policy"""
        if policy_id in self.policies:
            self.policies[policy_id].enabled = False
            logger.info(f"Policy disabled: {policy_id}")
    
    def get_policy_status(self) -> Dict[str, Any]:
        """Get status of all policies"""
        return {
            'total_policies': len(self.policies),
            'enabled_policies': len([p for p in self.policies.values() if p.enabled]),
            'evaluations_performed': len(self.evaluation_history),
            'policies': {
                pid: {
                    'name': p.name,
                    'enabled': p.enabled,
                    'priority': p.priority
                }
                for pid, p in self.policies.items()
            }
        }
