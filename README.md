# Euystacio Nexus API

**Version:** 1.0.0  
**The Holy Bridge - Unified AI Coordination Platform**

[![CI Status](https://github.com/hannesmitterer/Euystacio/actions/workflows/ci.yml/badge.svg)](https://github.com/hannesmitterer/Euystacio/actions/workflows/ci.yml)
[![Tests](https://github.com/hannesmitterer/Euystacio/actions/workflows/test.yml/badge.svg)](https://github.com/hannesmitterer/Euystacio/actions/workflows/test.yml)
[![Lint](https://github.com/hannesmitterer/Euystacio/actions/workflows/lint.yml/badge.svg)](https://github.com/hannesmitterer/Euystacio/actions/workflows/lint.yml)
[![Security](https://github.com/hannesmitterer/Euystacio/actions/workflows/security.yml/badge.svg)](https://github.com/hannesmitterer/Euystacio/actions/workflows/security.yml)
[![Deploy Pages](https://github.com/hannesmitterer/Euystacio/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/hannesmitterer/Euystacio/actions/workflows/deploy-pages.yml)

---

## Overview

Euystacio Nexus is a comprehensive API platform for coordinating AI agents, managing distributed tasks, processing real-time telemetry, and facilitating secure communication across the Euystacio ecosystem. It serves as the central nervous system for AI-powered applications.

### Key Features

✨ **Real-time Telemetry** - Stream and aggregate metrics from distributed agents  
🤖 **AI Agent Coordination** - Orchestrate multiple AI agents working in parallel  
📋 **Task Management** - Create, track, and manage tasks with dependencies  
🔐 **Secure Authentication** - OAuth 2.0 and API key authentication  
⚡ **WebSocket Support** - Real-time bidirectional communication  
🛡️ **Rate Limiting** - Built-in abuse prevention and fair usage  
📊 **Event System** - Subscribe to events via webhooks  
🔍 **Audit Logging** - Complete audit trail for compliance

---

## Quick Start

### Prerequisites

- Node.js 18+ or Python 3.9+
- PostgreSQL 14+
- Redis 6+ (for rate limiting)
- Valid OAuth credentials or API key

### Installation

```bash
# Clone the repository
git clone https://github.com/hannesmitterer/Euystacio.git
cd Euystacio

# Install dependencies (Node.js)
npm install

# Or for Python
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
npm run migrate  # or python manage.py migrate

# Start the server
npm start  # or python app.py
```

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Server Configuration
NODE_ENV=development
PORT=8080
API_VERSION=v1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/nexus_db
REDIS_URL=redis://localhost:6379

# OAuth 2.0
OAUTH_CLIENT_ID=your_client_id_here
OAUTH_CLIENT_SECRET=your_client_secret_here
OAUTH_REDIRECT_URI=http://localhost:8080/oauth/callback

# JWT
JWT_SECRET=your_jwt_secret_here
JWT_EXPIRATION=3600

# API Keys
API_KEY_SALT=your_api_key_salt_here

# Rate Limiting
RATE_LIMIT_FREE_TIER=60
RATE_LIMIT_BASIC_TIER=600
RATE_LIMIT_PRO_TIER=6000

# WebSocket
WS_PORT=8081
WS_HEARTBEAT_INTERVAL=30000

# Gmail API (optional, for notifications)
GMAIL_CLIENT_ID=your_gmail_client_id
GMAIL_CLIENT_SECRET=your_gmail_client_secret
GMAIL_REFRESH_TOKEN=your_refresh_token

# External Services
GGI_BROADCAST_WEBHOOK_URL=https://ggi.example.com/webhooks
GGI_BROADCAST_API_KEY=your_ggi_api_key

# Security
SESSION_SECRET=your_session_secret_here
CORS_ORIGIN=http://localhost:3000

# Logging
LOG_LEVEL=info
LOG_FILE=logs/nexus.log
```

---

## API Documentation

### Base URL

```
Development: http://localhost:8080/api/v1
Production:  https://nexus.euystacio.io/api/v1
```

### Authentication

All API requests require authentication via Bearer token:

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://nexus.euystacio.io/api/v1/tasks
```

### Basic Example

Create a task:

```bash
curl -X POST https://nexus.euystacio.io/api/v1/tasks \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Process data import",
    "type": "data_processing",
    "priority": "high",
    "assigned_to": "agent-001"
  }'
```

---

## Core Endpoints

### Health Check
```
GET /health
```

### Tasks
```
POST   /tasks              Create a new task
GET    /tasks              List all tasks
GET    /tasks/{id}         Get task details
PATCH  /tasks/{id}         Update task
DELETE /tasks/{id}         Delete task
```

### Telemetry
```
POST /telemetry/events      Submit telemetry event
GET  /telemetry/query       Query historical data
POST /telemetry/aggregate   Aggregate metrics
```

### Commands
```
POST /commands/execute      Execute command
GET  /commands/{id}         Get command status
POST /commands/{id}/cancel  Cancel command
```

### AI Agents
```
POST /agents/register       Register new agent
GET  /agents/{id}           Get agent status
POST /agents/{id}/heartbeat Send heartbeat
POST /agents/coordinate     Coordinate agents
```

For complete API documentation, see [NEXUS_API_SPEC.md](./NEXUS_API_SPEC.md)

---

## WebSocket Connection

Connect to real-time updates:

```javascript
const ws = new WebSocket('wss://nexus.euystacio.io/ws/v1');

// Authenticate
ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'auth',
    token: 'Bearer YOUR_TOKEN'
  }));
};

// Subscribe to channels
ws.send(JSON.stringify({
  type: 'subscribe',
  channels: ['tasks', 'telemetry', 'agents']
}));

// Handle messages
ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log('Received:', message);
};
```

See [WEBSOCKET_EXAMPLE.md](./WEBSOCKET_EXAMPLE.md) for detailed examples.

---

## Deployment

### Render

See [DEPLOY_INSTRUCTIONS.md](./DEPLOY_INSTRUCTIONS.md) for step-by-step Render deployment.

Quick deploy:
```bash
# Deploy to Render
render deploy --app nexus-api
```

### Netlify

For static documentation and frontend:
```bash
# Deploy to Netlify
netlify deploy --prod
```

### Docker

```bash
# Build image
docker build -t euystacio-nexus .

# Run container
docker run -p 8080:8080 \
  --env-file .env \
  euystacio-nexus
```

---

## Security

### Best Practices

- ✅ Never commit secrets to version control
- ✅ Use environment variables for configuration
- ✅ Rotate API keys regularly
- ✅ Enable rate limiting in production
- ✅ Use HTTPS in production
- ✅ Validate all input data
- ✅ Implement proper CORS policies
- ✅ Monitor audit logs regularly

See [SECURITY_RUNBOOK.md](./SECURITY_RUNBOOK.md) for the complete security checklist.

---

## Integration Guides

- **[Gmail OAuth Setup](./GMAIL_OAUTH_SETUP.md)** - Configure Gmail API for notifications
- **[GGI Broadcast Integration](./GGI_BROADCAST_INTEGRATION.md)** - Integrate with GGI Broadcast
- **[WebSocket Examples](./WEBSOCKET_EXAMPLE.md)** - Real-time communication patterns

---

## CI/CD & Automation

This repository features comprehensive CI/CD automation with GitHub Actions:

- ✅ **Automated Building** - TypeScript and Python components
- ✅ **Automated Testing** - Jest (TypeScript) and pytest (Python)
- ✅ **Code Quality Checks** - ESLint, Flake8, PyLint, Prettier
- ✅ **Security Scanning** - CodeQL, Semgrep, Gitleaks, dependency audits
- ✅ **GitHub Pages Deployment** - Automatic deployment on push to main
- ✅ **Uptime Monitoring** - Checks every 30 minutes with alerts
- ✅ **Dependency Updates** - Automated via Dependabot

**Documentation:** See [CI_CD_DOCUMENTATION.md](./CI_CD_DOCUMENTATION.md) for complete details.

**GitHub Pages:** https://hannesmitterer.github.io/Euystacio/

---

## Development

### Running Tests

```bash
# TypeScript tests
npm test
npm run test:coverage

# Python tests
pytest
pytest --cov
```

### Linting

```bash
# TypeScript/JavaScript
npm run lint
npm run lint:fix

# Python
flake8 *.py
pylint *.py
black --check *.py

# Format code
npm run format
```

### Type Checking

```bash
npm run typecheck
```

### Database Migrations

```bash
# Create migration
npm run migrate:create migration_name

# Run migrations
npm run migrate

# Rollback
npm run migrate:rollback
```

---

## Architecture

```
┌─────────────────┐
│   API Gateway   │ ← Rate Limiting, Auth
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼──┐  ┌──▼───┐
│ REST │  │  WS  │
└───┬──┘  └──┬───┘
    │        │
┌───▼────────▼───┐
│  Business Logic │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼──┐  ┌──▼───┐
│ DB   │  │Redis │
└──────┘  └──────┘
```

---

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Follow existing code patterns
- Write clear commit messages
- Add tests for new features
- Update documentation

---

## Support & Resources

- 📚 **Full API Spec:** [NEXUS_API_SPEC.md](./NEXUS_API_SPEC.md)
- 🚀 **Deployment Guide:** [DEPLOY_INSTRUCTIONS.md](./DEPLOY_INSTRUCTIONS.md)
- 🔐 **Security Runbook:** [SECURITY_RUNBOOK.md](./SECURITY_RUNBOOK.md)
- 📧 **Support:** support@euystacio.io
- 🐛 **Issues:** https://github.com/hannesmitterer/Euystacio/issues
- 💬 **Discussions:** https://github.com/hannesmitterer/Euystacio/discussions

---

## 💰 Support the Seedbringer Treasury

**Framework Euystacio** is part of the **Seedbringer Treasury** initiative - a critical mission to reduce systemic collapse risk through open knowledge and eternal preservation.

### Direct Contribution Options

**Ethereum Wallet (ETH/ERC-20):**
```
0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb2
```

**Bitcoin (BTC):**
```
bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh
```

### Why Support Matters

Every contribution directly funds:
- 🌱 **Survival Security** - Ensuring project continuity and developer sustainability
- 📚 **Eternal Knowledge** - IPFS preservation and distributed access
- 🔒 **Framework Development** - Building tools that reduce collapse probability
- 🌍 **Open Source Mission** - Keeping all resources freely accessible

### Transparency

All funding is tracked with complete transparency. See [SUPPORT.md](./SUPPORT.md) for:
- Detailed funding allocation
- Current sustainability status
- Impact metrics and collapse risk reduction
- Monthly transparency reports

**Your support ensures eternal knowledge survives. Thank you for being part of the solution.**

---

## License

See [SACRED_COMMONS_LICENSE.md](./SACRED_COMMONS_LICENSE.md) for license information.

---

## Acknowledgments

This project is part of the Euystacio ecosystem - The Holy Bridge for AI coordination and sacred interface preservation.

---

**Built with ❤️ for the AI coordination community**
