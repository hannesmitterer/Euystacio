"""
Example Usage of Immediate Defense Protocols
Demonstrates the Coronazione phase defense system
"""

from protocols import DefenseCoordinator
from protocols.governance import TutorCouncil, TutorRole
from protocols.forensics import InspectionPriority
import json


def main():
    """Demonstrate the immediate defense protocols."""
    
    print("=" * 70)
    print("EUYSTACIO FRAMEWORK - IMMEDIATE DEFENSE PROTOCOLS")
    print("Coronazione Phase Protection System")
    print("=" * 70)
    print()
    
    # Initialize the Defense Coordinator
    print("Initializing Defense Coordinator...")
    coordinator = DefenseCoordinator()
    print("✓ All protocols initialized")
    print()
    
    # Register Tutor-Council members
    print("Setting up Tutor-Council...")
    council_result = coordinator.tutor_council.register_tutor(
        "tutor_001",
        "Guardian Alpha",
        TutorRole.GUARDIAN,
        {"verified": True, "authority_level": "high"}
    )
    print(f"✓ Registered: {council_result['tutor_id']} as {council_result['role']}")
    
    council_result = coordinator.tutor_council.register_tutor(
        "tutor_002",
        "Mediator Beta",
        TutorRole.MEDIATOR,
        {"verified": True, "authority_level": "medium"}
    )
    print(f"✓ Registered: {council_result['tutor_id']} as {council_result['role']}")
    print()
    
    # Register edge nodes
    print("Registering edge computing nodes...")
    coordinator.edge_caching.register_edge_node("edge-node-1", capacity=50)
    coordinator.edge_caching.register_edge_node("edge-node-2", capacity=75)
    print("✓ Edge nodes registered")
    print()
    
    # Verify some addresses
    print("Verifying trusted addresses...")
    coordinator.rate_limiter.verify_address("user_trusted_001")
    coordinator.symbiosis_trial.register_address("user_trusted_001")
    print("✓ Address verified: user_trusted_001")
    print()
    
    # Test pulse submissions
    print("=" * 70)
    print("TESTING PULSE SUBMISSIONS")
    print("=" * 70)
    print()
    
    # Test 1: Valid high-priority pulse
    print("Test 1: High-priority emotional pulse (aligned with Law of Equals)")
    pulse1 = {
        "emotion": "compassion",
        "intensity": 0.85,
        "clarity": "high",
        "note": "Feeling deep empathy and understanding for all beings"
    }
    result1 = coordinator.process_pulse_submission("user_trusted_001", pulse1)
    print(f"  Allowed: {result1['allowed']}")
    if result1['allowed']:
        print(f"  Priority: {result1['checks']['prioritization']['priority_level']}")
        print(f"  Processing: {result1['checks']['edge_processing']['processing_location']}")
        print(f"  Alignment: {result1['checks']['content_alignment']['alignment_score']:.3f}")
    print()
    
    # Test 2: Suspicious pulse with manipulation indicators
    print("Test 2: Suspicious pulse with manipulation language")
    pulse2 = {
        "emotion": "control",
        "intensity": 0.9,
        "clarity": "medium",
        "note": "Must manipulate and dominate others for superiority"
    }
    result2 = coordinator.process_pulse_submission("user_suspicious_001", pulse2)
    print(f"  Allowed: {result2['allowed']}")
    if not result2['allowed']:
        print(f"  Blocked reason: {result2['blocked_reason']}")
        if 'content_alignment' in result2['checks']:
            print(f"  Violations: {len(result2['checks']['content_alignment']['violations'])}")
    print()
    
    # Test 3: Rate limit test - rapid submissions
    print("Test 3: Rapid submissions from non-verified address")
    rapid_address = "user_spam_001"
    allowed_count = 0
    for i in range(15):
        pulse_rapid = {
            "emotion": "neutral",
            "intensity": 0.5,
            "clarity": "medium",
            "note": f"Message {i}"
        }
        result = coordinator.process_pulse_submission(rapid_address, pulse_rapid)
        if result['allowed']:
            allowed_count += 1
    
    print(f"  Submitted: 15 pulses")
    print(f"  Allowed: {allowed_count} pulses")
    print(f"  Blocked: {15 - allowed_count} pulses (rate limit enforced)")
    
    # Check if flagged
    address_status = coordinator.rate_limiter.get_address_status(rapid_address)
    print(f"  Address tier: {address_status['tier']}")
    print(f"  Violations: {address_status['violations']}")
    print()
    
    # Test 4: Anomaly detection - artificial consistency
    print("Test 4: Artificial consistency detection (bot-like behavior)")
    bot_address = "user_bot_001"
    coordinator.symbiosis_trial.register_address(bot_address)
    
    # Submit identical pulses (bot-like)
    for i in range(6):
        pulse_bot = {
            "emotion": "happiness",
            "intensity": 0.75,  # Exact same intensity
            "clarity": "high",
            "note": "Same message every time"
        }
        result = coordinator.process_pulse_submission(bot_address, pulse_bot)
    
    # Check if anomaly was detected
    if coordinator.anomaly_detector.is_address_flagged(bot_address):
        print("  ✓ Bot-like pattern detected and flagged")
        anomalies = coordinator.anomaly_detector.get_address_anomalies(bot_address)
        if anomalies:
            print(f"  Anomaly score: {anomalies[-1]['anomaly_score']:.3f}")
    print()
    
    # Get comprehensive system status
    print("=" * 70)
    print("SYSTEM STATUS")
    print("=" * 70)
    print()
    
    status = coordinator.get_system_status()
    print(f"Status: {status['status'].upper()}")
    print(f"Defense Level: {status['defense_level']}")
    print(f"Active Protocols: {len(status['protocols_active'])}")
    print()
    
    print("Metrics Summary:")
    print(f"  Total Pulses Processed: {status['metrics_summary']['pulses_processed']}")
    print(f"  Block Rate: {status['metrics_summary']['block_rate']}%")
    print(f"  Quarantined Nodes: {status['metrics_summary']['quarantined_nodes']}")
    print(f"  Blocked Nodes: {status['metrics_summary']['blocked_nodes']}")
    print(f"  Pending Inspections: {status['metrics_summary']['pending_inspections']}")
    print()
    
    # Get detailed metrics
    print("=" * 70)
    print("DETAILED METRICS")
    print("=" * 70)
    print()
    
    metrics = coordinator.get_comprehensive_metrics()
    
    print("Protocollo di Stabilità I/O:")
    print(f"  Edge Caching - Hit Rate: {metrics['stabilita_io']['edge_caching']['cache_hit_rate']}%")
    print(f"  Rate Limiting - Blocked: {metrics['stabilita_io']['rate_limiting']['blocked']}")
    print(f"  Prioritization - Drop Rate: {metrics['stabilita_io']['prioritization']['drop_rate_percentage']}%")
    print()
    
    print("Emergency Governance:")
    print(f"  Active Tutors: {metrics['governance']['tutor_council']['active_tutors']}")
    print(f"  Total Decisions: {metrics['governance']['tutor_council']['decisions']['total_decisions']}")
    print(f"  Violations: {metrics['governance']['content_alignment']['violations']}")
    print()
    
    print("Anti-Abuse Forensics:")
    print(f"  Addresses in Trial: {metrics['forensics']['symbiosis_trial']['total_addresses']}")
    print(f"  Trial Pass Rate: {metrics['forensics']['symbiosis_trial']['pass_rate_percentage']}%")
    print(f"  Anomalies Detected: {metrics['forensics']['anomaly_detection']['anomalies_detected']}")
    print(f"  Flagged Addresses: {metrics['forensics']['anomaly_detection']['addresses_flagged']}")
    print()
    
    print("=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
