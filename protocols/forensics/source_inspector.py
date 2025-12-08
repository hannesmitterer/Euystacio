"""
Source Node Inspector
Isolate and inspect suspicious source nodes for manual review
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum


class InspectionStatus(Enum):
    """Status of source node inspection"""
    PENDING = "pending"              # Awaiting inspection
    IN_REVIEW = "in_review"          # Currently being reviewed
    CLEARED = "cleared"              # Cleared after inspection
    QUARANTINED = "quarantined"      # Isolated for safety
    BLOCKED = "blocked"              # Permanently blocked


class InspectionPriority(Enum):
    """Priority levels for inspection"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SourceNodeInspector:
    """
    Manages isolation and inspection of suspicious source nodes.
    Provides quarantine capabilities and manual review workflow.
    """
    
    def __init__(self):
        """Initialize Source Node Inspector."""
        self.nodes = {}  # node_id (address) -> inspection data
        self.inspection_queue = []  # Priority queue of nodes awaiting inspection
        self.quarantined_nodes = set()
        self.blocked_nodes = set()
        
        self.metrics = {
            "total_inspections": 0,
            "by_status": {s.value: 0 for s in InspectionStatus},
            "by_priority": {p.value: 0 for p in InspectionPriority},
            "quarantined": 0,
            "blocked": 0,
            "cleared": 0
        }
    
    def flag_for_inspection(
        self,
        node_id: str,
        reason: str,
        evidence: Dict[str, Any],
        priority: InspectionPriority = InspectionPriority.MEDIUM,
        requester: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Flag a source node for inspection.
        
        Args:
            node_id: Identifier of the source node (address)
            reason: Reason for flagging
            evidence: Evidence data (anomalies, violations, etc.)
            priority: Inspection priority level
            requester: Who requested the inspection (system/tutor)
            
        Returns:
            Flagging result
        """
        if node_id in self.nodes:
            # Already flagged, update if higher priority
            existing_priority = InspectionPriority[self.nodes[node_id]["priority"].upper()]
            
            if priority.value in ["critical", "high"] and existing_priority.value in ["low", "medium"]:
                # Escalate priority
                self.nodes[node_id]["priority"] = priority.value
                self.nodes[node_id]["evidence"].append(evidence)
                self.nodes[node_id]["updated_at"] = datetime.utcnow().isoformat()
                
                return {
                    "success": True,
                    "action": "priority_escalated",
                    "node_id": node_id,
                    "new_priority": priority.value
                }
            
            return {
                "success": False,
                "reason": "already_flagged",
                "current_status": self.nodes[node_id]["status"]
            }
        
        # Create new inspection record
        self.nodes[node_id] = {
            "node_id": node_id,
            "status": InspectionStatus.PENDING.value,
            "priority": priority.value,
            "reason": reason,
            "evidence": [evidence],
            "flagged_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "requester": requester,
            "inspector": None,
            "notes": [],
            "actions_taken": []
        }
        
        # Add to inspection queue
        self.inspection_queue.append({
            "node_id": node_id,
            "priority": priority.value,
            "flagged_at": datetime.utcnow()
        })
        
        # Sort queue by priority
        self._sort_inspection_queue()
        
        self.metrics["total_inspections"] += 1
        self.metrics["by_status"][InspectionStatus.PENDING.value] += 1
        self.metrics["by_priority"][priority.value] += 1
        
        return {
            "success": True,
            "action": "flagged_for_inspection",
            "node_id": node_id,
            "priority": priority.value,
            "queue_position": self._get_queue_position(node_id)
        }
    
    def _sort_inspection_queue(self) -> None:
        """Sort inspection queue by priority."""
        priority_order = {
            "critical": 0,
            "high": 1,
            "medium": 2,
            "low": 3
        }
        
        self.inspection_queue.sort(
            key=lambda x: (
                priority_order.get(x["priority"], 999),
                x["flagged_at"]
            )
        )
    
    def _get_queue_position(self, node_id: str) -> int:
        """Get position of node in inspection queue."""
        for i, item in enumerate(self.inspection_queue):
            if item["node_id"] == node_id:
                return i + 1
        return -1
    
    def start_inspection(
        self,
        node_id: str,
        inspector_id: str
    ) -> Dict[str, Any]:
        """
        Start inspection of a flagged node.
        
        Args:
            node_id: Node to inspect
            inspector_id: Tutor/inspector ID
            
        Returns:
            Inspection start result
        """
        if node_id not in self.nodes:
            return {
                "success": False,
                "reason": "node_not_flagged"
            }
        
        node_data = self.nodes[node_id]
        
        if node_data["status"] != InspectionStatus.PENDING.value:
            return {
                "success": False,
                "reason": "inspection_already_started",
                "current_status": node_data["status"]
            }
        
        # Update status
        old_status = node_data["status"]
        node_data["status"] = InspectionStatus.IN_REVIEW.value
        node_data["inspector"] = inspector_id
        node_data["inspection_started_at"] = datetime.utcnow().isoformat()
        node_data["updated_at"] = datetime.utcnow().isoformat()
        
        # Update metrics
        self.metrics["by_status"][old_status] -= 1
        self.metrics["by_status"][InspectionStatus.IN_REVIEW.value] += 1
        
        # Remove from queue
        self.inspection_queue = [
            item for item in self.inspection_queue
            if item["node_id"] != node_id
        ]
        
        return {
            "success": True,
            "node_id": node_id,
            "inspector": inspector_id,
            "evidence_count": len(node_data["evidence"])
        }
    
    def complete_inspection(
        self,
        node_id: str,
        inspector_id: str,
        decision: InspectionStatus,
        notes: str,
        actions: List[str]
    ) -> Dict[str, Any]:
        """
        Complete inspection with a decision.
        
        Args:
            node_id: Node being inspected
            inspector_id: Inspector completing review
            decision: Inspection decision (CLEARED, QUARANTINED, BLOCKED)
            notes: Inspector notes
            actions: Actions taken or recommended
            
        Returns:
            Completion result
        """
        if node_id not in self.nodes:
            return {
                "success": False,
                "reason": "node_not_found"
            }
        
        node_data = self.nodes[node_id]
        
        if node_data["inspector"] != inspector_id:
            return {
                "success": False,
                "reason": "inspector_mismatch"
            }
        
        # Update status
        old_status = node_data["status"]
        node_data["status"] = decision.value
        node_data["completed_at"] = datetime.utcnow().isoformat()
        node_data["updated_at"] = datetime.utcnow().isoformat()
        node_data["notes"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "inspector": inspector_id,
            "note": notes
        })
        node_data["actions_taken"].extend(actions)
        
        # Update metrics
        self.metrics["by_status"][old_status] -= 1
        self.metrics["by_status"][decision.value] += 1
        
        # Apply decision
        if decision == InspectionStatus.QUARANTINED:
            self.quarantined_nodes.add(node_id)
            self.metrics["quarantined"] += 1
        elif decision == InspectionStatus.BLOCKED:
            self.blocked_nodes.add(node_id)
            self.metrics["blocked"] += 1
        elif decision == InspectionStatus.CLEARED:
            # Remove from quarantine if present
            self.quarantined_nodes.discard(node_id)
            self.metrics["cleared"] += 1
        
        return {
            "success": True,
            "node_id": node_id,
            "decision": decision.value,
            "actions_taken": actions
        }
    
    def quarantine_node(
        self,
        node_id: str,
        reason: str,
        requester: str
    ) -> Dict[str, Any]:
        """
        Immediately quarantine a node (emergency action).
        
        Args:
            node_id: Node to quarantine
            reason: Reason for quarantine
            requester: Who requested quarantine
            
        Returns:
            Quarantine result
        """
        if node_id not in self.nodes:
            # Create inspection record
            self.flag_for_inspection(
                node_id,
                reason,
                {"emergency_quarantine": True},
                InspectionPriority.CRITICAL,
                requester
            )
        
        node_data = self.nodes[node_id]
        old_status = node_data["status"]
        
        node_data["status"] = InspectionStatus.QUARANTINED.value
        node_data["quarantined_at"] = datetime.utcnow().isoformat()
        node_data["updated_at"] = datetime.utcnow().isoformat()
        node_data["actions_taken"].append({
            "action": "emergency_quarantine",
            "reason": reason,
            "requester": requester,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        self.quarantined_nodes.add(node_id)
        
        # Update metrics
        if old_status in [s.value for s in InspectionStatus]:
            self.metrics["by_status"][old_status] -= 1
        self.metrics["by_status"][InspectionStatus.QUARANTINED.value] += 1
        self.metrics["quarantined"] += 1
        
        return {
            "success": True,
            "node_id": node_id,
            "status": "quarantined"
        }
    
    def is_node_quarantined(self, node_id: str) -> bool:
        """Check if a node is quarantined."""
        return node_id in self.quarantined_nodes
    
    def is_node_blocked(self, node_id: str) -> bool:
        """Check if a node is blocked."""
        return node_id in self.blocked_nodes
    
    def get_node_status(self, node_id: str) -> Dict[str, Any]:
        """Get inspection status for a node."""
        if node_id not in self.nodes:
            return {
                "flagged": False,
                "quarantined": node_id in self.quarantined_nodes,
                "blocked": node_id in self.blocked_nodes
            }
        
        node_data = self.nodes[node_id]
        
        return {
            "flagged": True,
            "node_id": node_id,
            "status": node_data["status"],
            "priority": node_data["priority"],
            "reason": node_data["reason"],
            "flagged_at": node_data["flagged_at"],
            "inspector": node_data.get("inspector"),
            "quarantined": node_id in self.quarantined_nodes,
            "blocked": node_id in self.blocked_nodes,
            "evidence_count": len(node_data["evidence"]),
            "notes_count": len(node_data["notes"])
        }
    
    def get_inspection_queue(self) -> List[Dict[str, Any]]:
        """Get current inspection queue."""
        return [
            {
                "node_id": item["node_id"],
                "priority": item["priority"],
                "flagged_at": item["flagged_at"].isoformat(),
                "queue_position": i + 1
            }
            for i, item in enumerate(self.inspection_queue)
        ]
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get inspection metrics."""
        return {
            "total_inspections": self.metrics["total_inspections"],
            "by_status": dict(self.metrics["by_status"]),
            "by_priority": dict(self.metrics["by_priority"]),
            "currently_quarantined": len(self.quarantined_nodes),
            "currently_blocked": len(self.blocked_nodes),
            "total_cleared": self.metrics["cleared"],
            "pending_inspections": len(self.inspection_queue)
        }
