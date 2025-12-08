"""
Affective Prioritization System
Prioritize submissions with high Custos Sentimento intensity over low-relevance traffic
"""

from typing import Dict, Any, List
from datetime import datetime
import heapq


class AffectivePrioritizer:
    """
    Prioritizes pulse submissions based on Custos Sentimento (emotional guardian) intensity.
    High-intensity emotional pulses are processed before low-relevance traffic.
    """
    
    # Priority levels based on emotional intensity
    PRIORITY_LEVELS = {
        "critical": 1,      # Intensity >= 0.9
        "high": 2,          # Intensity >= 0.7
        "medium": 3,        # Intensity >= 0.4
        "low": 4,           # Intensity < 0.4
        "noise": 5          # Very low intensity or unclear pulses
    }
    
    # Emotional alignments that increase priority (aligned with Law of Equals)
    HIGH_VALUE_EMOTIONS = {
        "trust", "love", "humility", "compassion", 
        "empathy", "harmony", "peace", "unity"
    }
    
    # Emotions that may indicate manipulation (reduce priority)
    SUSPICIOUS_EMOTIONS = {
        "manipulation", "deception", "malice", "aggression"
    }
    
    def __init__(self, max_queue_size: int = 1000):
        """
        Initialize Affective Prioritizer.
        
        Args:
            max_queue_size: Maximum number of pulses to queue
        """
        self.queue = []  # Priority queue (min-heap)
        self.max_queue_size = max_queue_size
        self.processed_count = 0
        self.metrics = {
            "total_received": 0,
            "by_priority": {level: 0 for level in self.PRIORITY_LEVELS.keys()},
            "dropped": 0,
            "processed": 0
        }
    
    def calculate_priority_score(self, pulse_data: Dict[str, Any]) -> float:
        """
        Calculate priority score for a pulse submission.
        Lower score = higher priority.
        
        Args:
            pulse_data: Pulse submission data
            
        Returns:
            Priority score (lower is higher priority)
        """
        intensity = float(pulse_data.get("intensity", 0.5))
        emotion = pulse_data.get("emotion", "").lower()
        clarity = pulse_data.get("clarity", "medium")
        
        # Base priority from intensity
        if intensity >= 0.9:
            base_priority = self.PRIORITY_LEVELS["critical"]
        elif intensity >= 0.7:
            base_priority = self.PRIORITY_LEVELS["high"]
        elif intensity >= 0.4:
            base_priority = self.PRIORITY_LEVELS["medium"]
        else:
            base_priority = self.PRIORITY_LEVELS["low"]
        
        # Adjust for clarity
        clarity_multiplier = {
            "high": 0.8,
            "medium": 1.0,
            "low": 1.3
        }.get(clarity, 1.0)
        
        # Adjust for emotion alignment
        emotion_modifier = 0
        if emotion in self.HIGH_VALUE_EMOTIONS:
            emotion_modifier = -0.5  # Increase priority
        elif emotion in self.SUSPICIOUS_EMOTIONS:
            emotion_modifier = 2.0   # Decrease priority
        
        # Calculate final score
        priority_score = (base_priority * clarity_multiplier) + emotion_modifier
        
        return max(0.1, priority_score)  # Ensure positive score
    
    def get_priority_level_name(self, score: float) -> str:
        """Get the human-readable priority level name from score."""
        if score <= 1.5:
            return "critical"
        elif score <= 2.5:
            return "high"
        elif score <= 3.5:
            return "medium"
        elif score <= 4.5:
            return "low"
        else:
            return "noise"
    
    def enqueue_pulse(self, pulse_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a pulse submission to the priority queue.
        
        Args:
            pulse_data: Pulse submission data
            
        Returns:
            Dict with enqueue status and priority info
        """
        self.metrics["total_received"] += 1
        
        # Calculate priority
        priority_score = self.calculate_priority_score(pulse_data)
        priority_level = self.get_priority_level_name(priority_score)
        
        self.metrics["by_priority"][priority_level] += 1
        
        # Check if queue is full
        if len(self.queue) >= self.max_queue_size:
            # Remove lowest priority item if current pulse has higher priority
            if self.queue and priority_score < self.queue[0][0]:
                dropped_item = heapq.heappop(self.queue)
                self.metrics["dropped"] += 1
            else:
                # Drop current pulse if it's lower priority
                self.metrics["dropped"] += 1
                return {
                    "enqueued": False,
                    "reason": "queue_full_and_low_priority",
                    "priority_score": priority_score,
                    "priority_level": priority_level,
                    "queue_size": len(self.queue)
                }
        
        # Add timestamp and metadata
        queue_item = (
            priority_score,
            datetime.utcnow().timestamp(),  # Tiebreaker (FIFO for same priority)
            {
                **pulse_data,
                "priority_score": priority_score,
                "priority_level": priority_level,
                "enqueued_at": datetime.utcnow().isoformat()
            }
        )
        
        heapq.heappush(self.queue, queue_item)
        
        return {
            "enqueued": True,
            "priority_score": priority_score,
            "priority_level": priority_level,
            "queue_size": len(self.queue),
            "queue_position": self._estimate_position(priority_score)
        }
    
    def _estimate_position(self, priority_score: float) -> int:
        """Estimate position in queue based on priority score."""
        position = sum(1 for item in self.queue if item[0] < priority_score)
        return position + 1
    
    def dequeue_pulse(self) -> Dict[str, Any]:
        """
        Remove and return the highest priority pulse from queue.
        
        Returns:
            Pulse data with priority info, or None if queue is empty
        """
        if not self.queue:
            return None
        
        priority_score, timestamp, pulse_data = heapq.heappop(self.queue)
        self.processed_count += 1
        self.metrics["processed"] += 1
        
        # Add processing metadata
        pulse_data["dequeued_at"] = datetime.utcnow().isoformat()
        pulse_data["queue_wait_time"] = (
            datetime.utcnow().timestamp() - timestamp
        )
        
        return pulse_data
    
    def peek_next_pulse(self) -> Dict[str, Any]:
        """View the next pulse without removing it from queue."""
        if not self.queue:
            return None
        
        return self.queue[0][2]
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get current status of the priority queue."""
        priority_distribution = {level: 0 for level in self.PRIORITY_LEVELS.keys()}
        
        for item in self.queue:
            priority_level = item[2].get("priority_level", "low")
            priority_distribution[priority_level] += 1
        
        return {
            "queue_size": len(self.queue),
            "max_size": self.max_queue_size,
            "utilization_percentage": round(
                len(self.queue) / self.max_queue_size * 100, 2
            ),
            "priority_distribution": priority_distribution,
            "next_priority": self.queue[0][2].get("priority_level") if self.queue else None
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get prioritization metrics."""
        return {
            "total_received": self.metrics["total_received"],
            "total_processed": self.metrics["processed"],
            "dropped": self.metrics["dropped"],
            "currently_queued": len(self.queue),
            "drop_rate_percentage": round(
                self.metrics["dropped"] / self.metrics["total_received"] * 100
                if self.metrics["total_received"] > 0 else 0,
                2
            ),
            "by_priority_level": dict(self.metrics["by_priority"])
        }
    
    def clear_queue(self) -> int:
        """
        Clear all pulses from queue.
        
        Returns:
            Number of pulses cleared
        """
        count = len(self.queue)
        self.queue = []
        return count
