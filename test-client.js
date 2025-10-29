#!/usr/bin/env node
/**
 * Test client for WebSocket functionality
 * Tests connection, message reception, and data ingestion
 */

const http = require('http');
const WebSocket = require('ws');

const PORT = process.env.PORT || 3000;
const BASE_URL = `http://localhost:${PORT}`;
const WS_URL = `ws://localhost:${PORT}/api/v2/sentimento/live`;

async function testHealthEndpoint() {
  console.log('\n📋 Testing GET /health...');
  return new Promise((resolve, reject) => {
    http.get(`${BASE_URL}/health`, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        const response = JSON.parse(data);
        console.log('✅ Health check passed:', response.status);
        resolve(response);
      });
    }).on('error', reject);
  });
}

async function testALO001Endpoints() {
  console.log('\n🛡️  Testing ALO-001 endpoints...');
  
  const endpoints = [
    { method: 'GET', path: '/sfi' },
    { method: 'GET', path: '/mcl/live' },
  ];

  for (const endpoint of endpoints) {
    await new Promise((resolve, reject) => {
      http.get(`${BASE_URL}${endpoint.path}`, (res) => {
        let data = '';
        res.on('data', (chunk) => { data += chunk; });
        res.on('end', () => {
          const response = JSON.parse(data);
          console.log(`✅ ${endpoint.method} ${endpoint.path}:`, response.status);
          resolve(response);
        });
      }).on('error', reject);
    });
  }

  // Test POST /allocations
  await new Promise((resolve, reject) => {
    const postData = JSON.stringify({
      amount: 1000,
      recipient: 'test-recipient',
      purpose: 'testing'
    });

    const options = {
      hostname: 'localhost',
      port: PORT,
      path: '/allocations',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
      }
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        const response = JSON.parse(data);
        console.log('✅ POST /allocations:', response.status);
        resolve(response);
      });
    });

    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

async function testWebSocket() {
  console.log('\n🔌 Testing WebSocket connection...');
  
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(WS_URL);
    let messageCount = 0;

    ws.on('open', () => {
      console.log('✅ WebSocket connected');
    });

    ws.on('message', (data) => {
      const event = JSON.parse(data.toString());
      messageCount++;
      console.log(`📨 Received message ${messageCount}:`, {
        timestamp: event.timestamp,
        composites: event.composites,
        source: event.source,
        sequence: event.sequence
      });

      // Close after receiving 3 messages
      if (messageCount >= 3) {
        ws.close();
      }
    });

    ws.on('close', () => {
      console.log('✅ WebSocket closed gracefully');
      resolve(messageCount);
    });

    ws.on('error', (error) => {
      console.error('❌ WebSocket error:', error.message);
      reject(error);
    });
  });
}

async function testIngestEndpoint() {
  console.log('\n📥 Testing POST /ingest/sentimento...');
  
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify({
      composites: {
        hope: 0.75,
        sorrow: 0.25
      },
      source: 'test-client'
    });

    const options = {
      hostname: 'localhost',
      port: PORT,
      path: '/ingest/sentimento',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
      }
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        const response = JSON.parse(data);
        console.log('✅ Ingest successful:', {
          status: response.status,
          broadcasted: response.broadcasted
        });
        resolve(response);
      });
    });

    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

async function testWebSocketWithBroadcast() {
  console.log('\n🔌 Testing WebSocket with live broadcast...');
  
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(WS_URL);
    let receivedMessages = [];

    ws.on('open', async () => {
      console.log('✅ WebSocket connected');
      
      // Wait a bit for welcome message
      setTimeout(async () => {
        // Trigger a broadcast
        console.log('📤 Sending ingest request...');
        await testIngestEndpoint();
        
        // Wait for broadcast to arrive
        setTimeout(() => {
          ws.close();
        }, 1000);
      }, 500);
    });

    ws.on('message', (data) => {
      const event = JSON.parse(data.toString());
      receivedMessages.push(event);
      console.log(`📨 Received:`, {
        source: event.source,
        hope: event.composites.hope,
        sorrow: event.composites.sorrow,
        sequence: event.sequence
      });
    });

    ws.on('close', () => {
      console.log(`✅ Received ${receivedMessages.length} messages total`);
      resolve(receivedMessages);
    });

    ws.on('error', (error) => {
      console.error('❌ WebSocket error:', error.message);
      reject(error);
    });
  });
}

async function runTests() {
  console.log('🧪 Starting WebSocket API Tests');
  console.log('='.repeat(50));

  try {
    await testHealthEndpoint();
    await testALO001Endpoints();
    await testWebSocketWithBroadcast();
    
    console.log('\n' + '='.repeat(50));
    console.log('✅ All tests passed!');
    console.log('='.repeat(50));
  } catch (error) {
    console.error('\n❌ Test failed:', error.message);
    process.exit(1);
  }
}

// Run tests
runTests();
