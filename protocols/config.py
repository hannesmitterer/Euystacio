"""
Configuration for Immediate Defense Protocols
Coronazione Phase parameters and settings
"""

# Protocollo di Stabilità I/O Configuration
EDGE_CACHING_CONFIG = {
    "cache_ttl": 300,  # 5 minutes cache TTL
    "max_edge_nodes": 10,
    "edge_capacity": 100  # Requests per edge node
}

RATE_LIMITING_CONFIG = {
    "window_seconds": 60,
    "rate_limits": {
        "verified": 120,      # 120 requests per minute
        "non_verified": 10,   # 10 requests per minute (stringent)
        "suspicious": 2,      # 2 requests per minute
        "blocked": 0          # 0 requests (fully blocked)
    },
    "auto_escalate_threshold": 5,    # Violations before escalation
    "auto_block_threshold": 20       # Violations before blocking
}

PRIORITIZATION_CONFIG = {
    "max_queue_size": 1000,
    "priority_levels": {
        "critical": 1,   # Intensity >= 0.9
        "high": 2,       # Intensity >= 0.7
        "medium": 3,     # Intensity >= 0.4
        "low": 4,        # Intensity < 0.4
        "noise": 5       # Very low intensity
    }
}

# Emergency Governance Configuration
TUTOR_COUNCIL_CONFIG = {
    "tutor_quorum": 3,              # Minimum tutors for major decisions
    "decision_validity_hours": 24,  # Decision validity period
    "operational_boundaries": {
        "max_pulse_rate_per_address": 10,
        "min_custos_sentimento_intensity": 0.3,
        "max_queue_size": 1000,
        "content_review_threshold": 0.7,
        "emergency_lockdown_threshold": 0.9,
        "min_cdr_rate": 0.6
    }
}

AUDIT_PROTOCOL_CONFIG = {
    "log_file": "logs/audit.log",
    "retention_days": 90,
    "enable_file_logging": True
}

CONTENT_ALIGNMENT_CONFIG = {
    "strict_mode": True,  # Zero tolerance enforcement
    "alignment_thresholds": {
        "aligned": 0.8,
        "acceptable": 0.7,
        "questionable": 0.5,
        "violating": 0.3
    },
    "auto_block_on_critical": True
}

# Anti-Abuse Forensic Configuration
SYMBIOSIS_TRIAL_CONFIG = {
    "min_cdr_required": 0.6,  # 60% de-escalation rate
    "cdr_thresholds": {
        "trial": 0.0,
        "provisional": 0.5,
        "standard": 0.6,
        "trusted": 0.75
    },
    "trial_periods": {
        "initial_hours": 24,
        "provisional_days": 7,
        "standard_days": 30
    },
    "min_conflicts_for_evaluation": 3
}

ANOMALY_DETECTION_CONFIG = {
    "consistency_threshold": 0.85,  # Detect artificial consistency
    "spam_threshold": 10,           # Pulses in window to consider spam
    "time_window_minutes": 60,
    "auto_flag_score": 0.8,
    "auto_quarantine_score": 0.9
}

SOURCE_INSPECTION_CONFIG = {
    "auto_quarantine_on_critical": True,
    "inspection_priority_levels": ["low", "medium", "high", "critical"]
}

# Comprehensive Defense Configuration
DEFAULT_DEFENSE_CONFIG = {
    "cache_ttl": EDGE_CACHING_CONFIG["cache_ttl"],
    "rate_limit_window": RATE_LIMITING_CONFIG["window_seconds"],
    "max_queue_size": PRIORITIZATION_CONFIG["max_queue_size"],
    "audit_log_file": AUDIT_PROTOCOL_CONFIG["log_file"],
    "strict_mode": CONTENT_ALIGNMENT_CONFIG["strict_mode"],
    "min_cdr": SYMBIOSIS_TRIAL_CONFIG["min_cdr_required"],
    "consistency_threshold": ANOMALY_DETECTION_CONFIG["consistency_threshold"],
    "spam_threshold": ANOMALY_DETECTION_CONFIG["spam_threshold"]
}

# Operational Parameters
CORONAZIONE_PHASE_PARAMS = {
    "phase_name": "Coronazione",
    "defense_level": "immediate",
    "law_of_equals_enforcement": "zero_tolerance",
    "description": "Initial operational phase with heightened security measures",
    "objectives": [
        "Prevent traffic overload",
        "Establish governance authority",
        "Mitigate manipulation risks",
        "Ensure Law of Equals compliance"
    ]
}
