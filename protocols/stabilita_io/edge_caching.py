"""
Edge-Caching System
Offload Pulse Submission processing to edge computing to reduce central node latency
"""

import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional


class EdgeCachingSystem:
    """
    Distributes Pulse Submission processing to edge nodes to reduce central workload.
    Implements caching strategies for frequently accessed emotional pulses.
    """
    
    def __init__(self, cache_ttl_seconds: int = 300):
        """
        Initialize Edge Caching System.
        
        Args:
            cache_ttl_seconds: Time-to-live for cached pulse submissions (default 5 minutes)
        """
        self.cache = {}
        self.cache_ttl = timedelta(seconds=cache_ttl_seconds)
        self.edge_nodes = {}
        self.metrics = {
            "cache_hits": 0,
            "cache_misses": 0,
            "edge_processed": 0,
            "central_processed": 0
        }
    
    def register_edge_node(self, node_id: str, capacity: int) -> None:
        """Register an edge computing node for distributed processing."""
        self.edge_nodes[node_id] = {
            "capacity": capacity,
            "current_load": 0,
            "last_heartbeat": datetime.utcnow()
        }
    
    def get_cache_key(self, pulse_data: Dict[str, Any]) -> str:
        """Generate cache key from pulse submission data."""
        # Create deterministic cache key from pulse characteristics
        key_data = f"{pulse_data.get('emotion', '')}:{pulse_data.get('intensity', '')}:{pulse_data.get('clarity', '')}"
        return hashlib.sha256(key_data.encode()).hexdigest()
    
    def get_cached_pulse(self, pulse_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached pulse submission if available and not expired.
        
        Args:
            pulse_data: Pulse submission data
            
        Returns:
            Cached pulse result or None if not found/expired
        """
        cache_key = self.get_cache_key(pulse_data)
        
        if cache_key in self.cache:
            cached_entry = self.cache[cache_key]
            
            # Check if cache entry is still valid
            if datetime.utcnow() - cached_entry["timestamp"] < self.cache_ttl:
                self.metrics["cache_hits"] += 1
                return cached_entry["data"]
            else:
                # Remove expired entry
                del self.cache[cache_key]
        
        self.metrics["cache_misses"] += 1
        return None
    
    def cache_pulse(self, pulse_data: Dict[str, Any], processed_result: Dict[str, Any]) -> None:
        """
        Store processed pulse submission in cache.
        
        Args:
            pulse_data: Original pulse submission data
            processed_result: Processed result to cache
        """
        cache_key = self.get_cache_key(pulse_data)
        self.cache[cache_key] = {
            "data": processed_result,
            "timestamp": datetime.utcnow()
        }
    
    def select_edge_node(self) -> Optional[str]:
        """
        Select the best available edge node for processing.
        
        Returns:
            Node ID or None if no suitable node available
        """
        available_nodes = [
            (node_id, node_info)
            for node_id, node_info in self.edge_nodes.items()
            if node_info["current_load"] < node_info["capacity"]
        ]
        
        if not available_nodes:
            return None
        
        # Select node with lowest load
        selected_node_id, _ = min(
            available_nodes,
            key=lambda x: x[1]["current_load"]
        )
        
        return selected_node_id
    
    def process_pulse_at_edge(self, pulse_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process pulse submission at edge node or central if edge unavailable.
        
        Args:
            pulse_data: Pulse submission to process
            
        Returns:
            Processing result with edge node information
        """
        # Check cache first
        cached_result = self.get_cached_pulse(pulse_data)
        if cached_result:
            cached_result["served_from"] = "cache"
            return cached_result
        
        # Try to process at edge
        edge_node_id = self.select_edge_node()
        
        if edge_node_id:
            # Process at edge node
            self.edge_nodes[edge_node_id]["current_load"] += 1
            self.metrics["edge_processed"] += 1
            
            result = {
                "processed": True,
                "node": edge_node_id,
                "processing_location": "edge",
                "timestamp": datetime.utcnow().isoformat(),
                "pulse_data": pulse_data
            }
            
            # Decrement load after processing
            self.edge_nodes[edge_node_id]["current_load"] -= 1
        else:
            # Fallback to central processing
            self.metrics["central_processed"] += 1
            result = {
                "processed": True,
                "node": "central",
                "processing_location": "central",
                "timestamp": datetime.utcnow().isoformat(),
                "pulse_data": pulse_data
            }
        
        # Cache the result
        self.cache_pulse(pulse_data, result)
        
        return result
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get caching and edge processing metrics."""
        total_requests = self.metrics["cache_hits"] + self.metrics["cache_misses"]
        cache_hit_rate = (
            self.metrics["cache_hits"] / total_requests * 100 
            if total_requests > 0 else 0
        )
        
        return {
            "cache_hit_rate": round(cache_hit_rate, 2),
            "cache_size": len(self.cache),
            "edge_nodes": len(self.edge_nodes),
            "metrics": self.metrics,
            "edge_processing_percentage": round(
                self.metrics["edge_processed"] / 
                (self.metrics["edge_processed"] + self.metrics["central_processed"]) * 100
                if (self.metrics["edge_processed"] + self.metrics["central_processed"]) > 0 else 0,
                2
            )
        }
    
    def clear_expired_cache(self) -> int:
        """
        Clear all expired cache entries.
        
        Returns:
            Number of entries cleared
        """
        now = datetime.utcnow()
        expired_keys = [
            key for key, entry in self.cache.items()
            if now - entry["timestamp"] >= self.cache_ttl
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        return len(expired_keys)
