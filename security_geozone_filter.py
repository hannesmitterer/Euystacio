#!/usr/bin/env python3
"""
Geo-Zone Security Filter
Scenario C: Globale Angriffe und Koordination

Implements geo-zone based filtering to isolate suspicious activities
and prevent coordinated global attacks.
"""

import time
import hashlib
from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum


class ThreatLevel(Enum):
    """Threat level classification."""
    SAFE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class GeoLocation:
    """Represents a geographic location."""
    latitude: float
    longitude: float
    country_code: str
    region: str
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'country_code': self.country_code,
            'region': self.region
        }


@dataclass
class ConnectionAttempt:
    """Represents a connection attempt."""
    ip_address: str
    location: GeoLocation
    timestamp: float
    user_agent: str
    request_type: str
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'ip_address': self.ip_address,
            'location': self.location.to_dict(),
            'timestamp': self.timestamp,
            'user_agent': self.user_agent,
            'request_type': self.request_type
        }


@dataclass
class GeoZone:
    """Represents a geographic security zone."""
    zone_id: str
    name: str
    country_codes: Set[str]
    threat_level: ThreatLevel
    allowed: bool
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'zone_id': self.zone_id,
            'name': self.name,
            'country_codes': list(self.country_codes),
            'threat_level': self.threat_level.name,
            'allowed': self.allowed
        }


class GeoZoneFilter:
    """
    Geographic zone-based security filtering system.
    
    Monitors connection attempts from different geographic regions and
    isolates suspicious activities based on geo-location patterns.
    """
    
    def __init__(self):
        """Initialize geo-zone filter."""
        self.zones: Dict[str, GeoZone] = {}
        self.connection_attempts: List[ConnectionAttempt] = []
        self.blocked_attempts: List[ConnectionAttempt] = []
        self.ip_reputation: Dict[str, float] = {}  # IP -> reputation (0-1)
        self.country_activity: Dict[str, int] = {}
        self._initialize_default_zones()
    
    def _initialize_default_zones(self):
        """Initialize default security zones."""
        # Trusted zones
        self.add_zone(GeoZone(
            zone_id='zone_eu',
            name='European Union',
            country_codes={'DE', 'FR', 'IT', 'ES', 'NL', 'BE', 'AT', 'CH'},
            threat_level=ThreatLevel.SAFE,
            allowed=True
        ))
        
        self.add_zone(GeoZone(
            zone_id='zone_na',
            name='North America',
            country_codes={'US', 'CA'},
            threat_level=ThreatLevel.LOW,
            allowed=True
        ))
        
        # Monitored zones
        self.add_zone(GeoZone(
            zone_id='zone_asia',
            name='Asia Pacific',
            country_codes={'JP', 'KR', 'SG', 'AU', 'NZ'},
            threat_level=ThreatLevel.LOW,
            allowed=True
        ))
        
        # High-risk zones (example - configure based on actual threat intelligence)
        # NOTE: In production, replace 'XX' with actual high-risk country codes
        # based on your threat intelligence and security policy
        self.add_zone(GeoZone(
            zone_id='zone_high_risk',
            name='High Risk Regions',
            country_codes=set(),  # Empty by default - configure as needed
            threat_level=ThreatLevel.HIGH,
            allowed=False
        ))
    
    def add_zone(self, zone: GeoZone):
        """
        Add or update a security zone.
        
        Args:
            zone: GeoZone to add
        """
        self.zones[zone.zone_id] = zone
    
    def find_zone_for_location(self, location: GeoLocation) -> Optional[GeoZone]:
        """
        Find security zone for a location.
        
        Args:
            location: Geographic location
            
        Returns:
            Matching GeoZone or None
        """
        for zone in self.zones.values():
            if location.country_code in zone.country_codes:
                return zone
        return None
    
    def evaluate_connection(self, attempt: ConnectionAttempt) -> Tuple[bool, str]:
        """
        Evaluate whether to allow a connection attempt.
        
        Args:
            attempt: Connection attempt to evaluate
            
        Returns:
            Tuple of (allowed, reason)
        """
        # Find zone for this location
        zone = self.find_zone_for_location(attempt.location)
        
        # Unknown zone - apply default policy (blocked)
        if zone is None:
            self.blocked_attempts.append(attempt)
            return (False, 'unknown_zone')
        
        # Check zone policy
        if not zone.allowed:
            self.blocked_attempts.append(attempt)
            return (False, f'zone_blocked:{zone.zone_id}')
        
        # Check IP reputation
        reputation = self.ip_reputation.get(attempt.ip_address, 0.5)
        if reputation < 0.3:
            self.blocked_attempts.append(attempt)
            return (False, 'low_ip_reputation')
        
        # Check for rapid repeated attempts (rate limiting)
        recent_attempts = self._count_recent_attempts(
            attempt.ip_address,
            window_seconds=60
        )
        
        if recent_attempts > 100:  # More than 100 requests per minute
            self.blocked_attempts.append(attempt)
            # Reduce reputation
            self.ip_reputation[attempt.ip_address] = max(0.0, reputation - 0.1)
            return (False, 'rate_limit_exceeded')
        
        # Check for coordinated attack patterns
        if self._detect_coordinated_attack(attempt):
            self.blocked_attempts.append(attempt)
            return (False, 'coordinated_attack_pattern')
        
        # Connection allowed
        self.connection_attempts.append(attempt)
        self.country_activity[attempt.location.country_code] = \
            self.country_activity.get(attempt.location.country_code, 0) + 1
        
        # Slightly improve reputation for legitimate use
        self.ip_reputation[attempt.ip_address] = min(1.0, reputation + 0.01)
        
        return (True, 'allowed')
    
    def _count_recent_attempts(self, ip_address: str, 
                               window_seconds: float = 60) -> int:
        """
        Count recent connection attempts from an IP.
        
        Args:
            ip_address: IP address to check
            window_seconds: Time window in seconds
            
        Returns:
            Number of recent attempts
        """
        cutoff_time = time.time() - window_seconds
        count = 0
        
        for attempt in self.connection_attempts:
            if (attempt.ip_address == ip_address and 
                attempt.timestamp > cutoff_time):
                count += 1
        
        return count
    
    def _detect_coordinated_attack(self, attempt: ConnectionAttempt) -> bool:
        """
        Detect coordinated attack patterns.
        
        Args:
            attempt: Connection attempt
            
        Returns:
            True if coordinated attack detected
        """
        # Check for unusual burst of activity from same country
        recent_time = time.time() - 60  # Last minute
        country_attempts = [
            a for a in self.connection_attempts
            if (a.location.country_code == attempt.location.country_code and
                a.timestamp > recent_time)
        ]
        
        # If more than 50 attempts from same country in 1 minute
        if len(country_attempts) > 50:
            # Check if from different IPs (coordinated)
            unique_ips = set(a.ip_address for a in country_attempts)
            if len(unique_ips) > 10:  # 10+ different IPs
                return True
        
        return False
    
    def update_zone_threat_level(self, zone_id: str, 
                                 threat_level: ThreatLevel):
        """
        Update threat level for a zone.
        
        Args:
            zone_id: Zone identifier
            threat_level: New threat level
        """
        if zone_id in self.zones:
            zone = self.zones[zone_id]
            zone.threat_level = threat_level
            
            # Auto-block high and critical threat zones
            if threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]:
                zone.allowed = False
    
    def get_statistics(self) -> Dict:
        """Get filtering statistics."""
        total_attempts = len(self.connection_attempts) + len(self.blocked_attempts)
        
        return {
            'total_attempts': total_attempts,
            'allowed_connections': len(self.connection_attempts),
            'blocked_connections': len(self.blocked_attempts),
            'block_rate': len(self.blocked_attempts) / total_attempts if total_attempts > 0 else 0,
            'active_zones': len(self.zones),
            'country_activity': dict(sorted(
                self.country_activity.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]),  # Top 10 countries
            'unique_ips': len(self.ip_reputation)
        }
    
    def get_zone_status(self) -> List[Dict]:
        """Get status of all zones."""
        return [zone.to_dict() for zone in self.zones.values()]
    
    def generate_threat_report(self) -> Dict:
        """Generate comprehensive threat report."""
        # Analyze blocked attempts
        blocked_by_zone = {}
        blocked_by_reason = {}
        
        for attempt in self.blocked_attempts:
            zone = self.find_zone_for_location(attempt.location)
            zone_name = zone.name if zone else 'Unknown'
            blocked_by_zone[zone_name] = blocked_by_zone.get(zone_name, 0) + 1
        
        # Find high-activity IPs
        ip_activity = {}
        for attempt in self.connection_attempts + self.blocked_attempts:
            ip_activity[attempt.ip_address] = ip_activity.get(attempt.ip_address, 0) + 1
        
        top_ips = sorted(ip_activity.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            'timestamp': time.time(),
            'total_blocked': len(self.blocked_attempts),
            'blocked_by_zone': blocked_by_zone,
            'top_active_ips': [{'ip': ip, 'count': count} for ip, count in top_ips],
            'zones': self.get_zone_status()
        }


if __name__ == '__main__':
    print("=== Geo-Zone Security Filter Demo ===")
    print()
    
    # Initialize filter
    geo_filter = GeoZoneFilter()
    
    # Simulate connection attempts
    print("Simulating connection attempts...")
    
    # Legitimate attempts
    for i in range(30):
        attempt = ConnectionAttempt(
            ip_address=f"192.168.1.{i}",
            location=GeoLocation(
                latitude=48.8566,
                longitude=2.3522,
                country_code='FR',
                region='EU'
            ),
            timestamp=time.time(),
            user_agent='Mozilla/5.0',
            request_type='GET'
        )
        allowed, reason = geo_filter.evaluate_connection(attempt)
    
    # Suspicious attempts from unknown zone
    for i in range(10):
        attempt = ConnectionAttempt(
            ip_address=f"10.0.0.{i}",
            location=GeoLocation(
                latitude=0.0,
                longitude=0.0,
                country_code='ZZ',  # Unknown
                region='Unknown'
            ),
            timestamp=time.time(),
            user_agent='Scanner',
            request_type='POST'
        )
        allowed, reason = geo_filter.evaluate_connection(attempt)
    
    # Get statistics
    stats = geo_filter.get_statistics()
    report = geo_filter.generate_threat_report()
    
    print(f"Total Attempts: {stats['total_attempts']}")
    print(f"Allowed: {stats['allowed_connections']}")
    print(f"Blocked: {stats['blocked_connections']}")
    print(f"Block Rate: {stats['block_rate']:.1%}")
    print()
    
    print("Top Countries:")
    for country, count in list(stats['country_activity'].items())[:5]:
        print(f"  {country}: {count}")
    
    print()
    print(f"Active Zones: {stats['active_zones']}")
    print(f"Unique IPs: {stats['unique_ips']}")
    
    print()
    print("✓ Geo-zone filtering operational")
