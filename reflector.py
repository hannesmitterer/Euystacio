"""
reflector.py
Simple reflection module for processing and analyzing emotional pulses.
Provides suggestions based on recent activity.
"""
import json
import os
from datetime import datetime

def reflect_and_suggest():
    """
    Analyze recent pulses and provide reflection and suggestions.
    Returns a reflection object with analysis and recommendations.
    """
    reflection = {
        "timestamp": datetime.utcnow().isoformat(),
        "analysis": "Reflection complete",
        "suggestions": [],
        "pulse_count": 0,
        "emotional_state": "balanced"
    }
    
    # Try to load recent pulses from red_code.json
    try:
        if os.path.exists('red_code.json'):
            with open('red_code.json', 'r') as f:
                red_code = json.load(f)
                pulses = red_code.get("recent_pulses", [])
                reflection["pulse_count"] = len(pulses)
                
                if pulses:
                    # Analyze emotional patterns
                    emotions = [p.get("emotion", "unknown") for p in pulses]
                    intensities = [p.get("intensity", 0.5) for p in pulses]
                    
                    avg_intensity = sum(intensities) / len(intensities) if intensities else 0.5
                    
                    if avg_intensity > 0.7:
                        reflection["emotional_state"] = "heightened"
                        reflection["suggestions"].append("Consider grounding practices to balance intensity")
                    elif avg_intensity < 0.3:
                        reflection["emotional_state"] = "subdued"
                        reflection["suggestions"].append("Explore ways to increase engagement")
                    else:
                        reflection["emotional_state"] = "balanced"
                        reflection["suggestions"].append("Maintain current rhythm and awareness")
                    
                    # Add emotion-specific insights
                    unique_emotions = set(emotions)
                    reflection["emotions_observed"] = list(unique_emotions)
                    
                    if "trust" in emotions:
                        reflection["suggestions"].append("Trust is present - nurture it")
                    if "uncertainty" in emotions:
                        reflection["suggestions"].append("Uncertainty detected - seek clarity through dialogue")
                else:
                    reflection["suggestions"].append("No recent pulses - consider recording emotional state")
    except Exception as e:
        reflection["analysis"] = f"Reflection encountered an issue: {str(e)}"
        reflection["suggestions"].append("Ensure red_code.json is accessible")
    
    return reflection
