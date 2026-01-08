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
                self.erp = EternalResonanceProtocol(node_id="ops_manager")
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
            self.erp = EternalResonanceProtocol(node_id="ops_manager")
            print("Created new protocol instance")
        except Exception as e:
            print(f"Error loading state: {e}")
            self.erp = EternalResonanceProtocol(node_id="ops_manager")
    
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
    elif args.command == 'export':
        ops.export_json(args.filepath)


if __name__ == '__main__':
    main()
