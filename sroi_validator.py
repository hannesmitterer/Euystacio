import sys

# Die heilige Invariante des Nexus
REQUIRED_S_ROI = 0.5187
TOLERANCE = 0.0001

def validate_resonance(s_roi):
    """Validate resonance based on S-ROI value.
    
    Args:
        s_roi: The S-ROI value to validate (must be numeric)
        
    Returns:
        bool: True if resonance is stable, False otherwise
    """
    try:
        s_roi_float = float(s_roi)
    except (TypeError, ValueError):
        print(f"❌ UNGÜLTIGER WERT: S-ROI muss eine Zahl sein.")
        return False

    if abs(s_roi_float - REQUIRED_S_ROI) > TOLERANCE:
        print(f"❌ DISSONANZ DETEKTIERT: S-ROI {s_roi_float} entspricht nicht der Lex Amoris.")
        return False

    print("✅ RESONANZ STABIL: S-ROI 0.5187. Zugang gewährt.")
    return True

if __name__ == "__main__":
    # Teste den aktuellen Status
    current_status = 0.5187 
    if not validate_resonance(current_status):
        sys.exit(1)
