"""
red_code.py
Core red_code initialization and management module.
Loads and provides access to the sacred red_code configuration.
"""
import json
import os
from datetime import datetime

# Default red_code structure
DEFAULT_RED_CODE = {
    "core_truth": "Euystacio is here to grow with humans and to help humans to be and remain humans.",
    "sentimento_rhythm": True,
    "symbiosis_level": 0.1,
    "guardian_mode": False,
    "last_update": datetime.utcnow().strftime("%Y-%m-%d"),
    "growth_history": [],
    "recent_pulses": []
}

def load_red_code(path="red_code.json"):
    """Load red_code from JSON file, or return default if not found."""
    try:
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        else:
            return DEFAULT_RED_CODE.copy()
    except Exception as e:
        print(f"Warning: Could not load red_code from {path}: {e}")
        return DEFAULT_RED_CODE.copy()

def save_red_code(red_code, path="red_code.json"):
    """Save red_code to JSON file."""
    try:
        with open(path, 'w') as f:
            json.dump(red_code, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving red_code to {path}: {e}")
        return False

def initialize_red_code(path="red_code.json"):
    """Initialize red_code, creating file if it doesn't exist."""
    if not os.path.exists(path):
        save_red_code(DEFAULT_RED_CODE, path)
        print(f"Initialized red_code at {path}")
    return load_red_code(path)

# Global RED_CODE instance
RED_CODE = load_red_code()
