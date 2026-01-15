#!/usr/bin/env python3
"""
Blockchain Fork Consensus Validator
Scenario B: Systemstörungen und Sabotage

Implements simultaneous consensus checking for blockchain forks to ensure
header continuity and prevent fork-based attacks.
"""

import hashlib
import time
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class BlockHeader:
    """Represents a blockchain block header."""
    height: int
    hash: str
    previous_hash: str
    timestamp: float
    merkle_root: str
    nonce: int
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'height': self.height,
            'hash': self.hash,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'merkle_root': self.merkle_root,
            'nonce': self.nonce
        }


@dataclass
class ForkDetection:
    """Represents a detected blockchain fork."""
    fork_height: int
    chain_a_hash: str
    chain_b_hash: str
    detection_time: float
    severity: str
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'fork_height': self.fork_height,
            'chain_a_hash': self.chain_a_hash,
            'chain_b_hash': self.chain_b_hash,
            'detection_time': self.detection_time,
            'severity': self.severity
        }


class BlockchainChain:
    """Represents a blockchain chain."""
    
    def __init__(self, chain_id: str):
        """
        Initialize blockchain chain.
        
        Args:
            chain_id: Unique identifier for this chain
        """
        self.chain_id = chain_id
        self.headers: List[BlockHeader] = []
        self.genesis_hash = self._create_genesis_block()
    
    def _create_genesis_block(self) -> str:
        """Create genesis block."""
        genesis = BlockHeader(
            height=0,
            hash=hashlib.sha256(f"genesis_{self.chain_id}".encode()).hexdigest(),
            previous_hash="0" * 64,
            timestamp=time.time(),
            merkle_root=hashlib.sha256(b"genesis_merkle").hexdigest(),
            nonce=0
        )
        self.headers.append(genesis)
        return genesis.hash
    
    def add_header(self, merkle_root: str, nonce: int) -> BlockHeader:
        """
        Add new block header to chain.
        
        Args:
            merkle_root: Merkle root of transactions
            nonce: Proof-of-work nonce
            
        Returns:
            New block header
        """
        if not self.headers:
            raise ValueError("Chain has no genesis block")
        
        previous = self.headers[-1]
        
        # Calculate block hash
        header_data = f"{previous.hash}{merkle_root}{nonce}".encode()
        block_hash = hashlib.sha256(header_data).hexdigest()
        
        header = BlockHeader(
            height=previous.height + 1,
            hash=block_hash,
            previous_hash=previous.hash,
            timestamp=time.time(),
            merkle_root=merkle_root,
            nonce=nonce
        )
        
        self.headers.append(header)
        return header
    
    def get_header(self, height: int) -> Optional[BlockHeader]:
        """Get header at specific height."""
        if 0 <= height < len(self.headers):
            return self.headers[height]
        return None
    
    def get_chain_head(self) -> BlockHeader:
        """Get latest block header."""
        return self.headers[-1]
    
    def get_chain_length(self) -> int:
        """Get chain length."""
        return len(self.headers)
    
    def validate_continuity(self, start_height: int = 0) -> bool:
        """
        Validate header continuity from start_height.
        
        Args:
            start_height: Height to start validation from
            
        Returns:
            True if chain is continuous
        """
        for i in range(start_height + 1, len(self.headers)):
            current = self.headers[i]
            previous = self.headers[i - 1]
            
            # Check height continuity
            if current.height != previous.height + 1:
                return False
            
            # Check hash linkage
            if current.previous_hash != previous.hash:
                return False
        
        return True


class ForkConsensusValidator:
    """
    Validates blockchain consensus across multiple chains to detect forks.
    
    Performs simultaneous checking of multiple chain versions to identify
    fork attacks and ensure header continuity.
    """
    
    def __init__(self):
        """Initialize fork consensus validator."""
        self.chains: Dict[str, BlockchainChain] = {}
        self.fork_detections: List[ForkDetection] = []
        self.canonical_chain_id: Optional[str] = None
    
    def register_chain(self, chain_id: str) -> BlockchainChain:
        """
        Register a blockchain chain for monitoring.
        
        Args:
            chain_id: Unique chain identifier
            
        Returns:
            Registered chain
        """
        if chain_id in self.chains:
            return self.chains[chain_id]
        
        chain = BlockchainChain(chain_id)
        self.chains[chain_id] = chain
        
        # First chain becomes canonical
        if self.canonical_chain_id is None:
            self.canonical_chain_id = chain_id
        
        return chain
    
    def detect_forks(self, height: Optional[int] = None) -> List[ForkDetection]:
        """
        Detect forks at specified height or across all heights.
        
        Args:
            height: Optional specific height to check
            
        Returns:
            List of detected forks
        """
        if len(self.chains) < 2:
            return []
        
        forks = []
        chain_list = list(self.chains.values())
        
        # Determine heights to check
        if height is not None:
            heights_to_check = [height]
        else:
            max_height = min(chain.get_chain_length() - 1 for chain in chain_list)
            heights_to_check = range(1, max_height + 1)
        
        # Check each height
        for check_height in heights_to_check:
            headers_at_height = []
            
            for chain in chain_list:
                header = chain.get_header(check_height)
                if header:
                    headers_at_height.append((chain.chain_id, header))
            
            # Compare headers at this height
            if len(headers_at_height) >= 2:
                for i in range(len(headers_at_height)):
                    for j in range(i + 1, len(headers_at_height)):
                        chain_a_id, header_a = headers_at_height[i]
                        chain_b_id, header_b = headers_at_height[j]
                        
                        if header_a.hash != header_b.hash:
                            # Fork detected
                            fork = ForkDetection(
                                fork_height=check_height,
                                chain_a_hash=header_a.hash,
                                chain_b_hash=header_b.hash,
                                detection_time=time.time(),
                                severity=self._assess_fork_severity(check_height)
                            )
                            forks.append(fork)
        
        self.fork_detections.extend(forks)
        return forks
    
    def _assess_fork_severity(self, fork_height: int) -> str:
        """
        Assess fork severity based on depth.
        
        Args:
            fork_height: Height where fork occurred
            
        Returns:
            Severity level
        """
        if not self.canonical_chain_id:
            return 'unknown'
        
        canonical = self.chains[self.canonical_chain_id]
        chain_head_height = canonical.get_chain_head().height
        depth = chain_head_height - fork_height
        
        if depth < 6:
            return 'critical'  # Recent fork, high risk
        elif depth < 20:
            return 'high'
        elif depth < 100:
            return 'medium'
        else:
            return 'low'  # Deep fork, likely orphaned
    
    def validate_all_chains(self) -> Dict[str, bool]:
        """
        Validate continuity of all registered chains.
        
        Returns:
            Dictionary mapping chain_id to validation result
        """
        results = {}
        
        for chain_id, chain in self.chains.items():
            results[chain_id] = chain.validate_continuity()
        
        return results
    
    def select_canonical_chain(self) -> str:
        """
        Select canonical chain based on longest valid chain.
        
        Returns:
            Chain ID of canonical chain
        """
        if not self.chains:
            raise ValueError("No chains registered")
        
        # Validate all chains first
        validations = self.validate_all_chains()
        
        # Among valid chains, select longest
        longest_chain_id = None
        longest_length = 0
        
        for chain_id, is_valid in validations.items():
            if is_valid:
                chain = self.chains[chain_id]
                length = chain.get_chain_length()
                
                if length > longest_length:
                    longest_length = length
                    longest_chain_id = chain_id
        
        if longest_chain_id:
            self.canonical_chain_id = longest_chain_id
            return longest_chain_id
        
        raise ValueError("No valid chains found")
    
    def get_consensus_status(self) -> Dict:
        """
        Get comprehensive consensus status.
        
        Returns:
            Status dictionary
        """
        status = {
            'num_chains': len(self.chains),
            'canonical_chain': self.canonical_chain_id,
            'total_forks_detected': len(self.fork_detections),
            'chain_validations': self.validate_all_chains(),
            'chains': {}
        }
        
        for chain_id, chain in self.chains.items():
            head = chain.get_chain_head()
            status['chains'][chain_id] = {
                'length': chain.get_chain_length(),
                'head_height': head.height,
                'head_hash': head.hash[:16] + '...',
                'is_canonical': chain_id == self.canonical_chain_id
            }
        
        return status
    
    def get_fork_summary(self) -> Dict:
        """Get summary of detected forks."""
        severity_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        
        for fork in self.fork_detections:
            severity_counts[fork.severity] = severity_counts.get(fork.severity, 0) + 1
        
        return {
            'total_forks': len(self.fork_detections),
            'by_severity': severity_counts,
            'latest_fork': self.fork_detections[-1].to_dict() if self.fork_detections else None
        }


if __name__ == '__main__':
    print("=== Blockchain Fork Consensus Validator Demo ===")
    print()
    
    # Initialize validator
    validator = ForkConsensusValidator()
    
    # Register main chain
    main_chain = validator.register_chain("main")
    
    # Add some blocks to main chain
    for i in range(10):
        merkle = hashlib.sha256(f"tx_batch_{i}".encode()).hexdigest()
        main_chain.add_header(merkle, nonce=i * 1000)
    
    # Create a fork at height 5
    fork_chain = validator.register_chain("fork_a")
    
    # Copy first 5 blocks from main chain
    for i in range(5):
        merkle = hashlib.sha256(f"tx_batch_{i}".encode()).hexdigest()
        fork_chain.add_header(merkle, nonce=i * 1000)
    
    # Fork diverges here
    for i in range(5, 8):
        merkle = hashlib.sha256(f"different_tx_{i}".encode()).hexdigest()
        fork_chain.add_header(merkle, nonce=i * 2000)
    
    # Detect forks
    forks = validator.detect_forks()
    
    # Get status
    status = validator.get_consensus_status()
    fork_summary = validator.get_fork_summary()
    
    print(f"Chains Monitored: {status['num_chains']}")
    print(f"Canonical Chain: {status['canonical_chain']}")
    print(f"Forks Detected: {fork_summary['total_forks']}")
    print()
    
    print("Chain Status:")
    for chain_id, chain_info in status['chains'].items():
        valid = status['chain_validations'][chain_id]
        print(f"  {chain_id}: length={chain_info['length']}, "
              f"valid={valid}, canonical={chain_info['is_canonical']}")
    
    if forks:
        print(f"\nDetected {len(forks)} fork(s):")
        for fork in forks[:3]:  # Show first 3
            print(f"  - Height {fork.fork_height}: {fork.severity} severity")
    
    print()
    print("✓ Blockchain fork validation operational")
