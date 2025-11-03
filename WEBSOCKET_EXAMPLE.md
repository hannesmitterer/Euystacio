# WebSocket Example - Bidirectional Messaging

This guide provides complete examples for implementing WebSocket communication with the Nexus API using Node.js.

---

## Overview

WebSocket enables real-time, bidirectional communication between clients and the Nexus API. Use cases include:

- Real-time task status updates
- Live telemetry streaming
- Agent coordination messages
- Event notifications
- Command acknowledgments

---

## Server Implementation (Node.js)

### Basic WebSocket Server

```javascript
// server/websocket.js
const WebSocket = require('ws');
const jwt = require('jsonwebtoken');

class NexusWebSocketServer {
  constructor(server) {
    this.wss = new WebSocket.Server({ server });
    this.clients = new Map(); // clientId -> { ws, channels, userId }
    
    this.setupServer();
  }

  setupServer() {
    this.wss.on('connection', (ws, req) => {
      console.log('New WebSocket connection');
      
      const clientId = this.generateClientId();
      this.clients.set(clientId, {
        ws,
        channels: new Set(),
        userId: null,
        authenticated: false
      });

      ws.on('message', (data) => this.handleMessage(clientId, data));
      ws.on('close', () => this.handleClose(clientId));
      ws.on('error', (error) => this.handleError(clientId, error));
      ws.on('pong', () => this.handlePong(clientId));

      // Send welcome message
      this.sendToClient(clientId, {
        type: 'welcome',
        client_id: clientId,
        timestamp: new Date().toISOString()
      });
    });

    // Heartbeat interval
    this.heartbeatInterval = setInterval(() => {
      this.sendHeartbeat();
    }, 30000); // 30 seconds
  }

  handleMessage(clientId, data) {
    const client = this.clients.get(clientId);
    if (!client) return;

    let message;
    try {
      message = JSON.parse(data);
    } catch (error) {
      this.sendError(clientId, 'Invalid JSON');
      return;
    }

    switch (message.type) {
      case 'auth':
        this.handleAuth(clientId, message);
        break;
      case 'subscribe':
        this.handleSubscribe(clientId, message);
        break;
      case 'unsubscribe':
        this.handleUnsubscribe(clientId, message);
        break;
      case 'ping':
        this.handlePing(clientId);
        break;
      default:
        this.sendError(clientId, `Unknown message type: ${message.type}`);
    }
  }

  handleAuth(clientId, message) {
    const client = this.clients.get(clientId);
    if (!client) return;

    const token = message.token?.replace('Bearer ', '');
    if (!token) {
      this.sendError(clientId, 'Missing token');
      return;
    }

    try {
      const decoded = jwt.verify(token, process.env.JWT_SECRET);
      client.userId = decoded.userId;
      client.authenticated = true;

      this.sendToClient(clientId, {
        type: 'auth_success',
        client_id: clientId,
        user_id: decoded.userId,
        timestamp: new Date().toISOString()
      });
    } catch (error) {
      this.sendError(clientId, 'Invalid token');
    }
  }

  handleSubscribe(clientId, message) {
    const client = this.clients.get(clientId);
    if (!client) return;

    if (!client.authenticated) {
      this.sendError(clientId, 'Not authenticated');
      return;
    }

    const channels = message.channels || [];
    channels.forEach(channel => client.channels.add(channel));

    this.sendToClient(clientId, {
      type: 'subscribed',
      channels: Array.from(client.channels),
      timestamp: new Date().toISOString()
    });
  }

  handleUnsubscribe(clientId, message) {
    const client = this.clients.get(clientId);
    if (!client) return;

    const channels = message.channels || [];
    channels.forEach(channel => client.channels.delete(channel));

    this.sendToClient(clientId, {
      type: 'unsubscribed',
      channels: channels,
      timestamp: new Date().toISOString()
    });
  }

  handlePing(clientId) {
    this.sendToClient(clientId, {
      type: 'pong',
      timestamp: new Date().toISOString()
    });
  }

  handlePong(clientId) {
    const client = this.clients.get(clientId);
    if (client) {
      client.lastPong = Date.now();
    }
  }

  handleClose(clientId) {
    console.log(`Client ${clientId} disconnected`);
    this.clients.delete(clientId);
  }

  handleError(clientId, error) {
    console.error(`WebSocket error for client ${clientId}:`, error);
  }

  sendToClient(clientId, message) {
    const client = this.clients.get(clientId);
    if (!client || client.ws.readyState !== WebSocket.OPEN) return;

    try {
      client.ws.send(JSON.stringify(message));
    } catch (error) {
      console.error('Error sending message:', error);
    }
  }

  sendError(clientId, errorMessage) {
    this.sendToClient(clientId, {
      type: 'error',
      error: errorMessage,
      timestamp: new Date().toISOString()
    });
  }

  broadcast(channel, message) {
    for (const [clientId, client] of this.clients.entries()) {
      if (client.authenticated && client.channels.has(channel)) {
        this.sendToClient(clientId, {
          ...message,
          channel,
          timestamp: new Date().toISOString()
        });
      }
    }
  }

  sendHeartbeat() {
    for (const [clientId, client] of this.clients.entries()) {
      if (client.ws.readyState === WebSocket.OPEN) {
        client.ws.ping();
      }
    }
  }

  generateClientId() {
    return `client_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  close() {
    clearInterval(this.heartbeatInterval);
    this.wss.close();
  }
}

module.exports = NexusWebSocketServer;
```

### Server Setup with Express

```javascript
// server/index.js
const express = require('express');
const http = require('http');
const NexusWebSocketServer = require('./websocket');

const app = express();
const server = http.createServer(app);
const wsServer = new NexusWebSocketServer(server);

// REST API routes
app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

app.post('/api/v1/broadcast', (req, res) => {
  const { channel, message } = req.body;
  
  wsServer.broadcast(channel, {
    type: 'broadcast',
    data: message
  });
  
  res.json({ success: true });
});

// Start server
const PORT = process.env.PORT || 8080;
server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, closing server...');
  wsServer.close();
  server.close(() => {
    console.log('Server closed');
    process.exit(0);
  });
});
```

---

## Client Implementation (Node.js)

### Basic WebSocket Client

```javascript
// client/websocket-client.js
const WebSocket = require('ws');
const EventEmitter = require('events');

class NexusWebSocketClient extends EventEmitter {
  constructor(url, token) {
    super();
    this.url = url;
    this.token = token;
    this.ws = null;
    this.authenticated = false;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 1000;
  }

  connect() {
    this.ws = new WebSocket(this.url);

    this.ws.on('open', () => {
      console.log('Connected to Nexus WebSocket');
      this.reconnectAttempts = 0;
      this.authenticate();
    });

    this.ws.on('message', (data) => {
      try {
        const message = JSON.parse(data);
        this.handleMessage(message);
      } catch (error) {
        console.error('Error parsing message:', error);
      }
    });

    this.ws.on('close', () => {
      console.log('Disconnected from Nexus WebSocket');
      this.authenticated = false;
      this.attemptReconnect();
    });

    this.ws.on('error', (error) => {
      console.error('WebSocket error:', error);
      this.emit('error', error);
    });

    this.ws.on('ping', () => {
      this.ws.pong();
    });
  }

  authenticate() {
    this.send({
      type: 'auth',
      token: `Bearer ${this.token}`
    });
  }

  handleMessage(message) {
    switch (message.type) {
      case 'welcome':
        console.log('Received welcome:', message.client_id);
        this.emit('welcome', message);
        break;
      
      case 'auth_success':
        console.log('Authentication successful');
        this.authenticated = true;
        this.emit('authenticated', message);
        break;
      
      case 'subscribed':
        console.log('Subscribed to channels:', message.channels);
        this.emit('subscribed', message);
        break;
      
      case 'task_update':
        this.emit('task_update', message.data);
        break;
      
      case 'telemetry_event':
        this.emit('telemetry_event', message.data);
        break;
      
      case 'agent_update':
        this.emit('agent_update', message.data);
        break;
      
      case 'pong':
        this.emit('pong', message);
        break;
      
      case 'error':
        console.error('Server error:', message.error);
        this.emit('server_error', message);
        break;
      
      default:
        this.emit('message', message);
    }
  }

  subscribe(channels) {
    if (!this.authenticated) {
      console.error('Cannot subscribe: not authenticated');
      return;
    }

    this.send({
      type: 'subscribe',
      channels: Array.isArray(channels) ? channels : [channels]
    });
  }

  unsubscribe(channels) {
    this.send({
      type: 'unsubscribe',
      channels: Array.isArray(channels) ? channels : [channels]
    });
  }

  ping() {
    this.send({ type: 'ping' });
  }

  send(message) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    } else {
      console.error('WebSocket not connected');
    }
  }

  attemptReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      this.emit('max_reconnect_attempts');
      return;
    }

    this.reconnectAttempts++;
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
    
    console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
    
    setTimeout(() => {
      console.log('Attempting to reconnect...');
      this.connect();
    }, delay);
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}

module.exports = NexusWebSocketClient;
```

### Client Usage Example

```javascript
// example/client-usage.js
const NexusWebSocketClient = require('./client/websocket-client');

const WS_URL = 'wss://nexus.euystacio.io/ws/v1';
const API_TOKEN = process.env.API_TOKEN;

// Create client
const client = new NexusWebSocketClient(WS_URL, API_TOKEN);

// Event handlers
client.on('authenticated', (message) => {
  console.log('Authenticated as:', message.user_id);
  
  // Subscribe to channels
  client.subscribe(['tasks', 'telemetry', 'agents']);
});

client.on('subscribed', (message) => {
  console.log('Subscribed to:', message.channels);
});

client.on('task_update', (task) => {
  console.log('Task update:', task);
  console.log(`  Task ${task.task_id}: ${task.status} (${task.progress}%)`);
});

client.on('telemetry_event', (event) => {
  console.log('Telemetry event:', event);
  console.log(`  ${event.source}: ${event.metric} = ${event.value}`);
});

client.on('agent_update', (agent) => {
  console.log('Agent update:', agent);
  console.log(`  Agent ${agent.agent_id}: ${agent.status}`);
});

client.on('error', (error) => {
  console.error('Client error:', error);
});

client.on('max_reconnect_attempts', () => {
  console.error('Failed to reconnect after maximum attempts');
  process.exit(1);
});

// Connect
client.connect();

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\nShutting down...');
  client.disconnect();
  process.exit(0);
});

// Send periodic pings
setInterval(() => {
  client.ping();
}, 30000);
```

---

## Browser Client Implementation

### Vanilla JavaScript

```javascript
// public/js/websocket-client.js
class NexusWebSocketClient {
  constructor(url, token) {
    this.url = url;
    this.token = token;
    this.ws = null;
    this.authenticated = false;
    this.handlers = {};
  }

  connect() {
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      console.log('Connected to Nexus WebSocket');
      this.authenticate();
    };

    this.ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        this.handleMessage(message);
      } catch (error) {
        console.error('Error parsing message:', error);
      }
    };

    this.ws.onclose = () => {
      console.log('Disconnected from Nexus WebSocket');
      this.authenticated = false;
      this.trigger('disconnected');
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      this.trigger('error', error);
    };
  }

  authenticate() {
    this.send({
      type: 'auth',
      token: `Bearer ${this.token}`
    });
  }

  handleMessage(message) {
    console.log('Received:', message);

    switch (message.type) {
      case 'auth_success':
        this.authenticated = true;
        this.trigger('authenticated', message);
        break;
      case 'task_update':
        this.trigger('task_update', message.data);
        break;
      case 'telemetry_event':
        this.trigger('telemetry_event', message.data);
        break;
      default:
        this.trigger('message', message);
    }
  }

  subscribe(channels) {
    this.send({
      type: 'subscribe',
      channels: Array.isArray(channels) ? channels : [channels]
    });
  }

  send(message) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    }
  }

  on(event, handler) {
    if (!this.handlers[event]) {
      this.handlers[event] = [];
    }
    this.handlers[event].push(handler);
  }

  trigger(event, data) {
    if (this.handlers[event]) {
      this.handlers[event].forEach(handler => handler(data));
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
    }
  }
}

// Usage
const client = new NexusWebSocketClient('wss://nexus.euystacio.io/ws/v1', 'YOUR_TOKEN');

client.on('authenticated', () => {
  console.log('Authenticated!');
  client.subscribe(['tasks', 'telemetry']);
});

client.on('task_update', (task) => {
  console.log('Task update:', task);
  updateTaskUI(task);
});

client.connect();
```

---

## Message Types Reference

### Client → Server

| Message Type | Description | Required Fields |
|-------------|-------------|-----------------|
| `auth` | Authenticate connection | `token` |
| `subscribe` | Subscribe to channels | `channels` (array) |
| `unsubscribe` | Unsubscribe from channels | `channels` (array) |
| `ping` | Keep-alive ping | none |

### Server → Client

| Message Type | Description | Fields |
|-------------|-------------|--------|
| `welcome` | Connection established | `client_id`, `timestamp` |
| `auth_success` | Authentication successful | `client_id`, `user_id` |
| `subscribed` | Subscription confirmed | `channels` |
| `task_update` | Task status changed | `data` (task object) |
| `telemetry_event` | New telemetry data | `data` (event object) |
| `agent_update` | Agent status changed | `data` (agent object) |
| `pong` | Ping response | `timestamp` |
| `error` | Error occurred | `error` (message) |

---

## Complete Integration Example

```javascript
// app.js - Full example with task monitoring
const NexusWebSocketClient = require('./client/websocket-client');
const axios = require('axios');

const API_URL = 'https://nexus.euystacio.io/api/v1';
const WS_URL = 'wss://nexus.euystacio.io/ws/v1';
const API_TOKEN = process.env.API_TOKEN;

// HTTP client
const api = axios.create({
  baseURL: API_URL,
  headers: { 'Authorization': `Bearer ${API_TOKEN}` }
});

// WebSocket client
const wsClient = new NexusWebSocketClient(WS_URL, API_TOKEN);

// Track tasks
const activeTasks = new Map();

// WebSocket event handlers
wsClient.on('authenticated', async () => {
  console.log('✓ WebSocket authenticated');
  wsClient.subscribe(['tasks']);
  
  // Create a test task
  const response = await api.post('/tasks', {
    title: 'Process data batch',
    type: 'data_processing',
    priority: 'high'
  });
  
  const task = response.data;
  activeTasks.set(task.task_id, task);
  console.log(`Created task ${task.task_id}`);
});

wsClient.on('task_update', (taskUpdate) => {
  const task = activeTasks.get(taskUpdate.task_id);
  if (task) {
    Object.assign(task, taskUpdate);
    console.log(`Task ${task.task_id}: ${task.status} (${task.progress}%)`);
    
    if (task.status === 'completed') {
      console.log(`✓ Task ${task.task_id} completed!`);
      activeTasks.delete(task.task_id);
    }
  }
});

// Connect
wsClient.connect();
```

---

## Testing

### Manual Testing with wscat

```bash
# Install wscat
npm install -g wscat

# Connect
wscat -c wss://nexus.euystacio.io/ws/v1

# Authenticate
> {"type":"auth","token":"Bearer YOUR_TOKEN"}

# Subscribe
> {"type":"subscribe","channels":["tasks","telemetry"]}

# Ping
> {"type":"ping"}
```

---

## Troubleshooting

**Connection refused:**
- Check WebSocket server is running
- Verify URL and port
- Check firewall/security groups

**Authentication fails:**
- Verify token is valid and not expired
- Check token format (`Bearer TOKEN`)
- Ensure JWT_SECRET matches server

**No messages received:**
- Verify subscription to correct channels
- Check client is authenticated
- Review server logs

---

**Last Updated:** 2025-11-03
