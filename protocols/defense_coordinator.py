"""
Defense Coordinator
Orchestrates all immediate defense protocols during the Coronazione phase
"""

from typing import Dict, Any, Optional
from datetime import datetime

from .stabilita_io import EdgeCachingSystem, DynamicRateLimiter, AffectivePrioritizer
from .governance import TutorCouncil, AuditProtocol, ContentAlignmentRules
from .forensics import GatedSymbiosisTrial, AnomalyDetector, SourceNodeInspector


class DefenseCoordinator:
    """
    Central coordinator for all immediate defense protocols.
    Integrates Stabilità I/O, Governance, and Forensic protocols.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Defense Coordinator with all protocol systems.
        
        Args:
            config: Optional configuration overrides
        """
        config = config or {}
        
        # Initialize Protocollo di Stabilità I/O
        self.edge_caching = EdgeCachingSystem(
            cache_ttl_seconds=config.get("cache_ttl", 300)
        )
        self.rate_limiter = DynamicRateLimiter(
            window_seconds=config.get("rate_limit_window", 60)
        )
        self.prioritizer = AffectivePrioritizer(
            max_queue_size=config.get("max_queue_size", 1000)
        )
        
        # Initialize Emergency Governance Protocols
        self.tutor_council = TutorCouncil()
        self.audit_protocol = AuditProtocol(
            log_file=config.get("audit_log_file", "logs/audit.log")
        )
        self.content_alignment = ContentAlignmentRules(
            strict_mode=config.get("strict_mode", True)
        )
        
        # Initialize Anti-Abuse Forensic Protocols
        self.symbiosis_trial = GatedSymbiosisTrial(
            min_cdr_required=config.get("min_cdr", 0.6)
        )
        self.anomaly_detector = AnomalyDetector(
            consistency_threshold=config.get("consistency_threshold", 0.85),
            spam_threshold=config.get("spam_threshold", 10)
        )
        self.source_inspector = SourceNodeInspector()
        
        self.metrics = {
            "total_pulses_processed": 0,
            "pulses_blocked": 0,
            "pulses_allowed": 0
        }
    
    def process_pulse_submission(
        self,
        address: str,
        pulse_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process a pulse submission through all defense protocols.
        
        Args:
            address: Source address submitting pulse
            pulse_data: Pulse submission data
            
        Returns:
            Processing result with all protocol checks
        """
        self.metrics["total_pulses_processed"] += 1
        
        result = {
            "address": address,
            "timestamp": datetime.utcnow().isoformat(),
            "allowed": False,
            "checks": {}
        }
        
        # 1. Check if source node is quarantined or blocked
        if self.source_inspector.is_node_quarantined(address):
            result["blocked_reason"] = "address_quarantined"
            self.metrics["pulses_blocked"] += 1
            self.audit_protocol.log_event(
                self.audit_protocol.AuditEventType.PULSE_SUBMISSION,
                self.audit_protocol.AuditSeverity.WARNING,
                f"Pulse blocked from quarantined address: {address}",
                {"address": address, "reason": "quarantined"},
                actor=address
            )
            return result
        
        if self.source_inspector.is_node_blocked(address):
            result["blocked_reason"] = "address_blocked"
            self.metrics["pulses_blocked"] += 1
            self.audit_protocol.log_event(
                self.audit_protocol.AuditEventType.PULSE_SUBMISSION,
                self.audit_protocol.AuditSeverity.CRITICAL,
                f"Pulse blocked from blocked address: {address}",
                {"address": address, "reason": "blocked"},
                actor=address
            )
            return result
        
        # 2. Check rate limits (Dynamic Rate Limiting)
        rate_check = self.rate_limiter.check_rate_limit(address)
        result["checks"]["rate_limit"] = rate_check
        
        if not rate_check["allowed"]:
            result["blocked_reason"] = "rate_limit_exceeded"
            self.metrics["pulses_blocked"] += 1
            
            # Log violation
            self.audit_protocol.log_rate_limit_violation(
                address,
                rate_check["tier"],
                rate_check["violations"]
            )
            
            # Flag for inspection if severe violations
            if rate_check["violations"] >= 10:
                self.source_inspector.flag_for_inspection(
                    address,
                    "Severe rate limit violations",
                    {"violations": rate_check["violations"], "tier": rate_check["tier"]},
                    self.source_inspector.InspectionPriority.HIGH
                )
            
            return result
        
        # 3. Check Gated Symbiosis Trial (CDR requirements)
        access_check = self.symbiosis_trial.check_access(address)
        result["checks"]["symbiosis_trial"] = access_check
        
        if not access_check["access_granted"]:
            result["blocked_reason"] = f"symbiosis_trial_{access_check['reason']}"
            self.metrics["pulses_blocked"] += 1
            
            # Log CDR failure
            self.audit_protocol.log_event(
                self.audit_protocol.AuditEventType.CDR_FAILURE,
                self.audit_protocol.AuditSeverity.WARNING,
                f"CDR check failed for {address}: {access_check['reason']}",
                access_check,
                actor=address
            )
            
            return result
        
        # 4. Check Content Alignment (Law of Equals)
        alignment_check = self.content_alignment.check_alignment(pulse_data, address)
        result["checks"]["content_alignment"] = alignment_check
        
        if alignment_check["blocked"]:
            result["blocked_reason"] = "content_violation"
            self.metrics["pulses_blocked"] += 1
            
            # Log violation
            self.audit_protocol.log_content_violation(
                address,
                "law_of_equals_violation",
                {
                    "alignment_score": alignment_check["alignment_score"],
                    "violations": alignment_check["violations"]
                }
            )
            
            # Flag for inspection if critical
            if alignment_check["alignment_level"] == "critical":
                self.source_inspector.flag_for_inspection(
                    address,
                    "Critical content alignment violation",
                    {"alignment_check": alignment_check},
                    self.source_inspector.InspectionPriority.CRITICAL
                )
            
            return result
        
        # 5. Anomaly Detection
        anomaly_check = self.anomaly_detector.analyze_pulse(address, pulse_data)
        result["checks"]["anomaly_detection"] = anomaly_check
        
        if anomaly_check["anomaly_detected"]:
            # Log anomaly
            self.audit_protocol.log_anomaly_detection(
                address,
                "pattern_anomaly",
                anomaly_check["anomaly_score"],
                {"anomalies": anomaly_check["anomalies"]}
            )
            
            # Flag for inspection if severe
            if anomaly_check["anomaly_score"] >= 0.8:
                self.source_inspector.flag_for_inspection(
                    address,
                    "Severe anomaly detected",
                    {"anomaly_check": anomaly_check},
                    self.source_inspector.InspectionPriority.HIGH
                )
            
            # Quarantine if critical
            if anomaly_check["anomaly_score"] >= 0.9:
                self.source_inspector.quarantine_node(
                    address,
                    f"Critical anomaly score: {anomaly_check['anomaly_score']}",
                    "defense_coordinator"
                )
                result["blocked_reason"] = "critical_anomaly"
                self.metrics["pulses_blocked"] += 1
                return result
        
        # 6. Enqueue with Affective Prioritization
        enqueue_result = self.prioritizer.enqueue_pulse(pulse_data)
        result["checks"]["prioritization"] = enqueue_result
        
        if not enqueue_result["enqueued"]:
            result["blocked_reason"] = "queue_full"
            self.metrics["pulses_blocked"] += 1
            return result
        
        # 7. Process at edge or central (Edge Caching)
        processing_result = self.edge_caching.process_pulse_at_edge(pulse_data)
        result["checks"]["edge_processing"] = processing_result
        
        # All checks passed
        result["allowed"] = True
        self.metrics["pulses_allowed"] += 1
        
        # Log successful submission
        self.audit_protocol.log_pulse_submission(
            address,
            pulse_data,
            processing_result
        )
        
        # Record interaction for Symbiosis Trial
        # Determine if this was de-escalation (simplified heuristic)
        emotion = pulse_data.get("emotion", "").lower()
        deescalated = emotion in ["peace", "harmony", "understanding", "compassion"]
        
        self.symbiosis_trial.record_interaction(
            address,
            "pulse_submission",
            pulse_data,
            deescalated
        )
        
        return result
    
    def get_comprehensive_metrics(self) -> Dict[str, Any]:
        """Get metrics from all protocol systems."""
        return {
            "defense_coordinator": {
                "total_pulses": self.metrics["total_pulses_processed"],
                "allowed": self.metrics["pulses_allowed"],
                "blocked": self.metrics["pulses_blocked"],
                "block_rate": round(
                    self.metrics["pulses_blocked"] / self.metrics["total_pulses_processed"] * 100
                    if self.metrics["total_pulses_processed"] > 0 else 0,
                    2
                )
            },
            "stabilita_io": {
                "edge_caching": self.edge_caching.get_metrics(),
                "rate_limiting": self.rate_limiter.get_metrics(),
                "prioritization": self.prioritizer.get_metrics()
            },
            "governance": {
                "tutor_council": self.tutor_council.get_metrics(),
                "audit_protocol": self.audit_protocol.get_metrics(),
                "content_alignment": self.content_alignment.get_metrics()
            },
            "forensics": {
                "symbiosis_trial": self.symbiosis_trial.get_metrics(),
                "anomaly_detection": self.anomaly_detector.get_metrics(),
                "source_inspection": self.source_inspector.get_metrics()
            }
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status."""
        metrics = self.get_comprehensive_metrics()
        
        return {
            "status": "operational",
            "timestamp": datetime.utcnow().isoformat(),
            "defense_level": "coronazione_phase",
            "protocols_active": [
                "edge_caching",
                "dynamic_rate_limiting",
                "affective_prioritization",
                "tutor_council",
                "audit_protocol",
                "content_alignment",
                "gated_symbiosis_trial",
                "anomaly_detection",
                "source_inspection"
            ],
            "metrics_summary": {
                "pulses_processed": metrics["defense_coordinator"]["total_pulses"],
                "block_rate": metrics["defense_coordinator"]["block_rate"],
                "quarantined_nodes": metrics["forensics"]["source_inspection"]["currently_quarantined"],
                "blocked_nodes": metrics["forensics"]["source_inspection"]["currently_blocked"],
                "pending_inspections": metrics["forensics"]["source_inspection"]["pending_inspections"]
            }
        }
