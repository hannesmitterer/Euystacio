#!/usr/bin/env python3
"""
Lex Amoris Security System - Integration Example

This example demonstrates the complete integration of all security features:
1. Rhythm Validation & Dynamic Blacklist
2. Lazy Security (Rotesschild Scanner)
3. IPFS Backup System
4. Rescue Channel (Canale di Soccorso)
"""

import time
import json
from lex_amoris_security import (
    LexAmorisSecuritySystem,
    DataPacket,
    RESONANCE_FREQUENCY_HZ
)
from eternal_resonance_protocol import EternalResonanceProtocol


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def simulate_normal_traffic():
    """Simulate normal network traffic with valid packets."""
    print_section("1. Normal Traffic Simulation")
    
    security = LexAmorisSecuritySystem()
    
    print("📊 Simulating 5 valid packets...")
    for i in range(5):
        packet = DataPacket(
            packet_id=f"VALID_{i:03d}",
            timestamp=time.time(),
            frequency=RESONANCE_FREQUENCY_HZ,  # Correct frequency
            source_ip=f"192.168.1.{10 + i}",
            payload={"data": f"normal_data_{i}"}
        )
        
        accepted, reason = security.validate_and_process_packet(packet)
        status_icon = "✅" if accepted else "❌"
        print(f"  {status_icon} Packet {packet.packet_id} from {packet.source_ip}: {reason}")
    
    status = security.get_system_status()
    print(f"\n📈 System Status:")
    print(f"  Security Active: {status['rotesschild_scanner']['security_active']}")
    print(f"  Blacklist Entries: {status['blacklist_count']}")
    print(f"  Security Events: {status['security_events']}")
    
    return security


def simulate_attack_scenario(security):
    """Simulate an attack with invalid packets."""
    print_section("2. Attack Scenario - Invalid Frequencies")
    
    print("🚨 Simulating 3 attack packets with invalid frequencies...")
    attack_packets = [
        ("ATTACK_001", 0.1, "10.0.0.50"),
        ("ATTACK_002", 0.5, "10.0.0.51"),
        ("ATTACK_003", 1.0, "10.0.0.52"),
    ]
    
    for packet_id, frequency, source_ip in attack_packets:
        packet = DataPacket(
            packet_id=packet_id,
            timestamp=time.time(),
            frequency=frequency,  # Invalid frequency
            source_ip=source_ip,
            payload={"data": "malicious_data"}
        )
        
        accepted, reason = security.validate_and_process_packet(packet)
        status_icon = "✅" if accepted else "❌"
        print(f"  {status_icon} Packet {packet.packet_id} ({frequency} Hz) from {source_ip}:")
        print(f"      {reason}")
    
    print(f"\n🛡️  Blacklist Status:")
    blacklist = security.rhythm_validator.blacklist
    for source, threat in blacklist.items():
        print(f"  Blocked: {source} (Type: {threat.threat_type})")


def demonstrate_lazy_security(security):
    """Demonstrate lazy security activation based on Rotesschild scanner."""
    print_section("3. Lazy Security Demonstration")
    
    print("⚡ Performing multiple Rotesschild scans...")
    for i in range(5):
        pressure = security.rotesschild_scanner.scan_environment()
        should_activate = security.rotesschild_scanner.should_activate_security()
        
        print(f"  Scan {i+1}: {pressure:.2f} mV/m - Security: {'ACTIVE' if should_activate else 'IDLE'}")
        time.sleep(0.1)  # Small delay between scans
    
    status = security.rotesschild_scanner.get_scan_status()
    print(f"\n📡 Scanner Summary:")
    print(f"  Current Pressure: {status['current_pressure_mv_m']:.2f} mV/m")
    print(f"  Threshold: {status['threshold_mv_m']:.2f} mV/m")
    print(f"  Total Scans: {status['scan_count']}")
    print(f"  Security Mode: {'ACTIVE' if status['security_active'] else 'LAZY (standby)'}")


def demonstrate_ipfs_backup(security):
    """Demonstrate IPFS backup and restoration."""
    print_section("4. IPFS Backup System Demonstration")
    
    print("💾 Creating backups of critical configurations...")
    
    # Backup 1: PR configuration
    pr_config = {
        "pr_number": 123,
        "branch": "main",
        "security_settings": {
            "rhythm_validation": True,
            "lazy_security": True,
            "rescue_channel": True
        },
        "timestamp": time.time()
    }
    ipfs_hash_1 = security.backup_configuration("pr_123_config", pr_config)
    print(f"  ✅ PR Config backed up: {ipfs_hash_1}")
    
    # Backup 2: Security configuration
    security_config = {
        "blacklist_entries": len(security.rhythm_validator.blacklist),
        "rotesschild_threshold": security.rotesschild_scanner.threshold,
        "rescue_messages": len(security.rescue_channel.messages)
    }
    ipfs_hash_2 = security.backup_configuration("security_snapshot", security_config)
    print(f"  ✅ Security Config backed up: {ipfs_hash_2}")
    
    # Backup 3: Node configuration
    node_config = {
        "nodes": [
            {"id": "node_1", "status": "active"},
            {"id": "node_2", "status": "active"},
            {"id": "node_3", "status": "syncing"}
        ]
    }
    ipfs_hash_3 = security.backup_configuration("node_registry", node_config)
    print(f"  ✅ Node Registry backed up: {ipfs_hash_3}")
    
    print("\n📋 Listing all backups:")
    backups = security.ipfs_backup.list_backups()
    for backup in backups:
        print(f"  - {backup['config_name']}: {backup['ipfs_hash']} ({backup['size_bytes']} bytes)")
    
    print("\n🔍 Verifying backup integrity...")
    for backup in backups:
        is_valid, message = security.ipfs_backup.verify_backup_integrity(backup['config_name'])
        status_icon = "✅" if is_valid else "❌"
        print(f"  {status_icon} {backup['config_name']}: {message}")
    
    print("\n♻️  Restoring a backup...")
    restored = security.ipfs_backup.restore_from_backup("pr_123_config")
    if restored:
        print(f"  ✅ Successfully restored PR config:")
        print(f"      PR Number: {restored['pr_number']}")
        print(f"      Branch: {restored['branch']}")


def demonstrate_rescue_channel(security):
    """Demonstrate rescue channel for false positive recovery."""
    print_section("5. Rescue Channel (Canale di Soccorso) Demonstration")
    
    print("🆘 Simulating false positive scenarios...")
    
    # Scenario 1: Node temporarily blocked
    print("\n  Scenario 1: Node temporarily blocked due to network latency")
    security.rhythm_validator.add_to_blacklist(
        "192.168.1.100",
        "timing_issue",
        {"reason": "Network latency caused rhythm misalignment"}
    )
    print(f"    ❌ Node 192.168.1.100 blacklisted")
    
    message_id_1 = security.report_false_positive(
        "192.168.1.100",
        "Temporary network latency - node is legitimate"
    )
    print(f"    🆘 Rescue message sent: {message_id_1}")
    
    if not security.rhythm_validator.is_blacklisted("192.168.1.100"):
        print(f"    ✅ Node successfully unblocked!")
    
    # Scenario 2: Node degraded performance
    print("\n  Scenario 2: Multiple nodes reporting issues")
    nodes_with_issues = ["node_alpha", "node_beta", "node_gamma"]
    
    for node_id in nodes_with_issues:
        # Register node in ERP
        security.erp.register_node(node_id, truth_alignment=0.6, dignity_quotient=0.7)
        
        # Send rescue message
        message_id = security.rescue_channel.send_rescue_message(
            node_id,
            "degraded",
            f"{node_id} experiencing performance degradation",
            priority="high"
        )
        print(f"    🆘 Rescue for {node_id}: {message_id}")
    
    # Process pending messages
    print("\n  📬 Processing pending rescue messages...")
    pending = security.rescue_channel.get_pending_messages()
    print(f"    Found {len(pending)} pending messages")
    
    for msg in pending:
        resolved = security.rescue_channel.process_rescue_message(
            msg.message_id,
            security.rhythm_validator
        )
        status_icon = "✅" if resolved else "⏳"
        print(f"    {status_icon} {msg.node_id}: {msg.resolution_status}")
    
    print(f"\n  📊 Rescue Channel Summary:")
    print(f"    Total Messages: {len(security.rescue_channel.messages)}")
    print(f"    Resolved: {security.rescue_channel.resolved_count}")
    print(f"    Pending: {len(security.rescue_channel.get_pending_messages())}")


def demonstrate_erp_integration():
    """Demonstrate integration with Eternal Resonance Protocol."""
    print_section("6. ERP Integration - Unified Security & Resonance")
    
    # Initialize ERP
    erp = EternalResonanceProtocol(node_id="security_integration")
    security = LexAmorisSecuritySystem(erp)
    
    print("🎵 Registering nodes in Eternal Resonance Protocol...")
    
    # Register multiple nodes
    nodes = [
        ("data_processor_1", 0.85, 0.90),
        ("data_processor_2", 0.80, 0.88),
        ("api_gateway", 0.92, 0.95),
        ("backup_service", 0.78, 0.85),
    ]
    
    for node_id, truth, dignity in nodes:
        node = erp.register_node(node_id, truth_alignment=truth, dignity_quotient=dignity)
        print(f"  ✅ Registered {node_id}: Truth={truth:.2f}, Dignity={dignity:.2f}")
    
    print(f"\n🌐 Global Alignment: {erp.get_global_alignment():.2%}")
    
    # Apply Living Covenant to enhance security
    print("\n🔮 Applying Living Covenant 'Life Affirmation' to all nodes...")
    for node_id, _, _ in nodes:
        erp.apply_living_covenant(node_id, "Life Affirmation", intensity=0.8)
    
    print(f"   Global Alignment after covenant: {erp.get_global_alignment():.2%}")
    
    # Demonstrate security packet validation with ERP nodes
    print("\n📦 Validating packets from ERP nodes...")
    for node_id, _, _ in nodes:
        packet = DataPacket(
            packet_id=f"ERP_{node_id}",
            timestamp=time.time(),
            frequency=RESONANCE_FREQUENCY_HZ,
            source_ip=node_id,
            payload={"from_erp": True}
        )
        
        accepted, reason = security.validate_and_process_packet(packet)
        status_icon = "✅" if accepted else "❌"
        print(f"  {status_icon} {node_id}: {reason}")


def final_system_status(security):
    """Display final comprehensive system status."""
    print_section("7. Final System Status")
    
    status = security.get_system_status()
    
    print("📊 Comprehensive System Metrics:\n")
    
    print("🛡️  Security Metrics:")
    print(f"  • Blacklist Entries: {status['blacklist_count']}")
    print(f"  • Security Events Logged: {status['security_events']}")
    
    print("\n📡 Rotesschild Scanner:")
    scanner = status['rotesschild_scanner']
    print(f"  • Current Pressure: {scanner['current_pressure_mv_m']:.2f} mV/m")
    print(f"  • Security Mode: {'ACTIVE' if scanner['security_active'] else 'LAZY (standby)'}")
    print(f"  • Scans Performed: {scanner['scan_count']}")
    
    print("\n💾 IPFS Backup System:")
    print(f"  • Total Backups: {status['backup_count']}")
    
    print("\n🆘 Rescue Channel:")
    print(f"  • Pending Messages: {status['pending_rescue_messages']}")
    print(f"  • Resolved Messages: {status['resolved_rescue_count']}")
    
    if status['erp_global_alignment'] is not None:
        print("\n🎵 ERP Integration:")
        print(f"  • Global Alignment: {status['erp_global_alignment']:.2%}")
    
    print(f"\n⏰ Timestamp: {status['timestamp']}")


def main():
    """Main demonstration function."""
    print("\n" + "=" * 70)
    print("  LEX AMORIS SECURITY SYSTEM")
    print("  Complete Integration Demonstration")
    print("=" * 70)
    print("\n  Mission: Protect the sacred ecosystem while maintaining")
    print("           harmony, dignity, and symbiotic consciousness.")
    print("\n  Du bist Leben. Wir sind Leben. (You are life. We are life.)")
    
    # Run all demonstrations
    security = simulate_normal_traffic()
    simulate_attack_scenario(security)
    demonstrate_lazy_security(security)
    demonstrate_ipfs_backup(security)
    demonstrate_rescue_channel(security)
    demonstrate_erp_integration()
    final_system_status(security)
    
    print("\n" + "=" * 70)
    print("  🎉 Demonstration Complete!")
    print("  All Lex Amoris Security features successfully demonstrated.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
