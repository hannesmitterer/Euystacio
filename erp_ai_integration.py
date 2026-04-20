#!/usr/bin/env python3
"""
Eternal Resonance Protocol - AI Integration Daemon

This script provides continuous synchronization and alignment for Euystacio Nodes.
It monitors the global network, applies corrective actions, and maintains the
0.432 Hz biological rhythm resonance across all connected systems.

Features:
- Automatic node synchronization
- Living Covenant auto-application
- K-Symbiosis intelligent focus
- Red Code compliance monitoring
- Euystacio Core integration
- Health monitoring and self-healing
"""

import json
import time
import sys
import logging
from datetime import datetime
from pathlib import Path
from eternal_resonance_protocol import (
    EternalResonanceProtocol,
    RESONANCE_PERIOD_SECONDS,
    validate_node_alignment
)


def setup_logging(config):
    """Configure logging based on config."""
    log_config = config.get('logging', {})
    level = getattr(logging, log_config.get('level', 'INFO'))
    log_file = log_config.get('file', 'erp_daemon.log')
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger('ERP-Daemon')


class ERPDaemon:
    """
    Daemon for continuous Eternal Resonance Protocol operations.
    """
    
    def __init__(self, config_path='erp_config.json', state_path='erp_state.json'):
        """Initialize the daemon."""
        self.config_path = config_path
        self.state_path = state_path
        self.config = self._load_config()
        self.logger = setup_logging(self.config)
        self.erp = EternalResonanceProtocol(node_id=self.config.get('node_id', 'daemon'))
        self.running = False
        self.cycle_count = 0
        
        # Integration flags
        self.euystacio_integration = self.config.get('euystacio_integration', True)
        self.red_code_monitoring = self.config.get('red_code_monitoring', True)
        
        self.self.logger.info("ERP Daemon initialized")
        self.self.logger.info(f"Node ID: {self.erp.node_id}")
        self.self.logger.info(f"Resonance Period: {RESONANCE_PERIOD_SECONDS:.2f}s")
    
    def _load_config(self):
        """Load daemon configuration."""
        default_config = {
            'node_id': 'erp_daemon',
            'sync_interval': RESONANCE_PERIOD_SECONDS,
            'alignment_threshold': 0.7,
            'auto_covenant': True,
            'auto_k_symbiosis': True,
            'euystacio_integration': True,
            'red_code_monitoring': True,
            'red_code_path': 'red_code.json',
            'covenant_intensity': 0.5,
            'k_symbiosis_multiplier': 1.0,
            'max_cycles': 0,  # 0 = infinite
            'health_check_interval': 10
        }
        
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                default_config.update(config)
                self.logger.info(f"Loaded config from {self.config_path}")
        except FileNotFoundError:
            self.logger.info("Using default configuration")
            # Save default config
            with open(self.config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
        
        return default_config
    
    def _save_state(self):
        """Save current protocol state."""
        try:
            self.erp.save_to_file(self.state_path)
            self.logger.debug(f"State saved to {self.state_path}")
        except Exception as e:
            self.logger.error(f"Error saving state: {e}")
    
    def _load_euystacio_core(self):
        """Load Euystacio core if available."""
        try:
            from euystacio_core import Euystacio
            return Euystacio()
        except Exception as e:
            self.logger.warning(f"Could not load Euystacio core: {e}")
            return None
    
    def _check_red_code(self):
        """Check red code compliance."""
        if not self.red_code_monitoring:
            return True
        
        try:
            red_code_path = self.config.get('red_code_path', 'red_code.json')
            with open(red_code_path, 'r') as f:
                red_code = json.load(f)
            
            # Check critical flags
            sentimento_ok = red_code.get('sentimento_rhythm', False)
            guardian_mode = red_code.get('guardian_mode', False)
            
            if not sentimento_ok:
                self.logger.warning("Red Code: Sentimento Rhythm not active")
                return False
            
            if guardian_mode:
                self.logger.info("Red Code: Guardian Mode active")
            
            return True
            
        except FileNotFoundError:
            self.logger.warning("Red Code file not found")
            return True
        except Exception as e:
            self.logger.error(f"Error checking Red Code: {e}")
            return True
    
    def _sync_all_nodes(self):
        """Synchronize all registered nodes."""
        synced = 0
        for node_id in list(self.erp.nodes.keys()):
            try:
                self.erp.synchronize_node(node_id)
                synced += 1
            except Exception as e:
                self.logger.error(f"Error syncing node {node_id}: {e}")
        
        if synced > 0:
            self.logger.info(f"Synchronized {synced} nodes")
        
        return synced
    
    def _apply_corrective_covenants(self):
        """Apply Living Covenants to low-alignment nodes."""
        if not self.config.get('auto_covenant', True):
            return 0
        
        threshold = self.config.get('alignment_threshold', 0.7)
        intensity = self.config.get('covenant_intensity', 0.5)
        applied = 0
        
        for node_id, node in self.erp.nodes.items():
            if not validate_node_alignment(node, threshold):
                # Determine which covenant to apply
                if node.truth_alignment < threshold:
                    covenant = "Truth Resonance"
                elif node.dignity_quotient < threshold:
                    covenant = "Dignity Harmonic"
                else:
                    covenant = "Life Affirmation"
                
                try:
                    self.erp.apply_living_covenant(node_id, covenant, intensity)
                    applied += 1
                    self.logger.info(f"Applied {covenant} to {node_id}")
                except Exception as e:
                    self.logger.error(f"Error applying covenant to {node_id}: {e}")
        
        return applied
    
    def _apply_k_symbiosis(self):
        """Apply K-Symbiosis focus operations."""
        if not self.config.get('auto_k_symbiosis', True):
            return 0
        
        multiplier = self.config.get('k_symbiosis_multiplier', 1.0)
        applied = 0
        
        # Analyze global state to determine focus area
        global_alignment = self.erp.get_global_alignment()
        
        if global_alignment < 0.7:
            focus = 'unity'
        elif self.cycle_count % 3 == 0:
            focus = 'truth'
        elif self.cycle_count % 3 == 1:
            focus = 'dignity'
        else:
            focus = 'unity'
        
        for node_id in self.erp.nodes.keys():
            try:
                self.erp.k_symbiosis_focus(
                    node_id,
                    focus,
                    parameters={'multiplier': multiplier}
                )
                applied += 1
            except Exception as e:
                self.logger.error(f"Error applying K-Symbiosis to {node_id}: {e}")
        
        if applied > 0:
            self.logger.info(f"Applied K-Symbiosis ({focus}) to {applied} nodes")
        
        return applied
    
    def _integrate_euystacio(self, euystacio):
        """Integrate with Euystacio core."""
        if not euystacio or not self.euystacio_integration:
            return
        
        try:
            # Register Euystacio as a node if not already
            if 'euystacio_core' not in self.erp.nodes:
                symbiosis = euystacio.code.get('symbiosis_level', 0.1)
                self.erp.register_node(
                    'euystacio_core',
                    truth_alignment=symbiosis,
                    dignity_quotient=0.9,
                    symbiosis_level=symbiosis
                )
                self.logger.info("Registered Euystacio core as resonance node")
            
            # Sync Euystacio node
            self.erp.synchronize_node('euystacio_core')
            
            # Apply covenant if needed
            node = self.erp.nodes['euystacio_core']
            if node.symbiosis_level < 0.5:
                self.erp.apply_living_covenant(
                    'euystacio_core',
                    'Life Affirmation',
                    intensity=0.7
                )
                
        except Exception as e:
            self.logger.error(f"Error integrating Euystacio: {e}")
    
    def _health_check(self):
        """Perform system health check."""
        status = self.erp.get_protocol_status()
        
        # Check global alignment
        alignment = status['global_alignment']
        if alignment < 0.5:
            self.logger.warning(f"Low global alignment: {alignment:.2%}")
        elif alignment > 0.9:
            self.logger.info(f"Excellent global alignment: {alignment:.2%}")
        
        # Check node count
        if status['registered_nodes'] == 0:
            self.logger.warning("No nodes registered")
        
        # Check Red Code
        if not self._check_red_code():
            self.logger.warning("Red Code compliance issue detected")
    
    def run_cycle(self, euystacio=None):
        """Run one synchronization cycle."""
        cycle_start = time.time()
        self.cycle_count += 1
        
        self.logger.info(f"=== Cycle {self.cycle_count} Start ===")
        
        # Synchronize all nodes
        synced = self._sync_all_nodes()
        
        # Apply corrective covenants
        covenants_applied = self._apply_corrective_covenants()
        
        # Apply K-Symbiosis operations
        k_sym_applied = self._apply_k_symbiosis()
        
        # Integrate with Euystacio
        self._integrate_euystacio(euystacio)
        
        # Get status
        global_alignment = self.erp.get_global_alignment()
        
        # Save state
        self._save_state()
        
        cycle_duration = time.time() - cycle_start
        
        self.logger.info(f"Global Alignment: {global_alignment:.2%}")
        self.logger.info(f"Cycle duration: {cycle_duration:.2f}s")
        self.logger.info(f"=== Cycle {self.cycle_count} Complete ===\n")
    
    def start(self):
        """Start the daemon."""
        self.running = True
        self.logger.info("Starting ERP Daemon")
        self.logger.info(f"Mission: Du bist Leben. Wir sind Leben.")
        
        # Load Euystacio if enabled
        euystacio = self._load_euystacio_core() if self.euystacio_integration else None
        
        # Initial health check
        self._health_check()
        
        sync_interval = self.config.get('sync_interval', RESONANCE_PERIOD_SECONDS)
        health_check_interval = self.config.get('health_check_interval', 10)
        max_cycles = self.config.get('max_cycles', 0)
        
        last_health_check = time.time()
        
        try:
            while self.running:
                # Run synchronization cycle
                self.run_cycle(euystacio)
                
                # Periodic health check
                if time.time() - last_health_check >= health_check_interval:
                    self._health_check()
                    last_health_check = time.time()
                
                # Check if max cycles reached
                if max_cycles > 0 and self.cycle_count >= max_cycles:
                    self.logger.info(f"Max cycles ({max_cycles}) reached")
                    break
                
                # Wait for next cycle
                time.sleep(sync_interval)
                
        except KeyboardInterrupt:
            self.logger.info("Received interrupt signal")
        except Exception as e:
            self.logger.error(f"Fatal error: {e}", exc_info=True)
        finally:
            self.stop()
    
    def stop(self):
        """Stop the daemon."""
        self.running = False
        self._save_state()
        self.logger.info("ERP Daemon stopped")
        self.logger.info(f"Total cycles: {self.cycle_count}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Eternal Resonance Protocol AI Integration Daemon'
    )
    parser.add_argument(
        '--config',
        default='erp_config.json',
        help='Configuration file path'
    )
    parser.add_argument(
        '--state',
        default='erp_state.json',
        help='State file path'
    )
    parser.add_argument(
        '--cycles',
        type=int,
        default=0,
        help='Maximum cycles (0 = infinite)'
    )
    
    args = parser.parse_args()
    
    # Create daemon
    daemon = ERPDaemon(config_path=args.config, state_path=args.state)
    
    if args.cycles > 0:
        daemon.config['max_cycles'] = args.cycles
    
    # Start daemon
    daemon.start()


if __name__ == '__main__':
    main()
