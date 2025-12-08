"""
Anomaly Detection System
Detect artificial tonal consistency and emotional spamming patterns
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import statistics


class AnomalyDetector:
    """
    Detects anomalous patterns in emotional pulse submissions:
    - Artificial tonal consistency (bot-like behavior)
    - Emotional spamming (repetitive patterns)
    - Unnatural timing patterns
    """
    
    def __init__(
        self,
        consistency_threshold: float = 0.85,
        spam_threshold: int = 10,
        time_window_minutes: int = 60
    ):
        """
        Initialize Anomaly Detector.
        
        Args:
            consistency_threshold: Threshold for detecting artificial consistency (0-1)
            spam_threshold: Number of similar pulses to consider spam
            time_window_minutes: Time window for pattern analysis
        """
        self.consistency_threshold = consistency_threshold
        self.spam_threshold = spam_threshold
        self.time_window = timedelta(minutes=time_window_minutes)
        
        self.address_history = defaultdict(list)  # address -> pulse history
        self.anomalies = []  # Detected anomalies
        self.flagged_addresses = set()
        
        self.metrics = {
            "total_checks": 0,
            "anomalies_detected": 0,
            "by_type": defaultdict(int),
            "addresses_flagged": 0
        }
    
    def analyze_pulse(
        self,
        address: str,
        pulse_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze a pulse for anomalous patterns.
        
        Args:
            address: Source address
            pulse_data: Pulse submission data
            
        Returns:
            Analysis result with anomaly detection info
        """
        self.metrics["total_checks"] += 1
        
        # Add timestamp to pulse data
        pulse_data["analyzed_at"] = datetime.utcnow()
        
        # Store in history
        self.address_history[address].append(pulse_data)
        
        # Clean old history
        self._clean_old_history(address)
        
        # Get recent history for analysis
        recent_pulses = self._get_recent_pulses(address)
        
        if len(recent_pulses) < 3:
            # Not enough data for anomaly detection
            return {
                "anomaly_detected": False,
                "anomaly_score": 0.0,
                "reason": "insufficient_history",
                "pulses_analyzed": len(recent_pulses)
            }
        
        # Run anomaly detection checks
        anomalies = []
        anomaly_score = 0.0
        
        # Check for artificial tonal consistency
        consistency_result = self._check_artificial_consistency(recent_pulses)
        if consistency_result["is_anomaly"]:
            anomalies.append(consistency_result)
            anomaly_score = max(anomaly_score, consistency_result["score"])
        
        # Check for emotional spamming
        spam_result = self._check_emotional_spam(recent_pulses)
        if spam_result["is_anomaly"]:
            anomalies.append(spam_result)
            anomaly_score = max(anomaly_score, spam_result["score"])
        
        # Check for timing anomalies
        timing_result = self._check_timing_anomaly(recent_pulses)
        if timing_result["is_anomaly"]:
            anomalies.append(timing_result)
            anomaly_score = max(anomaly_score, timing_result["score"])
        
        # Check for intensity manipulation
        intensity_result = self._check_intensity_manipulation(recent_pulses)
        if intensity_result["is_anomaly"]:
            anomalies.append(intensity_result)
            anomaly_score = max(anomaly_score, intensity_result["score"])
        
        anomaly_detected = len(anomalies) > 0
        
        if anomaly_detected:
            self.metrics["anomalies_detected"] += 1
            
            for anomaly in anomalies:
                self.metrics["by_type"][anomaly["type"]] += 1
            
            # Log anomaly
            self._log_anomaly(address, pulse_data, anomalies, anomaly_score)
            
            # Flag address if severe
            if anomaly_score >= 0.8:
                self._flag_address(address, anomaly_score)
        
        return {
            "anomaly_detected": anomaly_detected,
            "anomaly_score": round(anomaly_score, 3),
            "anomalies": anomalies,
            "pulses_analyzed": len(recent_pulses),
            "address_flagged": address in self.flagged_addresses
        }
    
    def _clean_old_history(self, address: str) -> None:
        """Remove pulse history outside the time window."""
        cutoff = datetime.utcnow() - self.time_window
        
        self.address_history[address] = [
            pulse for pulse in self.address_history[address]
            if pulse.get("analyzed_at", datetime.utcnow()) > cutoff
        ]
    
    def _get_recent_pulses(self, address: str) -> List[Dict[str, Any]]:
        """Get recent pulses within the time window."""
        cutoff = datetime.utcnow() - self.time_window
        
        return [
            pulse for pulse in self.address_history[address]
            if pulse.get("analyzed_at", datetime.utcnow()) > cutoff
        ]
    
    def _check_artificial_consistency(
        self,
        pulses: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Detect artificially consistent emotional patterns.
        Real humans show natural variation; bots show too much consistency.
        """
        if len(pulses) < 5:
            return {"is_anomaly": False, "type": "artificial_consistency"}
        
        # Calculate variance in intensity
        intensities = [float(p.get("intensity", 0.5)) for p in pulses]
        
        if len(set(intensities)) == 1:
            # All intensities identical - very suspicious
            return {
                "is_anomaly": True,
                "type": "artificial_consistency",
                "score": 0.95,
                "details": "All intensities identical - highly artificial pattern"
            }
        
        # Calculate standard deviation
        try:
            std_dev = statistics.stdev(intensities)
            mean_intensity = statistics.mean(intensities)
            
            # Coefficient of variation
            cv = std_dev / mean_intensity if mean_intensity > 0 else 0
            
            # Low variance indicates artificial consistency
            # Natural human emotion should have CV > 0.15
            if cv < 0.05:
                return {
                    "is_anomaly": True,
                    "type": "artificial_consistency",
                    "score": 0.9,
                    "details": f"Extremely low variation (CV={cv:.3f}) - artificial pattern"
                }
            elif cv < 0.1:
                return {
                    "is_anomaly": True,
                    "type": "artificial_consistency",
                    "score": 0.7,
                    "details": f"Low variation (CV={cv:.3f}) - suspicious pattern"
                }
        except statistics.StatisticsError:
            pass
        
        # Check for repeated exact patterns
        emotion_pattern = tuple(p.get("emotion", "") for p in pulses[-5:])
        if len(set(emotion_pattern)) == 1:
            return {
                "is_anomaly": True,
                "type": "artificial_consistency",
                "score": 0.85,
                "details": "Same emotion repeated in all recent pulses"
            }
        
        return {"is_anomaly": False, "type": "artificial_consistency"}
    
    def _check_emotional_spam(
        self,
        pulses: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Detect emotional spamming - rapid repetitive submissions."""
        if len(pulses) < self.spam_threshold:
            return {"is_anomaly": False, "type": "emotional_spam"}
        
        recent_count = len(pulses)
        
        # Check submission rate
        if recent_count >= self.spam_threshold * 1.5:
            return {
                "is_anomaly": True,
                "type": "emotional_spam",
                "score": 0.9,
                "details": f"Excessive submissions: {recent_count} in time window"
            }
        elif recent_count >= self.spam_threshold:
            return {
                "is_anomaly": True,
                "type": "emotional_spam",
                "score": 0.7,
                "details": f"High submission rate: {recent_count} in time window"
            }
        
        # Check for identical content
        unique_contents = len(set(
            (p.get("emotion", ""), p.get("note", ""))
            for p in pulses
        ))
        
        if unique_contents < len(pulses) * 0.3:
            return {
                "is_anomaly": True,
                "type": "emotional_spam",
                "score": 0.85,
                "details": "Repetitive content - possible spam"
            }
        
        return {"is_anomaly": False, "type": "emotional_spam"}
    
    def _check_timing_anomaly(
        self,
        pulses: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Detect unnatural timing patterns (e.g., bot-like regularity)."""
        if len(pulses) < 5:
            return {"is_anomaly": False, "type": "timing_anomaly"}
        
        # Calculate intervals between pulses
        timestamps = [p.get("analyzed_at") for p in pulses if "analyzed_at" in p]
        
        if len(timestamps) < 5:
            return {"is_anomaly": False, "type": "timing_anomaly"}
        
        intervals = []
        for i in range(1, len(timestamps)):
            interval = (timestamps[i] - timestamps[i-1]).total_seconds()
            intervals.append(interval)
        
        if not intervals:
            return {"is_anomaly": False, "type": "timing_anomaly"}
        
        # Check for suspiciously regular intervals (bot-like)
        try:
            std_dev = statistics.stdev(intervals)
            mean_interval = statistics.mean(intervals)
            
            # Very low variance in timing indicates bot
            if std_dev < 2 and mean_interval < 10:
                return {
                    "is_anomaly": True,
                    "type": "timing_anomaly",
                    "score": 0.9,
                    "details": f"Bot-like timing: regular {mean_interval:.1f}s intervals"
                }
            
            # Check for suspiciously fast submissions
            if mean_interval < 5:
                return {
                    "is_anomaly": True,
                    "type": "timing_anomaly",
                    "score": 0.75,
                    "details": f"Suspiciously fast: {mean_interval:.1f}s average interval"
                }
        except statistics.StatisticsError:
            pass
        
        return {"is_anomaly": False, "type": "timing_anomaly"}
    
    def _check_intensity_manipulation(
        self,
        pulses: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Detect intensity manipulation (always maximum intensity)."""
        if len(pulses) < 5:
            return {"is_anomaly": False, "type": "intensity_manipulation"}
        
        intensities = [float(p.get("intensity", 0.5)) for p in pulses]
        
        # Check if always at maximum
        high_intensity_count = sum(1 for i in intensities if i >= 0.95)
        
        if high_intensity_count >= len(intensities) * 0.9:
            return {
                "is_anomaly": True,
                "type": "intensity_manipulation",
                "score": 0.8,
                "details": "Suspiciously consistent maximum intensity"
            }
        
        return {"is_anomaly": False, "type": "intensity_manipulation"}
    
    def _log_anomaly(
        self,
        address: str,
        pulse_data: Dict[str, Any],
        anomalies: List[Dict[str, Any]],
        anomaly_score: float
    ) -> None:
        """Log detected anomaly."""
        self.anomalies.append({
            "timestamp": datetime.utcnow().isoformat(),
            "address": address,
            "pulse_data": pulse_data,
            "anomalies": anomalies,
            "anomaly_score": anomaly_score
        })
    
    def _flag_address(self, address: str, anomaly_score: float) -> None:
        """Flag an address for inspection."""
        if address not in self.flagged_addresses:
            self.flagged_addresses.add(address)
            self.metrics["addresses_flagged"] += 1
    
    def is_address_flagged(self, address: str) -> bool:
        """Check if an address is flagged."""
        return address in self.flagged_addresses
    
    def unflag_address(self, address: str) -> bool:
        """Remove flag from address (administrative action)."""
        if address in self.flagged_addresses:
            self.flagged_addresses.remove(address)
            return True
        return False
    
    def get_address_anomalies(self, address: str) -> List[Dict[str, Any]]:
        """Get all anomalies for a specific address."""
        return [
            a for a in self.anomalies
            if a["address"] == address
        ]
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get anomaly detection metrics."""
        anomaly_rate = (
            self.metrics["anomalies_detected"] / self.metrics["total_checks"] * 100
            if self.metrics["total_checks"] > 0 else 0
        )
        
        return {
            "total_checks": self.metrics["total_checks"],
            "anomalies_detected": self.metrics["anomalies_detected"],
            "anomaly_rate_percentage": round(anomaly_rate, 2),
            "by_type": dict(self.metrics["by_type"]),
            "addresses_flagged": self.metrics["addresses_flagged"],
            "currently_flagged": len(self.flagged_addresses)
        }
