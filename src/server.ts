/**
 * Euystacio Bridge Server
 * WebSocket API with Seed-003 metrics and ALO-001 protections
 */

import express, { Request, Response, NextFunction } from 'express';
import * as http from 'http';
import { loadConfig } from './config';
import { SentimentoWSHub } from './ws/sentimento';
import { seed003Metrics } from './metrics/seed003';
import alo001Router from './middleware/alo001';
import { SentimentoIngestPayload, SentimentoLiveEvent } from './types/sentimento';

const app = express();
const config = loadConfig();

// Middleware
app.use(express.json());

// Request logging
app.use((req: Request, res: Response, next: NextFunction) => {
  console.log(`${req.method} ${req.path}`);
  next();
});

// Health check endpoint
app.get('/health', (req: Request, res: Response) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
  });
});

// ALO-001 protected routes
app.use('/', alo001Router);

/**
 * Council-protected middleware
 * Requires valid COUNCIL_TOKEN in Authorization header
 */
function requireCouncil(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization;
  const token = authHeader?.replace('Bearer ', '');

  if (!config.councilToken || token !== config.councilToken) {
    return res.status(403).json({
      error: 'Council authorization required',
    });
  }

  next();
}

/**
 * GET /kpi/hope-ratio - Seed-003 KPI endpoint
 * Council-protected endpoint for retrieving hope ratio metrics
 */
app.get('/kpi/hope-ratio', requireCouncil, (req: Request, res: Response) => {
  const stats = seed003Metrics.getStats();
  
  res.json({
    hopeRatio: stats.hopeRatio,
    stats,
    timestamp: new Date().toISOString(),
  });
});

/**
 * POST /ingest/sentimento - Sentimento data ingestion endpoint
 * Accepts sentimento data and broadcasts via WebSocket
 * Currently unauthenticated (can be gated later)
 */
app.post('/ingest/sentimento', (req: Request, res: Response) => {
  const payload: SentimentoIngestPayload = req.body;

  // Validate payload
  if (!payload.composites || 
      typeof payload.composites.hope !== 'number' ||
      typeof payload.composites.sorrow !== 'number') {
    return res.status(400).json({
      error: 'Invalid payload: composites.hope and composites.sorrow are required',
    });
  }

  // Create event for broadcast
  const event: SentimentoLiveEvent = {
    timestamp: new Date().toISOString(),
    composites: {
      hope: payload.composites.hope,
      sorrow: payload.composites.sorrow,
    },
    source: payload.source || 'ingest',
  };

  // Broadcast to WebSocket clients (hub will be set after server starts)
  if (sentimentoHub) {
    sentimentoHub.broadcast(event);
  }

  res.json({
    status: 'ingested',
    timestamp: event.timestamp,
    broadcasted: sentimentoHub ? sentimentoHub.getClientCount() : 0,
  });
});

// 404 handler
app.use((req: Request, res: Response) => {
  res.status(404).json({
    error: 'Not found',
    path: req.path,
  });
});

// Error handler
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error('Error:', err);
  res.status(500).json({
    error: 'Internal server error',
    message: err.message,
  });
});

// Create HTTP server
const server = http.createServer(app);

// Initialize WebSocket hub
let sentimentoHub: SentimentoWSHub;

// Start server
server.listen(config.port, () => {
  console.log('='.repeat(60));
  console.log('🌉 Euystacio Bridge Server');
  console.log('='.repeat(60));
  console.log(`Port: ${config.port}`);
  console.log(`WebSocket: ws://localhost:${config.port}/api/v2/sentimento/live`);
  console.log(`Broadcast Hz: ${config.sentimentoBroadcastHz}`);
  console.log(`Buffer Max: ${config.sentimentoBufferMaxKb}KB`);
  console.log('='.repeat(60));
  console.log('Endpoints:');
  console.log('  GET  /health');
  console.log('  GET  /sfi (ALO-001)');
  console.log('  GET  /mcl/live (ALO-001)');
  console.log('  POST /allocations (ALO-001)');
  console.log('  GET  /kpi/hope-ratio (Council-protected)');
  console.log('  POST /ingest/sentimento');
  console.log('  WS   /api/v2/sentimento/live');
  console.log('='.repeat(60));

  // Initialize WebSocket hub after server starts
  sentimentoHub = new SentimentoWSHub(server, config);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');
  if (sentimentoHub) {
    sentimentoHub.shutdown();
  }
  server.close(() => {
    console.log('Server closed');
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  console.log('SIGINT received, shutting down gracefully');
  if (sentimentoHub) {
    sentimentoHub.shutdown();
  }
  server.close(() => {
    console.log('Server closed');
    process.exit(0);
  });
});
