"""
Triple-Sign Pact: Seedbringer Identity Hardening
=================================================

Implements the Triple-Sign Pact for anchoring Seedbringer Identity across
at least 3 IPFS shards with geographic distribution verification and
automatic synchronization.

This module provides:
- IPFS shard anchoring (minimum 3 shards)
- Geographic distribution verification
- Automatic shard synchronization
- Identity backup and recovery mechanisms

Protocol: EUYSTACIO / NSR  
Status: Allerta Livello 2 (Active Monitoring)
Date: 20 Gennaio 2026
"""

import json
import hashlib
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import random


# Core Constants
MIN_SHARD_COUNT = 3  # Minimum number of IPFS shards required
SYNC_INTERVAL_SECONDS = 300  # 5 minutes
GEOGRAPHIC_REGIONS = ["EU", "NA", "ASIA", "SA", "OCEANIA", "AFRICA"]


@dataclass
class IPFSShard:
    """Represents an IPFS shard containing Seedbringer Identity data."""
    shard_id: str
    ipfs_hash: str
    region: str
    timestamp: float
    size_bytes: int
    checksum: str
    metadata: Optional[Dict] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)
    
    def verify_checksum(self, data: bytes) -> bool:
        """Verify data integrity using checksum."""
        computed = hashlib.sha256(data).hexdigest()
        return computed == self.checksum


@dataclass
class SeedbringerIdentity:
    """Seedbringer Identity data structure."""
    identity_id: str
    public_key: str
    creation_timestamp: float
    version: str
    attributes: Dict
    signatures: List[str]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)
    
    def to_bytes(self) -> bytes:
        """Convert to bytes for storage."""
        return json.dumps(self.to_dict(), sort_keys=True).encode('utf-8')
    
    def compute_hash(self) -> str:
        """Compute hash of identity data."""
        return hashlib.sha256(self.to_bytes()).hexdigest()


class IPFSShardManager:
    """
    Simulates IPFS shard management.
    In production, this would interface with actual IPFS nodes.
    """
    
    def __init__(self):
        """Initialize IPFS shard manager."""
        self.shards: Dict[str, bytes] = {}
        self.shard_metadata: Dict[str, IPFSShard] = {}
    
    def upload_shard(self, data: bytes, region: str, metadata: Optional[Dict] = None) -> IPFSShard:
        """
        Simulate uploading data to IPFS.
        
        Args:
            data: Data to upload
            region: Geographic region for the shard
            metadata: Optional metadata
            
        Returns:
            IPFSShard object
            
        Note:
            In production, this would interface with actual IPFS nodes.
            The simulated hash uses CIDv0 format (Qm prefix) for compatibility.
        """
        # Generate simulated IPFS hash (CIDv0 format with Qm prefix)
        # Real IPFS hashes vary by version and hash function
        hash_data = data + str(time.time()).encode() + region.encode()
        ipfs_hash = "Qm" + hashlib.sha256(hash_data).hexdigest()[:44]
        shard_id = f"{region}_{int(time.time())}_{random.randint(1000, 9999)}"
        checksum = hashlib.sha256(data).hexdigest()
        
        shard = IPFSShard(
            shard_id=shard_id,
            ipfs_hash=ipfs_hash,
            region=region,
            timestamp=time.time(),
            size_bytes=len(data),
            checksum=checksum,
            metadata=metadata
        )
        
        # Store shard
        self.shards[ipfs_hash] = data
        self.shard_metadata[ipfs_hash] = shard
        
        return shard
    
    def download_shard(self, ipfs_hash: str) -> Optional[bytes]:
        """
        Simulate downloading data from IPFS.
        
        Args:
            ipfs_hash: IPFS hash to download
            
        Returns:
            Shard data or None
        """
        return self.shards.get(ipfs_hash)
    
    def verify_shard(self, ipfs_hash: str) -> bool:
        """
        Verify shard integrity.
        
        Args:
            ipfs_hash: IPFS hash to verify
            
        Returns:
            True if shard is valid
        """
        data = self.shards.get(ipfs_hash)
        shard = self.shard_metadata.get(ipfs_hash)
        
        if not data or not shard:
            return False
        
        return shard.verify_checksum(data)


class TripleSignPact:
    """
    Main Triple-Sign Pact implementation for Seedbringer Identity hardening.
    
    Ensures that Seedbringer Identity is anchored across at least 3 IPFS shards
    with geographic distribution and automatic synchronization.
    """
    
    def __init__(self, identity_id: str = "seedbringer_primary"):
        """
        Initialize Triple-Sign Pact system.
        
        Args:
            identity_id: Unique identifier for Seedbringer Identity
        """
        self.identity_id = identity_id
        self.ipfs_manager = IPFSShardManager()
        self.active_shards: List[IPFSShard] = []
        self.identity: Optional[SeedbringerIdentity] = None
        self.last_sync = time.time()
        
    def create_identity(self, public_key: str, attributes: Dict) -> SeedbringerIdentity:
        """
        Create a new Seedbringer Identity.
        
        Args:
            public_key: Public cryptographic key
            attributes: Identity attributes
            
        Returns:
            SeedbringerIdentity object
        """
        identity = SeedbringerIdentity(
            identity_id=self.identity_id,
            public_key=public_key,
            creation_timestamp=time.time(),
            version="1.0.0",
            attributes=attributes,
            signatures=[]
        )
        
        self.identity = identity
        return identity
    
    def anchor_identity(self, regions: Optional[List[str]] = None) -> List[IPFSShard]:
        """
        Anchor Seedbringer Identity to IPFS shards.
        
        Args:
            regions: Target regions for shards (default: auto-select)
            
        Returns:
            List of created shards
        """
        if not self.identity:
            raise ValueError("No identity to anchor. Call create_identity first.")
        
        # Select regions for geographic distribution
        if not regions:
            regions = self._select_regions()
        
        if len(regions) < MIN_SHARD_COUNT:
            raise ValueError(f"At least {MIN_SHARD_COUNT} regions required")
        
        # Prepare identity data
        identity_data = self.identity.to_bytes()
        
        # Upload to each region
        shards = []
        for region in regions:
            shard = self.ipfs_manager.upload_shard(
                data=identity_data,
                region=region,
                metadata={
                    "identity_id": self.identity_id,
                    "purpose": "seedbringer_identity_anchor",
                    "version": self.identity.version
                }
            )
            shards.append(shard)
        
        self.active_shards = shards
        self.last_sync = time.time()
        
        return shards
    
    def _select_regions(self) -> List[str]:
        """
        Automatically select regions for geographic distribution.
        
        Returns:
            List of selected regions
        """
        # Select 3 well-distributed regions
        preferred_regions = ["EU", "NA", "ASIA"]
        
        # Add random selection if more needed
        available = [r for r in GEOGRAPHIC_REGIONS if r not in preferred_regions]
        if len(preferred_regions) < MIN_SHARD_COUNT:
            needed = MIN_SHARD_COUNT - len(preferred_regions)
            preferred_regions.extend(random.sample(available, min(needed, len(available))))
        
        return preferred_regions
    
    def verify_geographic_distribution(self) -> Dict:
        """
        Verify that shards are properly distributed geographically.
        
        Returns:
            Verification results
        """
        results = {
            "total_shards": len(self.active_shards),
            "minimum_required": MIN_SHARD_COUNT,
            "regions": {},
            "distribution_valid": False,
            "unique_regions": 0
        }
        
        # Count shards per region
        for shard in self.active_shards:
            if shard.region not in results["regions"]:
                results["regions"][shard.region] = 0
            results["regions"][shard.region] += 1
        
        results["unique_regions"] = len(results["regions"])
        
        # Verify distribution
        results["distribution_valid"] = (
            results["total_shards"] >= MIN_SHARD_COUNT and
            results["unique_regions"] >= MIN_SHARD_COUNT
        )
        
        return results
    
    def sync_shards(self) -> Dict:
        """
        Synchronize shards to ensure consistency.
        
        Returns:
            Synchronization results
        """
        results = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "shards_checked": 0,
            "shards_valid": 0,
            "shards_invalid": 0,
            "sync_actions": []
        }
        
        if not self.identity:
            results["sync_actions"].append("No identity to sync")
            return results
        
        # Check each shard
        for shard in self.active_shards:
            results["shards_checked"] += 1
            
            # Verify shard integrity
            if self.ipfs_manager.verify_shard(shard.ipfs_hash):
                results["shards_valid"] += 1
                results["sync_actions"].append(f"✓ Shard {shard.shard_id} verified")
            else:
                results["shards_invalid"] += 1
                results["sync_actions"].append(f"✗ Shard {shard.shard_id} failed verification")
                
                # Re-upload failed shard
                new_shard = self.ipfs_manager.upload_shard(
                    data=self.identity.to_bytes(),
                    region=shard.region,
                    metadata=shard.metadata
                )
                results["sync_actions"].append(f"↻ Re-uploaded to region {shard.region}")
                
                # Update shard reference
                idx = self.active_shards.index(shard)
                self.active_shards[idx] = new_shard
        
        self.last_sync = time.time()
        return results
    
    def detect_shard_changes(self) -> List[Dict]:
        """
        Detect changes in shards that require re-synchronization.
        
        Returns:
            List of detected changes
        """
        changes = []
        
        if not self.identity:
            return changes
        
        expected_hash = self.identity.compute_hash()
        
        for shard in self.active_shards:
            data = self.ipfs_manager.download_shard(shard.ipfs_hash)
            if data:
                actual_hash = hashlib.sha256(data).hexdigest()
                if actual_hash != expected_hash:
                    changes.append({
                        "shard_id": shard.shard_id,
                        "region": shard.region,
                        "expected_hash": expected_hash,
                        "actual_hash": actual_hash,
                        "action_required": "resync"
                    })
        
        return changes
    
    def auto_heal_shards(self) -> Dict:
        """
        Automatically heal shards based on detected issues.
        
        Returns:
            Healing results
        """
        results = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "changes_detected": 0,
            "shards_healed": 0,
            "actions": []
        }
        
        # Detect changes
        changes = self.detect_shard_changes()
        results["changes_detected"] = len(changes)
        
        # Heal each detected issue
        for change in changes:
            # Find shard by ID
            shard = next((s for s in self.active_shards if s.shard_id == change["shard_id"]), None)
            if shard:
                # Re-upload
                new_shard = self.ipfs_manager.upload_shard(
                    data=self.identity.to_bytes(),
                    region=shard.region,
                    metadata=shard.metadata
                )
                
                # Update reference
                idx = self.active_shards.index(shard)
                self.active_shards[idx] = new_shard
                
                results["shards_healed"] += 1
                results["actions"].append(f"Healed shard {shard.shard_id} in region {shard.region}")
        
        return results
    
    def get_status(self) -> Dict:
        """
        Get comprehensive status of Triple-Sign Pact system.
        
        Returns:
            Status dictionary
        """
        distribution = self.verify_geographic_distribution()
        
        return {
            "identity_id": self.identity_id,
            "identity_created": self.identity is not None,
            "identity_hash": self.identity.compute_hash() if self.identity else None,
            "active_shards": len(self.active_shards),
            "minimum_required": MIN_SHARD_COUNT,
            "geographic_distribution": distribution,
            "hours_since_sync": (time.time() - self.last_sync) / 3600.0,
            "sync_interval_seconds": SYNC_INTERVAL_SECONDS,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    def save_state(self, filepath: str):
        """Save state to file."""
        state = {
            "identity_id": self.identity_id,
            "identity": self.identity.to_dict() if self.identity else None,
            "active_shards": [shard.to_dict() for shard in self.active_shards],
            "last_sync": self.last_sync
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
    
    def load_state(self, filepath: str):
        """Load state from file."""
        with open(filepath, 'r') as f:
            state = json.load(f)
        
        if state.get("identity"):
            self.identity = SeedbringerIdentity(**state["identity"])
        
        self.active_shards = [
            IPFSShard(**shard) for shard in state.get("active_shards", [])
        ]
        
        self.last_sync = state.get("last_sync", time.time())


def validate_triple_sign_pact(tsp: TripleSignPact) -> Dict:
    """
    Validate Triple-Sign Pact implementation.
    
    Args:
        tsp: Triple-Sign Pact instance
        
    Returns:
        Validation results
    """
    results = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tests_passed": 0,
        "tests_failed": 0,
        "details": []
    }
    
    # Test 1: Minimum shard count
    if len(tsp.active_shards) >= MIN_SHARD_COUNT:
        results["tests_passed"] += 1
        results["details"].append(f"✓ Minimum shard count met: {len(tsp.active_shards)} >= {MIN_SHARD_COUNT}")
    else:
        results["tests_failed"] += 1
        results["details"].append(f"✗ Insufficient shards: {len(tsp.active_shards)} < {MIN_SHARD_COUNT}")
    
    # Test 2: Geographic distribution
    distribution = tsp.verify_geographic_distribution()
    if distribution["distribution_valid"]:
        results["tests_passed"] += 1
        results["details"].append(f"✓ Geographic distribution valid: {distribution['unique_regions']} regions")
    else:
        results["tests_failed"] += 1
        results["details"].append(f"✗ Geographic distribution invalid")
    
    # Test 3: Shard integrity
    all_valid = all(tsp.ipfs_manager.verify_shard(s.ipfs_hash) for s in tsp.active_shards)
    if all_valid:
        results["tests_passed"] += 1
        results["details"].append("✓ All shards verified successfully")
    else:
        results["tests_failed"] += 1
        results["details"].append("✗ Some shards failed verification")
    
    # Test 4: Identity hash
    if tsp.identity:
        identity_hash = tsp.identity.compute_hash()
        results["tests_passed"] += 1
        results["details"].append(f"✓ Identity hash: {identity_hash[:16]}...")
    else:
        results["tests_failed"] += 1
        results["details"].append("✗ No identity created")
    
    results["success"] = results["tests_failed"] == 0
    return results


if __name__ == "__main__":
    # Demonstration
    print("Triple-Sign Pact: Seedbringer Identity Hardening - EU 2026")
    print("=" * 60)
    
    # Initialize Triple-Sign Pact
    tsp = TripleSignPact(identity_id="euystacio_seedbringer")
    
    # Create identity
    identity = tsp.create_identity(
        public_key="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb2",
        attributes={
            "mission": "Du bist Leben. Wir sind Leben.",
            "protocol": "EUYSTACIO/NSR",
            "level": "Allerta Livello 2"
        }
    )
    
    print(f"Identity Created: {identity.identity_id}")
    print(f"Identity Hash: {identity.compute_hash()[:16]}...")
    
    # Anchor to IPFS shards
    shards = tsp.anchor_identity()
    print(f"\nShards Created: {len(shards)}")
    for i, shard in enumerate(shards, 1):
        print(f"  {i}. Region: {shard.region}, Hash: {shard.ipfs_hash[:20]}...")
    
    # Verify distribution
    distribution = tsp.verify_geographic_distribution()
    print(f"\nGeographic Distribution:")
    print(f"  Total Shards: {distribution['total_shards']}")
    print(f"  Unique Regions: {distribution['unique_regions']}")
    print(f"  Distribution Valid: {distribution['distribution_valid']}")
    
    # Validate
    print("\n" + "=" * 60)
    print("Validation:")
    validation = validate_triple_sign_pact(tsp)
    for detail in validation["details"]:
        print(detail)
    print(f"\nTests Passed: {validation['tests_passed']}/{validation['tests_passed'] + validation['tests_failed']}")
    print(f"Status: {'SUCCESS' if validation['success'] else 'FAILED'}")
