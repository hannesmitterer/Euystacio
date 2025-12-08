"""
Constraint Manager
==================

Manages operational constraints applied to CaaS providers.
Ensures constraints are properly enforced and monitored.
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class OperationalConstraint:
    """Represents an operational constraint"""
    constraint_id: str
    provider: str
    constraint_type: str
    parameters: Dict[str, Any]
    enforced_at: str
    compliance_status: str = 'pending'  # pending, compliant, violated
    
    def to_dict(self) -> Dict:
        return {
            'constraint_id': self.constraint_id,
            'provider': self.provider,
            'constraint_type': self.constraint_type,
            'parameters': self.parameters,
            'enforced_at': self.enforced_at,
            'compliance_status': self.compliance_status
        }


class ConstraintManager:
    """
    Manages operational constraints for Peace Bonds.
    
    Tracks constraint enforcement, monitors compliance, and
    reports violations.
    """
    
    def __init__(self):
        """Initialize the Constraint Manager"""
        self.active_constraints: Dict[str, OperationalConstraint] = {}
        self.constraint_history: List[OperationalConstraint] = []
        self.violations: List[Dict[str, Any]] = []
        
        logger.info("Constraint Manager initialized")
    
    def apply_constraints(self, provider: str, constraints: Dict[str, Any]) -> List[OperationalConstraint]:
        """
        Apply a set of constraints to a provider.
        
        Args:
            provider: Name of the CaaS provider
            constraints: Dictionary of constraints to apply
            
        Returns:
            List of created OperationalConstraint objects
        """
        applied = []
        
        for constraint_type, parameters in constraints.items():
            constraint = self._create_constraint(provider, constraint_type, parameters)
            self.active_constraints[constraint.constraint_id] = constraint
            self.constraint_history.append(constraint)
            applied.append(constraint)
            
            logger.info(f"Applied constraint to {provider}: {constraint_type}")
        
        return applied
    
    def _create_constraint(
        self, 
        provider: str, 
        constraint_type: str, 
        parameters: Any
    ) -> OperationalConstraint:
        """Create a new operational constraint"""
        
        constraint_id = f"constraint_{provider}_{constraint_type}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        # Normalize parameters to dict
        if not isinstance(parameters, dict):
            parameters = {'value': parameters}
        
        return OperationalConstraint(
            constraint_id=constraint_id,
            provider=provider,
            constraint_type=constraint_type,
            parameters=parameters,
            enforced_at=datetime.utcnow().isoformat()
        )
    
    def check_compliance(self, provider: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check compliance with constraints for a provider.
        
        Args:
            provider: Name of the provider
            metrics: Current operational metrics
            
        Returns:
            Compliance report
        """
        provider_constraints = [
            c for c in self.active_constraints.values() 
            if c.provider == provider
        ]
        
        compliant = []
        violated = []
        
        for constraint in provider_constraints:
            if self._check_constraint_compliance(constraint, metrics):
                constraint.compliance_status = 'compliant'
                compliant.append(constraint.constraint_id)
            else:
                constraint.compliance_status = 'violated'
                violated.append(constraint.constraint_id)
                self._record_violation(constraint, metrics)
        
        return {
            'provider': provider,
            'timestamp': datetime.utcnow().isoformat(),
            'total_constraints': len(provider_constraints),
            'compliant': compliant,
            'violated': violated,
            'compliance_rate': len(compliant) / len(provider_constraints) if provider_constraints else 1.0
        }
    
    def _check_constraint_compliance(
        self, 
        constraint: OperationalConstraint, 
        metrics: Dict[str, Any]
    ) -> bool:
        """Check if a constraint is being complied with"""
        
        constraint_type = constraint.constraint_type
        parameters = constraint.parameters
        
        if constraint_type == 'throughput_limit':
            limit = parameters.get('value', '100%')
            if isinstance(limit, str) and limit.endswith('%'):
                limit_pct = float(limit.rstrip('%')) / 100
                current = metrics.get('throughput_utilization', 0)
                return current <= limit_pct
        
        elif constraint_type == 'monitoring_interval':
            # Check if monitoring is happening at required interval
            return metrics.get('monitoring_active', False)
        
        elif constraint_type == 'data_portability_required':
            return metrics.get('data_export_available', False)
        
        elif constraint_type == 'transparency_reporting':
            return metrics.get('transparency_reports_enabled', False)
        
        elif constraint_type == 'migration_plan_required':
            return metrics.get('migration_plan_exists', False)
        
        elif constraint_type == 'redundant_provider_active':
            return metrics.get('redundant_provider_configured', False)
        
        elif constraint_type == 'audit_trail_enabled':
            return metrics.get('audit_logging_active', False)
        
        # Default to compliant if we can't check
        return True
    
    def _record_violation(self, constraint: OperationalConstraint, metrics: Dict[str, Any]):
        """Record a constraint violation"""
        violation = {
            'timestamp': datetime.utcnow().isoformat(),
            'constraint_id': constraint.constraint_id,
            'provider': constraint.provider,
            'constraint_type': constraint.constraint_type,
            'parameters': constraint.parameters,
            'metrics': metrics
        }
        
        self.violations.append(violation)
        
        logger.warning(
            f"Constraint violation detected: {constraint.constraint_type} "
            f"for {constraint.provider}"
        )
    
    def remove_constraint(self, constraint_id: str):
        """Remove a constraint"""
        if constraint_id in self.active_constraints:
            constraint = self.active_constraints[constraint_id]
            del self.active_constraints[constraint_id]
            
            logger.info(f"Removed constraint: {constraint_id} for {constraint.provider}")
    
    def remove_provider_constraints(self, provider: str):
        """Remove all constraints for a provider"""
        to_remove = [
            cid for cid, c in self.active_constraints.items() 
            if c.provider == provider
        ]
        
        for cid in to_remove:
            self.remove_constraint(cid)
        
        logger.info(f"Removed {len(to_remove)} constraints for {provider}")
    
    def get_active_constraints(self, provider: Optional[str] = None) -> List[OperationalConstraint]:
        """Get active constraints, optionally filtered by provider"""
        constraints = list(self.active_constraints.values())
        
        if provider:
            constraints = [c for c in constraints if c.provider == provider]
        
        return constraints
    
    def get_violations(self, provider: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent violations"""
        violations = self.violations[-limit:]
        
        if provider:
            violations = [v for v in violations if v['provider'] == provider]
        
        return violations
    
    def get_constraint_status(self) -> Dict[str, Any]:
        """Get overall constraint status"""
        compliant = len([c for c in self.active_constraints.values() if c.compliance_status == 'compliant'])
        violated = len([c for c in self.active_constraints.values() if c.compliance_status == 'violated'])
        
        return {
            'total_constraints': len(self.active_constraints),
            'compliant': compliant,
            'violated': violated,
            'total_violations': len(self.violations),
            'compliance_rate': compliant / len(self.active_constraints) if self.active_constraints else 1.0
        }
