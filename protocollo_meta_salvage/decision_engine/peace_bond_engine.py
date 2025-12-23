"""
Peace Bond Engine
=================

Core decision engine for Peace Bonds (Vincoli Preventivi).
Implements autonomous decision-making for ethical risk mitigation.
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class BondSeverity(Enum):
    """Severity levels for Peace Bonds"""
    PREVENTIVE = "preventive"  # Precautionary measures
    STANDARD = "standard"      # Standard restrictions
    ELEVATED = "elevated"      # Heightened controls
    CRITICAL = "critical"      # Maximum restrictions


@dataclass
class PeaceBond:
    """Represents a Peace Bond (Vincolo Preventivo)"""
    bond_id: str
    provider: str
    severity: BondSeverity
    constraints: Dict[str, Any]
    reason: str
    activated_at: str
    expires_at: Optional[str] = None
    active: bool = True
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['severity'] = self.severity.value
        return data


class PeaceBondEngine:
    """
    Engine for creating and managing Peace Bonds.
    
    Peace Bonds are operational constraints applied to CaaS providers
    during periods of ethical risk to preserve system integrity and
    prevent lock-in scenarios.
    """
    
    def __init__(self):
        """Initialize the Peace Bond Engine"""
        self.active_bonds: Dict[str, PeaceBond] = {}
        self.bond_history: List[PeaceBond] = []
        self.decision_log: List[Dict[str, Any]] = []
        
        logger.info("Peace Bond Engine initialized")
    
    def evaluate_situation(self, metrics: Dict[str, Any]) -> Optional[PeaceBond]:
        """
        Evaluate the current situation and decide if a Peace Bond is needed.
        
        Args:
            metrics: Current system metrics and risk indicators
            
        Returns:
            PeaceBond if one should be activated, None otherwise
        """
        provider = metrics.get('provider', 'unknown')
        symbiosis_score = metrics.get('symbiosis_score', 1.0)
        lock_in_risk = metrics.get('lock_in_risk', 0)
        ethical_compliance = metrics.get('ethical_compliance', 1.0)
        
        # Determine severity level
        severity = self._determine_severity(symbiosis_score, lock_in_risk, ethical_compliance)
        
        if severity is None:
            logger.info(f"No Peace Bond required for {provider}")
            return None
        
        # Create constraints based on severity
        constraints = self._create_constraints(severity, metrics)
        
        # Create Peace Bond
        bond = PeaceBond(
            bond_id=f"bond_{provider}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            provider=provider,
            severity=severity,
            constraints=constraints,
            reason=self._generate_reason(metrics),
            activated_at=datetime.utcnow().isoformat()
        )
        
        # Log decision
        self._log_decision(bond, metrics)
        
        logger.warning(f"Peace Bond created for {provider}: {severity.value}")
        
        return bond
    
    def _determine_severity(
        self, 
        symbiosis_score: float, 
        lock_in_risk: float, 
        ethical_compliance: float
    ) -> Optional[BondSeverity]:
        """Determine the appropriate severity level for a Peace Bond"""
        
        # Critical situation - immediate action required
        if symbiosis_score < 0.3 or ethical_compliance < 0.5:
            return BondSeverity.CRITICAL
        
        # Elevated risk - strong measures needed
        elif symbiosis_score < 0.5 or lock_in_risk > 0.7:
            return BondSeverity.ELEVATED
        
        # Standard risk - normal protective measures
        elif symbiosis_score < 0.7 or lock_in_risk > 0.4:
            return BondSeverity.STANDARD
        
        # Preventive - early warning signs
        elif symbiosis_score < 0.85 or lock_in_risk > 0.2:
            return BondSeverity.PREVENTIVE
        
        # No bond needed
        return None
    
    def _create_constraints(self, severity: BondSeverity, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Create operational constraints based on severity level"""
        
        base_constraints = {
            'data_portability_required': True,
            'transparency_reporting': True,
            'audit_trail_enabled': True
        }
        
        if severity == BondSeverity.PREVENTIVE:
            return {
                **base_constraints,
                'monitoring_interval': '1h',
                'alert_threshold': 0.85,
                'data_export_available': True
            }
        
        elif severity == BondSeverity.STANDARD:
            return {
                **base_constraints,
                'monitoring_interval': '30m',
                'alert_threshold': 0.7,
                'throughput_limit': '80%',
                'migration_plan_required': True,
                'alternative_provider_identified': True
            }
        
        elif severity == BondSeverity.ELEVATED:
            return {
                **base_constraints,
                'monitoring_interval': '15m',
                'alert_threshold': 0.5,
                'throughput_limit': '60%',
                'migration_plan_required': True,
                'migration_testing_required': True,
                'redundant_provider_active': True,
                'data_replication_enabled': True
            }
        
        elif severity == BondSeverity.CRITICAL:
            return {
                **base_constraints,
                'monitoring_interval': '5m',
                'alert_threshold': 0.3,
                'throughput_limit': '40%',
                'immediate_migration_prepared': True,
                'redundant_provider_active': True,
                'active_active_configuration': True,
                'data_synchronization_continuous': True,
                'manual_approval_required': True
            }
        
        return base_constraints
    
    def _generate_reason(self, metrics: Dict[str, Any]) -> str:
        """Generate a human-readable reason for the Peace Bond"""
        reasons = []
        
        if metrics.get('symbiosis_score', 1.0) < 0.7:
            reasons.append(f"Low symbiosis score: {metrics['symbiosis_score']:.2f}")
        
        if metrics.get('lock_in_risk', 0) > 0.4:
            reasons.append(f"Elevated lock-in risk: {metrics['lock_in_risk']:.2f}")
        
        if metrics.get('ethical_compliance', 1.0) < 0.8:
            reasons.append(f"Ethical compliance concern: {metrics['ethical_compliance']:.2f}")
        
        if metrics.get('transparency_level', 1.0) < 0.6:
            reasons.append(f"Insufficient transparency: {metrics['transparency_level']:.2f}")
        
        return "; ".join(reasons) if reasons else "Preventive measure"
    
    def _log_decision(self, bond: PeaceBond, metrics: Dict[str, Any]):
        """Log the decision for audit purposes"""
        self.decision_log.append({
            'timestamp': datetime.utcnow().isoformat(),
            'bond_id': bond.bond_id,
            'provider': bond.provider,
            'severity': bond.severity.value,
            'reason': bond.reason,
            'metrics': metrics
        })
    
    def activate_bond(self, bond: PeaceBond):
        """Activate a Peace Bond"""
        self.active_bonds[bond.bond_id] = bond
        self.bond_history.append(bond)
        
        logger.info(f"Peace Bond activated: {bond.bond_id}")
    
    def deactivate_bond(self, bond_id: str):
        """Deactivate a Peace Bond"""
        if bond_id in self.active_bonds:
            bond = self.active_bonds[bond_id]
            bond.active = False
            del self.active_bonds[bond_id]
            
            logger.info(f"Peace Bond deactivated: {bond_id}")
    
    def get_active_bonds(self) -> List[PeaceBond]:
        """Get all active Peace Bonds"""
        return list(self.active_bonds.values())
    
    def get_bonds_for_provider(self, provider: str) -> List[PeaceBond]:
        """Get all active bonds for a specific provider"""
        return [b for b in self.active_bonds.values() if b.provider == provider]
    
    def get_engine_status(self) -> Dict[str, Any]:
        """Get status of the Peace Bond Engine"""
        return {
            'active_bonds': len(self.active_bonds),
            'total_bonds_created': len(self.bond_history),
            'decisions_logged': len(self.decision_log),
            'bonds_by_severity': self._count_by_severity()
        }
    
    def _count_by_severity(self) -> Dict[str, int]:
        """Count active bonds by severity"""
        counts = {s.value: 0 for s in BondSeverity}
        for bond in self.active_bonds.values():
            counts[bond.severity.value] += 1
        return counts
