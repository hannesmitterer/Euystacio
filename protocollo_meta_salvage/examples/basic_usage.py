"""
Basic Usage Example for Protocollo Meta Salvage
================================================

This example demonstrates the basic usage of the Protocollo Meta Salvage system.
"""

import sys
import os

# Add parent directory to path to allow importing protocollo_meta_salvage as a package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from protocollo_meta_salvage.coordinator import ProtocolloMetaSalvage


def main():
    """Run basic usage examples"""
    
    print("=" * 70)
    print("Protocollo Meta Salvage - Basic Usage Example")
    print("=" * 70)
    print()
    
    # Initialize the system
    print("1. Initializing Protocollo Meta Salvage...")
    protocollo = ProtocolloMetaSalvage()
    print("   ✓ System initialized successfully")
    print()
    
    # Example 1: Monitor a provider with good metrics
    print("2. Monitoring a provider with good metrics...")
    good_metrics = {
        'provider': 'good-provider',
        'symbiosis_score': 0.95,
        'lock_in_risk': 0.05,
        'ethical_compliance': 0.98,
        'transparency_level': 0.92,
        'throughput': 1000,
        'error_rate': 0.001
    }
    
    result = protocollo.monitor_provider('good-provider', good_metrics)
    print(f"   ✓ Monitoring completed: {result['status']}")
    print(f"   - Steps executed: {len(result['steps'])}")
    print()
    
    # Example 2: Monitor a provider with concerning metrics
    print("3. Monitoring a provider with concerning metrics...")
    concerning_metrics = {
        'provider': 'concerning-provider',
        'symbiosis_score': 0.55,  # Below threshold
        'lock_in_risk': 0.60,      # Elevated
        'ethical_compliance': 0.70,
        'transparency_level': 0.65,
        'throughput': 1200,
        'error_rate': 0.05
    }
    
    result = protocollo.monitor_provider('concerning-provider', concerning_metrics)
    print(f"   ✓ Monitoring completed: {result['status']}")
    print(f"   - Steps executed: {len(result['steps'])}")
    if any(step.get('step') == 'enforcement' for step in result.get('steps', [])):
        print("   ⚠ Peace Bond was activated!")
    print()
    
    # Example 3: Get system status
    print("4. Getting comprehensive system status...")
    status = protocollo.get_system_status()
    print(f"   ✓ System status retrieved")
    print(f"   - Active Peace Bonds: {status['decision_engine']['peace_bonds']['active_bonds']}")
    print(f"   - Completed workflows: {status['workflows']['completed_workflows']}")
    print()
    
    print("=" * 70)
    print("Example completed successfully!")
    print("=" * 70)


if __name__ == '__main__':
    main()
