#!/usr/bin/env python3
"""
Distributed Encrypted Backup System
Automated backups with GnuPG encryption and IPFS distributed storage
"""

import json
import os
import subprocess
import shutil
import tempfile
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('DistributedBackup')

class DistributedBackupManager:
    """Manages distributed encrypted backups using IPFS and GnuPG"""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize the backup manager"""
        self.config_path = config_path or Path(__file__).parent / 'backup_config.json'
        self.config = self.load_config()
        self.backup_dirs = [Path(d) for d in self.config.get('backup_directories', [])]
        self.gpg_recipient = self.config.get('gpg_recipient', '')
        self.ipfs_enabled = self.config.get('ipfs_enabled', True)
        self.local_backup_dir = Path(self.config.get('local_backup_dir', '/var/backups/euystacio'))
        self.metadata_file = self.local_backup_dir / 'backup_metadata.json'
        
    def load_config(self) -> Dict:
        """Load configuration"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return self.get_default_config()
    
    def get_default_config(self) -> Dict:
        """Return default configuration"""
        return {
            "backup_directories": [
                "/home/runner/work/Euystacio/Euystacio",
                "/etc/euystacio"
            ],
            "exclude_patterns": [
                "*.tmp",
                "*.log",
                "__pycache__",
                ".git",
                "node_modules"
            ],
            "gpg_recipient": "",
            "ipfs_enabled": True,
            "ipfs_api": "/ip4/127.0.0.1/tcp/5001",
            "local_backup_dir": "/var/backups/euystacio",
            "max_local_backups": 10,
            "backup_schedule": "daily",
            "compression": "gzip"
        }
    
    def check_dependencies(self) -> bool:
        """Check if required tools are installed"""
        required_tools = ['gpg', 'tar']
        
        if self.ipfs_enabled:
            required_tools.append('ipfs')
        
        missing = []
        for tool in required_tools:
            if not shutil.which(tool):
                missing.append(tool)
        
        if missing:
            logger.error(f"Missing required tools: {', '.join(missing)}")
            logger.error("Install with: sudo apt-get install gnupg ipfs")
            return False
        
        return True
    
    def create_tarball(self, output_path: Path) -> bool:
        """Create compressed tarball of backup directories"""
        logger.info("Creating backup tarball...")
        
        try:
            # Build tar command with exclusions
            tar_cmd = ['tar', '-czf', str(output_path)]
            
            # Add exclusion patterns
            for pattern in self.config.get('exclude_patterns', []):
                tar_cmd.extend(['--exclude', pattern])
            
            # Add directories
            for backup_dir in self.backup_dirs:
                if backup_dir.exists():
                    tar_cmd.append(str(backup_dir))
                else:
                    logger.warning(f"Backup directory not found: {backup_dir}")
            
            # Execute tar command
            subprocess.run(tar_cmd, check=True, timeout=600)
            
            logger.info(f"✓ Tarball created: {output_path}")
            logger.info(f"  Size: {output_path.stat().st_size / (1024*1024):.2f} MB")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create tarball: {e}")
            return False
        except Exception as e:
            logger.error(f"Error creating tarball: {e}")
            return False
    
    def encrypt_file(self, input_path: Path, output_path: Path) -> bool:
        """Encrypt file with GnuPG"""
        logger.info("Encrypting backup with GnuPG...")
        
        if not self.gpg_recipient:
            logger.error("GPG recipient not configured")
            return False
        
        # Verify GPG recipient key exists
        try:
            result = subprocess.run(
                ['gpg', '--list-keys', self.gpg_recipient],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0:
                logger.error(f"GPG recipient key not found: {self.gpg_recipient}")
                logger.error("Import the recipient's public key first:")
                logger.error(f"  gpg --import recipient_key.asc")
                return False
        except Exception as e:
            logger.error(f"Error checking GPG key: {e}")
            return False
        
        try:
            # Build GPG command
            gpg_cmd = [
                'gpg',
                '--encrypt',
                '--recipient', self.gpg_recipient,
                '--armor',
                '--output', str(output_path),
                str(input_path)
            ]
            
            # Execute GPG encryption
            subprocess.run(gpg_cmd, check=True, timeout=600)
            
            logger.info(f"✓ File encrypted: {output_path}")
            logger.info(f"  Size: {output_path.stat().st_size / (1024*1024):.2f} MB")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"GPG encryption failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Error during encryption: {e}")
            return False
    
    def decrypt_file(self, input_path: Path, output_path: Path) -> bool:
        """Decrypt file with GnuPG"""
        logger.info("Decrypting backup with GnuPG...")
        
        try:
            # Build GPG command
            gpg_cmd = [
                'gpg',
                '--decrypt',
                '--output', str(output_path),
                str(input_path)
            ]
            
            # Execute GPG decryption
            subprocess.run(gpg_cmd, check=True, timeout=600)
            
            logger.info(f"✓ File decrypted: {output_path}")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"GPG decryption failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Error during decryption: {e}")
            return False
    
    def upload_to_ipfs(self, file_path: Path) -> Optional[str]:
        """Upload file to IPFS and return CID"""
        logger.info("Uploading to IPFS...")
        
        if not self.ipfs_enabled:
            logger.info("IPFS upload disabled")
            return None
        
        try:
            # Check if IPFS daemon is running
            subprocess.run(['ipfs', 'id'], check=True, capture_output=True, timeout=10)
            
            # Upload to IPFS
            result = subprocess.run(
                ['ipfs', 'add', '-Q', str(file_path)],
                check=True,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            cid = result.stdout.strip()
            logger.info(f"✓ Uploaded to IPFS: {cid}")
            
            # Pin the file
            subprocess.run(['ipfs', 'pin', 'add', cid], check=True, timeout=60)
            logger.info(f"✓ Pinned: {cid}")
            
            return cid
            
        except subprocess.CalledProcessError as e:
            logger.error(f"IPFS upload failed: {e}")
            logger.error("Make sure IPFS daemon is running: ipfs daemon &")
            return None
        except Exception as e:
            logger.error(f"Error uploading to IPFS: {e}")
            return None
    
    def download_from_ipfs(self, cid: str, output_path: Path) -> bool:
        """Download file from IPFS"""
        logger.info(f"Downloading from IPFS: {cid}")
        
        try:
            # Download from IPFS
            result = subprocess.run(
                ['ipfs', 'get', cid, '-o', str(output_path)],
                check=True,
                capture_output=True,
                timeout=600
            )
            
            logger.info(f"✓ Downloaded from IPFS: {output_path}")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"IPFS download failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Error downloading from IPFS: {e}")
            return False
    
    def save_metadata(self, backup_info: Dict):
        """Save backup metadata"""
        metadata = []
        
        # Load existing metadata
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                metadata = json.load(f)
        
        # Add new backup
        metadata.append(backup_info)
        
        # Save metadata
        self.local_backup_dir.mkdir(parents=True, exist_ok=True)
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"✓ Metadata saved: {self.metadata_file}")
    
    def cleanup_old_backups(self):
        """Remove old local backups"""
        max_backups = self.config.get('max_local_backups', 10)
        
        # List all backup files
        backups = sorted(
            self.local_backup_dir.glob('backup_*.tar.gz.gpg'),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        
        # Remove old backups
        for old_backup in backups[max_backups:]:
            logger.info(f"Removing old backup: {old_backup}")
            old_backup.unlink()
    
    def create_backup(self) -> Optional[Dict]:
        """Create a new encrypted distributed backup"""
        logger.info("=== Starting Distributed Backup ===")
        
        # Check dependencies
        if not self.check_dependencies():
            return None
        
        # Create temporary directory
        with tempfile.TemporaryDirectory(prefix='euystacio_backup_') as temp_dir:
            temp_path = Path(temp_dir)
            
            # Generate filenames
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            tarball_name = f'backup_{timestamp}.tar.gz'
            encrypted_name = f'{tarball_name}.gpg'
            
            tarball_path = temp_path / tarball_name
            encrypted_path = self.local_backup_dir / encrypted_name
            
            # Create tarball
            if not self.create_tarball(tarball_path):
                return None
            
            # Encrypt tarball
            if not self.encrypt_file(tarball_path, encrypted_path):
                return None
            
            # Upload to IPFS
            ipfs_cid = self.upload_to_ipfs(encrypted_path)
            
            # Create backup info
            backup_info = {
                'timestamp': timestamp,
                'datetime': datetime.now().isoformat(),
                'filename': encrypted_name,
                'local_path': str(encrypted_path),
                'ipfs_cid': ipfs_cid,
                'size_bytes': encrypted_path.stat().st_size,
                'directories': [str(d) for d in self.backup_dirs if d.exists()]
            }
            
            # Save metadata
            self.save_metadata(backup_info)
            
            # Cleanup old backups
            self.cleanup_old_backups()
            
            logger.info("=== Backup Complete ===")
            logger.info(f"Local: {encrypted_path}")
            if ipfs_cid:
                logger.info(f"IPFS: {ipfs_cid}")
                logger.info(f"Gateway: https://ipfs.io/ipfs/{ipfs_cid}")
            
            return backup_info
    
    def restore_backup(self, source: str, restore_dir: Path) -> bool:
        """Restore from backup (source can be CID or local path)"""
        logger.info(f"=== Starting Backup Restore ===")
        logger.info(f"Source: {source}")
        logger.info(f"Restore to: {restore_dir}")
        
        # Check dependencies
        if not self.check_dependencies():
            return False
        
        with tempfile.TemporaryDirectory(prefix='euystacio_restore_') as temp_dir:
            temp_path = Path(temp_dir)
            encrypted_path = temp_path / 'backup.tar.gz.gpg'
            decrypted_path = temp_path / 'backup.tar.gz'
            
            # Download from IPFS or copy from local
            if source.startswith('Qm') or source.startswith('bafy'):
                # IPFS CID
                if not self.download_from_ipfs(source, encrypted_path):
                    return False
            else:
                # Local file
                source_path = Path(source)
                if not source_path.exists():
                    logger.error(f"Source file not found: {source}")
                    return False
                shutil.copy2(source_path, encrypted_path)
            
            # Decrypt
            if not self.decrypt_file(encrypted_path, decrypted_path):
                return False
            
            # Extract
            try:
                logger.info("Extracting backup...")
                restore_dir.mkdir(parents=True, exist_ok=True)
                
                subprocess.run(
                    ['tar', '-xzf', str(decrypted_path), '-C', str(restore_dir)],
                    check=True,
                    timeout=600
                )
                
                logger.info(f"✓ Backup restored to: {restore_dir}")
                logger.info("=== Restore Complete ===")
                return True
                
            except subprocess.CalledProcessError as e:
                logger.error(f"Extraction failed: {e}")
                return False
    
    def list_backups(self) -> List[Dict]:
        """List all available backups"""
        if not self.metadata_file.exists():
            return []
        
        with open(self.metadata_file, 'r') as f:
            return json.load(f)

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Distributed Encrypted Backup Manager')
    parser.add_argument('action', choices=['create', 'restore', 'list'],
                       help='Action to perform')
    parser.add_argument('--source', help='Backup source (CID or path) for restore')
    parser.add_argument('--restore-dir', type=Path, help='Directory to restore to')
    parser.add_argument('--config', type=Path, help='Config file path')
    
    args = parser.parse_args()
    
    manager = DistributedBackupManager(config_path=args.config)
    
    if args.action == 'create':
        result = manager.create_backup()
        return 0 if result else 1
    
    elif args.action == 'restore':
        if not args.source:
            logger.error("Source required for restore")
            return 1
        if not args.restore_dir:
            args.restore_dir = Path('/tmp/euystacio_restore')
        
        success = manager.restore_backup(args.source, args.restore_dir)
        return 0 if success else 1
    
    elif args.action == 'list':
        backups = manager.list_backups()
        if not backups:
            print("No backups found")
        else:
            print(f"Found {len(backups)} backups:")
            for backup in backups:
                print(f"\n  Timestamp: {backup.get('datetime')}")
                print(f"  File: {backup.get('filename')}")
                if backup.get('ipfs_cid'):
                    print(f"  IPFS: {backup.get('ipfs_cid')}")
                print(f"  Size: {backup.get('size_bytes', 0) / (1024*1024):.2f} MB")
        return 0

if __name__ == '__main__':
    exit(main())
