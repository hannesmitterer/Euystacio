#!/usr/bin/env python3
"""
Electromagnetic Signature Hardening Module
Scenario A: Spionage und Datenextraktion

Implements adaptive frequency switching protocols and Faraday-based 
protection measures to prevent electromagnetic eavesdropping and 
side-channel attacks.
"""

import time
import random
import hashlib
from typing import List, Dict, Optional
from dataclasses import dataclass
import math


@dataclass
class FrequencyChannel:
    """Represents a communication frequency channel."""
    frequency_mhz: float
    bandwidth_khz: float
    power_dbm: float
    in_use: bool = False
    last_used: float = 0.0
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'frequency_mhz': self.frequency_mhz,
            'bandwidth_khz': self.bandwidth_khz,
            'power_dbm': self.power_dbm,
            'in_use': self.in_use,
            'last_used': self.last_used
        }


class AdaptiveFrequencyHopping:
    """
    Implements adaptive frequency hopping to prevent EM signature detection.
    
    Uses pseudo-random frequency switching to make electromagnetic 
    emissions difficult to track and intercept.
    """
    
    def __init__(self, base_frequency: float = 2400.0, 
                 num_channels: int = 79,
                 hop_interval: float = 0.625):
        """
        Initialize frequency hopping system.
        
        Args:
            base_frequency: Base frequency in MHz
            num_channels: Number of frequency channels
            hop_interval: Time between hops in milliseconds
        """
        self.base_frequency = base_frequency
        self.num_channels = num_channels
        self.hop_interval = hop_interval
        self.current_channel = 0
        self.hop_sequence = []
        self.channels = self._initialize_channels()
        self.hop_count = 0
        self.last_hop_time = time.time()
        
    def _initialize_channels(self) -> List[FrequencyChannel]:
        """Initialize frequency channels."""
        channels = []
        for i in range(self.num_channels):
            freq = self.base_frequency + (i * 1.0)  # 1 MHz spacing
            channels.append(FrequencyChannel(
                frequency_mhz=freq,
                bandwidth_khz=1000.0,
                power_dbm=-10.0
            ))
        return channels
    
    def generate_hop_sequence(self, seed: Optional[str] = None) -> List[int]:
        """
        Generate pseudo-random frequency hopping sequence.
        
        Args:
            seed: Optional seed for reproducibility
            
        Returns:
            List of channel indices
        """
        if seed:
            # Use cryptographic hash for sequence generation
            hash_val = int(hashlib.sha256(seed.encode()).hexdigest(), 16)
            random.seed(hash_val)
        
        # Generate pseudo-random sequence covering all channels
        sequence = list(range(self.num_channels))
        random.shuffle(sequence)
        
        self.hop_sequence = sequence
        return sequence
    
    def hop_to_next_channel(self) -> FrequencyChannel:
        """
        Hop to next channel in sequence.
        
        Returns:
            New frequency channel
        """
        current_time = time.time()
        
        # Check if it's time to hop
        if not self.hop_sequence:
            self.generate_hop_sequence()
        
        # Mark current channel as not in use
        if self.current_channel < len(self.channels):
            self.channels[self.current_channel].in_use = False
        
        # Get next channel from sequence
        sequence_idx = self.hop_count % len(self.hop_sequence)
        self.current_channel = self.hop_sequence[sequence_idx]
        
        # Mark new channel as in use
        channel = self.channels[self.current_channel]
        channel.in_use = True
        channel.last_used = current_time
        
        self.hop_count += 1
        self.last_hop_time = current_time
        
        return channel
    
    def get_current_channel(self) -> FrequencyChannel:
        """Get currently active channel."""
        return self.channels[self.current_channel]
    
    def should_hop(self) -> bool:
        """Check if it's time to hop to next frequency."""
        elapsed = (time.time() - self.last_hop_time) * 1000  # Convert to ms
        return elapsed >= self.hop_interval
    
    def get_statistics(self) -> Dict:
        """Get hopping statistics."""
        return {
            'total_hops': self.hop_count,
            'current_channel': self.current_channel,
            'current_frequency_mhz': self.channels[self.current_channel].frequency_mhz,
            'hop_interval_ms': self.hop_interval,
            'num_channels': self.num_channels,
            'uptime_seconds': time.time() - (self.last_hop_time - (self.hop_count * self.hop_interval / 1000))
        }


class FaradayProtection:
    """
    Faraday cage simulation and electromagnetic shielding.
    
    Monitors and validates electromagnetic isolation to prevent 
    side-channel attacks and eavesdropping.
    """
    
    SHIELDING_LEVELS = {
        'none': 0,
        'basic': 30,      # 30 dB attenuation
        'standard': 60,   # 60 dB attenuation
        'high': 90,       # 90 dB attenuation
        'military': 120   # 120 dB attenuation
    }
    
    def __init__(self, shielding_level: str = 'standard'):
        """
        Initialize Faraday protection.
        
        Args:
            shielding_level: Level of electromagnetic shielding
        """
        if shielding_level not in self.SHIELDING_LEVELS:
            raise ValueError(f"Invalid shielding level: {shielding_level}")
        
        self.shielding_level = shielding_level
        self.attenuation_db = self.SHIELDING_LEVELS[shielding_level]
        self.monitoring_active = False
        self.leak_detections = []
    
    def calculate_signal_attenuation(self, input_power_dbm: float) -> float:
        """
        Calculate attenuated signal power.
        
        Args:
            input_power_dbm: Input signal power in dBm
            
        Returns:
            Attenuated signal power in dBm
        """
        return input_power_dbm - self.attenuation_db
    
    def detect_em_leak(self, external_power_dbm: float,
                       threshold_dbm: float = -100.0) -> bool:
        """
        Detect potential electromagnetic leakage.
        
        Args:
            external_power_dbm: Detected external EM power
            threshold_dbm: Detection threshold
            
        Returns:
            True if leak detected
        """
        # Calculate expected external power based on shielding
        expected_max = -50.0 - self.attenuation_db  # Assume -50 dBm internal
        
        leak_detected = external_power_dbm > expected_max
        
        if leak_detected:
            self.leak_detections.append({
                'timestamp': time.time(),
                'power_dbm': external_power_dbm,
                'expected_max': expected_max,
                'excess_db': external_power_dbm - expected_max
            })
        
        return leak_detected
    
    def get_effectiveness(self) -> float:
        """
        Get shielding effectiveness as percentage.
        
        Returns:
            Effectiveness percentage (0-100)
        """
        # Convert dB attenuation to percentage
        # -3 dB = 50%, -10 dB = 90%, -20 dB = 99%, -30 dB = 99.9%
        linear_ratio = 10 ** (-self.attenuation_db / 10)
        effectiveness = (1 - linear_ratio) * 100
        return min(99.999, effectiveness)
    
    def get_status(self) -> Dict:
        """Get protection status."""
        return {
            'shielding_level': self.shielding_level,
            'attenuation_db': self.attenuation_db,
            'effectiveness_percent': self.get_effectiveness(),
            'leak_count': len(self.leak_detections),
            'monitoring_active': self.monitoring_active
        }


class EMHardeningCoordinator:
    """
    Coordinates electromagnetic hardening measures.
    
    Combines frequency hopping and Faraday protection for comprehensive
    electromagnetic signature hardening.
    """
    
    def __init__(self, shielding_level: str = 'standard'):
        """
        Initialize EM hardening coordinator.
        
        Args:
            shielding_level: Faraday shielding level
        """
        self.freq_hopping = AdaptiveFrequencyHopping()
        self.faraday = FaradayProtection(shielding_level)
        self.active = False
        self.start_time = None
    
    def start_protection(self, seed: Optional[str] = None):
        """
        Start electromagnetic protection.
        
        Args:
            seed: Optional seed for frequency hopping
        """
        self.freq_hopping.generate_hop_sequence(seed)
        self.faraday.monitoring_active = True
        self.active = True
        self.start_time = time.time()
    
    def stop_protection(self):
        """Stop electromagnetic protection."""
        self.faraday.monitoring_active = False
        self.active = False
    
    def update(self):
        """Update protection systems."""
        if not self.active:
            return
        
        # Check if frequency hop is needed
        if self.freq_hopping.should_hop():
            self.freq_hopping.hop_to_next_channel()
    
    def get_comprehensive_status(self) -> Dict:
        """Get comprehensive protection status."""
        status = {
            'active': self.active,
            'uptime_seconds': time.time() - self.start_time if self.start_time else 0,
            'frequency_hopping': self.freq_hopping.get_statistics(),
            'faraday_protection': self.faraday.get_status(),
            'security_score': self._calculate_security_score()
        }
        return status
    
    def _calculate_security_score(self) -> float:
        """
        Calculate overall EM security score (0-100).
        
        Returns:
            Security score
        """
        if not self.active:
            return 0.0
        
        # Factor in Faraday effectiveness
        faraday_score = self.faraday.get_effectiveness() * 0.6
        
        # Factor in frequency hopping activity
        hop_score = min(40.0, self.freq_hopping.hop_count / 10.0)
        
        total_score = faraday_score + hop_score
        return min(100.0, total_score)


if __name__ == '__main__':
    print("=== Electromagnetic Hardening Demo ===")
    print()
    
    # Initialize coordinator
    coordinator = EMHardeningCoordinator(shielding_level='high')
    
    print("Starting EM protection...")
    coordinator.start_protection(seed="euystacio-em-protection")
    
    # Simulate some operations
    for i in range(5):
        time.sleep(0.001)  # Simulate time passing
        coordinator.update()
    
    # Get status
    status = coordinator.get_comprehensive_status()
    print(f"Protection Active: {status['active']}")
    print(f"Security Score: {status['security_score']:.2f}/100")
    print(f"Faraday Effectiveness: {status['faraday_protection']['effectiveness_percent']:.3f}%")
    print(f"Total Frequency Hops: {status['frequency_hopping']['total_hops']}")
    print(f"Current Frequency: {status['frequency_hopping']['current_frequency_mhz']:.2f} MHz")
    print()
    
    print("✓ Electromagnetic hardening operational")
