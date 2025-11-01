import express from 'express';
import { config, validateConfig } from './config';
import { verifyGoogleToken, requireCouncil, requireSeedbringer } from './middleware/googleAuth';

// Validate configuration on startup
validateConfig();

const app = express();

// Middleware
app.use(express.json());
app.use(express.static('public'));

// Routes that require Council access
app.get('/sfi', verifyGoogleToken, requireCouncil, (req, res) => {
  res.json({ message: 'SFI access granted', status: 'success' });
});

app.get('/mcl/live', verifyGoogleToken, requireCouncil, (req, res) => {
  res.json({ message: 'MCL Live access granted', status: 'success' });
});

// Route that requires Seedbringer access
app.post('/allocations', verifyGoogleToken, requireSeedbringer, (req, res) => {
  res.json({ message: 'Allocations access granted', status: 'success', data: req.body });
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

const PORT = config.port;

app.listen(PORT, () => {
  console.log(`Euystacio ALO-001 server running on port ${PORT}`);
  console.log(`Council allowlist: ${config.councilAllowlist.length} members`);
  console.log(`Seedbringer allowlist: ${config.seedbringerAllowlist.length} members`);
});

export default app;
