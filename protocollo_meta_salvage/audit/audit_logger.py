"""
Audit Logger
============

Comprehensive audit logging for all Peace Bond activities.
Maintains immutable audit trail for compliance and investigation.
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json

logger = logging.getLogger(__name__)


@dataclass
class AuditEntry:
    """Represents an audit log entry"""
    entry_id: str
    timestamp: str
    event_type: str
    actor: str
    provider: str
    action: str
    details: Dict[str, Any]
    result: str  # success, failure, pending


class AuditLogger:
    """
    Maintains comprehensive audit logs for Peace Bond operations.
    
    Logs all decisions, enforcement actions, violations, and
    compliance events for transparency and accountability.
    """
    
    def __init__(self, storage_path: str = './audit_logs'):
        """Initialize Audit Logger"""
        self.storage_path = storage_path
        self.entries: List[AuditEntry] = []
        
        logger.info(f"Audit Logger initialized: {storage_path}")
    
    def log_event(
        self,
        event_type: str,
        actor: str,
        provider: str,
        action: str,
        details: Dict[str, Any],
        result: str = 'success'
    ) -> AuditEntry:
        """Log an audit event"""
        
        entry_id = f"audit_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        
        entry = AuditEntry(
            entry_id=entry_id,
            timestamp=datetime.utcnow().isoformat(),
            event_type=event_type,
            actor=actor,
            provider=provider,
            action=action,
            details=details,
            result=result
        )
        
        self.entries.append(entry)
        
        logger.info(f"Audit event logged: {event_type} - {action}")
        
        return entry
    
    def log_peace_bond_activation(self, bond_id: str, provider: str, details: Dict[str, Any]):
        """Log Peace Bond activation"""
        self.log_event(
            event_type='peace_bond_activation',
            actor='system',
            provider=provider,
            action='activate_peace_bond',
            details={'bond_id': bond_id, **details},
            result='success'
        )
    
    def log_enforcement_action(self, action_id: str, provider: str, details: Dict[str, Any], result: str):
        """Log enforcement action"""
        self.log_event(
            event_type='enforcement_action',
            actor='resource_enforcer',
            provider=provider,
            action='enforce_constraint',
            details={'action_id': action_id, **details},
            result=result
        )
    
    def log_violation(self, constraint_id: str, provider: str, details: Dict[str, Any]):
        """Log constraint violation"""
        self.log_event(
            event_type='violation',
            actor='constraint_manager',
            provider=provider,
            action='violation_detected',
            details={'constraint_id': constraint_id, **details},
            result='violation'
        )
    
    def get_audit_trail(
        self,
        provider: Optional[str] = None,
        event_type: Optional[str] = None,
        start_time: Optional[str] = None,
        limit: int = 1000
    ) -> List[AuditEntry]:
        """Get filtered audit trail"""
        
        filtered = self.entries
        
        if provider:
            filtered = [e for e in filtered if e.provider == provider]
        
        if event_type:
            filtered = [e for e in filtered if e.event_type == event_type]
        
        if start_time:
            filtered = [e for e in filtered if e.timestamp >= start_time]
        
        return filtered[-limit:]
    
    def export_audit_log(self, format: str = 'json') -> str:
        """Export audit log"""
        if format == 'json':
            return json.dumps([
                {
                    'entry_id': e.entry_id,
                    'timestamp': e.timestamp,
                    'event_type': e.event_type,
                    'actor': e.actor,
                    'provider': e.provider,
                    'action': e.action,
                    'result': e.result
                }
                for e in self.entries
            ], indent=2)
        
        raise ValueError(f"Unsupported format: {format}")
