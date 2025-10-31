# FSEAP-001: Sentimento Live WebSocket API + Seed-003 Server Patch

## Summary

This PR implements a complete Node.js/TypeScript backend for real-time Sentimento data broadcasting via WebSocket, integrated with Seed-003 metrics tracking and protected by ALO-001 access controls.

## Implementation Details

### Dependencies Added

**Production:**
- `express` ^4.18.2 - HTTP server framework
- `ws` ^8.14.2 - WebSocket library

**Development:**
- `@types/express` ^4.17.20
- `@types/node` ^20.8.10
- `@types/ws` ^8.5.8
- `typescript` ^5.2.2
- `ts-node` ^10.9.1
- `eslint` ^8.52.0
- `@typescript-eslint/parser` ^6.9.1
- `@typescript-eslint/eslint-plugin` ^6.9.1

### Files Created

1. **src/types/sentimento.ts** - Canonical type definitions
   - `SentimentoLiveEvent` interface for WebSocket broadcasts
   - `SentimentoIngestPayload` interface for ingestion endpoint

2. **src/ws/sentimento.ts** - WebSocket hub implementation
   - `SentimentoWSHub` class managing WebSocket connections
   - `Seed003Metrics` class for 60-second rolling window analytics
   - Backpressure handling with configurable buffer limits
   - Automatic client lifecycle management

3. **src/server.ts** - Express server with WebSocket upgrade
   - Single HTTP server handling both REST and WebSocket
   - ALO-001 protected routes with email allowlist
   - Council-readable KPI endpoints
   - Unauthenticated ingestion endpoint
   - Graceful shutdown handling

4. **.env.example** - Environment configuration template
   - `PORT=3000`
   - `SENTIMENTO_BROADCAST_HZ=10` (reserved for future use)
   - `SENTIMENTO_BUFFER_MAX_KB=512`
   - `NODE_ENV=production`

5. **package.json** - Project configuration
6. **tsconfig.json** - TypeScript strict mode configuration
7. **.gitignore** - Node.js ignore patterns
8. **SENTIMENTO_API.md** - Complete API documentation

### ALO-001 Allowlists (Preserved)

**Seedbringer (Full Access):**
- hannes.mitterer@gmail.com

**Council (KPI Read Access):**
- dietmar.zuegg@gmail.com
- bioarchitettura.rivista@gmail.com
- consultant.laquila@gmail.com

### API Endpoints

#### Public Endpoints
- `GET /health` - Health check with system metrics
- `POST /ingest/sentimento` - Unauthenticated ingestion (accepts composites)

#### ALO-001 Protected (Seedbringer Only)
- `GET /sfi` - Seedbringer Financial Interface
- `GET /mcl/live` - Mission Critical Live feed
- `POST /allocations` - Resource allocation endpoint

#### Council Protected
- `GET /kpi/hope-ratio` - Hope ratio metric from Seed-003

#### WebSocket
- `ws://[host]/api/v2/sentimento/live` - Real-time broadcast endpoint

### Canonical JSON Schemas

**SentimentoLiveEvent (WebSocket broadcast):**
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

**SentimentoIngestPayload (POST /ingest/sentimento):**
```json
{
  "composites": {
    "hope": 0.7,
    "sorrow": 0.3
  }
}
```

### Seed-003 Integration

- Rolling 60-second window for sample tracking
- Automatic sample registration via `pushSample(sorrow, hope)`
- Real-time calculation of hope-to-total ratio
- Metrics included in every WebSocket broadcast
- Available via `/health` and `/kpi/hope-ratio` endpoints

### Security Features

1. **ALO-001 Email Allowlisting**
   - Strict email-based access control
   - Separate allowlists for Seedbringer and Council
   - 403 Forbidden for unauthorized access

2. **WebSocket Security**
   - Path-based routing prevents unauthorized upgrades
   - Backpressure handling prevents DoS
   - Graceful error handling and cleanup

3. **TypeScript Strict Mode**
   - Full type safety
   - No implicit any
   - Strict null checks
   - Comprehensive error handling

### Testing Performed

✅ TypeScript strict mode compilation  
✅ Server startup and configuration  
✅ Health endpoint functionality  
✅ Ingestion and broadcasting  
✅ Seed-003 metrics tracking  
✅ ALO-001 authentication  
✅ Council authentication  
✅ Unauthorized access rejection  
✅ WebSocket upgrade handling  
✅ Code review completed  
✅ CodeQL security scan (0 alerts)

### Build and Run

```bash
# Install dependencies
npm install

# Build TypeScript
npm run build

# Start server
npm start

# Development mode
npm run dev
```

## Compliance

- ✅ All ALO-001 protections preserved
- ✅ Seed-003 metrics integration complete
- ✅ WebSocket API fully functional
- ✅ TypeScript strict mode enabled
- ✅ No security vulnerabilities detected
- ✅ Comprehensive documentation provided

## Commit Message

```
FSEAP-001: Sentimento Live WebSocket API + Seed-003 server patch
```

## PR Title

```
FSEAP-001: Sentimento Live WebSocket API + Seed-003 server patch
```

## Request

Please auto-merge (squash) after all checks pass.
