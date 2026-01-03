"""
Integration Examples for Eternal Resonance Protocol

This module demonstrates various integration patterns for the ERP with
existing Euystacio components and external systems.
"""

import json
import time
from eternal_resonance_protocol import EternalResonanceProtocol, RESONANCE_PERIOD_SECONDS


def example_basic_usage():
    """Basic ERP usage example."""
    print("=== Basic ERP Usage ===\n")
    
    # Initialize protocol
    erp = EternalResonanceProtocol(node_id="example_basic")
    
    # Register nodes
    node1 = erp.register_node("worker_1", truth_alignment=0.7, dignity_quotient=0.8)
    node2 = erp.register_node("worker_2", truth_alignment=0.75, dignity_quotient=0.85)
    
    print(f"Registered {len(erp.nodes)} nodes")
    print(f"Global Alignment: {erp.get_global_alignment():.2%}\n")
    
    # Synchronize nodes
    erp.synchronize_node("worker_1")
    erp.synchronize_node("worker_2")
    print("Nodes synchronized\n")
    
    # Apply Living Covenant
    erp.apply_living_covenant("worker_1", "Life Affirmation", intensity=0.8)
    print("Applied Living Covenant to worker_1\n")
    
    # Apply K-Symbiosis
    erp.k_symbiosis_focus("worker_2", "unity", parameters={'multiplier': 1.2})
    print("Applied K-Symbiosis to worker_2\n")
    
    # Check final alignment
    print(f"Final Global Alignment: {erp.get_global_alignment():.2%}")


def example_euystacio_integration():
    """Integration with Euystacio core."""
    print("\n=== Euystacio Core Integration ===\n")
    
    try:
        from euystacio_core import Euystacio
        
        # Initialize both systems
        eu = Euystacio()
        erp = EternalResonanceProtocol(node_id="euystacio_main")
        
        # Register Euystacio as a resonance node
        symbiosis = eu.code.get('symbiosis_level', 0.1)
        node = erp.register_node(
            "euystacio_core",
            truth_alignment=symbiosis,
            dignity_quotient=0.9,
            symbiosis_level=symbiosis
        )
        
        print(f"Euystacio registered as resonance node")
        print(f"  Symbiosis Level: {node.symbiosis_level:.2%}\n")
        
        # Process an event through both systems
        event = {
            "type": "message",
            "feeling": "trust",
            "intent": "connection"
        }
        
        # Reflect in Euystacio
        eu.reflect(event)
        
        # Apply resonance alignment based on feeling
        if event.get("feeling") in ["trust", "love", "humility"]:
            erp.apply_living_covenant(
                "euystacio_core",
                "Life Affirmation",
                intensity=0.7
            )
            erp.k_symbiosis_focus(
                "euystacio_core",
                "unity",
                parameters={'multiplier': 1.0}
            )
            print("Applied resonance alignment based on positive feeling\n")
        
        # Show updated state
        node = erp.nodes["euystacio_core"]
        print(f"Updated Node State:")
        print(f"  Truth Alignment: {node.truth_alignment:.2%}")
        print(f"  Dignity Quotient: {node.dignity_quotient:.2%}")
        print(f"  Symbiosis Level: {node.symbiosis_level:.2%}")
        
    except ImportError:
        print("Euystacio core not available")


def example_red_code_monitoring():
    """Monitor and enforce Red Code compliance."""
    print("\n=== Red Code Monitoring ===\n")
    
    erp = EternalResonanceProtocol(node_id="red_code_monitor")
    
    # Register node
    node = erp.register_node("monitored_node", truth_alignment=0.6, dignity_quotient=0.7)
    
    def check_red_code_compliance():
        """Check if Red Code principles are maintained."""
        try:
            with open('red_code.json', 'r') as f:
                red_code = json.load(f)
            
            sentimento_ok = red_code.get('sentimento_rhythm', False)
            
            if not sentimento_ok:
                print("⚠️  Red Code violation: Sentimento Rhythm not active")
                # Apply corrective covenant
                erp.apply_living_covenant(
                    "monitored_node",
                    "Truth Resonance",
                    intensity=1.0
                )
                print("Applied corrective covenant\n")
                return False
            else:
                print("✓ Red Code compliance OK\n")
                return True
                
        except FileNotFoundError:
            print("Red Code file not found\n")
            return True
    
    # Check compliance
    check_red_code_compliance()
    
    # Show node state
    node = erp.nodes["monitored_node"]
    print(f"Node State:")
    print(f"  Truth Alignment: {node.truth_alignment:.2%}")
    print(f"  Dignity Quotient: {node.dignity_quotient:.2%}")


def example_continuous_sync():
    """Continuous synchronization loop."""
    print("\n=== Continuous Synchronization ===\n")
    print("Running 3 cycles with 5-second intervals...\n")
    
    erp = EternalResonanceProtocol(node_id="sync_master")
    
    # Register multiple nodes
    for i in range(3):
        erp.register_node(
            f"node_{i}",
            truth_alignment=0.6 + i * 0.1,
            dignity_quotient=0.7 + i * 0.1
        )
    
    # Run sync cycles
    for cycle in range(3):
        print(f"--- Cycle {cycle + 1} ---")
        
        # Get current phase
        phase = erp.get_current_phase()
        print(f"Current Phase: {phase:.4f} rad")
        
        # Synchronize all nodes
        for node_id in erp.nodes:
            erp.synchronize_node(node_id)
        
        # Check alignment
        alignment = erp.get_global_alignment()
        print(f"Global Alignment: {alignment:.2%}")
        
        # Apply correction if needed
        if alignment < 0.7:
            print("Applying corrective covenants...")
            for node_id in erp.nodes:
                erp.apply_living_covenant(
                    node_id,
                    "Truth Resonance",
                    intensity=0.5
                )
        
        print()
        
        # Wait for next cycle (shortened for demo)
        if cycle < 2:
            time.sleep(5)


def example_distributed_nodes():
    """Example of distributed node coordination."""
    print("\n=== Distributed Node Coordination ===\n")
    
    # Primary node
    erp_primary = EternalResonanceProtocol(node_id="primary")
    genesis_time = erp_primary.genesis_time
    
    # Register primary node
    erp_primary.register_node("primary_worker", truth_alignment=0.8, dignity_quotient=0.9)
    
    print("Primary node initialized")
    print(f"Genesis Time: {genesis_time}\n")
    
    # Simulate secondary node in different location
    # (In real deployment, this would be a separate process/machine)
    erp_secondary = EternalResonanceProtocol(node_id="secondary")
    erp_secondary.genesis_time = genesis_time  # Sync to same genesis
    
    # Register secondary node
    erp_secondary.register_node("secondary_worker", truth_alignment=0.75, dignity_quotient=0.85)
    
    print("Secondary node initialized with shared genesis time\n")
    
    # Both nodes should have similar phase
    print(f"Primary Phase: {erp_primary.get_current_phase():.4f} rad")
    print(f"Secondary Phase: {erp_secondary.get_current_phase():.4f} rad")
    print(f"Phase Difference: {abs(erp_primary.get_current_phase() - erp_secondary.get_current_phase()):.6f} rad\n")
    
    # Export state for network synchronization
    primary_state = erp_primary.export_state()
    print("Primary state exported for network distribution")


def example_covenant_progression():
    """Demonstrate Living Covenant progression."""
    print("\n=== Living Covenant Progression ===\n")
    
    erp = EternalResonanceProtocol(node_id="covenant_demo")
    
    # Register node with low alignment
    node = erp.register_node("evolving_node", truth_alignment=0.3, dignity_quotient=0.4)
    
    print("Initial State:")
    print(f"  Truth: {node.truth_alignment:.2%}, Dignity: {node.dignity_quotient:.2%}\n")
    
    # Apply covenants progressively
    covenants = ["Truth Resonance", "Dignity Harmonic", "Symbiotic Unity", "Life Affirmation"]
    
    for covenant in covenants:
        erp.apply_living_covenant("evolving_node", covenant, intensity=0.8)
        node = erp.nodes["evolving_node"]
        print(f"After {covenant}:")
        print(f"  Truth: {node.truth_alignment:.2%}, Dignity: {node.dignity_quotient:.2%}")
    
    print(f"\nFinal Symbiosis Level: {node.symbiosis_level:.2%}")


def example_k_symbiosis_focus():
    """Demonstrate K-Symbiosis focus operations."""
    print("\n=== K-Symbiosis Focus Operations ===\n")
    
    erp = EternalResonanceProtocol(node_id="k_symbiosis_demo")
    
    # Register node
    node = erp.register_node("focus_node", truth_alignment=0.5, dignity_quotient=0.5, symbiosis_level=0.2)
    
    print("Initial State:")
    print(f"  Truth: {node.truth_alignment:.2%}")
    print(f"  Dignity: {node.dignity_quotient:.2%}")
    print(f"  Symbiosis: {node.symbiosis_level:.2%}\n")
    
    # Apply different focus areas
    focus_areas = ['truth', 'dignity', 'unity']
    
    for focus in focus_areas:
        erp.k_symbiosis_focus("focus_node", focus, parameters={'multiplier': 1.5})
        node = erp.nodes["focus_node"]
        
        print(f"After {focus.upper()} focus:")
        print(f"  Truth: {node.truth_alignment:.2%}")
        print(f"  Dignity: {node.dignity_quotient:.2%}")
        print(f"  Symbiosis: {node.symbiosis_level:.2%}\n")


def run_all_examples():
    """Run all integration examples."""
    examples = [
        ("Basic Usage", example_basic_usage),
        ("Euystacio Integration", example_euystacio_integration),
        ("Red Code Monitoring", example_red_code_monitoring),
        ("Continuous Synchronization", example_continuous_sync),
        ("Distributed Nodes", example_distributed_nodes),
        ("Covenant Progression", example_covenant_progression),
        ("K-Symbiosis Focus", example_k_symbiosis_focus),
    ]
    
    print("\n" + "="*70)
    print("ETERNAL RESONANCE PROTOCOL - INTEGRATION EXAMPLES")
    print("="*70)
    
    for i, (name, func) in enumerate(examples, 1):
        try:
            func()
        except Exception as e:
            print(f"\n⚠️  Error in {name}: {e}\n")
        
        if i < len(examples):
            input("\nPress Enter to continue to next example...")
    
    print("\n" + "="*70)
    print("All examples completed!")
    print("="*70 + "\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        example_name = sys.argv[1]
        examples_map = {
            'basic': example_basic_usage,
            'euystacio': example_euystacio_integration,
            'redcode': example_red_code_monitoring,
            'sync': example_continuous_sync,
            'distributed': example_distributed_nodes,
            'covenant': example_covenant_progression,
            'k-symbiosis': example_k_symbiosis_focus,
        }
        
        if example_name in examples_map:
            examples_map[example_name]()
        else:
            print(f"Unknown example: {example_name}")
            print(f"Available: {', '.join(examples_map.keys())}")
    else:
        run_all_examples()
