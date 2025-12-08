"""
Trigger Manager
===============

Manages triggers that activate the Peace Bond protocol based on
monitoring data and detected anomalies.
"""

import logging
from typing import Dict, List, Callable, Any
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class Trigger:
    """Represents a trigger condition"""
    name: str
    condition: str
    threshold: float
    action: str
    activated: bool = False
    activation_time: str = None


class TriggerManager:
    """
    Manages protocol activation triggers.
    
    Coordinates between monitoring systems and decision engines to
    determine when Peace Bonds should be activated or escalated.
    """
    
    def __init__(self):
        """Initialize the Trigger Manager"""
        self.triggers: Dict[str, Trigger] = {}
        self.callbacks: Dict[str, List[Callable]] = {}
        self.activation_history: List[Dict[str, Any]] = []
        
        # Initialize default triggers
        self._initialize_default_triggers()
        
        logger.info("Trigger Manager initialized")
    
    def _initialize_default_triggers(self):
        """Initialize default trigger conditions"""
        default_triggers = [
            Trigger(
                name='symbiosis_score_critical',
                condition='symbiosis_score < threshold',
                threshold=0.3,
                action='activate_critical_peace_bonds'
            ),
            Trigger(
                name='symbiosis_score_degradation',
                condition='score_decrease > threshold',
                threshold=0.15,  # 15% decrease
                action='activate_standard_peace_bonds'
            ),
            Trigger(
                name='lock_in_risk_detected',
                condition='lock_in_risk > threshold',
                threshold=0.5,
                action='enforce_migration_readiness'
            ),
            Trigger(
                name='transparency_failure',
                condition='transparency_level < threshold',
                threshold=0.5,
                action='enforce_transparency_requirements'
            ),
            Trigger(
                name='ethical_violation',
                condition='ethical_compliance < threshold',
                threshold=0.7,
                action='activate_ethical_safeguards'
            ),
            Trigger(
                name='anomaly_critical',
                condition='anomaly_severity == critical',
                threshold=1.0,
                action='immediate_investigation'
            )
        ]
        
        for trigger in default_triggers:
            self.triggers[trigger.name] = trigger
    
    def register_callback(self, trigger_name: str, callback: Callable):
        """
        Register a callback function for a trigger.
        
        Args:
            trigger_name: Name of the trigger
            callback: Function to call when trigger activates
        """
        if trigger_name not in self.callbacks:
            self.callbacks[trigger_name] = []
        
        self.callbacks[trigger_name].append(callback)
        logger.info(f"Registered callback for trigger: {trigger_name}")
    
    def evaluate_triggers(self, metrics: Dict[str, Any]) -> List[str]:
        """
        Evaluate all triggers against current metrics.
        
        Args:
            metrics: Current system metrics
            
        Returns:
            List of activated trigger names
        """
        activated = []
        
        for name, trigger in self.triggers.items():
            should_activate = self._check_trigger_condition(trigger, metrics)
            
            if should_activate and not trigger.activated:
                self._activate_trigger(trigger, metrics)
                activated.append(name)
            elif not should_activate and trigger.activated:
                self._deactivate_trigger(trigger)
        
        return activated
    
    def _check_trigger_condition(self, trigger: Trigger, metrics: Dict[str, Any]) -> bool:
        """Check if a trigger condition is met"""
        if trigger.name == 'symbiosis_score_critical':
            return metrics.get('symbiosis_score', 1.0) < trigger.threshold
        
        elif trigger.name == 'symbiosis_score_degradation':
            current = metrics.get('symbiosis_score', 1.0)
            previous = metrics.get('previous_symbiosis_score', 1.0)
            decrease = previous - current
            return decrease > trigger.threshold
        
        elif trigger.name == 'lock_in_risk_detected':
            return metrics.get('lock_in_risk', 0) > trigger.threshold
        
        elif trigger.name == 'transparency_failure':
            return metrics.get('transparency_level', 1.0) < trigger.threshold
        
        elif trigger.name == 'ethical_violation':
            return metrics.get('ethical_compliance', 1.0) < trigger.threshold
        
        elif trigger.name == 'anomaly_critical':
            return metrics.get('anomaly_severity') == 'critical'
        
        return False
    
    def _activate_trigger(self, trigger: Trigger, metrics: Dict[str, Any]):
        """Activate a trigger and execute callbacks"""
        trigger.activated = True
        trigger.activation_time = datetime.utcnow().isoformat()
        
        activation_event = {
            'trigger_name': trigger.name,
            'action': trigger.action,
            'timestamp': trigger.activation_time,
            'metrics': metrics
        }
        
        self.activation_history.append(activation_event)
        
        logger.warning(f"TRIGGER ACTIVATED: {trigger.name} -> {trigger.action}")
        
        # Execute registered callbacks
        if trigger.name in self.callbacks:
            for callback in self.callbacks[trigger.name]:
                try:
                    callback(activation_event)
                except Exception as e:
                    logger.error(f"Error executing callback for {trigger.name}: {e}")
    
    def _deactivate_trigger(self, trigger: Trigger):
        """Deactivate a trigger"""
        trigger.activated = False
        trigger.activation_time = None
        
        logger.info(f"Trigger deactivated: {trigger.name}")
    
    def get_active_triggers(self) -> List[Trigger]:
        """Get list of currently active triggers"""
        return [t for t in self.triggers.values() if t.activated]
    
    def get_trigger_status(self) -> Dict[str, Any]:
        """Get status of all triggers"""
        return {
            'total_triggers': len(self.triggers),
            'active_triggers': len(self.get_active_triggers()),
            'trigger_list': {
                name: {
                    'activated': t.activated,
                    'threshold': t.threshold,
                    'action': t.action,
                    'activation_time': t.activation_time
                }
                for name, t in self.triggers.items()
            }
        }
    
    def get_activation_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent trigger activation history"""
        return self.activation_history[-limit:]
