"""
Public Audit Protocol
Transparent logging and auditing system for all Council actions and system events
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from enum import Enum
import json


class AuditEventType(Enum):
    """Types of events that can be audited"""
    PULSE_SUBMISSION = "pulse_submission"
    RATE_LIMIT_VIOLATION = "rate_limit_violation"
    CONTENT_VIOLATION = "content_violation"
    COUNCIL_DECISION = "council_decision"
    EMERGENCY_ACTION = "emergency_action"
    SYSTEM_PARAMETER_CHANGE = "system_parameter_change"
    ADDRESS_BLOCKED = "address_blocked"
    ADDRESS_VERIFIED = "address_verified"
    ANOMALY_DETECTED = "anomaly_detected"
    CDR_FAILURE = "cdr_failure"


class AuditSeverity(Enum):
    """Severity levels for audit events"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class AuditProtocol:
    """
    Implements transparent audit logging for all system actions.
    Provides public accountability and compliance tracking.
    """
    
    def __init__(self, log_file: Optional[str] = None):
        """
        Initialize Audit Protocol.
        
        Args:
            log_file: Optional file path for persistent audit log
        """
        self.audit_log = []
        self.log_file = log_file
        self.metrics = {
            "total_events": 0,
            "by_type": {et.value: 0 for et in AuditEventType},
            "by_severity": {s.value: 0 for s in AuditSeverity},
            "violations": 0,
            "emergency_events": 0
        }
    
    def log_event(
        self,
        event_type: AuditEventType,
        severity: AuditSeverity,
        description: str,
        metadata: Dict[str, Any],
        actor: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Log an audit event.
        
        Args:
            event_type: Type of event being logged
            severity: Severity level
            description: Human-readable description
            metadata: Additional event data
            actor: Optional actor (user/tutor/address) responsible
            
        Returns:
            Logged event with ID
        """
        event = {
            "event_id": f"AUD-{len(self.audit_log) + 1:08d}",
            "timestamp": datetime.utcnow().isoformat(),
            "type": event_type.value,
            "severity": severity.value,
            "description": description,
            "metadata": metadata,
            "actor": actor
        }
        
        self.audit_log.append(event)
        
        # Update metrics
        self.metrics["total_events"] += 1
        self.metrics["by_type"][event_type.value] += 1
        self.metrics["by_severity"][severity.value] += 1
        
        if "violation" in event_type.value.lower():
            self.metrics["violations"] += 1
        
        if severity == AuditSeverity.EMERGENCY:
            self.metrics["emergency_events"] += 1
        
        # Write to file if configured
        if self.log_file:
            self._write_to_file(event)
        
        return event
    
    def _write_to_file(self, event: Dict[str, Any]) -> None:
        """Write audit event to persistent log file."""
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(event) + '\n')
        except Exception as e:
            # Silently fail to avoid disrupting main operations
            pass
    
    def log_pulse_submission(
        self,
        address: str,
        pulse_data: Dict[str, Any],
        processing_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Log a pulse submission event."""
        return self.log_event(
            AuditEventType.PULSE_SUBMISSION,
            AuditSeverity.INFO,
            f"Pulse submission from {address}",
            {
                "address": address,
                "emotion": pulse_data.get("emotion"),
                "intensity": pulse_data.get("intensity"),
                "priority": processing_result.get("priority_level"),
                "cached": processing_result.get("served_from") == "cache"
            },
            actor=address
        )
    
    def log_rate_limit_violation(
        self,
        address: str,
        tier: str,
        violation_count: int
    ) -> Dict[str, Any]:
        """Log a rate limit violation."""
        severity = (
            AuditSeverity.CRITICAL if violation_count >= 10 
            else AuditSeverity.WARNING
        )
        
        return self.log_event(
            AuditEventType.RATE_LIMIT_VIOLATION,
            severity,
            f"Rate limit violation by {address} (tier: {tier}, violations: {violation_count})",
            {
                "address": address,
                "tier": tier,
                "violation_count": violation_count
            },
            actor=address
        )
    
    def log_content_violation(
        self,
        address: str,
        violation_type: str,
        details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Log a content alignment violation."""
        return self.log_event(
            AuditEventType.CONTENT_VIOLATION,
            AuditSeverity.CRITICAL,
            f"Content violation detected: {violation_type}",
            {
                "address": address,
                "violation_type": violation_type,
                **details
            },
            actor=address
        )
    
    def log_council_decision(
        self,
        decision: Dict[str, Any],
        tutor_id: str
    ) -> Dict[str, Any]:
        """Log a Tutor-Council decision."""
        severity = (
            AuditSeverity.EMERGENCY if decision["type"] == "emergency_action"
            else AuditSeverity.WARNING
        )
        
        return self.log_event(
            AuditEventType.COUNCIL_DECISION,
            severity,
            f"Council decision: {decision['description']}",
            {
                "decision_id": decision["decision_id"],
                "type": decision["type"],
                "parameters": decision["parameters"]
            },
            actor=tutor_id
        )
    
    def log_emergency_action(
        self,
        action_type: str,
        description: str,
        parameters: Dict[str, Any],
        tutor_id: str
    ) -> Dict[str, Any]:
        """Log an emergency action."""
        return self.log_event(
            AuditEventType.EMERGENCY_ACTION,
            AuditSeverity.EMERGENCY,
            f"Emergency action: {description}",
            {
                "action_type": action_type,
                "parameters": parameters
            },
            actor=tutor_id
        )
    
    def log_anomaly_detection(
        self,
        address: str,
        anomaly_type: str,
        anomaly_score: float,
        details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Log detection of anomalous behavior."""
        severity = (
            AuditSeverity.EMERGENCY if anomaly_score >= 0.9
            else AuditSeverity.CRITICAL if anomaly_score >= 0.7
            else AuditSeverity.WARNING
        )
        
        return self.log_event(
            AuditEventType.ANOMALY_DETECTED,
            severity,
            f"Anomaly detected: {anomaly_type} (score: {anomaly_score:.2f})",
            {
                "address": address,
                "anomaly_type": anomaly_type,
                "anomaly_score": anomaly_score,
                **details
            },
            actor=address
        )
    
    def get_events_by_type(
        self,
        event_type: AuditEventType,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get audit events of a specific type."""
        events = [
            event for event in self.audit_log
            if event["type"] == event_type.value
        ]
        
        if limit:
            events = events[-limit:]
        
        return events
    
    def get_events_by_severity(
        self,
        severity: AuditSeverity,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get audit events of a specific severity."""
        events = [
            event for event in self.audit_log
            if event["severity"] == severity.value
        ]
        
        if limit:
            events = events[-limit:]
        
        return events
    
    def get_events_by_actor(
        self,
        actor: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get all audit events for a specific actor (address/tutor)."""
        events = [
            event for event in self.audit_log
            if event["actor"] == actor
        ]
        
        if limit:
            events = events[-limit:]
        
        return events
    
    def get_recent_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get most recent audit events."""
        return self.audit_log[-limit:]
    
    def get_violations_summary(self) -> Dict[str, Any]:
        """Get summary of all violations."""
        violations = [
            event for event in self.audit_log
            if "violation" in event["type"].lower()
        ]
        
        by_type = {}
        by_actor = {}
        
        for violation in violations:
            vtype = violation["type"]
            actor = violation["actor"]
            
            by_type[vtype] = by_type.get(vtype, 0) + 1
            by_actor[actor] = by_actor.get(actor, 0) + 1
        
        return {
            "total_violations": len(violations),
            "by_type": by_type,
            "top_violators": sorted(
                by_actor.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get audit protocol metrics."""
        return {
            **self.metrics,
            "log_size": len(self.audit_log),
            "violations_summary": self.get_violations_summary()
        }
    
    def export_audit_log(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Export audit log for a specific time period.
        
        Args:
            start_date: Start of time period (inclusive)
            end_date: End of time period (inclusive)
            
        Returns:
            Filtered audit events
        """
        events = self.audit_log
        
        if start_date:
            events = [
                e for e in events
                if datetime.fromisoformat(e["timestamp"]) >= start_date
            ]
        
        if end_date:
            events = [
                e for e in events
                if datetime.fromisoformat(e["timestamp"]) <= end_date
            ]
        
        return events
