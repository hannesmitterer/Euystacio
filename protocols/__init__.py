"""
Euystacio Framework (AIC) - Immediate Defense Protocols
Coronazione Phase Protection System

This package implements the three core defense protocols:
1. Protocollo di Stabilità I/O - Traffic and workload management
2. Emergency Governance Protocols - Tutor-Council and content alignment
3. Anti-Abuse Forensic Protocols - Pre-entry filtering and anomaly detection
"""

from .stabilita_io import (
    EdgeCachingSystem,
    DynamicRateLimiter,
    AffectivePrioritizer
)
from .governance import (
    TutorCouncil,
    AuditProtocol,
    ContentAlignmentRules
)
from .forensics import (
    GatedSymbiosisTrial,
    AnomalyDetector,
    SourceNodeInspector
)
from .defense_coordinator import DefenseCoordinator

__version__ = "1.0.0"
__all__ = [
    "DefenseCoordinator",
    "EdgeCachingSystem",
    "DynamicRateLimiter", 
    "AffectivePrioritizer",
    "TutorCouncil",
    "AuditProtocol",
    "ContentAlignmentRules",
    "GatedSymbiosisTrial",
    "AnomalyDetector",
    "SourceNodeInspector",
]
