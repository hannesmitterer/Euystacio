# Nexus API Specification

**Version:** 1.0.0  
**Last Updated:** 2025-11-03

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Authentication & Authorization](#authentication--authorization)
4. [Core Endpoints](#core-endpoints)
5. [Telemetry System](#telemetry-system)
6. [Command Interface](#command-interface)
7. [Task Management](#task-management)
8. [AI Coordination](#ai-coordination)
9. [Security & Rate Limiting](#security--rate-limiting)
10. [Event System](#event-system)
11. [WebSocket Protocol](#websocket-protocol)
12. [Example Workflows](#example-workflows)

---

## Overview

The Nexus API provides a unified interface for coordinating AI agents, managing tasks, processing telemetry, and facilitating secure communication between distributed systems. It serves as the central nervous system for the Euystacio ecosystem.

### Key Features

- **Real-time telemetry** streaming and aggregation
- **Task orchestration** with dependency management
- **AI agent coordination** with context sharing
- **Secure authentication** via OAuth 2.0 and API keys
- **Event-driven architecture** with WebSocket support
- **Rate limiting** and abuse prevention
- **Audit logging** for compliance and debugging

### Base URL

```
Production:  https://nexus.euystacio.io/api/v1
Staging:     https://staging-nexus.euystacio.io/api/v1
Development: http://localhost:8080/api/v1
```

---

## Architecture

### System Components

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Clients   │────▶│  API Gateway │────▶│   Services  │
│  (Web/CLI)  │     │  (Rate Limit)│     │ (Task/Agent)│
└─────────────┘     └──────────────┘     └─────────────┘
                            │                     │
                            ▼                     ▼
                    ┌──────────────┐     ┌─────────────┐
                    │  Event Bus   │     │  Database   │
                    │ (WebSocket)  │     │ (Postgres)  │
                    └──────────────┘     └─────────────┘
```

### Data Flow

1. **Ingress**: Clients send requests via REST or WebSocket
2. **Authentication**: OAuth tokens or API keys validated
3. **Rate Limiting**: Request throttling per user/IP
4. **Processing**: Business logic execution
5. **Event Emission**: Real-time updates via WebSocket
6. **Response**: JSON or Protocol Buffer response

---

## Authentication & Authorization

### OAuth 2.0 Flow

The Nexus API supports OAuth 2.0 for user authentication:

```
GET /oauth/authorize
  ?client_id=YOUR_CLIENT_ID
  &redirect_uri=https://your-app.com/callback
  &response_type=code
  &scope=telemetry:read tasks:write

POST /oauth/token
  {
    "grant_type": "authorization_code",
    "code": "AUTH_CODE",
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "redirect_uri": "https://your-app.com/callback"
  }
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "def50200...",
  "scope": "telemetry:read tasks:write"
}
```

### API Key Authentication

For service-to-service communication:

```
GET /api/v1/tasks
Authorization: Bearer YOUR_API_KEY
```

### Available Scopes

| Scope | Description |
|-------|-------------|
| `telemetry:read` | Read telemetry data |
| `telemetry:write` | Submit telemetry events |
| `tasks:read` | View tasks and their status |
| `tasks:write` | Create and modify tasks |
| `tasks:execute` | Execute task commands |
| `agents:read` | View AI agent information |
| `agents:coordinate` | Coordinate AI agent actions |
| `admin:full` | Full administrative access |

---

## Core Endpoints

### Health Check

**GET** `/health`

Returns API health status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime": 86400,
  "timestamp": "2025-11-03T01:53:00Z"
}
```

### System Status

**GET** `/status`

Returns detailed system metrics.

**Headers:**
```
Authorization: Bearer {token}
```

**Response:**
```json
{
  "services": {
    "database": "healthy",
    "event_bus": "healthy",
    "task_processor": "healthy"
  },
  "metrics": {
    "active_tasks": 42,
    "connected_clients": 128,
    "events_per_minute": 1500
  },
  "version": "1.0.0"
}
```

---

## Telemetry System

### Submit Telemetry Event

**POST** `/telemetry/events`

Submits a telemetry event for processing.

**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "source": "agent-001",
  "event_type": "metric",
  "timestamp": "2025-11-03T01:53:00Z",
  "data": {
    "cpu_usage": 45.2,
    "memory_usage": 1024,
    "custom_metric": "value"
  },
  "tags": {
    "environment": "production",
    "region": "us-west"
  }
}
```

**Response:**
```json
{
  "event_id": "evt_1234567890",
  "status": "accepted",
  "timestamp": "2025-11-03T01:53:00Z"
}
```

### Query Telemetry

**GET** `/telemetry/query`

Query historical telemetry data.

**Query Parameters:**
- `source`: Filter by source (optional)
- `event_type`: Filter by event type (optional)
- `from`: Start timestamp (ISO 8601)
- `to`: End timestamp (ISO 8601)
- `limit`: Max results (default: 100, max: 1000)
- `offset`: Pagination offset

**Response:**
```json
{
  "events": [
    {
      "event_id": "evt_1234567890",
      "source": "agent-001",
      "event_type": "metric",
      "timestamp": "2025-11-03T01:53:00Z",
      "data": { "cpu_usage": 45.2 }
    }
  ],
  "pagination": {
    "total": 500,
    "limit": 100,
    "offset": 0,
    "has_more": true
  }
}
```

### Telemetry Aggregation

**POST** `/telemetry/aggregate`

Aggregate telemetry data over time windows.

**Request Body:**
```json
{
  "source": "agent-001",
  "event_type": "metric",
  "metric": "cpu_usage",
  "aggregation": "avg",
  "window": "5m",
  "from": "2025-11-03T00:00:00Z",
  "to": "2025-11-03T02:00:00Z"
}
```

**Response:**
```json
{
  "metric": "cpu_usage",
  "aggregation": "avg",
  "window": "5m",
  "data_points": [
    {
      "timestamp": "2025-11-03T01:50:00Z",
      "value": 42.1
    },
    {
      "timestamp": "2025-11-03T01:55:00Z",
      "value": 45.2
    }
  ]
}
```

---

## Command Interface

### Execute Command

**POST** `/commands/execute`

Execute a command on a target agent or service.

**Request Body:**
```json
{
  "target": "agent-001",
  "command": "restart_service",
  "parameters": {
    "service_name": "telemetry_processor",
    "graceful": true
  },
  "timeout_ms": 30000,
  "idempotency_key": "cmd_unique_12345"
}
```

**Response:**
```json
{
  "command_id": "cmd_1234567890",
  "status": "pending",
  "submitted_at": "2025-11-03T01:53:00Z",
  "estimated_completion": "2025-11-03T01:53:30Z"
}
```

### Get Command Status

**GET** `/commands/{command_id}`

Retrieve the status of a previously submitted command.

**Response:**
```json
{
  "command_id": "cmd_1234567890",
  "status": "completed",
  "result": {
    "success": true,
    "output": "Service restarted successfully",
    "duration_ms": 2500
  },
  "submitted_at": "2025-11-03T01:53:00Z",
  "completed_at": "2025-11-03T01:53:02Z"
}
```

### Cancel Command

**POST** `/commands/{command_id}/cancel`

Attempt to cancel a pending or in-progress command.

**Response:**
```json
{
  "command_id": "cmd_1234567890",
  "status": "cancelled",
  "cancelled_at": "2025-11-03T01:53:05Z"
}
```

---

## Task Management

### Create Task

**POST** `/tasks`

Create a new task in the system.

**Request Body:**
```json
{
  "title": "Process user data import",
  "description": "Import and validate user data from CSV",
  "type": "data_processing",
  "priority": "high",
  "assigned_to": "agent-002",
  "dependencies": ["task_9876"],
  "parameters": {
    "file_path": "/data/import/users.csv",
    "validation_rules": ["email", "phone"]
  },
  "deadline": "2025-11-03T12:00:00Z",
  "tags": ["import", "data-validation"]
}
```

**Response:**
```json
{
  "task_id": "task_1234567890",
  "status": "pending",
  "created_at": "2025-11-03T01:53:00Z",
  "estimated_start": "2025-11-03T02:00:00Z"
}
```

### Get Task

**GET** `/tasks/{task_id}`

Retrieve task details.

**Response:**
```json
{
  "task_id": "task_1234567890",
  "title": "Process user data import",
  "status": "in_progress",
  "progress": 45,
  "assigned_to": "agent-002",
  "created_at": "2025-11-03T01:53:00Z",
  "started_at": "2025-11-03T02:00:00Z",
  "updated_at": "2025-11-03T02:05:00Z"
}
```

### List Tasks

**GET** `/tasks`

List tasks with filtering and pagination.

**Query Parameters:**
- `status`: Filter by status (pending, in_progress, completed, failed)
- `assigned_to`: Filter by assignee
- `type`: Filter by task type
- `priority`: Filter by priority
- `page`: Page number (default: 1)
- `limit`: Results per page (default: 20, max: 100)

**Response:**
```json
{
  "tasks": [
    {
      "task_id": "task_1234567890",
      "title": "Process user data import",
      "status": "in_progress",
      "priority": "high",
      "assigned_to": "agent-002"
    }
  ],
  "pagination": {
    "total": 50,
    "page": 1,
    "limit": 20,
    "total_pages": 3
  }
}
```

### Update Task

**PATCH** `/tasks/{task_id}`

Update task properties.

**Request Body:**
```json
{
  "status": "completed",
  "progress": 100,
  "result": {
    "records_processed": 1000,
    "errors": 0
  }
}
```

### Delete Task

**DELETE** `/tasks/{task_id}`

Delete a task (only if not started).

**Response:**
```json
{
  "task_id": "task_1234567890",
  "status": "deleted",
  "deleted_at": "2025-11-03T01:53:00Z"
}
```

---

## AI Coordination

### Register Agent

**POST** `/agents/register`

Register a new AI agent in the system.

**Request Body:**
```json
{
  "agent_id": "agent-003",
  "agent_type": "task_processor",
  "capabilities": ["data_processing", "validation", "transformation"],
  "metadata": {
    "version": "2.1.0",
    "model": "gpt-4",
    "max_concurrent_tasks": 5
  }
}
```

**Response:**
```json
{
  "agent_id": "agent-003",
  "status": "registered",
  "api_key": "agt_abc123xyz...",
  "registered_at": "2025-11-03T01:53:00Z"
}
```

### Get Agent Status

**GET** `/agents/{agent_id}`

Retrieve agent information and status.

**Response:**
```json
{
  "agent_id": "agent-003",
  "status": "active",
  "capabilities": ["data_processing", "validation"],
  "current_tasks": 3,
  "max_concurrent_tasks": 5,
  "last_heartbeat": "2025-11-03T01:52:55Z"
}
```

### Agent Heartbeat

**POST** `/agents/{agent_id}/heartbeat`

Send agent heartbeat to indicate active status.

**Request Body:**
```json
{
  "status": "active",
  "current_load": 0.6,
  "metrics": {
    "tasks_completed": 150,
    "errors": 2
  }
}
```

**Response:**
```json
{
  "acknowledged": true,
  "next_heartbeat_expected": "2025-11-03T01:54:00Z"
}
```

### Request Agent Coordination

**POST** `/agents/coordinate`

Request coordination between multiple agents.

**Request Body:**
```json
{
  "coordinator": "agent-001",
  "participants": ["agent-002", "agent-003"],
  "task_id": "task_1234567890",
  "coordination_type": "parallel_processing",
  "context": {
    "data_partition": "shard_1_of_3"
  }
}
```

**Response:**
```json
{
  "coordination_id": "coord_9876543210",
  "status": "initiated",
  "participants": ["agent-002", "agent-003"],
  "created_at": "2025-11-03T01:53:00Z"
}
```

---

## Security & Rate Limiting

### Rate Limits

Rate limits are enforced per user/API key:

| Tier | Requests/min | Burst |
|------|--------------|-------|
| Free | 60 | 10 |
| Basic | 600 | 100 |
| Pro | 6000 | 1000 |
| Enterprise | Custom | Custom |

**Rate Limit Headers:**
```
X-RateLimit-Limit: 600
X-RateLimit-Remaining: 599
X-RateLimit-Reset: 1698969180
```

### Session Management

**POST** `/sessions/create`

Create a new authenticated session.

**Request Body:**
```json
{
  "user_id": "user_12345",
  "device_id": "device_abc",
  "ttl_seconds": 3600
}
```

**Response:**
```json
{
  "session_id": "sess_xyz789",
  "expires_at": "2025-11-03T02:53:00Z",
  "session_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**GET** `/sessions/{session_id}/validate`

Validate an active session.

**DELETE** `/sessions/{session_id}`

Terminate a session.

### Audit Logs

**GET** `/audit/logs`

Retrieve audit logs (admin only).

**Query Parameters:**
- `user_id`: Filter by user
- `action`: Filter by action type
- `from`: Start timestamp
- `to`: End timestamp
- `limit`: Max results

**Response:**
```json
{
  "logs": [
    {
      "log_id": "log_1234567890",
      "user_id": "user_12345",
      "action": "task_created",
      "resource": "task_1234567890",
      "timestamp": "2025-11-03T01:53:00Z",
      "ip_address": "192.168.1.1",
      "user_agent": "Mozilla/5.0..."
    }
  ]
}
```

---

## Event System

### Event Types

| Event Type | Description |
|------------|-------------|
| `task.created` | New task created |
| `task.started` | Task execution started |
| `task.completed` | Task completed successfully |
| `task.failed` | Task execution failed |
| `agent.registered` | New agent registered |
| `agent.offline` | Agent went offline |
| `telemetry.alert` | Telemetry threshold exceeded |
| `command.executed` | Command executed |

### Subscribe to Events

**POST** `/events/subscribe`

Subscribe to event types via webhook.

**Request Body:**
```json
{
  "webhook_url": "https://your-service.com/webhooks/nexus",
  "event_types": ["task.completed", "task.failed"],
  "secret": "webhook_secret_key",
  "filter": {
    "assigned_to": "agent-002"
  }
}
```

**Response:**
```json
{
  "subscription_id": "sub_1234567890",
  "status": "active",
  "created_at": "2025-11-03T01:53:00Z"
}
```

### Webhook Payload

When an event occurs, Nexus sends a POST request to your webhook URL:

**Headers:**
```
Content-Type: application/json
X-Nexus-Signature: sha256=...
X-Nexus-Event: task.completed
X-Nexus-Delivery: uuid-of-delivery
```

**Body:**
```json
{
  "event_type": "task.completed",
  "event_id": "evt_1234567890",
  "timestamp": "2025-11-03T01:53:00Z",
  "data": {
    "task_id": "task_1234567890",
    "result": {
      "success": true,
      "records_processed": 1000
    }
  }
}
```

---

## WebSocket Protocol

### Connection

Connect to the WebSocket endpoint:

```
wss://nexus.euystacio.io/ws/v1
```

**Initial handshake:**
```json
{
  "type": "auth",
  "token": "Bearer YOUR_TOKEN"
}
```

**Server response:**
```json
{
  "type": "auth_success",
  "client_id": "client_abc123",
  "timestamp": "2025-11-03T01:53:00Z"
}
```

### Subscribe to Channels

```json
{
  "type": "subscribe",
  "channels": ["tasks", "telemetry", "agents"]
}
```

### Real-time Messages

**Task Update:**
```json
{
  "type": "task_update",
  "channel": "tasks",
  "data": {
    "task_id": "task_1234567890",
    "status": "in_progress",
    "progress": 45
  },
  "timestamp": "2025-11-03T01:53:00Z"
}
```

**Telemetry Event:**
```json
{
  "type": "telemetry_event",
  "channel": "telemetry",
  "data": {
    "source": "agent-001",
    "metric": "cpu_usage",
    "value": 45.2
  },
  "timestamp": "2025-11-03T01:53:00Z"
}
```

### Ping/Pong

Keep connection alive with periodic ping:

```json
{
  "type": "ping"
}
```

Server responds:
```json
{
  "type": "pong",
  "timestamp": "2025-11-03T01:53:00Z"
}
```

---

## Example Workflows

### Workflow 1: Task Creation and Monitoring

```javascript
// 1. Create a task
const taskResponse = await fetch('https://nexus.euystacio.io/api/v1/tasks', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: 'Process data batch',
    type: 'data_processing',
    priority: 'high',
    assigned_to: 'agent-002'
  })
});

const { task_id } = await taskResponse.json();

// 2. Monitor via WebSocket
const ws = new WebSocket('wss://nexus.euystacio.io/ws/v1');

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'auth',
    token: 'Bearer YOUR_TOKEN'
  }));
};

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  if (message.type === 'task_update' && message.data.task_id === task_id) {
    console.log('Task progress:', message.data.progress);
  }
};

// 3. Subscribe to task updates
ws.send(JSON.stringify({
  type: 'subscribe',
  channels: ['tasks']
}));
```

### Workflow 2: Telemetry Collection and Alerting

```python
import requests
import time

API_BASE = 'https://nexus.euystacio.io/api/v1'
HEADERS = {'Authorization': 'Bearer YOUR_TOKEN'}

# Submit telemetry periodically
def submit_telemetry(cpu_usage, memory_usage):
    payload = {
        'source': 'monitoring-agent',
        'event_type': 'metric',
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'data': {
            'cpu_usage': cpu_usage,
            'memory_usage': memory_usage
        }
    }
    response = requests.post(
        f'{API_BASE}/telemetry/events',
        headers=HEADERS,
        json=payload
    )
    return response.json()

# Query aggregated metrics
def get_avg_cpu(window='5m'):
    payload = {
        'source': 'monitoring-agent',
        'event_type': 'metric',
        'metric': 'cpu_usage',
        'aggregation': 'avg',
        'window': window,
        'from': '2025-11-03T00:00:00Z',
        'to': '2025-11-03T02:00:00Z'
    }
    response = requests.post(
        f'{API_BASE}/telemetry/aggregate',
        headers=HEADERS,
        json=payload
    )
    return response.json()
```

### Workflow 3: Multi-Agent Coordination

```javascript
// 1. Register agents
const agents = ['agent-001', 'agent-002', 'agent-003'];
for (const agentId of agents) {
  await fetch('https://nexus.euystacio.io/api/v1/agents/register', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer YOUR_TOKEN',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      agent_id: agentId,
      agent_type: 'task_processor',
      capabilities: ['data_processing']
    })
  });
}

// 2. Create a distributed task
const taskResponse = await fetch('https://nexus.euystacio.io/api/v1/tasks', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: 'Distributed data processing',
    type: 'data_processing',
    priority: 'high'
  })
});

const { task_id } = await taskResponse.json();

// 3. Coordinate agents
await fetch('https://nexus.euystacio.io/api/v1/agents/coordinate', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    coordinator: 'agent-001',
    participants: ['agent-002', 'agent-003'],
    task_id: task_id,
    coordination_type: 'parallel_processing'
  })
});
```

---

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid task priority value",
    "details": {
      "field": "priority",
      "allowed_values": ["low", "medium", "high", "critical"]
    },
    "request_id": "req_1234567890",
    "timestamp": "2025-11-03T01:53:00Z"
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid request data |
| `UNAUTHORIZED` | 401 | Missing or invalid auth token |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |

---

## Versioning

The API uses URL-based versioning:
- Current version: `v1`
- Breaking changes will increment the version number
- Old versions supported for 12 months after deprecation notice

---

## Support

- **Documentation:** https://docs.euystacio.io/nexus-api
- **Status Page:** https://status.euystacio.io
- **Support:** support@euystacio.io
- **GitHub:** https://github.com/hannesmitterer/Euystacio

---

**End of Specification**
