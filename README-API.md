# Euystacio Bridge - WebSocket API

Euystacio Bridge Server with WebSocket API, Seed-003 metrics tracking, and ALO-001 protections.

## Features

- **WebSocket Live Stream**: Real-time sentimento event broadcasting at `/api/v2/sentimento/live`
- **Seed-003 Metrics**: KPI tracking for hope/sorrow ratios with Council-protected access
- **ALO-001 Protection**: Sacred interface routes for funding, consciousness, and allocations
- **Backpressure Control**: Automatic buffer management to prevent client overload
- **TypeScript**: Full type safety and modern development experience

## Quick Start

### Installation

```bash
npm install
```

### Configuration

Copy `.env.example` to `.env` and configure:

```env
PORT=3000
SENTIMENTO_BROADCAST_HZ=10
SENTIMENTO_BUFFER_MAX_KB=512
COUNCIL_TOKEN=your-secret-token
```

### Development

```bash
# Build TypeScript
npm run build

# Run in development mode with auto-reload
npm run dev

# Run in production mode
npm start
```

### Testing

Start the server, then run the test client:

```bash
# Terminal 1: Start server
npm start

# Terminal 2: Run tests
node test-client.js
```

## API Endpoints

### HTTP Endpoints

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-29T22:00:00.000Z",
  "uptime": 123.456
}
```

#### `GET /sfi` (ALO-001)
Sacred Funding Interface - Protected endpoint for sacred funding mechanisms.

**Response:**
```json
{
  "status": "active",
  "message": "Sacred Funding Interface - ALO-001 protected",
  "timestamp": "2025-10-29T22:00:00.000Z"
}
```

#### `GET /mcl/live` (ALO-001)
Market Consciousness Live - Protected endpoint for real-time market consciousness data.

**Response:**
```json
{
  "status": "streaming",
  "message": "Market Consciousness Live - ALO-001 protected",
  "timestamp": "2025-10-29T22:00:00.000Z",
  "data": {
    "consciousness": "active",
    "marketPulse": "steady"
  }
}
```

#### `POST /allocations` (ALO-001)
Resource allocation endpoint.

**Request:**
```json
{
  "amount": 1000,
  "recipient": "recipient-id",
  "purpose": "description"
}
```

**Response:**
```json
{
  "status": "received",
  "message": "Allocation request processed - ALO-001 protected",
  "timestamp": "2025-10-29T22:00:00.000Z",
  "allocation": {
    "amount": 1000,
    "recipient": "recipient-id",
    "purpose": "description"
  }
}
```

#### `GET /kpi/hope-ratio` (Council-Protected)
Retrieve hope ratio KPI from Seed-003 metrics. Requires Council authorization.

**Headers:**
```
Authorization: Bearer <COUNCIL_TOKEN>
```

**Response:**
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

#### `POST /ingest/sentimento`
Ingest sentimento data and broadcast to WebSocket clients.

**Request:**
```json
{
  "composites": {
    "hope": 0.75,
    "sorrow": 0.25
  },
  "source": "source-identifier"
}
```

**Response:**
```json
{
  "status": "ingested",
  "timestamp": "2025-10-29T22:00:00.000Z",
  "broadcasted": 5
}
```

### WebSocket Endpoint

#### `WS /api/v2/sentimento/live`
Real-time sentimento event stream.

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:3000/api/v2/sentimento/live');

ws.on('message', (data) => {
  const event = JSON.parse(data.toString());
  console.log(event);
});
```

**Event Schema (SentimentoLiveEvent):**
```typescript
{
  timestamp: string;        // ISO 8601 timestamp
  composites: {
    hope: number;          // Hope value
    sorrow: number;        // Sorrow value
  };
  source?: string;         // Optional source identifier
  sequence?: number;       // Sequence number for ordering
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

## Architecture

### Components

- **`src/server.ts`**: Express HTTP server with WebSocket upgrade handling
- **`src/ws/sentimento.ts`**: WebSocket hub managing client connections and broadcasts
- **`src/metrics/seed003.ts`**: Seed-003 KPI tracking system
- **`src/middleware/alo001.ts`**: ALO-001 protected route handlers
- **`src/types/sentimento.ts`**: TypeScript type definitions
- **`src/config.ts`**: Configuration management

### Backpressure Control

The WebSocket hub implements backpressure control to prevent overwhelming slow clients:

- Monitors `bufferedAmount` per client
- Drops sends when buffer exceeds `SENTIMENTO_BUFFER_MAX_KB`
- Prevents memory exhaustion on the server

### Seed-003 Metrics

Every broadcast event feeds into Seed-003 metrics via `pushSample(sorrow, hope)`:

- Maintains rolling window of last 1000 samples
- Calculates hope ratio: `hope / (hope + sorrow)`
- Provides statistical analysis of sentiment over time

## Security

- **Council Protection**: `/kpi/hope-ratio` requires Bearer token authentication
- **ALO-001 Routes**: Protected endpoints for sacred interfaces
- **Input Validation**: Request payload validation on all POST endpoints
- **Backpressure**: Automatic protection against client flooding

## License

See SACRED_COMMONS_LICENSE.md
