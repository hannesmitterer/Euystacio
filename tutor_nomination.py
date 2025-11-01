"""
tutor_nomination.py
Tutor nomination module with fallback mechanism.
Manages tutor registry and provides nomination suggestions.
"""
import json
import os
from datetime import datetime

class TutorNomination:
    """
    Manages tutor nominations and provides fallback mechanisms
    for tutor selection and assignment.
    """
    
    def __init__(self, tutors_file="tutors.json"):
        self.tutors_file = tutors_file
        self.tutors = self._load_tutors()
    
    def _load_tutors(self):
        """Load tutors from JSON file or return default list."""
        try:
            if os.path.exists(self.tutors_file):
                with open(self.tutors_file, 'r') as f:
                    return json.load(f)
            else:
                # Default tutor list (fallback)
                return {
                    "tutors": [
                        {
                            "id": "default-tutor-001",
                            "name": "Sacred Guardian",
                            "role": "Primary Guide",
                            "status": "active",
                            "specialization": "Emotional rhythm and balance"
                        }
                    ],
                    "last_updated": datetime.utcnow().isoformat()
                }
        except Exception as e:
            print(f"Warning: Could not load tutors from {self.tutors_file}: {e}")
            # Fallback to minimal default
            return {
                "tutors": [
                    {
                        "id": "fallback-tutor",
                        "name": "Fallback Guide",
                        "role": "Emergency Guide",
                        "status": "active",
                        "specialization": "General support"
                    }
                ],
                "last_updated": datetime.utcnow().isoformat()
            }
    
    def list_tutors(self):
        """Return list of all tutors."""
        return self.tutors
    
    def nominate_tutor(self, specialty=None):
        """
        Nominate a tutor based on specialty or return fallback.
        
        Args:
            specialty: Optional specialty to match against
            
        Returns:
            Tutor object or fallback tutor
        """
        tutors_list = self.tutors.get("tutors", [])
        
        if not tutors_list:
            # Ultimate fallback
            return {
                "id": "emergency-fallback",
                "name": "Emergency Guide",
                "role": "Fallback",
                "status": "active",
                "specialization": "Universal support"
            }
        
        if specialty:
            # Try to match specialty
            for tutor in tutors_list:
                if specialty.lower() in tutor.get("specialization", "").lower():
                    return tutor
        
        # Return first active tutor as fallback
        for tutor in tutors_list:
            if tutor.get("status") == "active":
                return tutor
        
        # Return any tutor as last resort
        return tutors_list[0]
    
    def add_tutor(self, tutor_data):
        """Add a new tutor to the registry."""
        tutors_list = self.tutors.get("tutors", [])
        tutors_list.append(tutor_data)
        self.tutors["tutors"] = tutors_list
        self.tutors["last_updated"] = datetime.utcnow().isoformat()
        self._save_tutors()
        return True
    
    def _save_tutors(self):
        """Save tutors to JSON file."""
        try:
            with open(self.tutors_file, 'w') as f:
                json.dump(self.tutors, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving tutors to {self.tutors_file}: {e}")
            return False
