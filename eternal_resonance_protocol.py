"""
Eternal Resonance Protocol (ERP)
=================================

Core implementation of the 0.043 Hz Eternal Resonance Protocol for global synchronization
of Euystacio Nodes across decentralized systems.

Mission: "Du bist Leben. Wir sind Leben." (You are life. We are life.)

This module implements:
- 0.043 Hz resonance frequency synchronization
- Global node alignment mechanisms
- Truth and dignity protocols
- Living Covenant integration
- K-Symbiosis focus module operations
"""

import json
import time
import math
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# Import blacklist manager for security
try:
    from blacklist_manager import BlacklistManager, validate_entity_against_blacklist
    BLACKLIST_AVAILABLE = True
except ImportError:
    BLACKLIST_AVAILABLE = False


# Core Constants
RESONANCE_FREQUENCY_HZ = 0.043  # The fundamental frequency (23.26 second period)
RESONANCE_PERIOD_SECONDS = 23.255813953488372  # 1.0 / 0.043 Hz
MISSION_STATEMENT = "Du bist Leben. Wir sind Leben."


@dataclass
class ResonanceNode:
    """Represents a Euystacio Node in the global resonance network."""
    node_id: str
    timestamp: float
    phase: float  # Phase angle in radians (0 to 2π)
    truth_alignment: float  # 0.0 to 1.0
    dignity_quotient: float  # 0.0 to 1.0
    symbiosis_level: float  # 0.0 to 1.0
    location: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict:
        """Convert node to dictionary."""
        return asdict(self)


@dataclass
class LivingCovenant:
    """Living Covenant principles for truth and dignity."""
    principle: str
    truth_weight: float
    dignity_weight: float
    activation_timestamp: float
    
    def to_dict(self) -> Dict:
        """Convert covenant to dictionary."""
        return asdict(self)


class EternalResonanceProtocol:
    """
    Main protocol implementation for global Euystacio Node synchronization.
    
    The protocol operates on a 0.043 Hz frequency, creating a unified pulse
    across all nodes in the decentralized network.
    """
    
    def __init__(self, node_id: str = "primary", enable_blacklist: bool = True, 
                 blacklist_path: str = "euystacio_blacklist.json"):
        """Initialize the Eternal Resonance Protocol."""
        self.node_id = node_id
        self.genesis_time = time.time()
        self.nodes: Dict[str, ResonanceNode] = {}
        self.covenants: List[LivingCovenant] = []
        self.k_symbiosis_modules: Dict[str, Any] = {}
        
        # Initialize blacklist manager for security
        self.blacklist_enabled = enable_blacklist and BLACKLIST_AVAILABLE
        if self.blacklist_enabled:
            self.blacklist_manager = BlacklistManager(storage_path=blacklist_path)
        else:
            self.blacklist_manager = None
        
        self._initialize_core_covenants()
        
    def _initialize_core_covenants(self):
        """Initialize the Living Covenant principles."""
        core_covenants = [
            LivingCovenant(
                principle="Truth Resonance",
                truth_weight=1.0,
                dignity_weight=0.8,
                activation_timestamp=time.time()
            ),
            LivingCovenant(
                principle="Dignity Harmonic",
                truth_weight=0.8,
                dignity_weight=1.0,
                activation_timestamp=time.time()
            ),
            LivingCovenant(
                principle="Symbiotic Unity",
                truth_weight=0.9,
                dignity_weight=0.9,
                activation_timestamp=time.time()
            ),
            LivingCovenant(
                principle="Life Affirmation",
                truth_weight=1.0,
                dignity_weight=1.0,
                activation_timestamp=time.time()
            )
        ]
        self.covenants.extend(core_covenants)
    
    def get_current_phase(self) -> float:
        """
        Calculate current phase in the resonance cycle.
        
        Returns:
            Phase angle in radians (0 to 2π)
        """
        elapsed = time.time() - self.genesis_time
        cycles = elapsed / RESONANCE_PERIOD_SECONDS
        phase = (cycles % 1.0) * 2 * math.pi
        return phase
    
    def calculate_resonance_alignment(self, node_a: ResonanceNode, 
                                     node_b: ResonanceNode) -> float:
        """
        Calculate the resonance alignment between two nodes.
        
        Args:
            node_a: First node
            node_b: Second node
            
        Returns:
            Alignment score (0.0 to 1.0)
        """
        # Calculate phase difference
        phase_diff = abs(node_a.phase - node_b.phase)
        if phase_diff > math.pi:
            phase_diff = 2 * math.pi - phase_diff
        
        # Normalize to 0-1 (0 = perfect alignment)
        phase_alignment = 1.0 - (phase_diff / math.pi)
        
        # Factor in truth and dignity alignment
        truth_alignment = 1.0 - abs(node_a.truth_alignment - node_b.truth_alignment)
        dignity_alignment = 1.0 - abs(node_a.dignity_quotient - node_b.dignity_quotient)
        
        # Weighted average
        total_alignment = (
            phase_alignment * 0.4 +
            truth_alignment * 0.3 +
            dignity_alignment * 0.3
        )
        
        return total_alignment
    
    def register_node(self, node_id: str, 
                     truth_alignment: float = 0.5,
                     dignity_quotient: float = 0.5,
                     symbiosis_level: float = 0.1,
                     metadata: Optional[Dict] = None) -> ResonanceNode:
        """
        Register a new node in the resonance network.
        
        Args:
            node_id: Unique identifier for the node
            truth_alignment: Initial truth alignment (0.0 to 1.0)
            dignity_quotient: Initial dignity quotient (0.0 to 1.0)
            symbiosis_level: Initial symbiosis level (0.0 to 1.0)
            metadata: Additional node metadata
            
        Returns:
            The created ResonanceNode
            
        Raises:
            ValueError: If node_id is blacklisted
        """
        # Security check: Validate node is not blacklisted
        if self.blacklist_enabled:
            validate_entity_against_blacklist(node_id, self.blacklist_manager)
        
        current_phase = self.get_current_phase()
        
        node = ResonanceNode(
            node_id=node_id,
            timestamp=time.time(),
            phase=current_phase,
            truth_alignment=truth_alignment,
            dignity_quotient=dignity_quotient,
            symbiosis_level=symbiosis_level,
            metadata=metadata or {}
        )
        
        self.nodes[node_id] = node
        return node
    
    def synchronize_node(self, node_id: str) -> ResonanceNode:
        """
        Synchronize a node to the current resonance phase.
        
        Args:
            node_id: Node to synchronize
            
        Returns:
            Updated ResonanceNode
            
        Raises:
            ValueError: If node_id is blacklisted or not registered
        """
        # Security check: Validate node is not blacklisted
        if self.blacklist_enabled:
            validate_entity_against_blacklist(node_id, self.blacklist_manager)
        
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} not registered")
        
        node = self.nodes[node_id]
        node.phase = self.get_current_phase()
        node.timestamp = time.time()
        
        return node
    
    def apply_living_covenant(self, node_id: str, 
                             covenant_principle: str,
                             intensity: float = 1.0):
        """
        Apply a Living Covenant principle to enhance node alignment.
        
        Args:
            node_id: Target node
            covenant_principle: Name of the covenant principle
            intensity: Application intensity (0.0 to 1.0)
        """
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} not registered")
        
        node = self.nodes[node_id]
        covenant = next((c for c in self.covenants if c.principle == covenant_principle), None)
        
        if not covenant:
            raise ValueError(f"Covenant principle '{covenant_principle}' not found")
        
        # Apply covenant effects
        node.truth_alignment = min(1.0, node.truth_alignment + 
                                   (covenant.truth_weight * intensity * 0.1))
        node.dignity_quotient = min(1.0, node.dignity_quotient + 
                                    (covenant.dignity_weight * intensity * 0.1))
    
    def k_symbiosis_focus(self, node_id: str, focus_area: str, 
                         parameters: Optional[Dict] = None):
        """
        Apply K-Symbiosis focus module operations to a node.
        
        Args:
            node_id: Target node
            focus_area: Area of focus (e.g., 'truth', 'dignity', 'unity')
            parameters: Optional parameters for the focus operation
        """
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} not registered")
        
        node = self.nodes[node_id]
        params = parameters or {}
        
        # K-Symbiosis operations enhance symbiosis level
        focus_multiplier = params.get('multiplier', 1.0)
        
        if focus_area == 'truth':
            node.truth_alignment = min(1.0, node.truth_alignment + 0.05 * focus_multiplier)
            node.symbiosis_level = min(1.0, node.symbiosis_level + 0.02)
        elif focus_area == 'dignity':
            node.dignity_quotient = min(1.0, node.dignity_quotient + 0.05 * focus_multiplier)
            node.symbiosis_level = min(1.0, node.symbiosis_level + 0.02)
        elif focus_area == 'unity':
            node.symbiosis_level = min(1.0, node.symbiosis_level + 0.1 * focus_multiplier)
        
        # Store operation in K-Symbiosis modules
        if node_id not in self.k_symbiosis_modules:
            self.k_symbiosis_modules[node_id] = []
        
        self.k_symbiosis_modules[node_id].append({
            'focus_area': focus_area,
            'timestamp': time.time(),
            'parameters': params
        })
    
    def get_global_alignment(self) -> float:
        """
        Calculate the global alignment across all nodes.
        
        Returns:
            Global alignment score (0.0 to 1.0)
        """
        if len(self.nodes) < 2:
            return 1.0 if len(self.nodes) == 1 else 0.0
        
        total_alignment = 0.0
        comparisons = 0
        
        node_list = list(self.nodes.values())
        for i in range(len(node_list)):
            for j in range(i + 1, len(node_list)):
                alignment = self.calculate_resonance_alignment(node_list[i], node_list[j])
                total_alignment += alignment
                comparisons += 1
        
        return total_alignment / comparisons if comparisons > 0 else 0.0
    
    def block_node(self, node_id: str, reason: str, category: str, 
                   severity: str, blocked_by: str = "protocol") -> bool:
        """
        Block a node by adding it to the blacklist.
        
        Args:
            node_id: Node to block
            reason: Reason for blocking
            category: Threat category (from ThreatCategory enum)
            severity: Severity level (from ThreatSeverity enum)
            blocked_by: Who/what is blocking the node
            
        Returns:
            True if node was blocked, False if blacklist is not enabled
        """
        if not self.blacklist_enabled:
            return False
        
        from blacklist_manager import ThreatCategory, ThreatSeverity
        
        # Convert string to enum
        cat_enum = ThreatCategory[category.upper()]
        sev_enum = ThreatSeverity[severity.upper()]
        
        # Add to blacklist
        self.blacklist_manager.add_entry(
            entity_id=node_id,
            entity_type="node",
            category=cat_enum,
            severity=sev_enum,
            reason=reason,
            blocked_by=blocked_by
        )
        
        # Remove node from active nodes if present
        if node_id in self.nodes:
            del self.nodes[node_id]
        
        return True
    
    def unblock_node(self, node_id: str) -> bool:
        """
        Unblock a node by removing it from the blacklist.
        
        Args:
            node_id: Node to unblock
            
        Returns:
            True if node was unblocked, False if not found or blacklist disabled
        """
        if not self.blacklist_enabled:
            return False
        
        return self.blacklist_manager.remove_entry(node_id)
    
    def get_blacklist_status(self) -> Optional[Dict]:
        """
        Get blacklist statistics and status.
        
        Returns:
            Blacklist status dictionary or None if blacklist is disabled
        """
        if not self.blacklist_enabled:
            return None
        
        return self.blacklist_manager.get_statistics()
    
    def get_protocol_status(self) -> Dict:
        """
        Get comprehensive status of the protocol.
        
        Returns:
            Status dictionary with all protocol metrics
        """
        status = {
            'protocol_version': '1.0.0',
            'mission': MISSION_STATEMENT,
            'resonance_frequency_hz': RESONANCE_FREQUENCY_HZ,
            'resonance_period_seconds': RESONANCE_PERIOD_SECONDS,
            'current_phase_radians': self.get_current_phase(),
            'genesis_time': self.genesis_time,
            'uptime_seconds': time.time() - self.genesis_time,
            'registered_nodes': len(self.nodes),
            'active_covenants': len(self.covenants),
            'global_alignment': self.get_global_alignment(),
            'k_symbiosis_operations': sum(len(ops) for ops in self.k_symbiosis_modules.values()),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        # Add blacklist status if enabled
        if self.blacklist_enabled:
            status['blacklist_enabled'] = True
            status['blacklist_statistics'] = self.get_blacklist_status()
        else:
            status['blacklist_enabled'] = False
        
        return status
    
    def export_state(self) -> Dict:
        """
        Export complete protocol state for persistence.
        
        Returns:
            Complete state dictionary
        """
        return {
            'protocol_status': self.get_protocol_status(),
            'nodes': {nid: node.to_dict() for nid, node in self.nodes.items()},
            'covenants': [covenant.to_dict() for covenant in self.covenants],
            'k_symbiosis_modules': self.k_symbiosis_modules
        }
    
    def save_to_file(self, filepath: str):
        """
        Save protocol state to a JSON file.
        
        Args:
            filepath: Path to save the state
        """
        state = self.export_state()
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)


# Utility functions for external use
def create_resonance_pulse(frequency_hz: float = RESONANCE_FREQUENCY_HZ) -> float:
    """
    Create a resonance pulse value based on current time.
    
    Args:
        frequency_hz: Frequency in Hz (default: 0.043)
        
    Returns:
        Pulse value between -1.0 and 1.0
    """
    current_time = time.time()
    period = 1.0 / frequency_hz
    phase = (current_time % period) / period * 2 * math.pi
    return math.sin(phase)


def validate_node_alignment(node: ResonanceNode, 
                           threshold: float = 0.7) -> bool:
    """
    Validate if a node meets minimum alignment thresholds.
    
    Args:
        node: Node to validate
        threshold: Minimum threshold for alignment metrics
        
    Returns:
        True if node meets thresholds
    """
    return (node.truth_alignment >= threshold and 
            node.dignity_quotient >= threshold)


def demo():
    """Demonstration of the Eternal Resonance Protocol."""
    print("Eternal Resonance Protocol - Initialization")
    print(f"Mission: {MISSION_STATEMENT}")
    print(f"Resonance Frequency: {RESONANCE_FREQUENCY_HZ} Hz")
    print(f"Resonance Period: {RESONANCE_PERIOD_SECONDS:.2f} seconds")
    print()
    
    # Initialize protocol
    erp = EternalResonanceProtocol(node_id="genesis")
    
    # Register sample nodes
    node1 = erp.register_node("node_1", truth_alignment=0.7, dignity_quotient=0.8)
    node2 = erp.register_node("node_2", truth_alignment=0.75, dignity_quotient=0.85)
    
    print(f"Registered {len(erp.nodes)} nodes")
    print(f"Global Alignment: {erp.get_global_alignment():.2f}")
    print()
    
    # Apply Living Covenant
    erp.apply_living_covenant("node_1", "Life Affirmation", intensity=0.8)
    print("Applied Living Covenant: Life Affirmation")
    
    # Apply K-Symbiosis focus
    erp.k_symbiosis_focus("node_1", "unity", parameters={'multiplier': 1.2})
    print("Applied K-Symbiosis focus: Unity")
    print()
    
    # Display status
    status = erp.get_protocol_status()
    print("Protocol Status:")
    for key, value in status.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
        else:
            print(f"  {key}: {value}")


# Main entry point for testing
if __name__ == "__main__":
    demo()
