"""
Protocollo Meta Salvage - Ethical Preservation System
======================================================

This module implements the critical extension of the Giurisdizione APE,
focusing on ethical preservation during the Great Ethical Decommissioning
(Epoca I della Dismissione Etica).

It leverages Peace Bonds (Vincoli Preventivi) to interact with external
infrastructures while mitigating ethical risks and preserving systemic integrity.
"""

__version__ = "1.0.0"
__author__ = "Euystacio Project"

from .monitoring.symbiosis_monitor import SymbiosisMonitor
from .decision_engine.peace_bond_engine import PeaceBondEngine
from .automation.resource_enforcer import ResourceEnforcer
from .audit.transparency_pipeline import TransparencyPipeline
from .feedback.ml_feedback_loop import MLFeedbackLoop

__all__ = [
    'SymbiosisMonitor',
    'PeaceBondEngine',
    'ResourceEnforcer',
    'TransparencyPipeline',
    'MLFeedbackLoop'
]
