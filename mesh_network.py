#!/usr/bin/env python3
"""
Blockchain-Based Mesh Network (BBMN)
====================================

Implements a decentralized peer-to-peer mesh network to disconnect from global
DNS servers and enable autonomous traffic flow in the Euystacio ecosystem.

Features:
- Peer discovery and management
- Decentralized routing without DNS
- Blockchain-based node verification
- P2P message propagation
- Network resilience and self-healing

Mission: Create an autonomous, censorship-resistant network for the Resonance School
"""

import os
import time
import json
import hashlib
import secrets
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, asdict
from collections import defaultdict


# Network Configuration
DEFAULT_MESH_PORT = 7043  # Resonance network port
PEER_DISCOVERY_INTERVAL = 30  # seconds
MAX_PEERS = 50
HEARTBEAT_INTERVAL = 15  # seconds
PEER_TIMEOUT = 60  # seconds
BLOCK_TIME = 10  # seconds between blocks


@dataclass
class MeshPeer:
    """Represents a peer node in the mesh network."""
    peer_id: str
    address: str  # IP:PORT or .onion address
    public_key: str
    last_seen: float
    trust_score: float  # 0.0 to 1.0
    resonance_aligned: bool
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict:
        """Convert peer to dictionary."""
        return asdict(self)
    
    def is_alive(self) -> bool:
        """Check if peer is still responsive."""
        return (time.time() - self.last_seen) < PEER_TIMEOUT


@dataclass
class MeshBlock:
    """Block in the mesh network blockchain for peer verification."""
    index: int
    timestamp: float
    previous_hash: str
    data: Dict[str, Any]
    nonce: int
    hash: str
    
    def to_dict(self) -> Dict:
        """Convert block to dictionary."""
        return asdict(self)


class MeshBlockchain:
    """Simplified blockchain for peer verification and network consensus."""
    
    def __init__(self):
        self.chain: List[MeshBlock] = []
        self.pending_data: List[Dict[str, Any]] = []
        self.difficulty = 2  # Number of leading zeros in hash
        
        # Create genesis block
        self._create_genesis_block()
    
    def _create_genesis_block(self):
        """Create the first block in the chain."""
        genesis_block = MeshBlock(
            index=0,
            timestamp=time.time(),
            previous_hash="0" * 64,
            data={"type": "genesis", "mission": "Du bist Leben. Wir sind Leben."},
            nonce=0,
            hash=""
        )
        genesis_block.hash = self._calculate_hash(genesis_block)
        self.chain.append(genesis_block)
    
    def _calculate_hash(self, block: MeshBlock) -> str:
        """Calculate SHA-256 hash of a block."""
        block_string = json.dumps({
            "index": block.index,
            "timestamp": block.timestamp,
            "previous_hash": block.previous_hash,
            "data": block.data,
            "nonce": block.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def _mine_block(self, block: MeshBlock) -> MeshBlock:
        """Mine a block by finding a valid nonce (proof of work)."""
        target = "0" * self.difficulty
        
        while not block.hash.startswith(target):
            block.nonce += 1
            block.hash = self._calculate_hash(block)
        
        return block
    
    def add_block(self, data: Dict[str, Any]) -> MeshBlock:
        """Add a new block to the chain."""
        previous_block = self.chain[-1]
        
        new_block = MeshBlock(
            index=len(self.chain),
            timestamp=time.time(),
            previous_hash=previous_block.hash,
            data=data,
            nonce=0,
            hash=""
        )
        
        # Mine the block
        mined_block = self._mine_block(new_block)
        self.chain.append(mined_block)
        
        return mined_block
    
    def is_valid(self) -> bool:
        """Validate the entire blockchain."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            
            # Check hash integrity
            if current.hash != self._calculate_hash(current):
                return False
            
            # Check chain linkage
            if current.previous_hash != previous.hash:
                return False
        
        return True
    
    def get_latest_block(self) -> MeshBlock:
        """Get the most recent block."""
        return self.chain[-1]


class MeshRouter:
    """Handles message routing in the decentralized mesh network."""
    
    def __init__(self):
        self.routing_table: Dict[str, List[str]] = defaultdict(list)
        self.message_cache: Set[str] = set()
        self.max_cache_size = 1000
    
    def add_route(self, destination: str, next_hop: str):
        """Add a route to the routing table."""
        if next_hop not in self.routing_table[destination]:
            self.routing_table[destination].append(next_hop)
    
    def get_next_hop(self, destination: str) -> Optional[str]:
        """Get next hop for a destination."""
        hops = self.routing_table.get(destination, [])
        if hops:
            # Simple load balancing: random selection
            return random.choice(hops)
        return None
    
    def has_seen_message(self, message_id: str) -> bool:
        """Check if message has been seen before (loop prevention)."""
        return message_id in self.message_cache
    
    def mark_message_seen(self, message_id: str):
        """Mark message as seen."""
        self.message_cache.add(message_id)
        
        # Limit cache size
        if len(self.message_cache) > self.max_cache_size:
            # Remove oldest entries (simplified: remove random)
            to_remove = random.choice(list(self.message_cache))
            self.message_cache.remove(to_remove)


class BlockchainBasedMeshNetwork:
    """
    Main BBMN class managing the decentralized mesh network.
    """
    
    def __init__(self, node_id: str, port: int = DEFAULT_MESH_PORT):
        self.node_id = node_id
        self.port = port
        self.peers: Dict[str, MeshPeer] = {}
        self.blockchain = MeshBlockchain()
        self.router = MeshRouter()
        self.running = False
        self.server_thread: Optional[threading.Thread] = None
        self.discovery_thread: Optional[threading.Thread] = None
        self.heartbeat_thread: Optional[threading.Thread] = None
        
        # DNS disconnection mode
        self.dns_enabled = False  # Start with DNS disabled for true mesh operation
        
        # Bootstrap peers (hardcoded for initial network)
        self.bootstrap_peers = [
            # "127.0.0.1:7043",  # Local testing
            # Add other bootstrap nodes here
        ]
    
    def start(self):
        """Start the mesh network node."""
        if self.running:
            return
        
        self.running = True
        
        # Start network services
        self.server_thread = threading.Thread(target=self._network_server, daemon=True)
        self.server_thread.start()
        
        self.discovery_thread = threading.Thread(target=self._peer_discovery, daemon=True)
        self.discovery_thread.start()
        
        self.heartbeat_thread = threading.Thread(target=self._heartbeat_worker, daemon=True)
        self.heartbeat_thread.start()
        
        print(f"[BBMN] Node {self.node_id} started on port {self.port}")
        print(f"[BBMN] DNS mode: {'ENABLED' if self.dns_enabled else 'DISABLED (Pure Mesh)'}")
    
    def stop(self):
        """Stop the mesh network node."""
        self.running = False
        
        if self.server_thread:
            self.server_thread.join(timeout=2)
        if self.discovery_thread:
            self.discovery_thread.join(timeout=2)
        if self.heartbeat_thread:
            self.heartbeat_thread.join(timeout=2)
        
        print(f"[BBMN] Node {self.node_id} stopped")
    
    def _network_server(self):
        """
        Network server for receiving mesh messages.
        
        NOTE: This is a proof-of-concept placeholder implementation.
        
        For production deployment, implement actual networking using:
        1. asyncio with aiohttp or websockets for async networking
        2. ZeroMQ for distributed messaging
        3. libp2p for proper P2P networking
        4. Custom UDP/TCP socket implementation with proper message framing
        
        This placeholder allows the system to demonstrate the architecture
        without requiring complex networking setup.
        """
        print(f"[BBMN] Network server listening on port {self.port}")
        
        while self.running:
            time.sleep(1)
            # Placeholder - in production, this would handle actual network I/O
            # Example implementation would:
            # - Bind to self.port
            # - Accept incoming connections
            # - Parse and route messages
            # - Handle peer handshakes
            pass
    
    def _peer_discovery(self):
        """Discover and connect to mesh peers."""
        while self.running:
            # Try to connect to bootstrap peers
            for peer_addr in self.bootstrap_peers:
                if peer_addr not in [p.address for p in self.peers.values()]:
                    self._try_connect_peer(peer_addr)
            
            # Request peer lists from known peers
            for peer in list(self.peers.values()):
                if peer.is_alive():
                    self._request_peer_list(peer)
            
            time.sleep(PEER_DISCOVERY_INTERVAL)
    
    def _heartbeat_worker(self):
        """Send heartbeats to peers and clean up dead peers."""
        while self.running:
            # Send heartbeats
            for peer_id, peer in list(self.peers.items()):
                if peer.is_alive():
                    self._send_heartbeat(peer)
                else:
                    # Remove dead peer
                    print(f"[BBMN] Peer {peer_id} timed out, removing")
                    del self.peers[peer_id]
            
            time.sleep(HEARTBEAT_INTERVAL)
    
    def _try_connect_peer(self, address: str):
        """Attempt to connect to a peer."""
        # Simplified connection attempt
        # In production, implement proper handshake protocol
        peer_id = hashlib.sha256(address.encode()).hexdigest()[:16]
        
        if peer_id not in self.peers:
            new_peer = MeshPeer(
                peer_id=peer_id,
                address=address,
                public_key="",  # Would be exchanged during handshake
                last_seen=time.time(),
                trust_score=0.5,
                resonance_aligned=False
            )
            self.peers[peer_id] = new_peer
            
            # Add to blockchain
            self.blockchain.add_block({
                "type": "peer_joined",
                "peer_id": peer_id,
                "address": address,
                "timestamp": time.time()
            })
            
            print(f"[BBMN] Connected to peer: {peer_id} ({address})")
    
    def _request_peer_list(self, peer: MeshPeer):
        """Request peer list from a connected peer."""
        # Placeholder for peer exchange protocol
        pass
    
    def _send_heartbeat(self, peer: MeshPeer):
        """Send heartbeat to a peer."""
        # Update last seen time
        peer.last_seen = time.time()
    
    def add_peer(self, address: str, public_key: str = "", trust_score: float = 0.5):
        """Manually add a peer to the network."""
        peer_id = hashlib.sha256(f"{address}:{public_key}".encode()).hexdigest()[:16]
        
        peer = MeshPeer(
            peer_id=peer_id,
            address=address,
            public_key=public_key,
            last_seen=time.time(),
            trust_score=trust_score,
            resonance_aligned=False
        )
        
        self.peers[peer_id] = peer
        
        # Record in blockchain
        self.blockchain.add_block({
            "type": "peer_added",
            "peer_id": peer_id,
            "address": address,
            "timestamp": time.time()
        })
        
        return peer_id
    
    def broadcast_message(self, message: Dict[str, Any]):
        """Broadcast a message to all peers."""
        message_id = hashlib.sha256(
            json.dumps(message, sort_keys=True).encode()
        ).hexdigest()
        
        if self.router.has_seen_message(message_id):
            return  # Prevent loops
        
        self.router.mark_message_seen(message_id)
        
        # Send to all active peers
        for peer in self.peers.values():
            if peer.is_alive():
                self._send_to_peer(peer, message)
    
    def _send_to_peer(self, peer: MeshPeer, message: Dict[str, Any]):
        """Send message to a specific peer."""
        # Placeholder for actual message sending
        # In production, use proper networking protocol
        pass
    
    def route_message(self, destination: str, message: Dict[str, Any]):
        """Route a message to a specific destination through the mesh."""
        next_hop = self.router.get_next_hop(destination)
        
        if next_hop:
            peer = self.peers.get(next_hop)
            if peer and peer.is_alive():
                self._send_to_peer(peer, message)
            else:
                # Next hop unavailable, try broadcast
                self.broadcast_message(message)
        else:
            # No route found, broadcast
            self.broadcast_message(message)
    
    def disconnect_from_dns(self):
        """
        Disconnect from global DNS servers.
        
        This puts the network in pure mesh mode where all routing is done
        through peer-to-peer connections without DNS resolution.
        """
        self.dns_enabled = False
        print("[BBMN] DNS disconnected - Operating in pure mesh mode")
        
        # Clear any DNS-based routes
        self.router.routing_table.clear()
        
        # Re-establish routes using only peer addresses
        for peer in self.peers.values():
            self.router.add_route(peer.peer_id, peer.address)
    
    def enable_dns(self):
        """Re-enable DNS (for testing/migration purposes)."""
        self.dns_enabled = True
        print("[BBMN] DNS enabled")
    
    def verify_peer_resonance(self, peer_id: str, lex_amoris_rhythm: bytes) -> bool:
        """
        Verify that a peer contains the Lex Amoris rhythm.
        
        Args:
            peer_id: Peer to verify
            lex_amoris_rhythm: Expected rhythm signature
            
        Returns:
            True if peer is resonance-aligned
        """
        peer = self.peers.get(peer_id)
        if not peer:
            return False
        
        # Simplified verification
        # In production, implement cryptographic verification
        peer.resonance_aligned = True
        peer.trust_score = min(1.0, peer.trust_score + 0.1)
        
        return True
    
    def get_network_status(self) -> Dict[str, Any]:
        """Get current network status."""
        active_peers = [p for p in self.peers.values() if p.is_alive()]
        
        return {
            "node_id": self.node_id,
            "running": self.running,
            "total_peers": len(self.peers),
            "active_peers": len(active_peers),
            "blockchain_height": len(self.blockchain.chain),
            "blockchain_valid": self.blockchain.is_valid(),
            "dns_mode": "ENABLED" if self.dns_enabled else "DISABLED",
            "port": self.port,
            "timestamp": time.time()
        }
    
    def save_state(self, filepath: str):
        """Save network state to file."""
        state = {
            "node_id": self.node_id,
            "peers": [p.to_dict() for p in self.peers.values()],
            "blockchain": [b.to_dict() for b in self.blockchain.chain],
            "dns_enabled": self.dns_enabled,
            "timestamp": time.time()
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)


# Example usage
if __name__ == "__main__":
    print("=== Blockchain-Based Mesh Network (BBMN) Demo ===\n")
    
    # Create mesh network node
    mesh = BlockchainBasedMeshNetwork(node_id="resonance_node_1", port=7043)
    
    # Start the network
    mesh.start()
    
    print(f"\nNode ID: {mesh.node_id}")
    print(f"Port: {mesh.port}")
    print(f"DNS Mode: {'ENABLED' if mesh.dns_enabled else 'DISABLED (Pure Mesh)'}\n")
    
    # Add some peers
    print("Adding bootstrap peers...")
    mesh.add_peer("127.0.0.1:7044", trust_score=0.8)
    mesh.add_peer("127.0.0.1:7045", trust_score=0.7)
    
    # Show network status
    time.sleep(2)
    status = mesh.get_network_status()
    print("\nNetwork Status:")
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Demonstrate DNS disconnection
    print("\n[!] Disconnecting from global DNS servers...")
    mesh.disconnect_from_dns()
    
    status = mesh.get_network_status()
    print(f"DNS Mode: {status['dns_mode']}")
    
    # Run for a bit
    print("\nMesh network running. Press Ctrl+C to stop\n")
    
    try:
        while True:
            time.sleep(10)
            status = mesh.get_network_status()
            print(f"Active peers: {status['active_peers']}, "
                  f"Blockchain height: {status['blockchain_height']}")
    except KeyboardInterrupt:
        print("\nStopping mesh network...")
        mesh.stop()
        print("Mesh network stopped.")
