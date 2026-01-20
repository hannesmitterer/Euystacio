#!/usr/bin/env python3
"""
Forensic Response Automation - Log Watcher
Monitors logs for suspicious activity and triggers defensive responses
"""

import json
import os
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/euystacio/forensic_watcher.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('ForensicWatcher')

# Configuration
CONFIG_FILE = Path(__file__).parent / 'forensic_config.json'
LOG_DIR = Path('/var/log/euystacio')
INTRUSION_LOG = LOG_DIR / 'intrusion.log'
SECURITY_LOG = LOG_DIR / 'security.log'

class ForensicWatcher:
    """Monitors logs for suspicious activity and triggers responses"""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize the forensic watcher"""
        self.config_path = config_path or CONFIG_FILE
        self.config = self.load_config()
        self.suspicious_patterns = self.config.get('suspicious_patterns', [])
        self.response_enabled = self.config.get('response_enabled', False)
        self.tor_enabled = self.config.get('tor_enabled', False)
        self.vpn_enabled = self.config.get('vpn_enabled', False)
        self.alert_threshold = self.config.get('alert_threshold', 5)
        self.time_window = self.config.get('time_window_seconds', 300)
        self.alert_counter = {}
        
    def load_config(self) -> Dict:
        """Load configuration from JSON file"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        else:
            logger.warning(f"Config file not found: {self.config_path}, using defaults")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict:
        """Return default configuration"""
        return {
            "response_enabled": False,
            "tor_enabled": False,
            "vpn_enabled": False,
            "alert_threshold": 5,
            "time_window_seconds": 300,
            "suspicious_patterns": [
                {
                    "name": "Multiple Failed Auth",
                    "pattern": "authentication failed|auth failure|invalid password",
                    "severity": "high",
                    "action": "tor_routing"
                },
                {
                    "name": "Port Scan Detection",
                    "pattern": "port scan|syn flood|scanning attempt",
                    "severity": "critical",
                    "action": "vpn_routing"
                },
                {
                    "name": "SQL Injection Attempt",
                    "pattern": "sql injection|union select|drop table",
                    "severity": "critical",
                    "action": "block_and_alert"
                },
                {
                    "name": "Unauthorized Access Attempt",
                    "pattern": "unauthorized|access denied|403|401",
                    "severity": "medium",
                    "action": "monitor"
                },
                {
                    "name": "Brute Force Attack",
                    "pattern": "brute force|too many requests|rate limit exceeded",
                    "severity": "high",
                    "action": "tor_routing"
                }
            ]
        }
    
    def analyze_log_line(self, line: str) -> Optional[Dict]:
        """Analyze a log line for suspicious patterns"""
        for pattern_config in self.suspicious_patterns:
            pattern = pattern_config.get('pattern', '')
            if re.search(pattern, line, re.IGNORECASE):
                return {
                    'timestamp': datetime.now().isoformat(),
                    'pattern_name': pattern_config.get('name'),
                    'severity': pattern_config.get('severity'),
                    'action': pattern_config.get('action'),
                    'log_line': line.strip()
                }
        return None
    
    def trigger_response(self, detection: Dict):
        """Trigger defensive response based on detection"""
        action = detection.get('action')
        severity = detection.get('severity')
        
        logger.warning(f"SUSPICIOUS ACTIVITY DETECTED: {detection['pattern_name']}")
        logger.warning(f"Severity: {severity}, Recommended Action: {action}")
        
        # Log to intrusion log
        self.log_intrusion(detection)
        
        if not self.response_enabled:
            logger.info("Automated response is DISABLED. Manual intervention required.")
            return
        
        # Execute response actions
        if action == 'tor_routing' and self.tor_enabled:
            self.activate_tor_routing()
        elif action == 'vpn_routing' and self.vpn_enabled:
            self.activate_vpn_routing()
        elif action == 'block_and_alert':
            self.block_source(detection)
        elif action == 'monitor':
            logger.info(f"Monitoring suspicious activity: {detection['pattern_name']}")
    
    def activate_tor_routing(self):
        """Activate Tor routing for enhanced privacy"""
        logger.info("Activating Tor routing...")
        script_path = Path(__file__).parent / 'activate_tor.sh'
        if script_path.exists():
            try:
                subprocess.run([str(script_path)], check=True, timeout=30)
                logger.info("Tor routing activated successfully")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to activate Tor routing: {e}")
            except subprocess.TimeoutExpired:
                logger.error("Tor activation timed out")
        else:
            logger.error(f"Tor activation script not found: {script_path}")
    
    def activate_vpn_routing(self):
        """Activate VPN routing for secure communication"""
        logger.info("Activating VPN routing...")
        script_path = Path(__file__).parent / 'activate_vpn.sh'
        if script_path.exists():
            try:
                subprocess.run([str(script_path)], check=True, timeout=30)
                logger.info("VPN routing activated successfully")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to activate VPN routing: {e}")
            except subprocess.TimeoutExpired:
                logger.error("VPN activation timed out")
        else:
            logger.error(f"VPN activation script not found: {script_path}")
    
    def block_source(self, detection: Dict):
        """Block the source of suspicious activity"""
        logger.warning(f"BLOCKING SOURCE for: {detection['pattern_name']}")
        # Extract IP from log line (simple regex, adjust as needed)
        ip_match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', detection['log_line'])
        if ip_match:
            ip = ip_match.group(0)
            logger.info(f"Blocking IP: {ip}")
            # Use iptables to block (requires root)
            try:
                subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'], 
                             check=True, timeout=10)
                logger.info(f"Successfully blocked IP: {ip}")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to block IP {ip}: {e}")
            except subprocess.TimeoutExpired:
                logger.error(f"Timeout while blocking IP {ip}")
    
    def log_intrusion(self, detection: Dict):
        """Log intrusion details to intrusion log"""
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        with open(INTRUSION_LOG, 'a') as f:
            log_entry = {
                'timestamp': detection['timestamp'],
                'pattern': detection['pattern_name'],
                'severity': detection['severity'],
                'action': detection['action'],
                'details': detection['log_line']
            }
            f.write(json.dumps(log_entry) + '\n')
    
    def watch_logs(self, log_files: List[Path], follow: bool = True):
        """Watch log files for suspicious activity"""
        logger.info(f"Starting log watch on {len(log_files)} files")
        
        file_positions = {str(f): 0 for f in log_files if f.exists()}
        
        while True:
            for log_file in log_files:
                if not log_file.exists():
                    continue
                
                log_file_str = str(log_file)
                
                try:
                    with open(log_file, 'r') as f:
                        # Seek to last position
                        f.seek(file_positions.get(log_file_str, 0))
                        
                        # Read new lines
                        for line in f:
                            detection = self.analyze_log_line(line)
                            if detection:
                                self.trigger_response(detection)
                        
                        # Update position
                        file_positions[log_file_str] = f.tell()
                
                except Exception as e:
                    logger.error(f"Error reading {log_file}: {e}")
            
            if not follow:
                break
            
            time.sleep(1)  # Check every second

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Forensic Response Automation - Log Watcher')
    parser.add_argument('--config', type=Path, help='Path to config file')
    parser.add_argument('--logs', nargs='+', type=Path, help='Log files to watch')
    parser.add_argument('--no-follow', action='store_true', help='Scan once and exit')
    parser.add_argument('--enable-response', action='store_true', help='Enable automated responses')
    
    args = parser.parse_args()
    
    # Create log directory
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    # Initialize watcher
    watcher = ForensicWatcher(config_path=args.config)
    
    if args.enable_response:
        watcher.response_enabled = True
        logger.warning("AUTOMATED RESPONSE IS ENABLED")
    
    # Determine log files to watch
    log_files = args.logs if args.logs else [
        LOG_DIR / 'app.log',
        LOG_DIR / 'security.log',
        Path('/var/log/auth.log'),
        Path('/var/log/syslog')
    ]
    
    try:
        watcher.watch_logs(log_files, follow=not args.no_follow)
    except KeyboardInterrupt:
        logger.info("Log watcher stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise

if __name__ == '__main__':
    main()
