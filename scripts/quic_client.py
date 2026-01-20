#!/usr/bin/env python3
"""
QUIC Client Example
Demonstrates secure communication using QUIC with TLS 1.3
"""

import asyncio
import json
import logging
from pathlib import Path

try:
    from aioquic.asyncio.client import connect
    from aioquic.quic.configuration import QuicConfiguration
    from aioquic.asyncio.protocol import QuicConnectionProtocol
    from aioquic.quic.events import QuicEvent, StreamDataReceived
    AIOQUIC_AVAILABLE = True
except ImportError:
    AIOQUIC_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('QUICClient')

class QUICClient(QuicConnectionProtocol):
    """QUIC client protocol"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.response_received = asyncio.Event()
        self.response_data = None
    
    def quic_event_received(self, event: QuicEvent):
        """Handle QUIC events"""
        if isinstance(event, StreamDataReceived):
            self.response_data = event.data
            self.response_received.set()

async def send_message(host: str, port: int, message: dict):
    """Send message to QUIC server"""
    if not AIOQUIC_AVAILABLE:
        logger.error("aioquic not available")
        return None
    
    # Create QUIC configuration
    configuration = QuicConfiguration(
        is_client=True,
        alpn_protocols=['h3']
    )
    configuration.verify_mode = False  # For self-signed certs
    
    # Connect to server
    async with connect(host, port, configuration=configuration, create_protocol=QUICClient) as client:
        # Create stream and send message
        stream_id = client._quic.get_next_available_stream_id()
        message_data = json.dumps(message).encode('utf-8')
        client._quic.send_stream_data(stream_id, message_data, end_stream=True)
        
        # Wait for response
        await client.response_received.wait()
        
        # Parse response
        if client.response_data:
            return json.loads(client.response_data.decode('utf-8'))
    
    return None

async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='QUIC Client')
    parser.add_argument('--host', default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=4433, help='Server port')
    parser.add_argument('--message', default='ping', 
                       choices=['ping', 'status', 'data'], 
                       help='Message type to send')
    
    args = parser.parse_args()
    
    # Prepare message
    message = {'type': args.message}
    
    if args.message == 'ping':
        import time
        message['timestamp'] = time.time()
    elif args.message == 'data':
        message['payload'] = 'Hello from QUIC client!'
    
    # Send message
    logger.info(f"Connecting to {args.host}:{args.port}")
    logger.info(f"Sending: {message}")
    
    response = await send_message(args.host, args.port, message)
    
    if response:
        logger.info(f"Response: {response}")
    else:
        logger.error("No response received")

if __name__ == '__main__':
    asyncio.run(main())
