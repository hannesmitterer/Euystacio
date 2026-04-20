"""
Protocollo di Stabilità I/O
Input/Output Stability Protocol

Manages traffic overload during the Coronazione phase through:
- Edge-Caching: Offload processing to edge computing
- Dynamic Rate Limiting: Stringent write-rate limits for non-verified addresses
- Affective Prioritization: Prioritize high Custos Sentimento intensity submissions
"""

from .edge_caching import EdgeCachingSystem
from .rate_limiter import DynamicRateLimiter
from .prioritizer import AffectivePrioritizer

__all__ = ["EdgeCachingSystem", "DynamicRateLimiter", "AffectivePrioritizer"]
