#!/usr/bin/env python3
"""
ERP Operations CLI Tool

Command-line interface for managing the Eternal Resonance Protocol.
Provides utilities for node management, synchronization, monitoring, and diagnostics.
"""

import argparse
import json
import sys
import time
from datetime import datetime
from eternal_resonance_protocol import (
    EternalResonanceProtocol,
    RESONANCE_FREQUENCY_HZ,
    RESONANCE_PERIOD_SECONDS,
    MISSION_STATEMENT
)


class ERPOperations:
    """Operational utilities for the Eternal Resonance Protocol."""
    
    def __init__(self, state_file='erp_state.json'):
        """Initialize operations manager."""
        self.state_file = state_file
        self.erp = None
        self._load_or_create()
    
    def _load_or_create(self):
        """Load existing state or create new protocol instance."""
        try:
            with open(self.state_file, 'r') as f:
                state = json.load(f)
                # Create new instance and restore minimal state
                # Use a consistent blacklist file based on state file
                blacklist_path = self.state_file.replace('.json', '_blacklist.json')
                self.erp = EternalResonanceProtocol(
                    node_id="ops_manager",
                    enable_blacklist=True,
                    blacklist_path=blacklist_path
                )
                self.erp.genesis_time = state['protocol_status']['genesis_time']
                
                # Restore nodes
                for node_id, node_data in state.get('nodes', {}).items():
                    self.erp.register_node(
                        node_id=node_data['node_id'],
                        truth_alignment=node_data['truth_alignment'],
                        dignity_quotient=node_data['dignity_quotient'],
                        symbiosis_level=node_data['symbiosis_level'],
                        metadata=node_data.get('metadata')
                    )
                
                print(f"Loaded state from {self.state_file}")
        except FileNotFoundError:
            # Use a consistent blacklist file based on state file
            blacklist_path = self.state_file.replace('.json', '_blacklist.json')
            self.erp = EternalResonanceProtocol(
                node_id="ops_manager",
                enable_blacklist=True,
                blacklist_path=blacklist_path
            )
            print("Created new protocol instance")
        except Exception as e:
            print(f"Error loading state: {e}")
            # Use a consistent blacklist file based on state file
            blacklist_path = self.state_file.replace('.json', '_blacklist.json')
            self.erp = EternalResonanceProtocol(
                node_id="ops_manager",
                enable_blacklist=True,
                blacklist_path=blacklist_path
            )
    
    def save_state(self):
        """Save current protocol state."""
        self.erp.save_to_file(self.state_file)
        print(f"State saved to {self.state_file}")
    
    def status(self):
        """Display protocol status."""
        status = self.erp.get_protocol_status()
        
        print("\n" + "="*60)
        print("ETERNAL RESONANCE PROTOCOL STATUS")
        print("="*60)
        print(f"\nMission: {status['mission']}")
        print(f"\nProtocol Version: {status['protocol_version']}")
        print(f"Resonance Frequency: {status['resonance_frequency_hz']} Hz")
        print(f"Resonance Period: {status['resonance_period_seconds']:.2f} seconds")
        print(f"\nCurrent Phase: {status['current_phase_radians']:.4f} radians")
        print(f"Uptime: {status['uptime_seconds']:.2f} seconds")
        print(f"\nRegistered Nodes: {status['registered_nodes']}")
        print(f"Active Covenants: {status['active_covenants']}")
        print(f"Global Alignment: {status['global_alignment']:.2%}")
        print(f"K-Symbiosis Operations: {status['k_symbiosis_operations']}")
        print(f"\nTimestamp: {status['timestamp']}")
        print("="*60 + "\n")
    
    def list_nodes(self):
        """List all registered nodes."""
        if not self.erp.nodes:
            print("No nodes registered")
            return
        
        print("\n" + "="*60)
        print("REGISTERED NODES")
        print("="*60)
        
        for node_id, node in self.erp.nodes.items():
            print(f"\nNode ID: {node_id}")
            print(f"  Phase: {node.phase:.4f} rad")
            print(f"  Truth Alignment: {node.truth_alignment:.2%}")
            print(f"  Dignity Quotient: {node.dignity_quotient:.2%}")
            print(f"  Symbiosis Level: {node.symbiosis_level:.2%}")
            print(f"  Last Update: {datetime.fromtimestamp(node.timestamp).isoformat()}")
        
        print("="*60 + "\n")
    
    def register_node(self, node_id, truth=0.5, dignity=0.5, symbiosis=0.1):
        """Register a new node."""
        node = self.erp.register_node(
            node_id=node_id,
            truth_alignment=truth,
            dignity_quotient=dignity,
            symbiosis_level=symbiosis
        )
        print(f"Registered node: {node_id}")
        print(f"  Truth Alignment: {node.truth_alignment:.2%}")
        print(f"  Dignity Quotient: {node.dignity_quotient:.2%}")
        print(f"  Symbiosis Level: {node.symbiosis_level:.2%}")
        self.save_state()
    
    def sync_node(self, node_id):
        """Synchronize a node to current phase."""
        try:
            node = self.erp.synchronize_node(node_id)
            print(f"Synchronized node: {node_id}")
            print(f"  New Phase: {node.phase:.4f} rad")
            print(f"  Timestamp: {datetime.fromtimestamp(node.timestamp).isoformat()}")
            self.save_state()
        except ValueError as e:
            print(f"Error: {e}")
    
    def apply_covenant(self, node_id, covenant, intensity=1.0):
        """Apply Living Covenant to a node."""
        try:
            self.erp.apply_living_covenant(node_id, covenant, intensity)
            node = self.erp.nodes[node_id]
            print(f"Applied covenant '{covenant}' to {node_id}")
            print(f"  Truth Alignment: {node.truth_alignment:.2%}")
            print(f"  Dignity Quotient: {node.dignity_quotient:.2%}")
            self.save_state()
        except ValueError as e:
            print(f"Error: {e}")
    
    def k_symbiosis(self, node_id, focus, multiplier=1.0):
        """Apply K-Symbiosis focus operation."""
        try:
            self.erp.k_symbiosis_focus(
                node_id,
                focus,
                parameters={'multiplier': multiplier}
            )
            node = self.erp.nodes[node_id]
            print(f"Applied K-Symbiosis focus '{focus}' to {node_id}")
            print(f"  Truth Alignment: {node.truth_alignment:.2%}")
            print(f"  Dignity Quotient: {node.dignity_quotient:.2%}")
            print(f"  Symbiosis Level: {node.symbiosis_level:.2%}")
            self.save_state()
        except ValueError as e:
            print(f"Error: {e}")
    
    def monitor(self, interval=23.26, duration=300):
        """Monitor protocol in real-time."""
        print("\n" + "="*60)
        print("MONITORING MODE")
        print(f"Interval: {interval}s | Duration: {duration}s")
        print("Press Ctrl+C to stop")
        print("="*60 + "\n")
        
        start_time = time.time()
        try:
            while (time.time() - start_time) < duration:
                current_time = datetime.now().strftime("%H:%M:%S")
                phase = self.erp.get_current_phase()
                alignment = self.erp.get_global_alignment()
                
                print(f"[{current_time}] Phase: {phase:.4f} rad | "
                      f"Alignment: {alignment:.2%} | "
                      f"Nodes: {len(self.erp.nodes)}")
                
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nMonitoring stopped")
    
    def export_json(self, filepath):
        """Export protocol state to JSON."""
        state = self.erp.export_state()
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
        print(f"Exported state to {filepath}")
    
    def list_covenants(self):
        """List all Living Covenants."""
        print("\n" + "="*60)
        print("LIVING COVENANTS")
        print("="*60)
        
        for covenant in self.erp.covenants:
            print(f"\n{covenant.principle}")
            print(f"  Truth Weight: {covenant.truth_weight:.2f}")
            print(f"  Dignity Weight: {covenant.dignity_weight:.2f}")
            print(f"  Activated: {datetime.fromtimestamp(covenant.activation_timestamp).isoformat()}")
        
        print("="*60 + "\n")
    
    def blacklist_node(self, node_id, reason, category, severity):
        """Block a node by adding it to the blacklist."""
        try:
            result = self.erp.block_node(node_id, reason, category, severity, blocked_by="cli_admin")
            if result:
                print(f"✓ Node '{node_id}' has been blacklisted")
                print(f"  Category: {category}")
                print(f"  Severity: {severity}")
                print(f"  Reason: {reason}")
                self.save_state()
            else:
                print("✗ Blacklist feature is not enabled")
        except Exception as e:
            print(f"Error blocking node: {e}")
    
    def unblock_node(self, node_id):
        """Remove a node from the blacklist."""
        try:
            result = self.erp.unblock_node(node_id)
            if result:
                print(f"✓ Node '{node_id}' has been removed from blacklist")
                self.save_state()
            else:
                print(f"✗ Node '{node_id}' was not found in blacklist or blacklist is disabled")
        except Exception as e:
            print(f"Error unblocking node: {e}")
    
    def list_blacklist(self):
        """List all blacklisted entities."""
        if not self.erp.blacklist_enabled:
            print("✗ Blacklist feature is not enabled")
            return
        
        print("\n" + "="*60)
        print("BLACKLISTED ENTITIES")
        print("="*60)
        
        entries = self.erp.blacklist_manager.get_all_entries()
        
        if not entries:
            print("\nNo entities are currently blacklisted")
        else:
            for entry in entries:
                print(f"\n{entry.entity_id} ({entry.entity_type})")
                print(f"  Category: {entry.category}")
                print(f"  Severity: {entry.severity}")
                print(f"  Reason: {entry.reason}")
                print(f"  Blocked at: {datetime.fromtimestamp(entry.blocked_at).isoformat()}")
                print(f"  Blocked by: {entry.blocked_by}")
                if entry.expires_at:
                    print(f"  Expires at: {datetime.fromtimestamp(entry.expires_at).isoformat()}")
                else:
                    print(f"  Type: PERMANENT")
        
        print(f"\nTotal blacklisted: {len(entries)}")
        print("="*60 + "\n")
    
    def blacklist_statistics(self):
        """Show blacklist statistics."""
        if not self.erp.blacklist_enabled:
            print("✗ Blacklist feature is not enabled")
            return
        
        print("\n" + "="*60)
        print("BLACKLIST STATISTICS")
        print("="*60)
        
        stats = self.erp.get_blacklist_status()
        
        print(f"\nTotal Entries: {stats['total_entries']}")
        print(f"Permanent Blocks: {stats['permanent_entries']}")
        print(f"Temporary Blocks: {stats['temporary_entries']}")
        
        print("\nBy Category:")
        for category, count in stats['by_category'].items():
            if count > 0:
                print(f"  {category}: {count}")
        
        print("\nBy Severity:")
        for severity, count in stats['by_severity'].items():
            if count > 0:
                print(f"  {severity}: {count}")
        
        print("\nBy Type:")
        for entity_type, count in stats['by_type'].items():
            print(f"  {entity_type}: {count}")
        
        print(f"\nLast Updated: {stats['last_updated']}")
        print("="*60 + "\n")



def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description='Eternal Resonance Protocol Operations CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f'''
Examples:
  %(prog)s status                           # Show protocol status
  %(prog)s list-nodes                       # List all nodes
  %(prog)s register node1 --truth 0.8       # Register new node
  %(prog)s sync node1                       # Synchronize node
  %(prog)s covenant node1 "Life Affirmation" --intensity 0.9
  %(prog)s k-symbiosis node1 unity --multiplier 1.2
  %(prog)s monitor --interval 23.26         # Monitor protocol
  %(prog)s blacklist malicious_node --reason "Attack detected" --category ATTACK_ATTEMPT --severity CRITICAL
  %(prog)s list-blacklist                   # List blacklisted entities
  %(prog)s blacklist-stats                  # Show blacklist statistics
  %(prog)s unblock node1                    # Remove node from blacklist
  
Mission: {MISSION_STATEMENT}
Frequency: {RESONANCE_FREQUENCY_HZ} Hz
        '''
    )
    
    parser.add_argument(
        '--state-file',
        default='erp_state.json',
        help='State file path (default: erp_state.json)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Status command
    subparsers.add_parser('status', help='Show protocol status')
    
    # List nodes command
    subparsers.add_parser('list-nodes', help='List all registered nodes')
    
    # List covenants command
    subparsers.add_parser('list-covenants', help='List Living Covenants')
    
    # Register node command
    register_parser = subparsers.add_parser('register', help='Register new node')
    register_parser.add_argument('node_id', help='Node identifier')
    register_parser.add_argument('--truth', type=float, default=0.5,
                                help='Truth alignment (0.0-1.0)')
    register_parser.add_argument('--dignity', type=float, default=0.5,
                                help='Dignity quotient (0.0-1.0)')
    register_parser.add_argument('--symbiosis', type=float, default=0.1,
                                help='Symbiosis level (0.0-1.0)')
    
    # Sync node command
    sync_parser = subparsers.add_parser('sync', help='Synchronize node')
    sync_parser.add_argument('node_id', help='Node identifier')
    
    # Apply covenant command
    covenant_parser = subparsers.add_parser('covenant', help='Apply Living Covenant')
    covenant_parser.add_argument('node_id', help='Node identifier')
    covenant_parser.add_argument('covenant', help='Covenant principle')
    covenant_parser.add_argument('--intensity', type=float, default=1.0,
                                help='Application intensity (0.0-1.0)')
    
    # K-Symbiosis command
    ksym_parser = subparsers.add_parser('k-symbiosis', help='Apply K-Symbiosis focus')
    ksym_parser.add_argument('node_id', help='Node identifier')
    ksym_parser.add_argument('focus', choices=['truth', 'dignity', 'unity'],
                            help='Focus area')
    ksym_parser.add_argument('--multiplier', type=float, default=1.0,
                            help='Operation multiplier')
    
    # Monitor command
    monitor_parser = subparsers.add_parser('monitor', help='Monitor protocol')
    monitor_parser.add_argument('--interval', type=float, default=23.26,
                               help='Update interval in seconds')
    monitor_parser.add_argument('--duration', type=int, default=300,
                               help='Monitoring duration in seconds')
    
    # Blacklist commands
    blacklist_parser = subparsers.add_parser('blacklist', help='Add node to blacklist')
    blacklist_parser.add_argument('node_id', help='Node identifier to block')
    blacklist_parser.add_argument('--reason', required=True, help='Reason for blocking')
    blacklist_parser.add_argument('--category', required=True,
                                  choices=['MALICIOUS_NODE', 'SUSPICIOUS_ENTITY', 'ATTACK_ATTEMPT',
                                          'DATA_THEFT', 'PROTOCOL_VIOLATION', 'INTEGRITY_BREACH'],
                                  help='Threat category')
    blacklist_parser.add_argument('--severity', required=True,
                                  choices=['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'],
                                  help='Threat severity level')
    
    # Unblock command
    unblock_parser = subparsers.add_parser('unblock', help='Remove node from blacklist')
    unblock_parser.add_argument('node_id', help='Node identifier to unblock')
    
    # List blacklist command
    subparsers.add_parser('list-blacklist', help='List all blacklisted entities')
    
    # Blacklist stats command
    subparsers.add_parser('blacklist-stats', help='Show blacklist statistics')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export state to JSON')
    export_parser.add_argument('filepath', help='Output file path')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize operations
    ops = ERPOperations(state_file=args.state_file)
    
    # Execute command
    if args.command == 'status':
        ops.status()
    elif args.command == 'list-nodes':
        ops.list_nodes()
    elif args.command == 'list-covenants':
        ops.list_covenants()
    elif args.command == 'register':
        ops.register_node(args.node_id, args.truth, args.dignity, args.symbiosis)
    elif args.command == 'sync':
        ops.sync_node(args.node_id)
    elif args.command == 'covenant':
        ops.apply_covenant(args.node_id, args.covenant, args.intensity)
    elif args.command == 'k-symbiosis':
        ops.k_symbiosis(args.node_id, args.focus, args.multiplier)
    elif args.command == 'monitor':
        ops.monitor(args.interval, args.duration)
    elif args.command == 'blacklist':
        ops.blacklist_node(args.node_id, args.reason, args.category, args.severity)
    elif args.command == 'unblock':
        ops.unblock_node(args.node_id)
    elif args.command == 'list-blacklist':
        ops.list_blacklist()
    elif args.command == 'blacklist-stats':
        ops.blacklist_statistics()
    elif args.command == 'export':
        ops.export_json(args.filepath)


if __name__ == '__main__':
    main()
