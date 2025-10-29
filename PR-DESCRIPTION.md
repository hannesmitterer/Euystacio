# Expanded WebSocket API - fseap-001/sentimento-live

## Summary

This PR implements the finalized Expanded WebSocket API and wires it into Seed-003 metrics, preserving all ALO-001 protections.

## Features Implemented

### 1. WebSocket Live Stream
- Real-time WebSocket endpoint at `wss://<host>/api/v2/sentimento/live`
- Broadcasts `SentimentoLiveEvent` payloads to all connected clients
- Automatic backpressure control to prevent client overload
- Sequence numbering for event ordering

### 2. Seed-003 Metrics Integration
- KPI tracking system that captures hope/sorrow samples from every broadcast
- Rolling window of last 1000 samples
- Calculates hope ratio: `hope / (hope + sorrow)`
- Council-protected endpoint at `GET /kpi/hope-ratio` for accessing metrics

### 3. ALO-001 Protected Routes
Preserves all sacred interface routes:
- `GET /sfi` - Sacred Funding Interface
- `GET /mcl/live` - Market Consciousness Live
- `POST /allocations` - Resource allocation requests

### 4. Data Ingestion
- `POST /ingest/sentimento` - Accept sentiment data and broadcast to WebSocket clients
- Currently unauthenticated (can be gated in future iterations)

### 5. Health & Monitoring
- `GET /health` - Basic health check endpoint
- Graceful shutdown handling
- Comprehensive logging

## JSON Schema

### WebSocket Event Schema

**Endpoint:** `wss://<host>/api/v2/sentimento/live`

**Event Type:** `SentimentoLiveEvent`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SentimentoLiveEvent",
  "description": "Real-time sentimento event broadcast to WebSocket clients",
  "type": "object",
  "required": ["timestamp", "composites"],
  "properties": {
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp of the event"
    },
    "composites": {
      "type": "object",
      "required": ["hope", "sorrow"],
      "properties": {
        "hope": {
          "type": "number",
          "description": "Hope value (typically 0-1 range)"
        },
        "sorrow": {
          "type": "number",
          "description": "Sorrow value (typically 0-1 range)"
        }
      }
    },
    "source": {
      "type": "string",
      "description": "Optional source identifier (e.g., 'ingest', 'welcome')"
    },
    "sequence": {
      "type": "integer",
      "description": "Sequence number for event ordering"
    }
  }
}
```

**Example Event:**
```json
{
  "timestamp": "2025-10-29T22:00:00.000Z",
  "composites": {
    "hope": 0.75,
    "sorrow": 0.25
  },
  "source": "ingest",
  "sequence": 42
}
```

### Ingest Request Schema

**Endpoint:** `POST /ingest/sentimento`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SentimentoIngestPayload",
  "description": "Payload for ingesting sentimento data",
  "type": "object",
  "required": ["composites"],
  "properties": {
    "composites": {
      "type": "object",
      "required": ["hope", "sorrow"],
      "properties": {
        "hope": {
          "type": "number",
          "description": "Hope value"
        },
        "sorrow": {
          "type": "number",
          "description": "Sorrow value"
        }
      }
    },
    "source": {
      "type": "string",
      "description": "Optional source identifier"
    },
    "metadata": {
      "type": "object",
      "description": "Optional metadata",
      "additionalProperties": true
    }
  }
}
```

**Example Request:**
```json
{
  "composites": {
    "hope": 0.75,
    "sorrow": 0.25
  },
  "source": "external-service"
}
```

### KPI Response Schema

**Endpoint:** `GET /kpi/hope-ratio` (Requires `Authorization: Bearer <COUNCIL_TOKEN>`)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "HopeRatioKPI",
  "description": "Seed-003 hope ratio KPI response",
  "type": "object",
  "required": ["hopeRatio", "stats", "timestamp"],
  "properties": {
    "hopeRatio": {
      "type": "number",
      "description": "Current hope ratio (0-1)",
      "minimum": 0,
      "maximum": 1
    },
    "stats": {
      "type": "object",
      "required": ["sampleCount", "hopeRatio", "avgHope", "avgSorrow"],
      "properties": {
        "sampleCount": {
          "type": "integer",
          "description": "Number of samples in the rolling window"
        },
        "hopeRatio": {
          "type": "number",
          "description": "Hope ratio (same as top-level)"
        },
        "avgHope": {
          "type": "number",
          "description": "Average hope value"
        },
        "avgSorrow": {
          "type": "number",
          "description": "Average sorrow value"
        }
      }
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp of the response"
    }
  }
}
```

**Example Response:**
```json
{
  "hopeRatio": 0.75,
  "stats": {
    "sampleCount": 100,
    "hopeRatio": 0.75,
    "avgHope": 0.7,
    "avgSorrow": 0.3
  },
  "timestamp": "2025-10-29T22:00:00.000Z"
}
```

## Configuration

### Environment Variables

```bash
# Server port
PORT=3000

# Sentimento WebSocket configuration
SENTIMENTO_BROADCAST_HZ=10          # Broadcast frequency hint (informational)
SENTIMENTO_BUFFER_MAX_KB=512        # Max buffer size before dropping sends

# Council authentication
COUNCIL_TOKEN=your-secret-token     # Required for /kpi/hope-ratio endpoint
```

## Architecture

### Components

- **`src/server.ts`** - Express HTTP server with WebSocket upgrade handling
- **`src/ws/sentimento.ts`** - WebSocket hub managing client connections and broadcasts
- **`src/metrics/seed003.ts`** - Seed-003 KPI tracking system
- **`src/middleware/alo001.ts`** - ALO-001 protected route handlers
- **`src/types/sentimento.ts`** - TypeScript type definitions
- **`src/config.ts`** - Configuration management

### Security Features

1. **Council Protection**: `/kpi/hope-ratio` requires Bearer token authentication
2. **ALO-001 Routes**: Protected endpoints for sacred interfaces
3. **Input Validation**: Request payload validation on all POST endpoints
4. **Backpressure Control**: Automatic protection against client flooding
5. **Error Handling**: Comprehensive error handling and logging

### Backpressure Control

The WebSocket hub monitors each client's `bufferedAmount` and:
- Drops sends when buffer exceeds `SENTIMENTO_BUFFER_MAX_KB * 1024` bytes
- Prevents memory exhaustion on the server
- Logs warnings when backpressure is applied

## Testing

All functionality has been tested:
- ✅ HTTP endpoints (health, ALO-001 routes, ingest, KPI)
- ✅ WebSocket connection and message reception
- ✅ Council-protected endpoint authentication
- ✅ Broadcast functionality with sequence numbering
- ✅ Seed-003 metrics integration
- ✅ Error handling and edge cases

Run tests with:
```bash
# Terminal 1: Start server
npm start

# Terminal 2: Run test client
node test-client.js
```

## Security Scan

✅ CodeQL security scan completed with **0 vulnerabilities**

## Documentation

- **`README-API.md`** - Comprehensive API documentation
- **`.env.example`** - Example environment configuration
- **`test-client.js`** - Test client demonstrating all features

## Files Changed

- Created: `package.json`, `tsconfig.json`, `.gitignore`, `.env.example`
- Created: `src/server.ts`, `src/config.ts`
- Created: `src/types/sentimento.ts`
- Created: `src/ws/sentimento.ts`
- Created: `src/metrics/seed003.ts`
- Created: `src/middleware/alo001.ts`
- Created: `README-API.md`
- Created: `test-client.js`

## Migration Notes

This is a new Node.js/TypeScript server implementation. No existing code was modified.

To deploy:
1. Install dependencies: `npm install`
2. Configure environment variables (copy `.env.example` to `.env`)
3. Build: `npm run build`
4. Run: `npm start`
