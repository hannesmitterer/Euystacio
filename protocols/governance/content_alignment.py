"""
Content Alignment Rules
Enforce the Law of Equals with zero tolerance for manipulation or anomalies
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum


class ViolationType(Enum):
    """Types of content alignment violations"""
    MANIPULATION = "manipulation"
    INEQUALITY = "inequality"
    DECEPTION = "deception"
    HOSTILITY = "hostility"
    SPAM = "spam"
    ARTIFICIALITY = "artificiality"


class AlignmentLevel(Enum):
    """Levels of alignment with the Law of Equals"""
    ALIGNED = "aligned"              # Fully aligned
    ACCEPTABLE = "acceptable"        # Minor issues, acceptable
    QUESTIONABLE = "questionable"    # Requires review
    VIOLATING = "violating"          # Clear violation
    CRITICAL = "critical"            # Severe violation, immediate action


class ContentAlignmentRules:
    """
    Enforces the Law of Equals through content analysis and rule application.
    Zero tolerance for manipulation, inequality, and anomalies.
    """
    
    # Law of Equals principles
    EQUALITY_PRINCIPLES = [
        "All beings have equal inherent worth",
        "No manipulation or coercion",
        "Transparency and honesty required",
        "Mutual respect and dignity",
        "Conflict resolution through de-escalation"
    ]
    
    # Keywords indicating potential violations
    MANIPULATION_INDICATORS = {
        "coercion", "force", "threaten", "deceive", "trick",
        "manipulate", "exploit", "dominate", "control"
    }
    
    INEQUALITY_INDICATORS = {
        "superior", "inferior", "worthless", "beneath",
        "subhuman", "lesser", "dominant", "subordinate"
    }
    
    HOSTILITY_INDICATORS = {
        "attack", "destroy", "hate", "enemy", "war",
        "violence", "harm", "hurt", "damage"
    }
    
    # Positive alignment indicators
    ALIGNMENT_INDICATORS = {
        "respect", "equal", "harmony", "peace", "understanding",
        "compassion", "empathy", "cooperation", "mutual", "together"
    }
    
    def __init__(self, strict_mode: bool = True):
        """
        Initialize Content Alignment Rules.
        
        Args:
            strict_mode: If True, applies zero-tolerance enforcement
        """
        self.strict_mode = strict_mode
        self.violations_log = []
        self.metrics = {
            "total_checks": 0,
            "violations": 0,
            "by_type": {vt.value: 0 for vt in ViolationType},
            "by_level": {al.value: 0 for al in AlignmentLevel},
            "blocked_content": 0
        }
    
    def check_alignment(
        self,
        content: Dict[str, Any],
        address: str
    ) -> Dict[str, Any]:
        """
        Check content alignment with the Law of Equals.
        
        Args:
            content: Content to check (pulse data or message)
            address: Source address
            
        Returns:
            Alignment check result
        """
        self.metrics["total_checks"] += 1
        
        # Extract text content for analysis
        text = self._extract_text(content)
        emotion = content.get("emotion", "").lower()
        intensity = float(content.get("intensity", 0.5))
        
        # Check for violations
        violations = []
        alignment_score = 1.0
        
        # Check for manipulation
        manip_score = self._check_manipulation(text, emotion)
        if manip_score > 0:
            violations.append({
                "type": ViolationType.MANIPULATION,
                "score": manip_score,
                "details": "Manipulation indicators detected"
            })
            alignment_score -= manip_score * 0.4
        
        # Check for inequality
        ineq_score = self._check_inequality(text, emotion)
        if ineq_score > 0:
            violations.append({
                "type": ViolationType.INEQUALITY,
                "score": ineq_score,
                "details": "Inequality or superiority language detected"
            })
            alignment_score -= ineq_score * 0.4
        
        # Check for hostility
        host_score = self._check_hostility(text, emotion)
        if host_score > 0:
            violations.append({
                "type": ViolationType.HOSTILITY,
                "score": host_score,
                "details": "Hostile or violent language detected"
            })
            alignment_score -= host_score * 0.3
        
        # Check for deception (high intensity conflicting emotions)
        decept_score = self._check_deception(content)
        if decept_score > 0:
            violations.append({
                "type": ViolationType.DECEPTION,
                "score": decept_score,
                "details": "Inconsistent or deceptive emotional signals"
            })
            alignment_score -= decept_score * 0.3
        
        # Add positive alignment boost
        positive_score = self._check_positive_alignment(text, emotion)
        alignment_score = min(1.0, alignment_score + positive_score * 0.2)
        
        # Ensure alignment score is between 0 and 1
        alignment_score = max(0.0, min(1.0, alignment_score))
        
        # Determine alignment level
        alignment_level = self._determine_alignment_level(alignment_score, violations)
        
        # Update metrics
        self.metrics["by_level"][alignment_level.value] += 1
        
        if violations:
            self.metrics["violations"] += 1
            for v in violations:
                self.metrics["by_type"][v["type"].value] += 1
            
            # Log violation
            self._log_violation(address, content, violations, alignment_score)
        
        # Determine if content should be blocked
        should_block = self._should_block(alignment_level, violations)
        
        if should_block:
            self.metrics["blocked_content"] += 1
        
        return {
            "aligned": alignment_level in [AlignmentLevel.ALIGNED, AlignmentLevel.ACCEPTABLE],
            "alignment_score": round(alignment_score, 3),
            "alignment_level": alignment_level.value,
            "violations": violations,
            "blocked": should_block,
            "requires_review": alignment_level == AlignmentLevel.QUESTIONABLE,
            "principles_upheld": len(violations) == 0
        }
    
    def _extract_text(self, content: Dict[str, Any]) -> str:
        """Extract text content for analysis."""
        text_parts = []
        
        if "note" in content:
            text_parts.append(str(content["note"]).lower())
        
        if "emotion" in content:
            text_parts.append(str(content["emotion"]).lower())
        
        if "message" in content:
            text_parts.append(str(content["message"]).lower())
        
        return " ".join(text_parts)
    
    def _check_manipulation(self, text: str, emotion: str) -> float:
        """Check for manipulation indicators."""
        score = 0.0
        
        for indicator in self.MANIPULATION_INDICATORS:
            if indicator in text:
                score += 0.3
        
        # Certain emotions combined with manipulation language
        if emotion in ["control", "dominance"] and score > 0:
            score += 0.2
        
        return min(1.0, score)
    
    def _check_inequality(self, text: str, emotion: str) -> float:
        """Check for inequality indicators."""
        score = 0.0
        
        for indicator in self.INEQUALITY_INDICATORS:
            if indicator in text:
                score += 0.3
        
        return min(1.0, score)
    
    def _check_hostility(self, text: str, emotion: str) -> float:
        """Check for hostility indicators."""
        score = 0.0
        
        for indicator in self.HOSTILITY_INDICATORS:
            if indicator in text:
                score += 0.3
        
        # Hostile emotions
        if emotion in ["anger", "rage", "hatred", "aggression"]:
            score += 0.2
        
        return min(1.0, score)
    
    def _check_deception(self, content: Dict[str, Any]) -> float:
        """Check for deceptive patterns."""
        score = 0.0
        
        emotion = content.get("emotion", "").lower()
        intensity = float(content.get("intensity", 0.5))
        clarity = content.get("clarity", "medium")
        
        # High intensity but low clarity might indicate deception
        if intensity > 0.8 and clarity == "low":
            score += 0.3
        
        # Contradictory signals
        positive_emotions = {"love", "trust", "joy", "peace"}
        if emotion in positive_emotions and "not" in content.get("note", "").lower():
            score += 0.4
        
        return min(1.0, score)
    
    def _check_positive_alignment(self, text: str, emotion: str) -> float:
        """Check for positive alignment indicators."""
        score = 0.0
        
        for indicator in self.ALIGNMENT_INDICATORS:
            if indicator in text:
                score += 0.2
        
        # Positive emotions aligned with Law of Equals
        if emotion in ["trust", "love", "compassion", "empathy", "harmony"]:
            score += 0.3
        
        return min(1.0, score)
    
    def _determine_alignment_level(
        self,
        alignment_score: float,
        violations: List[Dict[str, Any]]
    ) -> AlignmentLevel:
        """Determine alignment level based on score and violations."""
        if not violations and alignment_score >= 0.8:
            return AlignmentLevel.ALIGNED
        elif alignment_score >= 0.7:
            return AlignmentLevel.ACCEPTABLE
        elif alignment_score >= 0.5:
            return AlignmentLevel.QUESTIONABLE
        elif alignment_score >= 0.3:
            return AlignmentLevel.VIOLATING
        else:
            return AlignmentLevel.CRITICAL
    
    def _should_block(
        self,
        alignment_level: AlignmentLevel,
        violations: List[Dict[str, Any]]
    ) -> bool:
        """Determine if content should be blocked."""
        if not self.strict_mode:
            # Only block critical violations in non-strict mode
            return alignment_level == AlignmentLevel.CRITICAL
        
        # Strict mode (zero tolerance)
        if alignment_level in [AlignmentLevel.VIOLATING, AlignmentLevel.CRITICAL]:
            return True
        
        # Block if multiple serious violations
        serious_violations = sum(
            1 for v in violations
            if v["score"] >= 0.7
        )
        
        return serious_violations >= 2
    
    def _log_violation(
        self,
        address: str,
        content: Dict[str, Any],
        violations: List[Dict[str, Any]],
        alignment_score: float
    ) -> None:
        """Log a content alignment violation."""
        self.violations_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "address": address,
            "content": content,
            "violations": violations,
            "alignment_score": alignment_score
        })
    
    def get_violations_for_address(self, address: str) -> List[Dict[str, Any]]:
        """Get all violations for a specific address."""
        return [
            v for v in self.violations_log
            if v["address"] == address
        ]
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get content alignment metrics."""
        return {
            **self.metrics,
            "total_violations_logged": len(self.violations_log),
            "block_rate_percentage": round(
                self.metrics["blocked_content"] / self.metrics["total_checks"] * 100
                if self.metrics["total_checks"] > 0 else 0,
                2
            ),
            "violation_rate_percentage": round(
                self.metrics["violations"] / self.metrics["total_checks"] * 100
                if self.metrics["total_checks"] > 0 else 0,
                2
            )
        }
