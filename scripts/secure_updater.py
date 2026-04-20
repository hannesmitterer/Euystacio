#!/usr/bin/env python3
"""
Secure Firmware Update Mechanism
Handles secure updates with checksum verification and cryptographic signatures
"""

import json
import hashlib
import subprocess
import requests
import os
import shutil
from pathlib import Path
from typing import Dict, Optional, Tuple
import logging
import tempfile

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('SecureUpdater')

class SecureUpdateManager:
    """Manages secure firmware/software updates"""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize the update manager"""
        self.config_path = config_path or Path(__file__).parent / 'update_config.json'
        self.config = self.load_config()
        self.update_server = self.config.get('update_server', '')
        self.gpg_key_id = self.config.get('gpg_key_id', '')
        self.trusted_keys = self.config.get('trusted_keys', [])
        self.install_dir = Path(self.config.get('install_dir', '/opt/euystacio'))
        self.backup_dir = Path(self.config.get('backup_dir', '/var/backups/euystacio'))
        
    def load_config(self) -> Dict:
        """Load configuration"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return self.get_default_config()
    
    def get_default_config(self) -> Dict:
        """Return default configuration"""
        return {
            "update_server": "https://updates.euystacio.io",
            "gpg_key_id": "",
            "trusted_keys": [],
            "install_dir": "/opt/euystacio",
            "backup_dir": "/var/backups/euystacio",
            "verify_checksums": True,
            "verify_signatures": True,
            "auto_rollback": True,
            "max_backup_versions": 5
        }
    
    def compute_checksum(self, file_path: Path, algorithm: str = 'sha512') -> str:
        """Compute checksum of a file"""
        logger.info(f"Computing {algorithm.upper()} checksum for {file_path}")
        
        hash_func = getattr(hashlib, algorithm)()
        
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hash_func.update(chunk)
        
        checksum = hash_func.hexdigest()
        logger.info(f"Checksum: {checksum}")
        return checksum
    
    def verify_checksum(self, file_path: Path, expected_checksum: str, 
                       algorithm: str = 'sha512') -> bool:
        """Verify file checksum"""
        logger.info(f"Verifying checksum for {file_path}")
        actual_checksum = self.compute_checksum(file_path, algorithm)
        
        if actual_checksum == expected_checksum:
            logger.info("✓ Checksum verification PASSED")
            return True
        else:
            logger.error(f"✗ Checksum verification FAILED")
            logger.error(f"Expected: {expected_checksum}")
            logger.error(f"Actual:   {actual_checksum}")
            return False
    
    def verify_signature(self, file_path: Path, signature_path: Path) -> bool:
        """Verify GPG signature of a file"""
        logger.info(f"Verifying GPG signature for {file_path}")
        
        # Check if we have trusted keys configured
        if self.trusted_keys and len(self.trusted_keys) > 0:
            logger.info(f"Verifying against trusted keys: {', '.join(self.trusted_keys)}")
        else:
            logger.warning("No trusted keys configured - signature will be verified but not checked against whitelist")
        
        try:
            # Run GPG verification
            result = subprocess.run(
                ['gpg', '--verify', str(signature_path), str(file_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # Check if signature is from a trusted key
                if self.trusted_keys and len(self.trusted_keys) > 0:
                    # Extract key ID from verification output
                    import re
                    key_match = re.search(r'key ID ([A-F0-9]+)', result.stderr, re.IGNORECASE)
                    if key_match:
                        key_id = key_match.group(1)
                        if key_id not in self.trusted_keys:
                            logger.error(f"✗ Signature from untrusted key: {key_id}")
                            logger.error(f"Trusted keys: {', '.join(self.trusted_keys)}")
                            return False
                
                logger.info("✓ Signature verification PASSED")
                logger.debug(result.stderr)
                return True
            else:
                logger.error("✗ Signature verification FAILED")
                logger.error(result.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("GPG verification timed out")
            return False
        except FileNotFoundError:
            logger.error("GPG not found - install with: apt-get install gnupg")
            return False
        except Exception as e:
            logger.error(f"Error during signature verification: {e}")
            return False
    
    def download_update(self, version: str) -> Optional[Tuple[Path, Path, Dict]]:
        """Download update package and manifest"""
        logger.info(f"Downloading update version: {version}")
        
        # Create temporary directory
        temp_dir = Path(tempfile.mkdtemp(prefix='euystacio_update_'))
        
        try:
            # Download manifest
            manifest_url = f"{self.update_server}/updates/{version}/manifest.json"
            logger.info(f"Fetching manifest: {manifest_url}")
            
            response = requests.get(manifest_url, timeout=30)
            response.raise_for_status()
            manifest = response.json()
            
            manifest_path = temp_dir / 'manifest.json'
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)
            
            # Download update package
            package_url = manifest.get('package_url')
            if not package_url:
                logger.error("No package_url in manifest")
                return None
            
            logger.info(f"Downloading package: {package_url}")
            response = requests.get(package_url, stream=True, timeout=300)
            response.raise_for_status()
            
            package_path = temp_dir / manifest.get('package_name', 'update.tar.gz')
            with open(package_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Download signature
            signature_url = manifest.get('signature_url')
            signature_path = None
            if signature_url:
                logger.info(f"Downloading signature: {signature_url}")
                response = requests.get(signature_url, timeout=30)
                response.raise_for_status()
                
                signature_path = temp_dir / (manifest.get('package_name', 'update.tar.gz') + '.sig')
                with open(signature_path, 'wb') as f:
                    f.write(response.content)
            
            return package_path, signature_path, manifest
            
        except Exception as e:
            logger.error(f"Error downloading update: {e}")
            # Cleanup
            shutil.rmtree(temp_dir, ignore_errors=True)
            return None
    
    def create_backup(self) -> Optional[Path]:
        """Create backup of current installation"""
        logger.info("Creating backup of current installation...")
        
        if not self.install_dir.exists():
            logger.warning(f"Install directory does not exist: {self.install_dir}")
            return None
        
        # Create backup directory
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate backup filename with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"euystacio_backup_{timestamp}.tar.gz"
        backup_path = self.backup_dir / backup_name
        
        try:
            # Create tarball
            subprocess.run(
                ['tar', '-czf', str(backup_path), '-C', str(self.install_dir.parent), 
                 self.install_dir.name],
                check=True,
                timeout=300
            )
            
            logger.info(f"✓ Backup created: {backup_path}")
            
            # Cleanup old backups
            self.cleanup_old_backups()
            
            return backup_path
            
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return None
    
    def cleanup_old_backups(self):
        """Remove old backup files"""
        max_backups = self.config.get('max_backup_versions', 5)
        
        # List all backup files
        backups = sorted(
            self.backup_dir.glob('euystacio_backup_*.tar.gz'),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        
        # Remove old backups
        for old_backup in backups[max_backups:]:
            logger.info(f"Removing old backup: {old_backup}")
            old_backup.unlink()
    
    def rollback(self, backup_path: Path) -> bool:
        """Rollback to previous version"""
        logger.warning(f"Rolling back to: {backup_path}")
        
        if not backup_path.exists():
            logger.error(f"Backup file not found: {backup_path}")
            return False
        
        try:
            # Remove current installation
            if self.install_dir.exists():
                shutil.rmtree(self.install_dir)
            
            # Extract backup
            subprocess.run(
                ['tar', '-xzf', str(backup_path), '-C', str(self.install_dir.parent)],
                check=True,
                timeout=300
            )
            
            logger.info("✓ Rollback completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Rollback failed: {e}")
            return False
    
    def apply_update(self, package_path: Path, manifest: Dict) -> bool:
        """Apply the update"""
        logger.info("Applying update...")
        
        try:
            # Extract package to temporary location
            temp_extract = Path(tempfile.mkdtemp(prefix='euystacio_extract_'))
            
            subprocess.run(
                ['tar', '-xzf', str(package_path), '-C', str(temp_extract)],
                check=True,
                timeout=300
            )
            
            # Copy files to installation directory
            self.install_dir.mkdir(parents=True, exist_ok=True)
            
            # Use rsync for atomic update if available
            if shutil.which('rsync'):
                subprocess.run(
                    ['rsync', '-av', '--delete', str(temp_extract) + '/', str(self.install_dir) + '/'],
                    check=True,
                    timeout=300
                )
            else:
                # Fallback to copytree
                for item in temp_extract.iterdir():
                    dest = self.install_dir / item.name
                    if dest.exists():
                        if dest.is_dir():
                            shutil.rmtree(dest)
                        else:
                            dest.unlink()
                    if item.is_dir():
                        shutil.copytree(item, dest)
                    else:
                        shutil.copy2(item, dest)
            
            # Cleanup
            shutil.rmtree(temp_extract, ignore_errors=True)
            
            logger.info("✓ Update applied successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to apply update: {e}")
            return False
    
    def update(self, version: str) -> bool:
        """Execute secure update process"""
        logger.info(f"Starting secure update to version: {version}")
        
        # 1. Download update
        download_result = self.download_update(version)
        if not download_result:
            logger.error("Failed to download update")
            return False
        
        package_path, signature_path, manifest = download_result
        
        # 2. Verify checksum
        if self.config.get('verify_checksums', True):
            expected_checksum = manifest.get('checksum')
            if not expected_checksum:
                logger.error("No checksum in manifest")
                return False
            
            if not self.verify_checksum(package_path, expected_checksum):
                logger.error("Checksum verification failed - update aborted")
                return False
        
        # 3. Verify signature
        if self.config.get('verify_signatures', True):
            if not signature_path or not signature_path.exists():
                logger.error("Signature file not found - update aborted")
                return False
            
            if not self.verify_signature(package_path, signature_path):
                logger.error("Signature verification failed - update aborted")
                return False
        
        # 4. Create backup
        backup_path = self.create_backup()
        if not backup_path and self.config.get('auto_rollback', True):
            logger.error("Failed to create backup - update aborted")
            return False
        
        # 5. Apply update
        if not self.apply_update(package_path, manifest):
            logger.error("Failed to apply update")
            
            # Rollback if enabled
            if backup_path and self.config.get('auto_rollback', True):
                logger.warning("Attempting automatic rollback...")
                self.rollback(backup_path)
            
            return False
        
        logger.info(f"✓ Update to version {version} completed successfully!")
        return True

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Secure Firmware Update Manager')
    parser.add_argument('action', choices=['update', 'rollback', 'verify', 'backup'],
                       help='Action to perform')
    parser.add_argument('--version', help='Version to update to')
    parser.add_argument('--file', type=Path, help='File to verify')
    parser.add_argument('--checksum', help='Expected checksum')
    parser.add_argument('--signature', type=Path, help='Signature file')
    parser.add_argument('--backup', type=Path, help='Backup file to rollback to')
    parser.add_argument('--config', type=Path, help='Config file path')
    
    args = parser.parse_args()
    
    manager = SecureUpdateManager(config_path=args.config)
    
    if args.action == 'update':
        if not args.version:
            logger.error("Version required for update")
            return 1
        success = manager.update(args.version)
        return 0 if success else 1
    
    elif args.action == 'rollback':
        if not args.backup:
            # Use latest backup
            backups = sorted(
                manager.backup_dir.glob('euystacio_backup_*.tar.gz'),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )
            if not backups:
                logger.error("No backups found")
                return 1
            args.backup = backups[0]
        
        success = manager.rollback(args.backup)
        return 0 if success else 1
    
    elif args.action == 'verify':
        if not args.file:
            logger.error("File required for verification")
            return 1
        
        # Verify checksum
        if args.checksum:
            if not manager.verify_checksum(args.file, args.checksum):
                return 1
        
        # Verify signature
        if args.signature:
            if not manager.verify_signature(args.file, args.signature):
                return 1
        
        logger.info("✓ All verifications passed")
        return 0
    
    elif args.action == 'backup':
        backup_path = manager.create_backup()
        return 0 if backup_path else 1

if __name__ == '__main__':
    exit(main())
