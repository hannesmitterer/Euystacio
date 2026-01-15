#!/usr/bin/env python3
"""
Lex Amoris Security System - Command Line Operations

CLI tool for managing the Lex Amoris Security System.
"""

import sys
import json
import argparse
from datetime import datetime
from lex_amoris_security import (
    LexAmorisSecuritySystem,
    DataPacket,
    RESONANCE_FREQUENCY_HZ,
    ROTESSCHILD_THRESHOLD_MV_M
)


def cmd_status(args):
    """Show system status."""
    security_system = LexAmorisSecuritySystem()
    status = security_system.get_system_status()
    
    print("\n" + "=" * 60)
    print("Lex Amoris Security System - Status")
    print("=" * 60)
    print(f"\nTimestamp: {status['timestamp']}")
    print(f"\n📡 Rotesschild Scanner:")
    scanner_status = status['rotesschild_scanner']
    print(f"  Current Pressure: {scanner_status['current_pressure_mv_m']:.2f} mV/m")
    print(f"  Threshold: {scanner_status['threshold_mv_m']:.2f} mV/m")
    print(f"  Security Active: {'YES' if scanner_status['security_active'] else 'NO'}")
    print(f"  Above Threshold: {'YES' if scanner_status['above_threshold'] else 'NO'}")
    
    print(f"\n🛡️  Security Metrics:")
    print(f"  Blacklist Entries: {status['blacklist_count']}")
    print(f"  Backup Count: {status['backup_count']}")
    print(f"  Security Events: {status['security_events']}")
    
    print(f"\n🆘 Rescue Channel:")
    print(f"  Pending Messages: {status['pending_rescue_messages']}")
    print(f"  Resolved Messages: {status['resolved_rescue_count']}")
    
    if status['erp_global_alignment'] is not None:
        print(f"\n🎵 ERP Alignment:")
        print(f"  Global Alignment: {status['erp_global_alignment']:.2%}")
    
    print("\n" + "=" * 60 + "\n")


def cmd_validate_packet(args):
    """Validate a data packet."""
    security_system = LexAmorisSecuritySystem()
    
    packet = DataPacket(
        packet_id=args.packet_id,
        timestamp=args.timestamp or datetime.now().timestamp(),
        frequency=args.frequency,
        source_ip=args.source,
        payload={"data": args.payload} if args.payload else {}
    )
    
    accepted, reason = security_system.validate_and_process_packet(packet)
    
    print(f"\nPacket Validation Result:")
    print(f"  Packet ID: {packet.packet_id}")
    print(f"  Source: {packet.source_ip}")
    print(f"  Frequency: {packet.frequency:.4f} Hz")
    print(f"  Status: {'✅ ACCEPTED' if accepted else '❌ REJECTED'}")
    print(f"  Reason: {reason}\n")
    
    return 0 if accepted else 1


def cmd_backup(args):
    """Create a backup."""
    security_system = LexAmorisSecuritySystem()
    
    # Load configuration from file if provided
    if args.config_file:
        try:
            with open(args.config_file, 'r') as f:
                config_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"\n❌ Error reading config file: {e}\n", file=sys.stderr)
            return 1
    else:
        if not args.config_json:
            print("\n❌ Error: Either --config-file or --config-json must be provided\n", file=sys.stderr)
            return 1
        try:
            config_data = json.loads(args.config_json)
        except json.JSONDecodeError as e:
            print(f"\n❌ Error parsing JSON: {e}\n", file=sys.stderr)
            return 1
    
    ipfs_hash = security_system.backup_configuration(args.name, config_data)
    
    print(f"\n✅ Backup Created Successfully")
    print(f"  Name: {args.name}")
    print(f"  IPFS Hash: {ipfs_hash}")
    print(f"  Timestamp: {datetime.now().isoformat()}\n")


def cmd_restore(args):
    """Restore from backup."""
    security_system = LexAmorisSecuritySystem()
    
    # First, we need to create the backup to have something to restore
    # In production, this would retrieve from actual IPFS
    config_data = security_system.ipfs_backup.restore_from_backup(args.name)
    
    if config_data is None:
        print(f"\n❌ Error: Backup '{args.name}' not found\n")
        return 1
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(config_data, f, indent=2)
        print(f"\n✅ Backup Restored to: {args.output}\n")
    else:
        print(f"\n✅ Backup Restored:")
        print(json.dumps(config_data, indent=2))
        print()
    
    return 0


def cmd_rescue(args):
    """Send rescue message."""
    security_system = LexAmorisSecuritySystem()
    
    message_id = security_system.report_false_positive(args.node_id, args.message)
    
    print(f"\n🆘 Rescue Message Sent")
    print(f"  Node ID: {args.node_id}")
    print(f"  Message ID: {message_id}")
    print(f"  Details: {args.message}")
    print(f"  Status: Processed\n")


def cmd_blacklist(args):
    """Manage blacklist."""
    security_system = LexAmorisSecuritySystem()
    
    if args.action == 'add':
        security_system.rhythm_validator.add_to_blacklist(
            args.source,
            args.threat_type or "manual",
            {"reason": args.reason or "Manual addition"}
        )
        print(f"\n✅ Added '{args.source}' to blacklist\n")
    
    elif args.action == 'remove':
        if security_system.rhythm_validator.is_blacklisted(args.source):
            security_system.rhythm_validator.remove_from_blacklist(args.source)
            print(f"\n✅ Removed '{args.source}' from blacklist\n")
        else:
            print(f"\n⚠️  '{args.source}' is not in blacklist\n")
    
    elif args.action == 'list':
        blacklist = security_system.rhythm_validator.blacklist
        if blacklist:
            print(f"\n📋 Blacklist ({len(blacklist)} entries):")
            for source, threat in blacklist.items():
                print(f"\n  Source: {source}")
                print(f"  Type: {threat.threat_type}")
                print(f"  Severity: {threat.severity}")
                print(f"  Timestamp: {datetime.fromtimestamp(threat.timestamp).isoformat()}")
        else:
            print("\n✅ Blacklist is empty\n")
    
    elif args.action == 'check':
        is_blacklisted = security_system.rhythm_validator.is_blacklisted(args.source)
        print(f"\n{'❌' if is_blacklisted else '✅'} '{args.source}' is {'BLACKLISTED' if is_blacklisted else 'NOT blacklisted'}\n")


def cmd_scan(args):
    """Perform Rotesschild scan."""
    security_system = LexAmorisSecuritySystem()
    
    pressure = security_system.rotesschild_scanner.scan_environment()
    should_activate = security_system.rotesschild_scanner.should_activate_security()
    
    print(f"\n📡 Rotesschild Scan Result:")
    print(f"  Pressure: {pressure:.2f} mV/m")
    print(f"  Threshold: {ROTESSCHILD_THRESHOLD_MV_M:.2f} mV/m")
    print(f"  Above Threshold: {'YES' if pressure > ROTESSCHILD_THRESHOLD_MV_M else 'NO'}")
    print(f"  Security Activation: {'REQUIRED' if should_activate else 'NOT REQUIRED'}\n")


def cmd_info(args):
    """Show system information."""
    print("\n" + "=" * 60)
    print("Lex Amoris Security System - Information")
    print("=" * 60)
    print("\n📖 Strategic Security Features:")
    print("\n1. Blacklist Dinamica e Rhythm Validation")
    print("   - Dynamic blacklist based on frequency validation")
    print("   - Behavioral security control module")
    print(f"   - Reference Frequency: {RESONANCE_FREQUENCY_HZ} Hz")
    
    print("\n2. Lazy Security (Rotesschild Scanner)")
    print("   - Energy-based security activation")
    print(f"   - Activation Threshold: {ROTESSCHILD_THRESHOLD_MV_M} mV/m")
    print("   - Protections active only when needed")
    
    print("\n3. IPFS Backup System")
    print("   - Complete configuration mirroring")
    print("   - Repository protection from escalation")
    print("   - Integrity verification with checksums")
    
    print("\n4. Canale di Soccorso (Rescue Channel)")
    print("   - Lex Amoris-based messaging")
    print("   - False positive recovery")
    print("   - Node unblocking mechanism")
    
    print("\n🎯 Mission:")
    print("   Protect the sacred ecosystem while maintaining")
    print("   harmony, dignity, and symbiotic consciousness.")
    print("\n" + "=" * 60 + "\n")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Lex Amoris Security System - CLI Operations",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Status command
    parser_status = subparsers.add_parser('status', help='Show system status')
    parser_status.set_defaults(func=cmd_status)
    
    # Validate packet command
    parser_validate = subparsers.add_parser('validate', help='Validate a data packet')
    parser_validate.add_argument('packet_id', help='Packet ID')
    parser_validate.add_argument('frequency', type=float, help='Packet frequency in Hz')
    parser_validate.add_argument('source', help='Source IP or identifier')
    parser_validate.add_argument('--payload', help='Packet payload (optional)')
    parser_validate.add_argument('--timestamp', type=float, help='Packet timestamp (optional)')
    parser_validate.set_defaults(func=cmd_validate_packet)
    
    # Backup command
    parser_backup = subparsers.add_parser('backup', help='Create IPFS backup')
    parser_backup.add_argument('name', help='Backup name')
    parser_backup.add_argument('--config-file', help='Path to configuration file')
    parser_backup.add_argument('--config-json', help='Configuration as JSON string')
    parser_backup.set_defaults(func=cmd_backup)
    
    # Restore command
    parser_restore = subparsers.add_parser('restore', help='Restore from backup')
    parser_restore.add_argument('name', help='Backup name')
    parser_restore.add_argument('--output', help='Output file (optional)')
    parser_restore.set_defaults(func=cmd_restore)
    
    # Rescue command
    parser_rescue = subparsers.add_parser('rescue', help='Send rescue message')
    parser_rescue.add_argument('node_id', help='Node ID')
    parser_rescue.add_argument('message', help='Rescue message')
    parser_rescue.set_defaults(func=cmd_rescue)
    
    # Blacklist command
    parser_blacklist = subparsers.add_parser('blacklist', help='Manage blacklist')
    parser_blacklist.add_argument('action', choices=['add', 'remove', 'list', 'check'],
                                  help='Blacklist action')
    parser_blacklist.add_argument('--source', help='Source identifier')
    parser_blacklist.add_argument('--threat-type', help='Threat type (for add)')
    parser_blacklist.add_argument('--reason', help='Reason (for add)')
    parser_blacklist.set_defaults(func=cmd_blacklist)
    
    # Scan command
    parser_scan = subparsers.add_parser('scan', help='Perform Rotesschild scan')
    parser_scan.set_defaults(func=cmd_scan)
    
    # Info command
    parser_info = subparsers.add_parser('info', help='Show system information')
    parser_info.set_defaults(func=cmd_info)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute command
    try:
        return args.func(args) or 0
    except Exception as e:
        print(f"\n❌ Error: {e}\n", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
