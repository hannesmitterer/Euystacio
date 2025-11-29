# GGI Broadcast Integration Guide

This guide covers integrating the Nexus API with GGI Broadcast for distributed event broadcasting and webhook-based communication.

---

## Overview

GGI (Global Gateway Interface) Broadcast is a distributed messaging system that allows the Nexus API to send and receive events across multiple services and platforms.

### Key Features

- **Event Broadcasting:** Publish events to multiple subscribers
- **Webhook Integration:** Receive events via HTTP callbacks
- **Message Queuing:** Guaranteed delivery with retry logic
- **Topic-based Routing:** Subscribe to specific event types
- **Authentication:** Secure communication with API keys

---

## Architecture

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│  Nexus API   │────────▶│GGI Broadcast │────────▶│ Subscribers  │
│              │         │              │         │ (Webhooks)   │
└──────────────┘         └──────────────┘         └──────────────┘
       │                        │
       │                        ▼
       └──────────────────▶ Event Log
                          (Audit Trail)
```

---

## GGI Broadcast Setup

### Step 1: Register with GGI Broadcast

1. Sign up at: https://ggi-broadcast.example.com
2. Create a new application: `Euystacio Nexus`
3. Note your credentials:
   - **API Key:** `ggi_abc123xyz...`
   - **Webhook Secret:** `whsec_abc123...`
   - **Base URL:** `https://api.ggi-broadcast.example.com/v1`

### Step 2: Configure Environment Variables

Add to your `.env` file:

```bash
# GGI Broadcast Configuration
GGI_BROADCAST_API_KEY=ggi_abc123xyz...
GGI_BROADCAST_WEBHOOK_SECRET=whsec_abc123...
GGI_BROADCAST_BASE_URL=https://api.ggi-broadcast.example.com/v1

# Webhook Configuration
GGI_WEBHOOK_URL=https://nexus.euystacio.io/webhooks/ggi
GGI_WEBHOOK_ENABLED=true

# Retry Configuration
GGI_MAX_RETRIES=3
GGI_RETRY_DELAY=1000
```

---

## Publishing Events to GGI Broadcast

### Basic Event Publishing

```javascript
// services/ggi-broadcast.js
const axios = require('axios');
const crypto = require('crypto');

class GGIBroadcastService {
  constructor() {
    this.apiKey = process.env.GGI_BROADCAST_API_KEY;
    this.baseUrl = process.env.GGI_BROADCAST_BASE_URL;
    this.client = axios.create({
      baseURL: this.baseUrl,
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json'
      }
    });
  }

  /**
   * Publish an event to GGI Broadcast
   */
  async publishEvent(topic, event) {
    try {
      const response = await this.client.post('/events/publish', {
        topic,
        event_type: event.type,
        payload: event.data,
        timestamp: new Date().toISOString(),
        metadata: {
          source: 'nexus-api',
          version: '1.0.0',
          ...event.metadata
        }
      });

      return {
        success: true,
        event_id: response.data.event_id,
        published_at: response.data.published_at
      };
    } catch (error) {
      console.error('GGI Broadcast publish error:', error.response?.data || error.message);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Publish task update event
   */
  async publishTaskUpdate(task) {
    return this.publishEvent('nexus.tasks', {
      type: 'task.updated',
      data: {
        task_id: task.id,
        title: task.title,
        status: task.status,
        progress: task.progress,
        assigned_to: task.assignedTo,
        updated_at: task.updatedAt
      },
      metadata: {
        priority: task.priority,
        task_type: task.type
      }
    });
  }

  /**
   * Publish telemetry event
   */
  async publishTelemetry(telemetry) {
    return this.publishEvent('nexus.telemetry', {
      type: 'telemetry.metric',
      data: {
        source: telemetry.source,
        metric: telemetry.metric,
        value: telemetry.value,
        unit: telemetry.unit,
        timestamp: telemetry.timestamp
      },
      metadata: {
        tags: telemetry.tags
      }
    });
  }

  /**
   * Publish agent status event
   */
  async publishAgentStatus(agent) {
    return this.publishEvent('nexus.agents', {
      type: 'agent.status',
      data: {
        agent_id: agent.id,
        status: agent.status,
        current_tasks: agent.currentTasks,
        load: agent.load,
        last_heartbeat: agent.lastHeartbeat
      }
    });
  }

  /**
   * Subscribe to a topic via webhook
   */
  async subscribe(topic, webhookUrl) {
    try {
      const response = await this.client.post('/subscriptions', {
        topic,
        webhook_url: webhookUrl,
        secret: process.env.GGI_BROADCAST_WEBHOOK_SECRET,
        events: ['*'], // Subscribe to all events on this topic
        active: true
      });

      return {
        success: true,
        subscription_id: response.data.subscription_id
      };
    } catch (error) {
      console.error('GGI subscription error:', error.response?.data || error.message);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Verify webhook signature
   */
  verifyWebhookSignature(payload, signature, timestamp) {
    const secret = process.env.GGI_BROADCAST_WEBHOOK_SECRET;
    const signedPayload = `${timestamp}.${JSON.stringify(payload)}`;
    const expectedSignature = crypto
      .createHmac('sha256', secret)
      .update(signedPayload)
      .digest('hex');

    return crypto.timingSafeEqual(
      Buffer.from(signature),
      Buffer.from(expectedSignature)
    );
  }
}

module.exports = new GGIBroadcastService();
```

---

## Receiving Events via Webhooks

### Webhook Endpoint Implementation

```javascript
// routes/webhooks.js
const express = require('express');
const router = express.Router();
const ggiBroadcast = require('../services/ggi-broadcast');

/**
 * GGI Broadcast webhook endpoint
 */
router.post('/ggi', express.json(), (req, res) => {
  const signature = req.headers['x-ggi-signature'];
  const timestamp = req.headers['x-ggi-timestamp'];
  const payload = req.body;

  // Verify signature
  if (!ggiBroadcast.verifyWebhookSignature(payload, signature, timestamp)) {
    console.error('Invalid webhook signature');
    return res.status(401).json({ error: 'Invalid signature' });
  }

  // Check timestamp freshness (prevent replay attacks)
  const timestampMs = parseInt(timestamp);
  const currentMs = Date.now();
  const maxAge = 5 * 60 * 1000; // 5 minutes

  if (Math.abs(currentMs - timestampMs) > maxAge) {
    console.error('Webhook timestamp too old');
    return res.status(401).json({ error: 'Timestamp too old' });
  }

  // Process event
  handleGGIEvent(payload)
    .then(() => {
      res.status(200).json({ received: true });
    })
    .catch(error => {
      console.error('Error processing webhook:', error);
      res.status(500).json({ error: 'Processing failed' });
    });
});

/**
 * Handle incoming GGI event
 */
async function handleGGIEvent(event) {
  console.log('Received GGI event:', event.event_type);

  switch (event.event_type) {
    case 'task.priority_changed':
      await handleTaskPriorityChange(event.payload);
      break;
    
    case 'agent.command':
      await handleAgentCommand(event.payload);
      break;
    
    case 'telemetry.alert':
      await handleTelemetryAlert(event.payload);
      break;
    
    default:
      console.log('Unhandled event type:', event.event_type);
  }
}

async function handleTaskPriorityChange(payload) {
  // Update task priority based on external event
  const { task_id, new_priority } = payload;
  console.log(`Updating task ${task_id} priority to ${new_priority}`);
  // Implementation here...
}

async function handleAgentCommand(payload) {
  // Execute command on agent
  const { agent_id, command, parameters } = payload;
  console.log(`Executing command ${command} on agent ${agent_id}`);
  // Implementation here...
}

async function handleTelemetryAlert(payload) {
  // Handle telemetry alert
  const { source, metric, threshold, value } = payload;
  console.log(`Alert: ${source} ${metric} = ${value} (threshold: ${threshold})`);
  // Implementation here...
}

module.exports = router;
```

### Register Webhook Endpoint

```javascript
// app.js
const express = require('express');
const webhooksRouter = require('./routes/webhooks');

const app = express();

// Webhooks (no auth required, verified via signature)
app.use('/webhooks', webhooksRouter);

// Start server
app.listen(8080, () => {
  console.log('Server running on port 8080');
});
```

---

## Event Types and Schemas

### Task Events

**Topic:** `nexus.tasks`

```json
{
  "event_type": "task.created",
  "payload": {
    "task_id": "task_1234567890",
    "title": "Process data batch",
    "status": "pending",
    "priority": "high",
    "created_at": "2025-11-03T01:53:00Z"
  }
}
```

```json
{
  "event_type": "task.updated",
  "payload": {
    "task_id": "task_1234567890",
    "status": "in_progress",
    "progress": 45,
    "updated_at": "2025-11-03T02:00:00Z"
  }
}
```

```json
{
  "event_type": "task.completed",
  "payload": {
    "task_id": "task_1234567890",
    "status": "completed",
    "result": {
      "success": true,
      "records_processed": 1000
    },
    "completed_at": "2025-11-03T02:10:00Z"
  }
}
```

### Telemetry Events

**Topic:** `nexus.telemetry`

```json
{
  "event_type": "telemetry.metric",
  "payload": {
    "source": "agent-001",
    "metric": "cpu_usage",
    "value": 75.5,
    "unit": "percent",
    "timestamp": "2025-11-03T01:53:00Z",
    "tags": {
      "environment": "production",
      "region": "us-west"
    }
  }
}
```

```json
{
  "event_type": "telemetry.alert",
  "payload": {
    "source": "monitoring-service",
    "metric": "error_rate",
    "threshold": 5.0,
    "value": 8.2,
    "severity": "warning",
    "timestamp": "2025-11-03T01:53:00Z"
  }
}
```

### Agent Events

**Topic:** `nexus.agents`

```json
{
  "event_type": "agent.registered",
  "payload": {
    "agent_id": "agent-003",
    "agent_type": "task_processor",
    "capabilities": ["data_processing", "validation"],
    "registered_at": "2025-11-03T01:53:00Z"
  }
}
```

```json
{
  "event_type": "agent.status",
  "payload": {
    "agent_id": "agent-001",
    "status": "active",
    "current_tasks": 3,
    "load": 0.6,
    "last_heartbeat": "2025-11-03T01:52:55Z"
  }
}
```

---

## Integration Examples

### Example 1: Publishing Task Updates

```javascript
// In your task service
const ggiBroadcast = require('../services/ggi-broadcast');

async function updateTask(taskId, updates) {
  // Update task in database
  const task = await TaskModel.findByIdAndUpdate(taskId, updates, { new: true });
  
  // Publish to GGI Broadcast
  await ggiBroadcast.publishTaskUpdate(task);
  
  return task;
}
```

### Example 2: Subscribing to External Events

```javascript
// Setup script to subscribe to topics
const ggiBroadcast = require('./services/ggi-broadcast');

async function setupSubscriptions() {
  const webhookUrl = `${process.env.BASE_URL}/webhooks/ggi`;
  
  // Subscribe to task priority changes from external system
  await ggiBroadcast.subscribe('external.task_priority', webhookUrl);
  
  // Subscribe to agent commands
  await ggiBroadcast.subscribe('external.agent_commands', webhookUrl);
  
  // Subscribe to telemetry alerts
  await ggiBroadcast.subscribe('external.telemetry_alerts', webhookUrl);
  
  console.log('GGI subscriptions configured');
}

setupSubscriptions();
```

### Example 3: Broadcasting to Multiple Services

```javascript
// Broadcast task completion to multiple services
async function completeTask(taskId) {
  const task = await TaskModel.findById(taskId);
  task.status = 'completed';
  task.completedAt = new Date();
  await task.save();
  
  // Publish to GGI Broadcast
  await ggiBroadcast.publishEvent('nexus.tasks', {
    type: 'task.completed',
    data: {
      task_id: task.id,
      title: task.title,
      result: task.result,
      completed_at: task.completedAt
    }
  });
  
  // All subscribers will receive this event
  // - Analytics service
  // - Notification service
  // - Billing service
  // - Audit logging service
}
```

---

## Testing

### Test Event Publishing

```javascript
// test/ggi-broadcast.test.js
const ggiBroadcast = require('../services/ggi-broadcast');

async function testPublish() {
  const result = await ggiBroadcast.publishEvent('nexus.test', {
    type: 'test.event',
    data: { message: 'Hello GGI!' }
  });
  
  console.log('Publish result:', result);
}

testPublish();
```

### Test Webhook Signature Verification

```javascript
const crypto = require('crypto');
const ggiBroadcast = require('../services/ggi-broadcast');

function testSignatureVerification() {
  const payload = { event_type: 'test', data: {} };
  const timestamp = Date.now().toString();
  const secret = process.env.GGI_BROADCAST_WEBHOOK_SECRET;
  
  const signedPayload = `${timestamp}.${JSON.stringify(payload)}`;
  const signature = crypto
    .createHmac('sha256', secret)
    .update(signedPayload)
    .digest('hex');
  
  const isValid = ggiBroadcast.verifyWebhookSignature(payload, signature, timestamp);
  console.log('Signature valid:', isValid);
}

testSignatureVerification();
```

---

## Security Best Practices

### Webhook Security

1. **Verify Signatures:** Always verify webhook signatures
2. **Check Timestamps:** Reject old timestamps to prevent replay attacks
3. **Use HTTPS:** Only accept webhooks over HTTPS
4. **Rate Limiting:** Implement rate limiting on webhook endpoints
5. **Idempotency:** Handle duplicate events gracefully

### API Key Security

1. **Store Securely:** Never commit API keys to Git
2. **Rotate Regularly:** Rotate keys every 90 days
3. **Use Environment Variables:** Store in `.env` files
4. **Monitor Usage:** Track API key usage for anomalies

---

## Troubleshooting

### Event Not Published

- Check API key is valid
- Verify topic name is correct
- Review GGI Broadcast logs
- Check network connectivity

### Webhook Not Received

- Verify webhook URL is accessible
- Check signature verification
- Review webhook endpoint logs
- Test with GGI Broadcast test event

### Signature Verification Fails

- Ensure webhook secret matches
- Check timestamp format
- Verify payload is not modified
- Review signature algorithm

---

## Monitoring and Logging

```javascript
// Log all GGI events
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'ggi-events.log' })
  ]
});

// Log published events
async function publishWithLogging(topic, event) {
  logger.info('Publishing event', { topic, event_type: event.type });
  const result = await ggiBroadcast.publishEvent(topic, event);
  logger.info('Publish result', { result });
  return result;
}

// Log received webhooks
function logWebhookReceived(event) {
  logger.info('Webhook received', {
    event_type: event.event_type,
    timestamp: event.timestamp
  });
}
```

---

## Resources

- **GGI Broadcast Documentation:** https://docs.ggi-broadcast.example.com
- **API Reference:** https://api.ggi-broadcast.example.com/docs
- **Support:** support@ggi-broadcast.example.com

---

**Last Updated:** 2025-11-03
