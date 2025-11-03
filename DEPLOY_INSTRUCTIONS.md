# Deployment Instructions

This guide covers deploying the Euystacio Nexus API to Render and Netlify.

---

## Render Deployment

Render is recommended for deploying the backend API and WebSocket services.

### Prerequisites

- A Render account (free tier available)
- GitHub repository connected to Render
- PostgreSQL database (Render provides managed instances)

### Step 1: Create a New Web Service

1. Log in to [Render Dashboard](https://dashboard.render.com/)
2. Click **New** → **Web Service**
3. Connect your GitHub repository
4. Select the `hannesmitterer/Euystacio` repository

### Step 2: Configure Build Settings

**Build Command:**
```bash
npm install && npm run build
```

**Start Command:**
```bash
npm start
```

**Environment:**
- Runtime: `Node 18.x` (or `Python 3.9+` if using Python)
- Region: Choose closest to your users

### Step 3: Set Environment Variables

Add the following environment variables in the Render dashboard:

#### Required Variables

```bash
# Server
NODE_ENV=production
PORT=8080
API_VERSION=v1

# Database (provided by Render PostgreSQL)
DATABASE_URL=${DATABASE_URL}

# Redis (add Render Redis instance)
REDIS_URL=${REDIS_URL}

# OAuth 2.0
OAUTH_CLIENT_ID=your_production_client_id
OAUTH_CLIENT_SECRET=your_production_client_secret
OAUTH_REDIRECT_URI=https://your-app.onrender.com/oauth/callback

# JWT
JWT_SECRET=use_strong_random_secret_here
JWT_EXPIRATION=3600

# API Keys
API_KEY_SALT=use_strong_random_salt_here

# Rate Limiting
RATE_LIMIT_FREE_TIER=60
RATE_LIMIT_BASIC_TIER=600
RATE_LIMIT_PRO_TIER=6000

# WebSocket
WS_PORT=8081
WS_HEARTBEAT_INTERVAL=30000

# Security
SESSION_SECRET=use_strong_random_secret_here
CORS_ORIGIN=https://your-frontend-domain.com

# Logging
LOG_LEVEL=info
LOG_FILE=/var/log/nexus.log
```

#### Optional Variables (if using Gmail/GGI)

```bash
# Gmail API (for notifications)
GMAIL_CLIENT_ID=your_gmail_client_id
GMAIL_CLIENT_SECRET=your_gmail_client_secret
GMAIL_REFRESH_TOKEN=your_refresh_token

# GGI Broadcast
GGI_BROADCAST_WEBHOOK_URL=https://ggi.example.com/webhooks
GGI_BROADCAST_API_KEY=your_ggi_api_key
```

### Step 4: Add PostgreSQL Database

1. In Render dashboard, click **New** → **PostgreSQL**
2. Name: `nexus-db`
3. Region: Same as your web service
4. Plan: Free or paid tier
5. Click **Create Database**
6. Copy the **Internal Database URL**
7. Add it as `DATABASE_URL` environment variable in your web service

### Step 5: Add Redis Instance

1. Click **New** → **Redis**
2. Name: `nexus-redis`
3. Region: Same as your web service
4. Plan: Free (25MB) or paid tier
5. Click **Create Redis**
6. Copy the **Internal Redis URL**
7. Add it as `REDIS_URL` environment variable

### Step 6: Deploy

1. Click **Create Web Service**
2. Render will automatically build and deploy
3. Monitor logs in the dashboard
4. Your API will be available at: `https://your-service-name.onrender.com`

### Step 7: Run Database Migrations

After first deployment, run migrations via Render Shell:

1. Open your web service
2. Click **Shell** tab
3. Run: `npm run migrate` (or `python manage.py migrate`)

### Step 8: Configure Custom Domain (Optional)

1. Go to **Settings** → **Custom Domain**
2. Add your domain (e.g., `nexus.euystacio.io`)
3. Update DNS records as instructed
4. Wait for SSL certificate provisioning

---

## Netlify Deployment

Netlify is ideal for deploying static documentation, frontend dashboards, or API docs.

### Prerequisites

- A Netlify account (free tier available)
- GitHub repository connected to Netlify

### Step 1: Create a New Site

1. Log in to [Netlify Dashboard](https://app.netlify.com/)
2. Click **Add new site** → **Import an existing project**
3. Connect to GitHub
4. Select `hannesmitterer/Euystacio` repository

### Step 2: Configure Build Settings

**Build Command:**
```bash
npm run build:docs
```

**Publish Directory:**
```
public
```

**Base Directory:**
```
(leave empty or specify if docs are in subdirectory)
```

### Step 3: Set Environment Variables

Add environment variables in Netlify dashboard under **Site settings** → **Environment variables**:

```bash
# API Endpoint (points to Render backend)
REACT_APP_API_URL=https://your-service.onrender.com/api/v1
REACT_APP_WS_URL=wss://your-service.onrender.com/ws/v1

# Public OAuth Client ID (never use secret in frontend!)
REACT_APP_OAUTH_CLIENT_ID=your_public_client_id

# Feature Flags
REACT_APP_ENABLE_WEBSOCKET=true
REACT_APP_ENABLE_TELEMETRY=true
```

### Step 4: Deploy

1. Click **Deploy site**
2. Netlify will build and deploy automatically
3. Your site will be available at: `https://random-name.netlify.app`

### Step 5: Configure Custom Domain

1. Go to **Domain settings**
2. Click **Add custom domain**
3. Enter your domain (e.g., `docs.euystacio.io`)
4. Follow DNS configuration instructions
5. Enable HTTPS (automatic with Let's Encrypt)

### Step 6: Configure Redirects (Optional)

Create a `netlify.toml` in your repository:

```toml
[[redirects]]
  from = "/api/*"
  to = "https://your-service.onrender.com/api/:splat"
  status = 200
  force = true

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

---

## Docker Deployment (Alternative)

If you prefer Docker, use this setup:

### Dockerfile

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 8080

CMD ["npm", "start"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  nexus-api:
    build: .
    ports:
      - "8080:8080"
      - "8081:8081"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://postgres:password@db:5432/nexus
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  db:
    image: postgres:14-alpine
    environment:
      - POSTGRES_DB=nexus
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Deploy to Docker

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## Environment Variable Reference

### Critical Security Variables

**Never commit these to Git!** Use Render/Netlify environment variable settings.

| Variable | Description | Example |
|----------|-------------|---------|
| `JWT_SECRET` | Secret for signing JWT tokens | Random 64-char string |
| `SESSION_SECRET` | Express session secret | Random 64-char string |
| `API_KEY_SALT` | Salt for API key hashing | Random 32-char string |
| `OAUTH_CLIENT_SECRET` | OAuth client secret | From OAuth provider |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://...` |

### Generate Secrets

Use this command to generate strong secrets:

```bash
# Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"

# Python
python -c "import secrets; print(secrets.token_hex(32))"

# OpenSSL
openssl rand -hex 32
```

---

## Post-Deployment Checklist

### Initial Setup
- [ ] Verify API responds at `/health` endpoint
- [ ] Run database migrations
- [ ] Create admin user/API key
- [ ] Test OAuth flow
- [ ] Verify WebSocket connection
- [ ] Check rate limiting works
- [ ] Review audit logs

### Security
- [ ] Enable HTTPS only
- [ ] Configure CORS properly
- [ ] Set strong secrets (JWT, session, API key salt)
- [ ] Enable rate limiting
- [ ] Configure firewall rules
- [ ] Set up monitoring/alerts
- [ ] Review security headers

### Monitoring
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Configure log aggregation
- [ ] Set up uptime monitoring
- [ ] Configure database backups
- [ ] Test disaster recovery

---

## Troubleshooting

### Common Issues

**API returns 500 errors:**
- Check environment variables are set correctly
- Verify database connection string
- Review logs for specific errors
- Ensure migrations have run

**WebSocket connection fails:**
- Check WS_PORT is exposed
- Verify CORS settings allow WebSocket upgrade
- Check firewall/security group settings
- Test with `wscat` or similar tool

**Database connection timeout:**
- Use internal database URL (not external)
- Check database is in same region
- Verify connection pool settings
- Review database logs

**Rate limiting not working:**
- Verify Redis connection
- Check REDIS_URL environment variable
- Review rate limit tier settings
- Test with multiple requests

---

## Scaling Considerations

### Horizontal Scaling

For high traffic, scale horizontally:

1. **Render:** Increase instance count in dashboard
2. **Database:** Use connection pooling (PgBouncer)
3. **Redis:** Use Redis Cluster for high availability
4. **Load Balancing:** Render handles this automatically

### Performance Optimization

- Enable database query caching
- Use Redis for session storage
- Implement CDN for static assets
- Optimize database indexes
- Use database read replicas

---

## Backup and Recovery

### Database Backups

Render PostgreSQL includes automatic daily backups.

**Manual backup:**
```bash
pg_dump $DATABASE_URL > backup.sql
```

**Restore:**
```bash
psql $DATABASE_URL < backup.sql
```

### Redis Backups

Redis data is ephemeral. For persistence:

1. Use Redis persistence (RDB/AOF)
2. Enable backups in Render Redis settings
3. Store critical data in PostgreSQL

---

## Support

- **Render Docs:** https://render.com/docs
- **Netlify Docs:** https://docs.netlify.com
- **Issues:** https://github.com/hannesmitterer/Euystacio/issues

---

**Last Updated:** 2025-11-03
