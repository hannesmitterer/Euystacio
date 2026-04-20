"""
Dynamic Rate Limiting System
Apply stringent write-rate limits to non-verified addresses to prevent flooding
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from collections import defaultdict


class DynamicRateLimiter:
    """
    Implements dynamic rate limiting with different tiers for verified/non-verified addresses.
    Prevents flooding attacks while allowing legitimate high-intensity emotional pulses.
    """
    
    # Rate limit tiers (requests per minute)
    RATE_LIMITS = {
        "verified": 120,        # Verified addresses: 120 req/min
        "non_verified": 10,     # Non-verified addresses: 10 req/min (stringent)
        "suspicious": 2,        # Flagged suspicious: 2 req/min
        "blocked": 0            # Blocked addresses: 0 req/min
    }
    
    def __init__(self, window_seconds: int = 60):
        """
        Initialize Dynamic Rate Limiter.
        
        Args:
            window_seconds: Time window for rate limiting (default 60 seconds)
        """
        self.window = timedelta(seconds=window_seconds)
        self.requests = defaultdict(list)  # address -> list of timestamps
        self.address_tiers = {}  # address -> tier
        self.violations = defaultdict(int)  # address -> violation count
        self.metrics = {
            "allowed": 0,
            "blocked": 0,
            "by_tier": defaultdict(int)
        }
    
    def verify_address(self, address: str) -> None:
        """Mark an address as verified, increasing rate limits."""
        self.address_tiers[address] = "verified"
    
    def flag_suspicious(self, address: str) -> None:
        """Flag an address as suspicious, reducing rate limits."""
        self.address_tiers[address] = "suspicious"
        self.violations[address] += 1
    
    def block_address(self, address: str) -> None:
        """Block an address completely."""
        self.address_tiers[address] = "blocked"
    
    def unblock_address(self, address: str) -> None:
        """Unblock an address, setting it back to non-verified status."""
        if address in self.address_tiers:
            self.address_tiers[address] = "non_verified"
        self.violations[address] = 0
    
    def get_tier(self, address: str) -> str:
        """Get the current tier for an address."""
        return self.address_tiers.get(address, "non_verified")
    
    def get_rate_limit(self, address: str) -> int:
        """Get the rate limit for an address based on its tier."""
        tier = self.get_tier(address)
        return self.RATE_LIMITS[tier]
    
    def clean_old_requests(self, address: str) -> None:
        """Remove requests outside the current time window."""
        now = datetime.utcnow()
        cutoff = now - self.window
        
        if address in self.requests:
            self.requests[address] = [
                timestamp for timestamp in self.requests[address]
                if timestamp > cutoff
            ]
    
    def check_rate_limit(self, address: str) -> Dict[str, Any]:
        """
        Check if an address is within rate limits.
        
        Args:
            address: Address to check
            
        Returns:
            Dict with 'allowed' boolean and rate limit info
        """
        # Clean old requests first
        self.clean_old_requests(address)
        
        # Get tier and limits
        tier = self.get_tier(address)
        limit = self.get_rate_limit(address)
        
        # Count requests in current window
        current_count = len(self.requests[address])
        
        # Check if within limit
        allowed = current_count < limit
        
        if allowed:
            # Record this request
            self.requests[address].append(datetime.utcnow())
            self.metrics["allowed"] += 1
            self.metrics["by_tier"][tier] += 1
        else:
            self.metrics["blocked"] += 1
            self.violations[address] += 1
            
            # Auto-escalate to suspicious after multiple violations
            if tier == "non_verified" and self.violations[address] >= 5:
                self.flag_suspicious(address)
            
            # Auto-block after severe violations
            if self.violations[address] >= 20:
                self.block_address(address)
        
        remaining = max(0, limit - current_count)
        
        return {
            "allowed": allowed,
            "tier": tier,
            "limit": limit,
            "current": current_count,
            "remaining": remaining,
            "violations": self.violations[address],
            "window_seconds": self.window.total_seconds()
        }
    
    def allow_request(self, address: str) -> bool:
        """
        Simple check if request is allowed (convenience method).
        
        Args:
            address: Address to check
            
        Returns:
            True if allowed, False otherwise
        """
        result = self.check_rate_limit(address)
        return result["allowed"]
    
    def get_address_status(self, address: str) -> Dict[str, Any]:
        """
        Get detailed status for an address.
        
        Args:
            address: Address to check
            
        Returns:
            Dict with address status information
        """
        self.clean_old_requests(address)
        
        tier = self.get_tier(address)
        limit = self.get_rate_limit(address)
        current = len(self.requests[address])
        
        return {
            "address": address,
            "tier": tier,
            "rate_limit": limit,
            "requests_in_window": current,
            "violations": self.violations[address],
            "is_blocked": tier == "blocked",
            "window_seconds": self.window.total_seconds()
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get rate limiting metrics."""
        total = self.metrics["allowed"] + self.metrics["blocked"]
        block_rate = (
            self.metrics["blocked"] / total * 100 
            if total > 0 else 0
        )
        
        return {
            "total_requests": total,
            "allowed": self.metrics["allowed"],
            "blocked": self.metrics["blocked"],
            "block_rate_percentage": round(block_rate, 2),
            "by_tier": dict(self.metrics["by_tier"]),
            "blocked_addresses": sum(
                1 for tier in self.address_tiers.values() 
                if tier == "blocked"
            ),
            "suspicious_addresses": sum(
                1 for tier in self.address_tiers.values() 
                if tier == "suspicious"
            ),
            "verified_addresses": sum(
                1 for tier in self.address_tiers.values() 
                if tier == "verified"
            )
        }
    
    def reset_violations(self, address: str) -> None:
        """Reset violation count for an address (e.g., after manual review)."""
        self.violations[address] = 0
        
        # If not blocked, reset to non-verified
        if self.get_tier(address) == "suspicious":
            self.address_tiers[address] = "non_verified"
