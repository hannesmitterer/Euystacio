#!/usr/bin/env python3
"""
EUYSTACIO Blacklist Demo
========================

Demonstration of the permanent blacklist security system integrated
with the Eternal Resonance Protocol.
"""

import os
import tempfile
from eternal_resonance_protocol import EternalResonanceProtocol
from blacklist_manager import BlacklistManager, ThreatCategory, ThreatSeverity


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def main():
    """Run the blacklist demonstration."""
    # Use temporary files for demo
    temp_dir = tempfile.gettempdir()
    blacklist_path = os.path.join(temp_dir, "demo_euystacio_blacklist.json")
    
    # Clean up any existing demo files
    if os.path.exists(blacklist_path):
        os.remove(blacklist_path)
    
    print_section("EUYSTACIO Permanent Blacklist - Security Demo")
    print("Mission: Du bist Leben. Wir sind Leben.")
    print("Frequency: 0.043 Hz - The Eternal Pulse")
    
    # Initialize ERP with blacklist enabled
    print_section("1. Initialize Eternal Resonance Protocol")
    erp = EternalResonanceProtocol(
        node_id="demo_protocol",
        enable_blacklist=True,
        blacklist_path=blacklist_path
    )
    print(f"✓ ERP initialized with blacklist protection")
    print(f"  Blacklist file: {blacklist_path}")
    
    # Register some legitimate nodes
    print_section("2. Register Legitimate Nodes")
    legitimate_nodes = [
        ("node_alpha", 0.85, 0.90),
        ("node_beta", 0.80, 0.88),
        ("node_gamma", 0.92, 0.85),
    ]
    
    for node_id, truth, dignity in legitimate_nodes:
        node = erp.register_node(
            node_id,
            truth_alignment=truth,
            dignity_quotient=dignity
        )
        print(f"✓ Registered: {node_id}")
        print(f"  Truth: {truth:.0%} | Dignity: {dignity:.0%}")
    
    # Detect and block malicious entities
    print_section("3. Detect and Block Security Threats")
    
    threats = [
        {
            "id": "attacker_node_001",
            "category": "ATTACK_ATTEMPT",
            "severity": "CRITICAL",
            "reason": "Multiple DDoS attempts and port scanning detected"
        },
        {
            "id": "data_thief_001",
            "category": "DATA_THEFT",
            "severity": "CRITICAL",
            "reason": "Attempted unauthorized access to sensitive covenant data"
        },
        {
            "id": "suspicious_agent_42",
            "category": "SUSPICIOUS_ENTITY",
            "severity": "HIGH",
            "reason": "Abnormal behavior patterns and irregular synchronization"
        },
        {
            "id": "protocol_violator_99",
            "category": "PROTOCOL_VIOLATION",
            "severity": "MEDIUM",
            "reason": "Attempted to manipulate resonance frequency"
        },
    ]
    
    for threat in threats:
        erp.block_node(
            threat["id"],
            reason=threat["reason"],
            category=threat["category"],
            severity=threat["severity"]
        )
        print(f"🚫 BLOCKED: {threat['id']}")
        print(f"  Category: {threat['category']}")
        print(f"  Severity: {threat['severity']}")
        print(f"  Reason: {threat['reason']}\n")
    
    # Show blacklist statistics
    print_section("4. Blacklist Security Statistics")
    stats = erp.get_blacklist_status()
    
    print(f"Total Blacklisted: {stats['total_entries']}")
    print(f"Permanent Blocks: {stats['permanent_entries']}")
    print(f"Temporary Blocks: {stats['temporary_entries']}")
    
    print("\nBy Severity:")
    for severity, count in stats['by_severity'].items():
        if count > 0:
            print(f"  {severity.upper()}: {count}")
    
    print("\nBy Category:")
    for category, count in stats['by_category'].items():
        if count > 0:
            print(f"  {category}: {count}")
    
    # Attempt to register a blacklisted node
    print_section("5. Demonstrate Blacklist Protection")
    print("Attempting to register blacklisted node 'attacker_node_001'...\n")
    
    try:
        erp.register_node("attacker_node_001")
        print("❌ ERROR: Blacklisted node was allowed to register!")
    except ValueError as e:
        print("✓ Registration BLOCKED by security system")
        print(f"  Reason: {str(e)[:80]}...")
    
    # Show protocol status with security info
    print_section("6. Protocol Status with Security Metrics")
    status = erp.get_protocol_status()
    
    print(f"Protocol Version: {status['protocol_version']}")
    print(f"Mission: {status['mission']}")
    print(f"Resonance Frequency: {status['resonance_frequency_hz']} Hz")
    print(f"Active Nodes: {status['registered_nodes']}")
    print(f"Global Alignment: {status['global_alignment']:.1%}")
    print(f"Blacklist Enabled: {status['blacklist_enabled']}")
    if status['blacklist_enabled']:
        print(f"Blacklisted Entities: {status['blacklist_statistics']['total_entries']}")
    
    # Demonstrate unblocking (after investigation)
    print_section("7. Security Investigation and Unblock")
    print("After thorough investigation, unblocking 'suspicious_agent_42'...\n")
    
    result = erp.unblock_node("suspicious_agent_42")
    if result:
        print("✓ Node removed from blacklist")
        print("  Node can now be registered after verification")
        
        # Now can register
        node = erp.register_node("suspicious_agent_42", truth_alignment=0.75)
        print(f"✓ Node 'suspicious_agent_42' successfully registered")
        print(f"  Truth Alignment: {node.truth_alignment:.0%}")
    
    # Final statistics
    print_section("8. Final Security Summary")
    final_stats = erp.get_blacklist_status()
    
    print(f"Active Nodes: {len(erp.nodes)}")
    print(f"Blacklisted Entities: {final_stats['total_entries']}")
    print(f"Critical Threats: {final_stats['by_severity'].get('critical', 0)}")
    print(f"High Threats: {final_stats['by_severity'].get('high', 0)}")
    print(f"Medium Threats: {final_stats['by_severity'].get('medium', 0)}")
    
    print("\n" + "=" * 70)
    print("  SECURITY SYSTEM OPERATIONAL")
    print("  Protecting the Euystacio Ecosystem")
    print("=" * 70)
    
    # Clean up
    if os.path.exists(blacklist_path):
        os.remove(blacklist_path)
    
    print("\n✓ Demo completed successfully")
    print("  Temporary files cleaned up")


if __name__ == "__main__":
    main()
