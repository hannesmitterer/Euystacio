"""
Gated Symbiosis Trial
Universal pre-entry filter requiring minimum Conflict De-escalation Rates (CDR)
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict


class GatedSymbiosisTrial:
    """
    Implements pre-entry filtering based on Conflict De-escalation Rate (CDR).
    New addresses must demonstrate conflict de-escalation capability before full access.
    """
    
    # Minimum CDR required for different access levels
    CDR_THRESHOLDS = {
        "trial": 0.0,        # Initial trial access, no CDR requirement yet
        "provisional": 0.5,  # Provisional access, 50% de-escalation rate
        "standard": 0.6,     # Standard access, 60% de-escalation rate
        "trusted": 0.75      # Trusted access, 75% de-escalation rate
    }
    
    # Trial period durations
    TRIAL_PERIODS = {
        "initial": timedelta(hours=24),      # Initial trial: 24 hours
        "provisional": timedelta(days=7),    # Provisional: 7 days
        "standard": timedelta(days=30)       # Standard: 30 days before trusted
    }
    
    def __init__(self, min_cdr_required: float = 0.6):
        """
        Initialize Gated Symbiosis Trial system.
        
        Args:
            min_cdr_required: Minimum CDR rate for standard access
        """
        self.min_cdr = min_cdr_required
        self.addresses = {}  # address -> trial status
        self.interaction_history = defaultdict(list)  # address -> interactions
        self.metrics = {
            "total_addresses": 0,
            "trial_passes": 0,
            "trial_failures": 0,
            "by_status": defaultdict(int)
        }
    
    def register_address(self, address: str) -> Dict[str, Any]:
        """
        Register a new address for trial period.
        
        Args:
            address: Address to register
            
        Returns:
            Registration result with trial status
        """
        if address in self.addresses:
            return {
                "success": False,
                "reason": "address_already_registered",
                "current_status": self.addresses[address]["status"]
            }
        
        self.addresses[address] = {
            "address": address,
            "status": "trial",
            "registered_at": datetime.utcnow(),
            "trial_ends": datetime.utcnow() + self.TRIAL_PERIODS["initial"],
            "conflict_count": 0,
            "deescalation_count": 0,
            "escalation_count": 0,
            "cdr": 0.0,
            "violations": []
        }
        
        self.metrics["total_addresses"] += 1
        self.metrics["by_status"]["trial"] += 1
        
        return {
            "success": True,
            "address": address,
            "status": "trial",
            "trial_period_hours": self.TRIAL_PERIODS["initial"].total_seconds() / 3600,
            "min_cdr_required": self.min_cdr
        }
    
    def record_interaction(
        self,
        address: str,
        interaction_type: str,
        emotional_context: Dict[str, Any],
        deescalated: bool
    ) -> Dict[str, Any]:
        """
        Record an interaction and update CDR.
        
        Args:
            address: Address of interacting entity
            interaction_type: Type of interaction (pulse, response, etc.)
            emotional_context: Emotional data from interaction
            deescalated: Whether the interaction de-escalated conflict
            
        Returns:
            Updated CDR status
        """
        if address not in self.addresses:
            # Auto-register if not registered
            self.register_address(address)
        
        # Record interaction
        interaction = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": interaction_type,
            "emotional_context": emotional_context,
            "deescalated": deescalated
        }
        
        self.interaction_history[address].append(interaction)
        
        # Update conflict tracking
        addr_data = self.addresses[address]
        
        # Check if this was a conflict situation
        intensity = float(emotional_context.get("intensity", 0))
        emotion = emotional_context.get("emotion", "").lower()
        
        is_conflict = self._is_conflict_situation(emotion, intensity)
        
        if is_conflict:
            addr_data["conflict_count"] += 1
            
            if deescalated:
                addr_data["deescalation_count"] += 1
            else:
                addr_data["escalation_count"] += 1
        
        # Recalculate CDR
        if addr_data["conflict_count"] > 0:
            addr_data["cdr"] = addr_data["deescalation_count"] / addr_data["conflict_count"]
        
        return {
            "address": address,
            "current_cdr": round(addr_data["cdr"], 3),
            "conflicts_total": addr_data["conflict_count"],
            "deescalations": addr_data["deescalation_count"],
            "escalations": addr_data["escalation_count"]
        }
    
    def _is_conflict_situation(self, emotion: str, intensity: float) -> bool:
        """Determine if an interaction represents a conflict situation."""
        conflict_emotions = {
            "anger", "frustration", "disagreement", "tension",
            "hostility", "aggression", "conflict"
        }
        
        return emotion in conflict_emotions and intensity >= 0.5
    
    def check_access(self, address: str) -> Dict[str, Any]:
        """
        Check if an address has sufficient access rights.
        
        Args:
            address: Address to check
            
        Returns:
            Access check result
        """
        if address not in self.addresses:
            return {
                "access_granted": False,
                "reason": "not_registered",
                "action_required": "register_for_trial"
            }
        
        addr_data = self.addresses[address]
        current_status = addr_data["status"]
        current_cdr = addr_data["cdr"]
        
        # Check if trial period has expired
        if current_status == "trial":
            if datetime.utcnow() > addr_data["trial_ends"]:
                # Evaluate trial
                self._evaluate_trial(address)
                addr_data = self.addresses[address]  # Refresh after evaluation
                current_status = addr_data["status"]
                current_cdr = addr_data["cdr"]
        
        # Check CDR requirement for current status
        if current_status in ["provisional", "standard", "trusted"]:
            required_cdr = self.CDR_THRESHOLDS.get(current_status, self.min_cdr)
            
            if current_cdr < required_cdr:
                return {
                    "access_granted": False,
                    "reason": "insufficient_cdr",
                    "current_cdr": round(current_cdr, 3),
                    "required_cdr": required_cdr,
                    "status": current_status
                }
        
        return {
            "access_granted": True,
            "status": current_status,
            "current_cdr": round(current_cdr, 3),
            "conflicts_handled": addr_data["conflict_count"]
        }
    
    def _evaluate_trial(self, address: str) -> None:
        """Evaluate trial period and promote or demote address."""
        addr_data = self.addresses[address]
        cdr = addr_data["cdr"]
        conflict_count = addr_data["conflict_count"]
        
        old_status = addr_data["status"]
        
        # Need minimum interactions to evaluate
        if conflict_count < 3:
            # Extend trial if insufficient data
            addr_data["trial_ends"] = datetime.utcnow() + timedelta(hours=12)
            return
        
        # Evaluate based on CDR
        if cdr >= self.CDR_THRESHOLDS["trusted"]:
            new_status = "trusted"
            self.metrics["trial_passes"] += 1
        elif cdr >= self.CDR_THRESHOLDS["standard"]:
            new_status = "standard"
            self.metrics["trial_passes"] += 1
        elif cdr >= self.CDR_THRESHOLDS["provisional"]:
            new_status = "provisional"
            self.metrics["trial_passes"] += 1
        else:
            # Failed trial
            new_status = "failed"
            self.metrics["trial_failures"] += 1
            addr_data["violations"].append({
                "timestamp": datetime.utcnow().isoformat(),
                "reason": "insufficient_cdr",
                "cdr": cdr,
                "required": self.min_cdr
            })
        
        # Update status
        addr_data["status"] = new_status
        addr_data["evaluated_at"] = datetime.utcnow().isoformat()
        
        # Update metrics
        self.metrics["by_status"][old_status] -= 1
        self.metrics["by_status"][new_status] += 1
        
        # Set next evaluation period if applicable
        if new_status == "provisional":
            addr_data["next_evaluation"] = datetime.utcnow() + self.TRIAL_PERIODS["provisional"]
        elif new_status == "standard":
            addr_data["next_evaluation"] = datetime.utcnow() + self.TRIAL_PERIODS["standard"]
    
    def get_address_status(self, address: str) -> Dict[str, Any]:
        """Get detailed status for an address."""
        if address not in self.addresses:
            return {
                "registered": False,
                "address": address
            }
        
        addr_data = self.addresses[address]
        
        return {
            "registered": True,
            "address": address,
            "status": addr_data["status"],
            "cdr": round(addr_data["cdr"], 3),
            "conflicts_total": addr_data["conflict_count"],
            "deescalations": addr_data["deescalation_count"],
            "escalations": addr_data["escalation_count"],
            "registered_at": addr_data["registered_at"].isoformat(),
            "trial_ends": addr_data.get("trial_ends", "").isoformat() if isinstance(addr_data.get("trial_ends"), datetime) else None,
            "violations_count": len(addr_data["violations"])
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get trial system metrics."""
        total_evaluated = self.metrics["trial_passes"] + self.metrics["trial_failures"]
        pass_rate = (
            self.metrics["trial_passes"] / total_evaluated * 100
            if total_evaluated > 0 else 0
        )
        
        return {
            "total_addresses": self.metrics["total_addresses"],
            "trial_passes": self.metrics["trial_passes"],
            "trial_failures": self.metrics["trial_failures"],
            "pass_rate_percentage": round(pass_rate, 2),
            "by_status": dict(self.metrics["by_status"]),
            "min_cdr_required": self.min_cdr
        }
    
    def reset_address(self, address: str) -> bool:
        """
        Reset an address to trial status (administrative action).
        
        Args:
            address: Address to reset
            
        Returns:
            True if reset successful
        """
        if address not in self.addresses:
            return False
        
        old_status = self.addresses[address]["status"]
        
        # Re-register with trial status
        self.addresses[address] = {
            "address": address,
            "status": "trial",
            "registered_at": datetime.utcnow(),
            "trial_ends": datetime.utcnow() + self.TRIAL_PERIODS["initial"],
            "conflict_count": 0,
            "deescalation_count": 0,
            "escalation_count": 0,
            "cdr": 0.0,
            "violations": self.addresses[address]["violations"],  # Keep violation history
            "reset_count": self.addresses[address].get("reset_count", 0) + 1
        }
        
        # Update metrics
        self.metrics["by_status"][old_status] -= 1
        self.metrics["by_status"]["trial"] += 1
        
        return True
