import express, { Request, Response } from 'express';
import cors from 'cors';
import config from './config';
import { requireAuth, Role, AuthenticatedRequest } from './middleware/googleAuth';
import * as hopeKpi from './kpi/hope';

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Health check endpoint (public)
app.get('/health', (req: Request, res: Response) => {
  res.json({ 
    status: 'ok',
    timestamp: new Date().toISOString(),
    environment: config.nodeEnv,
  });
});

// GET /sfi - Seedbringer Financial Interface (Council or Seedbringer)
app.get('/sfi', requireAuth([Role.COUNCIL, Role.SEEDBRINGER]), (req: AuthenticatedRequest, res: Response) => {
  res.json({
    endpoint: '/sfi',
    message: 'Seedbringer Financial Interface data',
    user: {
      email: req.user?.email,
      role: req.user?.role,
      name: req.user?.name,
    },
    data: {
      // Placeholder for actual SFI data
      description: 'Sacred Financial Interface metrics',
      status: 'active',
    },
  });
});

// GET /mcl/live - Master Control Live (Council or Seedbringer)
app.get('/mcl/live', requireAuth([Role.COUNCIL, Role.SEEDBRINGER]), (req: AuthenticatedRequest, res: Response) => {
  res.json({
    endpoint: '/mcl/live',
    message: 'Master Control Live data',
    user: {
      email: req.user?.email,
      role: req.user?.role,
      name: req.user?.name,
    },
    data: {
      // Placeholder for actual MCL data
      description: 'Master Control Live metrics',
      timestamp: new Date().toISOString(),
      status: 'operational',
    },
  });
});

// POST /allocations - Resource Allocations (Seedbringer only)
app.post('/allocations', requireAuth([Role.SEEDBRINGER]), (req: AuthenticatedRequest, res: Response) => {
  const allocationData = req.body;
  
  // Validate allocation data (basic validation)
  if (!allocationData || Object.keys(allocationData).length === 0) {
    res.status(400).json({ error: 'Allocation data is required' });
    return;
  }

  res.json({
    endpoint: '/allocations',
    message: 'Allocation created successfully',
    user: {
      email: req.user?.email,
      role: req.user?.role,
      name: req.user?.name,
    },
    allocation: {
      ...allocationData,
      createdAt: new Date().toISOString(),
      createdBy: req.user?.email,
    },
  });
});

// GET /kpi/hope-ratio - Hope/Sorrow ratio KPI (Council or Seedbringer)
app.get('/kpi/hope-ratio', requireAuth([Role.COUNCIL, Role.SEEDBRINGER]), (req: AuthenticatedRequest, res: Response) => {
  const kpi = hopeKpi.getRollingKpi();
  res.json({
    kpi,
    principal: req.user?.email,
  });
});

// POST /ingest/sentimento - Ingest sorrow/hope samples (public, unauthenticated in this PR)
app.post('/ingest/sentimento', (req: Request, res: Response) => {
  const { sorrow, hope } = req.body;
  
  // Validate input
  if (typeof sorrow !== 'number' || typeof hope !== 'number') {
    res.status(400).json({ error: 'sorrow and hope must be numbers' });
    return;
  }
  
  if (sorrow < 0 || sorrow > 1 || hope < 0 || hope > 1) {
    res.status(400).json({ error: 'sorrow and hope must be in [0,1] range' });
    return;
  }
  
  hopeKpi.pushSample(sorrow, hope);
  res.json({ 
    status: 'accepted',
    timestamp: new Date().toISOString(),
  });
});

// Catch-all for undefined routes
app.use('*', (req: Request, res: Response) => {
  res.status(404).json({ 
    error: 'Not found',
    message: `Route ${req.method} ${req.originalUrl} does not exist`,
  });
});

// Start server
const PORT = config.port;
app.listen(PORT, () => {
  console.log(`🚀 Euystacio Backend API running on port ${PORT}`);
  console.log(`Environment: ${config.nodeEnv}`);
  console.log(`Seedbringer emails: ${config.seedbringerEmails.length} configured`);
  console.log(`Council emails: ${config.councilEmails.length} configured`);
});

export default app;
