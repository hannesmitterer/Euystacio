"""
Tutor-Council Authority System
Establishes governance structure with defined operational boundaries
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from enum import Enum


class TutorRole(Enum):
    """Tutor roles within the Council"""
    GUARDIAN = "guardian"           # Protects Law of Equals
    MEDIATOR = "mediator"           # Resolves conflicts
    OBSERVER = "observer"           # Monitors and reports
    ARCHITECT = "architect"         # Shapes system evolution


class DecisionType(Enum):
    """Types of decisions the Council can make"""
    CONTENT_MODERATION = "content_moderation"
    SYSTEM_PARAMETER = "system_parameter"
    EMERGENCY_ACTION = "emergency_action"
    POLICY_CHANGE = "policy_change"


class TutorCouncil:
    """
    Manages the Tutor-Council governance structure.
    Provides authority framework for emergency decisions during Coronazione phase.
    """
    
    def __init__(self):
        """Initialize the Tutor-Council system."""
        self.tutors = {}  # tutor_id -> tutor info
        self.decisions = []  # Historical decisions
        self.operational_boundaries = self._initialize_boundaries()
        self.active_actions = []  # Currently active emergency actions
        self.metrics = {
            "total_decisions": 0,
            "by_type": {dt.value: 0 for dt in DecisionType},
            "emergency_actions": 0,
            "overturned_decisions": 0
        }
    
    def _initialize_boundaries(self) -> Dict[str, Any]:
        """Define initial operational boundaries for the Coronazione phase."""
        return {
            "max_pulse_rate_per_address": 10,  # Aligned with rate limiter
            "min_custos_sentimento_intensity": 0.3,  # Minimum meaningful intensity
            "max_queue_size": 1000,  # Maximum pulses in queue
            "content_review_threshold": 0.7,  # Anomaly score requiring review
            "emergency_lockdown_threshold": 0.9,  # Critical anomaly score
            "min_cdr_rate": 0.6,  # Minimum Conflict De-escalation Rate
            "tutor_quorum": 3,  # Minimum tutors for major decisions
            "decision_validity_hours": 24,  # How long decisions remain active
        }
    
    def register_tutor(
        self, 
        tutor_id: str, 
        name: str, 
        role: TutorRole,
        credentials: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Register a new tutor with the Council.
        
        Args:
            tutor_id: Unique identifier for the tutor
            name: Human-readable name
            role: Tutor's role in the Council
            credentials: Verification credentials
            
        Returns:
            Registration result
        """
        if tutor_id in self.tutors:
            return {
                "success": False,
                "reason": "tutor_already_registered",
                "tutor_id": tutor_id
            }
        
        self.tutors[tutor_id] = {
            "tutor_id": tutor_id,
            "name": name,
            "role": role.value,
            "credentials": credentials,
            "registered_at": datetime.utcnow().isoformat(),
            "active": True,
            "decisions_made": 0,
            "last_activity": datetime.utcnow().isoformat()
        }
        
        return {
            "success": True,
            "tutor_id": tutor_id,
            "role": role.value
        }
    
    def deactivate_tutor(self, tutor_id: str) -> bool:
        """Deactivate a tutor (emergency action)."""
        if tutor_id in self.tutors:
            self.tutors[tutor_id]["active"] = False
            return True
        return False
    
    def get_active_tutors(self) -> List[Dict[str, Any]]:
        """Get list of all active tutors."""
        return [
            tutor for tutor in self.tutors.values()
            if tutor["active"]
        ]
    
    def get_tutors_by_role(self, role: TutorRole) -> List[Dict[str, Any]]:
        """Get tutors with a specific role."""
        return [
            tutor for tutor in self.tutors.values()
            if tutor["role"] == role.value and tutor["active"]
        ]
    
    def make_decision(
        self,
        decision_type: DecisionType,
        initiator_tutor_id: str,
        description: str,
        parameters: Dict[str, Any],
        requires_quorum: bool = False
    ) -> Dict[str, Any]:
        """
        Record a Council decision.
        
        Args:
            decision_type: Type of decision being made
            initiator_tutor_id: Tutor initiating the decision
            description: Human-readable description
            parameters: Decision parameters and actions
            requires_quorum: Whether this decision requires quorum
            
        Returns:
            Decision result
        """
        if initiator_tutor_id not in self.tutors:
            return {
                "success": False,
                "reason": "invalid_tutor",
                "tutor_id": initiator_tutor_id
            }
        
        if not self.tutors[initiator_tutor_id]["active"]:
            return {
                "success": False,
                "reason": "tutor_not_active",
                "tutor_id": initiator_tutor_id
            }
        
        # Check quorum if required
        if requires_quorum:
            active_count = len(self.get_active_tutors())
            required_quorum = self.operational_boundaries["tutor_quorum"]
            
            if active_count < required_quorum:
                return {
                    "success": False,
                    "reason": "insufficient_quorum",
                    "active_tutors": active_count,
                    "required": required_quorum
                }
        
        decision = {
            "decision_id": f"DEC-{len(self.decisions) + 1:06d}",
            "type": decision_type.value,
            "initiator": initiator_tutor_id,
            "description": description,
            "parameters": parameters,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "active",
            "requires_quorum": requires_quorum
        }
        
        self.decisions.append(decision)
        self.tutors[initiator_tutor_id]["decisions_made"] += 1
        self.tutors[initiator_tutor_id]["last_activity"] = datetime.utcnow().isoformat()
        
        self.metrics["total_decisions"] += 1
        self.metrics["by_type"][decision_type.value] += 1
        
        if decision_type == DecisionType.EMERGENCY_ACTION:
            self.metrics["emergency_actions"] += 1
            self.active_actions.append(decision)
        
        return {
            "success": True,
            "decision_id": decision["decision_id"],
            "decision": decision
        }
    
    def overturn_decision(
        self,
        decision_id: str,
        tutor_id: str,
        reason: str
    ) -> Dict[str, Any]:
        """
        Overturn a previous decision (requires high authority).
        
        Args:
            decision_id: ID of decision to overturn
            tutor_id: Tutor overturning the decision
            reason: Reason for overturning
            
        Returns:
            Result of overturn action
        """
        # Find decision
        decision = next(
            (d for d in self.decisions if d["decision_id"] == decision_id),
            None
        )
        
        if not decision:
            return {
                "success": False,
                "reason": "decision_not_found",
                "decision_id": decision_id
            }
        
        if decision["status"] != "active":
            return {
                "success": False,
                "reason": "decision_not_active",
                "decision_id": decision_id
            }
        
        # Only Guardians can overturn decisions
        if tutor_id not in self.tutors or self.tutors[tutor_id]["role"] != TutorRole.GUARDIAN.value:
            return {
                "success": False,
                "reason": "insufficient_authority",
                "required_role": TutorRole.GUARDIAN.value
            }
        
        decision["status"] = "overturned"
        decision["overturned_by"] = tutor_id
        decision["overturned_at"] = datetime.utcnow().isoformat()
        decision["overturn_reason"] = reason
        
        self.metrics["overturned_decisions"] += 1
        
        # Remove from active actions if applicable
        self.active_actions = [
            a for a in self.active_actions 
            if a["decision_id"] != decision_id
        ]
        
        return {
            "success": True,
            "decision_id": decision_id,
            "overturned_at": decision["overturned_at"]
        }
    
    def get_operational_boundary(self, key: str) -> Any:
        """Get a specific operational boundary value."""
        return self.operational_boundaries.get(key)
    
    def update_operational_boundary(
        self,
        key: str,
        value: Any,
        tutor_id: str,
        reason: str
    ) -> Dict[str, Any]:
        """
        Update an operational boundary (creates a decision record).
        
        Args:
            key: Boundary parameter to update
            value: New value
            tutor_id: Tutor making the change
            reason: Reason for change
            
        Returns:
            Update result
        """
        if key not in self.operational_boundaries:
            return {
                "success": False,
                "reason": "invalid_boundary_key",
                "key": key
            }
        
        old_value = self.operational_boundaries[key]
        
        # Create decision record
        decision_result = self.make_decision(
            DecisionType.SYSTEM_PARAMETER,
            tutor_id,
            f"Update {key}: {old_value} -> {value}. Reason: {reason}",
            {
                "boundary_key": key,
                "old_value": old_value,
                "new_value": value,
                "reason": reason
            },
            requires_quorum=True
        )
        
        if decision_result["success"]:
            self.operational_boundaries[key] = value
            return {
                "success": True,
                "key": key,
                "old_value": old_value,
                "new_value": value,
                "decision_id": decision_result["decision_id"]
            }
        
        return decision_result
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get Council governance metrics."""
        return {
            "active_tutors": len(self.get_active_tutors()),
            "total_tutors": len(self.tutors),
            "tutors_by_role": {
                role.value: len(self.get_tutors_by_role(role))
                for role in TutorRole
            },
            "decisions": self.metrics,
            "active_emergency_actions": len(self.active_actions)
        }
