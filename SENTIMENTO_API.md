# Euystacio Sentimento Live WebSocket API

## Overview

This implementation provides a real-time WebSocket API for broadcasting Sentimento metrics, integrated with Seed-003 analytics and protected by ALO-001 access controls.

## Architecture

### Components

1. **Express HTTP Server** (`src/server.ts`)
   - Single HTTP server serving REST endpoints and WebSocket upgrades
   - ALO-001 protected routes with email-based allowlists
   - Public health and ingestion endpoints
   - Council-readable KPI endpoints

2. **SentimentoWSHub** (`src/ws/sentimento.ts`)
   - WebSocket connection manager
   - Backpressure-aware broadcast system
   - Seed-003 metrics integration
   - Client lifecycle management

3. **Type Definitions** (`src/types/sentimento.ts`)
   - Canonical `SentimentoLiveEvent` interface
   - Ingestion payload types

## API Endpoints

### Public Endpoints

#### GET /health
Health check and status endpoint.

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-10-31T00:00:00.000Z",
  "uptime": 123.456,
  "websocket": {
    "clients": 0
  },
  "seed003": {
    "sampleCount": 10,
    "hopeRatio": 0.7
  }
}
```

#### POST /ingest/sentimento
**Unauthenticated** sentimento data ingestion endpoint.

**Request:**
```json
{
  "composites": {
    "hope": 0.7,
    "sorrow": 0.3
  }
}
```

**Response:**
```json
{
  "status": "accepted",
  "timestamp": "2025-10-31T00:00:00.000Z",
  "composites": {
    "hope": 0.7,
    "sorrow": 0.3
  },
  "broadcast": {
    "clients": 5
  }
}
```

### ALO-001 Protected Endpoints

These endpoints require `x-auth-email` header with an allowlisted email.

**Seedbringer Allowlist:**
- hannes.mitterer@gmail.com

**Council Allowlist:**
- dietmar.zuegg@gmail.com
- bioarchitettura.rivista@gmail.com
- consultant.laquila@gmail.com

#### GET /sfi
Seedbringer Financial Interface (placeholder).

**Headers:** `x-auth-email: hannes.mitterer@gmail.com`

#### GET /mcl/live
Mission Critical Live feed (placeholder).

**Headers:** `x-auth-email: hannes.mitterer@gmail.com`

#### POST /allocations
Resource allocation endpoint (placeholder).

**Headers:** `x-auth-email: hannes.mitterer@gmail.com`

### Council-Only Endpoints

#### GET /kpi/hope-ratio
Returns hope-to-total ratio from Seed-003 metrics.

**Headers:** `x-auth-email: dietmar.zuegg@gmail.com`

**Response:**
```json
{
  "hopeRatio": 0.7,
  "sampleCount": 10,
  "timestamp": "2025-10-31T00:00:00.000Z",
  "description": "Hope-to-total ratio from Seed-003 rolling window"
}
```

## WebSocket Endpoint

### ws://[host]/api/v2/sentimento/live

Real-time broadcast of sentimento events.

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:3000/api/v2/sentimento/live');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Sentimento event:', data);
};
```

**Message Format (SentimentoLiveEvent):**
```json
{
  "timestamp": "2025-10-31T00:00:00.000Z",
  "composites": {
    "hope": 0.7,
    "sorrow": 0.3
  },
  "seed003": {
    "sampleCount": 10,
    "hopeRatio": 0.7
  },
  "sequence": 123
}
```

### Backpressure Handling

The WebSocket hub implements automatic backpressure handling:
- Monitors client buffer levels
- Drops messages for clients exceeding `SENTIMENTO_BUFFER_MAX_KB`
- Prevents memory exhaustion and server overload

## Configuration

Environment variables (see `.env.example`):

- `PORT` - HTTP server port (default: 3000)
- `SENTIMENTO_BROADCAST_HZ` - Broadcast frequency limit (default: 10)
- `SENTIMENTO_BUFFER_MAX_KB` - Client buffer threshold for backpressure (default: 512)
- `NODE_ENV` - Environment mode (development/production)

## Seed-003 Metrics

The system maintains rolling 60-second windows of sentimento samples:

- **Sample Count**: Number of samples in current window
- **Hope Ratio**: `totalHope / (totalHope + totalSorrow)`

Metrics are:
- Updated on each ingestion via `pushSample(sorrow, hope)`
- Included in every WebSocket broadcast
- Available via `/health` and `/kpi/hope-ratio` endpoints

## Installation & Usage

### Install Dependencies
```bash
npm install
```

### Build
```bash
npm run build
```

### Start Server
```bash
npm start
```

### Development Mode
```bash
npm run dev
```

## Testing

### Manual Endpoint Tests

```bash
# Health check
curl http://localhost:3000/health

# Ingest sentimento data
curl -X POST http://localhost:3000/ingest/sentimento \
  -H "Content-Type: application/json" \
  -d '{"composites":{"hope":0.7,"sorrow":0.3}}'

# Get hope ratio (Council)
curl -H "x-auth-email: dietmar.zuegg@gmail.com" \
  http://localhost:3000/kpi/hope-ratio

# Access ALO-001 protected endpoint
curl -H "x-auth-email: hannes.mitterer@gmail.com" \
  http://localhost:3000/sfi
```

## Security

### ALO-001 Access Control

Protected endpoints implement strict email-based allowlists:
- Seedbringer: Full access to all ALO-001 routes
- Council: Read-only access to KPI endpoints
- Unauthorized requests return 403 Forbidden

### WebSocket Security

- Path-based routing prevents unauthorized upgrades
- Client connection limits via backpressure
- Graceful error handling and cleanup

## TypeScript Strictness

This implementation uses strict TypeScript configuration:
- `strict: true`
- No implicit any
- Strict null checks
- Unused parameter detection
- Comprehensive type safety

## License

See `SACRED_COMMONS_LICENSE.md`
