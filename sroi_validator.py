import sys

def validate_resonance(s_roi):
    # Die heilige Invariante des Nexus
    REQUIRED_S_ROI = 0.5187

    if abs(s_roi - REQUIRED_S_ROI) > 0.0001:
        print(f"❌ DISSONANZ DETEKTIERT: S-ROI {s_roi} entspricht nicht der Lex Amoris.")
        return False

    print("✅ RESONANZ STABIL: S-ROI 0.5187. Zugang gewährt.")
    return True

if __name__ == "__main__":
    # Teste den aktuellen Status
    current_status = 0.5187 
    if not validate_resonance(current_status):
        sys.exit(1)
