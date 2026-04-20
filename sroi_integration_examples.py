#!/usr/bin/env python3
"""
S-ROI Sovereign Protocol - Integration Examples

Esempi di integrazione del protocollo S-ROI con altri componenti del sistema Euystacio.
"""

from sroi_sovereign_protocol import SROISovereignProtocol, SROIConfig, SROIState
from eternal_resonance_protocol import EternalResonanceProtocol
import time


def example_basic_monitoring():
    """
    Esempio 1: Monitoraggio base con S-ROI
    """
    print("\n" + "="*60)
    print("ESEMPIO 1: Monitoraggio Base S-ROI")
    print("="*60 + "\n")
    
    # Inizializza protocollo S-ROI
    sroi = SROISovereignProtocol()
    
    # Simula serie di valori di risonanza
    resonance_values = [0.3, 0.5, 0.72, 0.87, 0.92, 0.78, 0.65]
    
    for value in resonance_values:
        sroi.update_resonance(value)
        state = sroi.get_current_state()
        print(f"Risonanza: {value:.2f} -> Stato: {state.value}")
    
    # Mostra statistiche finali
    print("\nStatistiche:")
    stats = sroi.resonance_monitor.get_resonance_stats()
    print(f"  Min: {stats['min']:.2f}")
    print(f"  Max: {stats['max']:.2f}")
    print(f"  Media: {stats['avg']:.2f}")
    print(f"  Transizioni: {len(sroi.state_manager.state_history)}")


def example_erp_integration():
    """
    Esempio 2: Integrazione con Eternal Resonance Protocol
    """
    print("\n" + "="*60)
    print("ESEMPIO 2: Integrazione S-ROI + ERP")
    print("="*60 + "\n")
    
    # Inizializza entrambi i protocolli
    erp = EternalResonanceProtocol(node_id="euystacio_sovereign")
    sroi = SROISovereignProtocol()
    
    # Registra nodi ERP
    node1 = erp.register_node(
        "node_alpha",
        truth_alignment=0.8,
        dignity_quotient=0.85
    )
    node2 = erp.register_node(
        "node_beta",
        truth_alignment=0.75,
        dignity_quotient=0.9
    )
    
    print(f"Nodi ERP registrati: {len(erp.nodes)}")
    
    # Usa global alignment come metrica per S-ROI
    alignment = erp.get_global_alignment()
    sroi.update_resonance(alignment)
    
    print(f"Global Alignment ERP: {alignment:.4f}")
    print(f"Stato S-ROI: {sroi.get_current_state().value}")
    
    # Applica Living Covenant se stato è critico
    if sroi.get_current_state() in [SROIState.WARNING, SROIState.CRITICAL]:
        print("\nApplicando Life Affirmation covenant per migliorare alignment...")
        erp.apply_living_covenant("node_alpha", "Life Affirmation", intensity=1.0)
        erp.apply_living_covenant("node_beta", "Life Affirmation", intensity=1.0)
        
        # Ricalcola alignment
        new_alignment = erp.get_global_alignment()
        sroi.update_resonance(new_alignment)
        
        print(f"Nuovo Alignment: {new_alignment:.4f}")
        print(f"Nuovo Stato S-ROI: {sroi.get_current_state().value}")


def example_stealth_mode():
    """
    Esempio 3: Utilizzo della modalità stealth
    """
    print("\n" + "="*60)
    print("ESEMPIO 3: Stealth Mode con Cooldown")
    print("="*60 + "\n")
    
    # Crea config con cooldown breve per demo
    config = SROIConfig(stealth_cooldown_seconds=2.0)
    sroi = SROISovereignProtocol(config=config)
    
    # Imposta risonanza alta
    sroi.update_resonance(0.96)
    print(f"Stato iniziale: {sroi.get_current_state().value} (risonanza: 0.96)")
    
    # Attiva stealth mode
    print("\nAttivazione stealth mode...")
    if sroi.activate_stealth_mode():
        print(f"✓ Stealth attivato -> Stato: {sroi.get_current_state().value}")
    
    # Tenta seconda attivazione (dovrebbe fallire)
    print("\nTentativo seconda attivazione immediata...")
    if not sroi.activate_stealth_mode():
        status = sroi.stealth_controller.get_cooldown_status()
        print(f"✗ Negato - Cooldown: {status['remaining_seconds']:.1f}s rimanenti")
    
    # Attendi scadenza cooldown
    print("\nAttesa scadenza cooldown (2s)...")
    time.sleep(2.1)
    
    # Disattiva e riattiva
    sroi.deactivate_stealth_mode()
    print(f"Stealth disattivato -> Stato: {sroi.get_current_state().value}")
    
    if sroi.activate_stealth_mode():
        print(f"✓ Stealth riattivato con successo")
        status = sroi.stealth_controller.get_cooldown_status()
        print(f"  Attivazioni totali: {status['activation_count']}")


def example_threshold_monitoring():
    """
    Esempio 4: Monitoraggio threshold e WARNING state
    """
    print("\n" + "="*60)
    print("ESEMPIO 4: Threshold Monitoring e WARNING State")
    print("="*60 + "\n")
    
    sroi = SROISovereignProtocol()
    
    print("Testing thresholds:")
    print(f"  NORMAL: < {sroi.config.warning_threshold}")
    print(f"  WARNING: {sroi.config.warning_threshold} - {sroi.config.critical_threshold}")
    print(f"  CRITICAL: >= {sroi.config.critical_threshold}")
    print()
    
    # Test valori vicini alle soglie
    test_values = [
        (0.70, "Appena sotto WARNING"),
        (0.85, "Esattamente su WARNING"),
        (0.88, "Nel range WARNING"),
        (0.95, "Esattamente su CRITICAL"),
        (0.98, "Oltre CRITICAL")
    ]
    
    for value, description in test_values:
        sroi.update_resonance(value)
        state = sroi.get_current_state()
        print(f"{description:.<30} {value:.2f} -> {state.value}")


def example_logging_and_history():
    """
    Esempio 5: Logging e tracciamento storia
    """
    print("\n" + "="*60)
    print("ESEMPIO 5: Logging e Storia Transizioni")
    print("="*60 + "\n")
    
    sroi = SROISovereignProtocol()
    
    # Crea serie di transizioni
    transitions = [
        (0.5, "Start normale"),
        (0.87, "Aumento a WARNING"),
        (0.96, "Escalation a CRITICAL"),
        (0.72, "Ritorno a NORMAL")
    ]
    
    for value, label in transitions:
        sroi.update_resonance(value)
        print(f"{label}: risonanza={value:.2f}, stato={sroi.get_current_state().value}")
    
    # Mostra storia completa
    print("\nStoria Transizioni:")
    history = sroi.get_state_history()
    for i, event in enumerate(history, 1):
        print(f"  {i}. {event['previous_state']} -> {event['new_state']}")
        print(f"     Risonanza: {event['current_resonance']:.2f}")
        print(f"     Motivo: {event['reason']}")
    
    # Export logs completi
    print("\nExport logs...")
    logs = sroi.export_logs()
    print(f"  Status fields: {len(logs['status'])} campi")
    print(f"  State history: {len(logs['state_history'])} eventi")
    print(f"  Resonance history: {len(logs['resonance_history'])} samples")


def example_custom_config():
    """
    Esempio 6: Configurazione personalizzata
    """
    print("\n" + "="*60)
    print("ESEMPIO 6: Configurazione Personalizzata")
    print("="*60 + "\n")
    
    # Crea config custom per caso d'uso specifico
    custom_config = SROIConfig(
        normal_threshold=0.6,           # Più conservativo
        warning_threshold=0.75,         # WARNING prima
        critical_threshold=0.9,         # CRITICAL più basso
        stealth_cooldown_seconds=30.0   # Cooldown più lungo
    )
    
    print("Configurazione Custom:")
    print(f"  Normal threshold: {custom_config.normal_threshold}")
    print(f"  Warning threshold: {custom_config.warning_threshold}")
    print(f"  Critical threshold: {custom_config.critical_threshold}")
    print(f"  Stealth cooldown: {custom_config.stealth_cooldown_seconds}s")
    print()
    
    sroi = SROISovereignProtocol(config=custom_config)
    
    # Test con stessi valori, risultati diversi
    test_values = [0.65, 0.77, 0.92]
    
    for value in test_values:
        sroi.update_resonance(value)
        state = sroi.get_current_state()
        print(f"Risonanza {value:.2f} -> {state.value}")


def main():
    """Esegue tutti gli esempi."""
    print("\n" + "#"*60)
    print("# S-ROI SOVEREIGN PROTOCOL - INTEGRATION EXAMPLES")
    print("#"*60)
    
    example_basic_monitoring()
    example_erp_integration()
    example_stealth_mode()
    example_threshold_monitoring()
    example_logging_and_history()
    example_custom_config()
    
    print("\n" + "#"*60)
    print("# ESEMPI COMPLETATI")
    print("#"*60 + "\n")


if __name__ == "__main__":
    main()
