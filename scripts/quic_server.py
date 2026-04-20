#!/usr/bin/env python3
"""
QUIC Protocol Server with TLS 1.3 
Hardened communication protocol implementation
"""

import asyncio
import logging
from pathlib import Path
from typing import Optional
import json

try:
    from aioquic.asyncio import serve
    from aioquic.quic.configuration import QuicConfiguration
    from aioquic.asyncio.protocol import QuicConnectionProtocol
    from aioquic.quic.events import QuicEvent, StreamDataReceived
    AIOQUIC_AVAILABLE = True
except ImportError:
    AIOQUIC_AVAILABLE = False
    logging.warning("aioquic not installed. Install with: pip install aioquic")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('QUICServer')

class SecureQuicProtocol(QuicConnectionProtocol):
    """QUIC protocol handler with TLS 1.3"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handlers = {}
    
    def quic_event_received(self, event: QuicEvent):
        """Handle QUIC events"""
        if isinstance(event, StreamDataReceived):
            # Process received data
            data = event.data
            stream_id = event.stream_id
            
            logger.info(f"Received data on stream {stream_id}: {len(data)} bytes")
            
            try:
                # Decode and process message
                message = json.loads(data.decode('utf-8'))
                response = self.process_message(message)
                
                # Send response
                response_data = json.dumps(response).encode('utf-8')
                self._quic.send_stream_data(stream_id, response_data, end_stream=True)
                
            except json.JSONDecodeError:
                logger.error("Invalid JSON received")
                error_response = json.dumps({"error": "Invalid JSON"}).encode('utf-8')
                self._quic.send_stream_data(stream_id, error_response, end_stream=True)
            except Exception as e:
                logger.error(f"Error processing message: {e}")
    
    def process_message(self, message: dict) -> dict:
        """Process incoming message and return response"""
        logger.info(f"Processing message: {message.get('type', 'unknown')}")
        
        msg_type = message.get('type')
        
        if msg_type == 'ping':
            return {'type': 'pong', 'timestamp': message.get('timestamp')}
        
        elif msg_type == 'status':
            return {
                'type': 'status_response',
                'status': 'healthy',
                'protocol': 'QUIC/TLS1.3'
            }
        
        elif msg_type == 'data':
            # Process data message
            return {
                'type': 'data_response',
                'received': len(message.get('payload', '')),
                'status': 'processed'
            }
        
        else:
            return {'type': 'error', 'message': f'Unknown message type: {msg_type}'}

class QUICServer:
    """QUIC server with TLS 1.3 encryption"""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize QUIC server"""
        self.config_path = config_path or Path(__file__).parent / 'quic_config.json'
        self.config = self.load_config()
        self.host = self.config.get('host', '0.0.0.0')
        self.port = self.config.get('port', 4433)
        self.cert_path = Path(self.config.get('certificate', 'certs/cert.pem'))
        self.key_path = Path(self.config.get('private_key', 'certs/key.pem'))
    
    def load_config(self) -> dict:
        """Load server configuration"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return self.get_default_config()
    
    def get_default_config(self) -> dict:
        """Return default configuration"""
        return {
            'host': '0.0.0.0',
            'port': 4433,
            'certificate': 'certs/cert.pem',
            'private_key': 'certs/key.pem',
            'alpn_protocols': ['h3'],
            'max_datagram_size': 1280,
            'disable_unencrypted': True,
            'tls_version': '1.3'
        }
    
    def create_quic_configuration(self) -> QuicConfiguration:
        """Create QUIC configuration with TLS 1.3"""
        configuration = QuicConfiguration(
            is_client=False,
            alpn_protocols=self.config.get('alpn_protocols', ['h3'])
        )
        
        # Load TLS certificate and key
        if self.cert_path.exists() and self.key_path.exists():
            configuration.load_cert_chain(str(self.cert_path), str(self.key_path))
            logger.info(f"Loaded TLS certificate: {self.cert_path}")
        else:
            logger.warning("TLS certificate not found - generating self-signed certificate")
            self.generate_self_signed_cert()
            configuration.load_cert_chain(str(self.cert_path), str(self.key_path))
        
        # Security settings
        configuration.max_datagram_size = self.config.get('max_datagram_size', 1280)
        
        return configuration
    
    def generate_self_signed_cert(self):
        """Generate self-signed certificate for testing"""
        import subprocess
        
        self.cert_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info("Generating self-signed certificate...")
        
        try:
            subprocess.run([
                'openssl', 'req', '-x509', '-newkey', 'rsa:2048',
                '-keyout', str(self.key_path),
                '-out', str(self.cert_path),
                '-days', '365',
                '-nodes',
                '-subj', '/CN=euystacio.local'
            ], check=True, capture_output=True)
            
            logger.info("✓ Self-signed certificate generated")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to generate certificate: {e}")
            raise
    
    async def run(self):
        """Run the QUIC server"""
        if not AIOQUIC_AVAILABLE:
            logger.error("aioquic library not available")
            logger.error("Install with: pip install aioquic")
            return
        
        logger.info(f"Starting QUIC server on {self.host}:{self.port}")
        logger.info("Protocol: QUIC with TLS 1.3")
        logger.info(f"ALPN: {self.config.get('alpn_protocols')}")
        
        # Create QUIC configuration
        configuration = self.create_quic_configuration()
        
        # Start server
        await serve(
            self.host,
            self.port,
            configuration=configuration,
            create_protocol=SecureQuicProtocol,
        )
        
        logger.info(f"✓ QUIC server running on {self.host}:{self.port}")
        
        # Keep server running
        await asyncio.Future()

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='QUIC Server with TLS 1.3')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=4433, help='Port to bind to')
    parser.add_argument('--config', type=Path, help='Config file path')
    
    args = parser.parse_args()
    
    server = QUICServer(config_path=args.config)
    
    if args.host:
        server.host = args.host
    if args.port:
        server.port = args.port
    
    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise

if __name__ == '__main__':
    main()
