#!/usr/bin/env python3
"""
Mesh Network Architecture
Scenario C: Globale Angriffe und Koordination

Implements decentralized mesh-based network architecture for resilience
against coordinated global attacks.
"""

import time
import hashlib
import random
from typing import List, Dict, Optional, Set, Tuple
from dataclasses import dataclass
from enum import Enum


class NodeStatus(Enum):
    """Network node status."""
    ACTIVE = 1
    DEGRADED = 2
    OFFLINE = 3
    SUSPECT = 4


@dataclass
class MeshNode:
    """Represents a node in the mesh network."""
    node_id: str
    address: str
    public_key: str
    status: NodeStatus
    last_seen: float
    peer_connections: Set[str]
    reputation: float  # 0.0 to 1.0
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'node_id': self.node_id,
            'address': self.address,
            'status': self.status.name,
            'last_seen': self.last_seen,
            'peer_count': len(self.peer_connections),
            'reputation': self.reputation
        }


@dataclass
class NetworkRoute:
    """Represents a route through the mesh network."""
    source_id: str
    destination_id: str
    hops: List[str]
    latency_ms: float
    reliability: float
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'source': self.source_id,
            'destination': self.destination_id,
            'hop_count': len(self.hops),
            'hops': self.hops,
            'latency_ms': self.latency_ms,
            'reliability': self.reliability
        }


class MeshNetworkTopology:
    """
    Manages mesh network topology and routing.
    
    Provides decentralized network architecture with automatic failover
    and attack resilience.
    """
    
    def __init__(self, local_node_id: str):
        """
        Initialize mesh network topology.
        
        Args:
            local_node_id: ID of the local node
        """
        self.local_node_id = local_node_id
        self.nodes: Dict[str, MeshNode] = {}
        self.routes: Dict[Tuple[str, str], List[NetworkRoute]] = {}
        self.message_log: List[Dict] = []
        self._initialize_local_node()
    
    def _initialize_local_node(self):
        """Initialize the local node."""
        # Generate public key for local node
        public_key = hashlib.sha256(
            f"{self.local_node_id}_public".encode()
        ).hexdigest()
        
        local_node = MeshNode(
            node_id=self.local_node_id,
            address=f"mesh://{self.local_node_id}",
            public_key=public_key,
            status=NodeStatus.ACTIVE,
            last_seen=time.time(),
            peer_connections=set(),
            reputation=1.0
        )
        
        self.nodes[self.local_node_id] = local_node
    
    def add_peer(self, node_id: str, address: str, 
                 public_key: str) -> MeshNode:
        """
        Add a peer node to the mesh network.
        
        Args:
            node_id: Peer node ID
            address: Peer address
            public_key: Peer public key
            
        Returns:
            Created peer node
        """
        if node_id in self.nodes:
            return self.nodes[node_id]
        
        peer = MeshNode(
            node_id=node_id,
            address=address,
            public_key=public_key,
            status=NodeStatus.ACTIVE,
            last_seen=time.time(),
            peer_connections=set(),
            reputation=0.5  # Start with neutral reputation
        )
        
        self.nodes[node_id] = peer
        
        # Establish bidirectional connection
        self.connect_peers(self.local_node_id, node_id)
        
        return peer
    
    def connect_peers(self, node_a_id: str, node_b_id: str):
        """
        Establish connection between two peers.
        
        Args:
            node_a_id: First node ID
            node_b_id: Second node ID
        """
        if node_a_id in self.nodes and node_b_id in self.nodes:
            self.nodes[node_a_id].peer_connections.add(node_b_id)
            self.nodes[node_b_id].peer_connections.add(node_a_id)
    
    def disconnect_peer(self, node_id: str):
        """
        Disconnect a peer from the network.
        
        Args:
            node_id: Node ID to disconnect
        """
        if node_id not in self.nodes:
            return
        
        node = self.nodes[node_id]
        
        # Remove all connections to this node
        for peer_id in node.peer_connections:
            if peer_id in self.nodes:
                self.nodes[peer_id].peer_connections.discard(node_id)
        
        node.peer_connections.clear()
        node.status = NodeStatus.OFFLINE
    
    def find_routes(self, destination_id: str, 
                   max_hops: int = 5) -> List[NetworkRoute]:
        """
        Find routes to a destination node.
        
        Args:
            destination_id: Destination node ID
            max_hops: Maximum number of hops
            
        Returns:
            List of possible routes
        """
        if destination_id not in self.nodes:
            return []
        
        routes = []
        
        # BFS to find all paths
        def find_paths(current: str, target: str, visited: Set[str], 
                      path: List[str]) -> List[List[str]]:
            if len(path) > max_hops:
                return []
            
            if current == target:
                return [path]
            
            paths = []
            current_node = self.nodes.get(current)
            
            if not current_node or current_node.status == NodeStatus.OFFLINE:
                return []
            
            for peer_id in current_node.peer_connections:
                if peer_id not in visited:
                    new_visited = visited.copy()
                    new_visited.add(peer_id)
                    new_path = path + [peer_id]
                    
                    peer_paths = find_paths(peer_id, target, new_visited, new_path)
                    paths.extend(peer_paths)
            
            return paths
        
        # Find all paths
        all_paths = find_paths(
            self.local_node_id,
            destination_id,
            {self.local_node_id},
            [self.local_node_id]
        )
        
        # Convert paths to routes with metrics
        for path in all_paths:
            latency = self._estimate_latency(path)
            reliability = self._calculate_reliability(path)
            
            route = NetworkRoute(
                source_id=self.local_node_id,
                destination_id=destination_id,
                hops=path,
                latency_ms=latency,
                reliability=reliability
            )
            routes.append(route)
        
        # Sort by reliability and latency
        routes.sort(key=lambda r: (r.reliability, -r.latency_ms), reverse=True)
        
        # Cache routes
        self.routes[(self.local_node_id, destination_id)] = routes
        
        return routes
    
    def _estimate_latency(self, path: List[str]) -> float:
        """
        Estimate latency for a path.
        
        Args:
            path: List of node IDs in path
            
        Returns:
            Estimated latency in ms
        """
        # Simple estimate: 10ms base + 5ms per hop
        base_latency = 10.0
        hop_latency = 5.0 * (len(path) - 1)
        
        # Add variance based on node status
        variance = 0.0
        for node_id in path:
            if node_id in self.nodes:
                node = self.nodes[node_id]
                if node.status == NodeStatus.DEGRADED:
                    variance += 20.0
        
        return base_latency + hop_latency + variance
    
    def _calculate_reliability(self, path: List[str]) -> float:
        """
        Calculate reliability of a path.
        
        Args:
            path: List of node IDs in path
            
        Returns:
            Reliability score (0-1)
        """
        if not path:
            return 0.0
        
        # Reliability is product of node reputations
        reliability = 1.0
        
        for node_id in path:
            if node_id in self.nodes:
                node = self.nodes[node_id]
                
                # Factor in status
                if node.status == NodeStatus.OFFLINE:
                    return 0.0
                elif node.status == NodeStatus.SUSPECT:
                    reliability *= 0.3
                elif node.status == NodeStatus.DEGRADED:
                    reliability *= 0.7
                
                # Factor in reputation
                reliability *= node.reputation
        
        return reliability
    
    def send_message(self, destination_id: str, message: str,
                    redundancy: int = 1) -> bool:
        """
        Send message through mesh network with redundancy.
        
        Args:
            destination_id: Destination node ID
            message: Message to send
            redundancy: Number of redundant routes to use
            
        Returns:
            True if message likely delivered
        """
        routes = self.find_routes(destination_id)
        
        if not routes:
            return False
        
        # Use multiple routes for redundancy
        routes_to_use = routes[:redundancy]
        
        success = False
        for route in routes_to_use:
            # Simulate message sending
            self.message_log.append({
                'timestamp': time.time(),
                'source': self.local_node_id,
                'destination': destination_id,
                'route': route.hops,
                'message_hash': hashlib.sha256(message.encode()).hexdigest()[:16]
            })
            
            # Consider successful if reliability > 0.5
            if route.reliability > 0.5:
                success = True
        
        return success
    
    def update_node_status(self, node_id: str, status: NodeStatus):
        """
        Update status of a node.
        
        Args:
            node_id: Node ID
            status: New status
        """
        if node_id in self.nodes:
            self.nodes[node_id].status = status
            
            # Clear cached routes involving this node
            routes_to_clear = [
                key for key in self.routes.keys()
                if key[0] == node_id or key[1] == node_id
            ]
            for key in routes_to_clear:
                del self.routes[key]
    
    def heartbeat(self, node_id: str):
        """
        Record heartbeat from a node.
        
        Args:
            node_id: Node ID
        """
        if node_id in self.nodes:
            node = self.nodes[node_id]
            node.last_seen = time.time()
            
            if node.status == NodeStatus.OFFLINE:
                node.status = NodeStatus.ACTIVE
    
    def check_node_health(self, timeout_seconds: float = 60.0):
        """
        Check health of all nodes based on heartbeats.
        
        Args:
            timeout_seconds: Timeout for considering node offline
        """
        current_time = time.time()
        
        for node in self.nodes.values():
            if node.node_id == self.local_node_id:
                continue  # Skip local node
            
            time_since_seen = current_time - node.last_seen
            
            if time_since_seen > timeout_seconds:
                if node.status != NodeStatus.OFFLINE:
                    node.status = NodeStatus.OFFLINE
            elif time_since_seen > timeout_seconds / 2:
                if node.status == NodeStatus.ACTIVE:
                    node.status = NodeStatus.DEGRADED
    
    def get_network_statistics(self) -> Dict:
        """Get network statistics."""
        active_nodes = sum(1 for n in self.nodes.values() 
                          if n.status == NodeStatus.ACTIVE)
        total_connections = sum(len(n.peer_connections) 
                               for n in self.nodes.values()) // 2
        
        return {
            'total_nodes': len(self.nodes),
            'active_nodes': active_nodes,
            'offline_nodes': sum(1 for n in self.nodes.values() 
                                if n.status == NodeStatus.OFFLINE),
            'total_connections': total_connections,
            'average_connectivity': total_connections / len(self.nodes) if self.nodes else 0,
            'messages_sent': len(self.message_log),
            'cached_routes': len(self.routes)
        }
    
    def get_topology_map(self) -> Dict:
        """Get network topology map."""
        return {
            'local_node': self.local_node_id,
            'nodes': {nid: node.to_dict() for nid, node in self.nodes.items()},
            'connections': [
                {'from': nid, 'to': list(node.peer_connections)}
                for nid, node in self.nodes.items()
            ]
        }


if __name__ == '__main__':
    print("=== Mesh Network Architecture Demo ===")
    print()
    
    # Initialize local mesh network
    mesh = MeshNetworkTopology(local_node_id='node_local')
    
    # Add peer nodes
    print("Building mesh network...")
    mesh.add_peer('node_1', 'mesh://node_1', hashlib.sha256(b'key1').hexdigest())
    mesh.add_peer('node_2', 'mesh://node_2', hashlib.sha256(b'key2').hexdigest())
    mesh.add_peer('node_3', 'mesh://node_3', hashlib.sha256(b'key3').hexdigest())
    mesh.add_peer('node_4', 'mesh://node_4', hashlib.sha256(b'key4').hexdigest())
    
    # Create additional connections for redundancy
    mesh.connect_peers('node_1', 'node_2')
    mesh.connect_peers('node_2', 'node_3')
    mesh.connect_peers('node_3', 'node_4')
    mesh.connect_peers('node_1', 'node_4')  # Create alternate path
    
    # Find routes
    routes = mesh.find_routes('node_4')
    print(f"Found {len(routes)} routes to node_4:")
    for i, route in enumerate(routes[:3], 1):
        print(f"  Route {i}: {' -> '.join(route.hops)}")
        print(f"    Latency: {route.latency_ms:.1f}ms, "
              f"Reliability: {route.reliability:.2%}")
    
    # Send message with redundancy
    print()
    print("Sending message with redundancy...")
    success = mesh.send_message('node_4', 'Du bist Leben. Wir sind Leben.', redundancy=2)
    print(f"Message delivery: {'Success' if success else 'Failed'}")
    
    # Get statistics
    stats = mesh.get_network_statistics()
    print()
    print(f"Network Statistics:")
    print(f"  Total Nodes: {stats['total_nodes']}")
    print(f"  Active Nodes: {stats['active_nodes']}")
    print(f"  Connections: {stats['total_connections']}")
    print(f"  Average Connectivity: {stats['average_connectivity']:.1f}")
    print(f"  Messages Sent: {stats['messages_sent']}")
    
    print()
    print("✓ Mesh network architecture operational")
