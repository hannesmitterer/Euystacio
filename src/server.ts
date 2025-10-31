import express, { Request, Response, NextFunction } from 'express';
import { createServer } from 'http';
import { SentimentoWSHub } from './ws/sentimento';
import { SentimentoIngestPayload } from './types/sentimento';

const app = express();

// Parse JSON bodies
app.use(express.json());

// Request logging middleware
app.use((req: Request, _res: Response, next: NextFunction) => {
  console.log(`${new Date().toISOString()} ${req.method} ${req.path}`);
  next();
});

// Create single HTTP server from Express app
const server = createServer(app);

// Configuration from environment
const SENTIMENTO_BROADCAST_HZ = parseInt(process.env.SENTIMENTO_BROADCAST_HZ || '10', 10);
const SENTIMENTO_BUFFER_MAX_KB = parseInt(process.env.SENTIMENTO_BUFFER_MAX_KB || '512', 10);
const PORT = parseInt(process.env.PORT || '3000', 10);

// Initialize SentimentoWSHub
const wsHub = new SentimentoWSHub(server, {
  broadcastHz: SENTIMENTO_BROADCAST_HZ,
  bufferMaxKb: SENTIMENTO_BUFFER_MAX_KB
});

console.log('[Server] SentimentoWSHub initialized');

// ============================================================================
// ALO-001 Protected Routes (Seedbringer & Council access)
// ============================================================================

/**
 * ALO-001 Authentication Middleware
 * Allowlists:
 * - Seedbringer: hannes.mitterer@gmail.com
 * - Council: dietmar.zuegg@gmail.com, bioarchitettura.rivista@gmail.com, consultant.laquila@gmail.com
 */
const ALO_001_ALLOWLIST = [
  'hannes.mitterer@gmail.com',      // Seedbringer
  'dietmar.zuegg@gmail.com',        // Council
  'bioarchitettura.rivista@gmail.com', // Council
  'consultant.laquila@gmail.com'    // Council
];

function alo001Auth(req: Request, res: Response, next: NextFunction): void {
  const email = req.headers['x-auth-email'] as string;
  
  if (!email || !ALO_001_ALLOWLIST.includes(email.toLowerCase())) {
    res.status(403).json({ 
      error: 'Forbidden',
      message: 'ALO-001: Access restricted to Seedbringer and Council only'
    });
    return;
  }
  
  next();
}

/**
 * Council-only Authentication Middleware
 * Allows Council members only (excludes Seedbringer for read-only endpoints)
 */
const COUNCIL_ALLOWLIST = [
  'dietmar.zuegg@gmail.com',
  'bioarchitettura.rivista@gmail.com',
  'consultant.laquila@gmail.com'
];

function councilAuth(req: Request, res: Response, next: NextFunction): void {
  const email = req.headers['x-auth-email'] as string;
  
  if (!email || !COUNCIL_ALLOWLIST.includes(email.toLowerCase())) {
    res.status(403).json({ 
      error: 'Forbidden',
      message: 'Council access required'
    });
    return;
  }
  
  next();
}

/**
 * GET /sfi
 * ALO-001 Protected: Seedbringer Financial Interface
 */
app.get('/sfi', alo001Auth, (_req: Request, res: Response) => {
  res.json({
    status: 'active',
    interface: 'Seedbringer Financial Interface',
    timestamp: new Date().toISOString(),
    message: 'ALO-001 protected endpoint - implementation pending'
  });
});

/**
 * GET /mcl/live
 * ALO-001 Protected: Mission Critical Live feed
 */
app.get('/mcl/live', alo001Auth, (_req: Request, res: Response) => {
  res.json({
    status: 'active',
    feed: 'Mission Critical Live',
    timestamp: new Date().toISOString(),
    seed003: wsHub.getSeed003Metrics(),
    connectedClients: wsHub.getClientCount(),
    message: 'ALO-001 protected endpoint - implementation pending'
  });
});

/**
 * POST /allocations
 * ALO-001 Protected: Resource allocation endpoint
 */
app.post('/allocations', alo001Auth, (req: Request, res: Response) => {
  res.json({
    status: 'received',
    endpoint: 'Resource Allocations',
    timestamp: new Date().toISOString(),
    payload: req.body,
    message: 'ALO-001 protected endpoint - implementation pending'
  });
});

// ============================================================================
// Public Routes
// ============================================================================

/**
 * GET /health
 * Health check endpoint
 */
app.get('/health', (_req: Request, res: Response) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    websocket: {
      clients: wsHub.getClientCount()
    },
    seed003: wsHub.getSeed003Metrics()
  });
});

// ============================================================================
// KPI Routes
// ============================================================================

/**
 * GET /kpi/hope-ratio
 * Council-readable hope ratio metric from Seed-003
 */
app.get('/kpi/hope-ratio', councilAuth, (_req: Request, res: Response) => {
  const metrics = wsHub.getSeed003Metrics();
  
  res.json({
    hopeRatio: metrics.hopeRatio,
    sampleCount: metrics.sampleCount,
    timestamp: new Date().toISOString(),
    description: 'Hope-to-total ratio from Seed-003 rolling window'
  });
});

// ============================================================================
// Ingestion Routes
// ============================================================================

/**
 * POST /ingest/sentimento
 * Unauthenticated scaffold for sentimento data ingestion
 * Accepts composites (hope, sorrow) and broadcasts to WebSocket clients
 */
app.post('/ingest/sentimento', (req: Request, res: Response) => {
  try {
    const payload = req.body as SentimentoIngestPayload;
    
    // Validate payload structure
    if (!payload.composites || 
        typeof payload.composites.hope !== 'number' ||
        typeof payload.composites.sorrow !== 'number') {
      res.status(400).json({
        error: 'Invalid payload',
        message: 'Expected: { composites: { hope: number, sorrow: number } }'
      });
      return;
    }

    // Validate ranges (0.0 to 1.0)
    const { hope, sorrow } = payload.composites;
    if (hope < 0 || hope > 1 || sorrow < 0 || sorrow > 1) {
      res.status(400).json({
        error: 'Invalid range',
        message: 'Hope and sorrow must be between 0.0 and 1.0'
      });
      return;
    }

    // Broadcast to WebSocket clients
    wsHub.broadcast(hope, sorrow);

    res.json({
      status: 'accepted',
      timestamp: new Date().toISOString(),
      composites: { hope, sorrow },
      broadcast: {
        clients: wsHub.getClientCount()
      }
    });
  } catch (error) {
    console.error('[Server] Ingest error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to process sentimento ingestion'
    });
  }
});

// ============================================================================
// Error Handling
// ============================================================================

// 404 handler
app.use((req: Request, res: Response) => {
  res.status(404).json({
    error: 'Not Found',
    path: req.path
  });
});

// Global error handler
app.use((err: Error, _req: Request, res: Response, _next: NextFunction) => {
  console.error('[Server] Error:', err);
  res.status(500).json({
    error: 'Internal Server Error',
    message: process.env.NODE_ENV === 'development' ? err.message : 'An error occurred'
  });
});

// ============================================================================
// Server Startup
// ============================================================================

server.listen(PORT, () => {
  console.log(`[Server] Euystacio Sentimento API listening on port ${PORT}`);
  console.log(`[Server] WebSocket endpoint: ws://localhost:${PORT}/api/v2/sentimento/live`);
  console.log(`[Server] ALO-001 protected routes active`);
  console.log(`[Server] Broadcast: ${SENTIMENTO_BROADCAST_HZ}Hz, Buffer limit: ${SENTIMENTO_BUFFER_MAX_KB}KB`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('[Server] SIGTERM received, shutting down gracefully...');
  server.close(() => {
    console.log('[Server] HTTP server closed');
    wsHub.close();
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  console.log('[Server] SIGINT received, shutting down gracefully...');
  server.close(() => {
    console.log('[Server] HTTP server closed');
    wsHub.close();
    process.exit(0);
  });
});

export { app, server, wsHub };
