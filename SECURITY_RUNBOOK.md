# Security Runbook

This security runbook provides essential security practices, checklists, and procedures for the Nexus API.

---

## Table of Contents

1. [Security Checklist](#security-checklist)
2. [Authentication & Authorization](#authentication--authorization)
3. [Session Management](#session-management)
4. [Secret Handling](#secret-handling)
5. [Rate Limiting](#rate-limiting)
6. [Input Validation](#input-validation)
7. [Audit Logging](#audit-logging)
8. [Incident Response](#incident-response)
9. [Regular Security Tasks](#regular-security-tasks)

---

## Security Checklist

### Pre-Deployment Security Checklist

- [ ] All secrets are stored in environment variables (not in code)
- [ ] Strong JWT secret is configured (64+ characters)
- [ ] Session secret is unique and random
- [ ] API key salt is configured
- [ ] HTTPS is enforced in production
- [ ] CORS is properly configured
- [ ] Rate limiting is enabled
- [ ] Database credentials are secure
- [ ] OAuth credentials are from production environment
- [ ] All dependencies are up to date
- [ ] Security headers are configured
- [ ] Error messages don't leak sensitive information
- [ ] Logging is configured (but doesn't log secrets)
- [ ] Database backups are automated
- [ ] Monitoring and alerting are set up

### Production Security Checklist

- [ ] Regular security audits scheduled
- [ ] API key rotation policy in place
- [ ] Session cleanup job is running
- [ ] Rate limit thresholds are appropriate
- [ ] Audit logs are reviewed weekly
- [ ] Security patches applied within 48 hours
- [ ] Incident response plan is documented
- [ ] Team has security training
- [ ] Penetration testing completed
- [ ] Compliance requirements met

---

## Authentication & Authorization

### JWT Token Security

**Generate Strong JWT Secret:**

```bash
# Generate a 64-character random secret
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

**Token Configuration:**

```javascript
// config/jwt.js
const jwt = require('jsonwebtoken');

const JWT_CONFIG = {
  secret: process.env.JWT_SECRET,
  expiresIn: '1h',  // Short expiration for security
  algorithm: 'HS256'
};

function generateToken(userId, scopes) {
  return jwt.sign(
    {
      userId,
      scopes,
      iat: Math.floor(Date.now() / 1000)
    },
    JWT_CONFIG.secret,
    {
      expiresIn: JWT_CONFIG.expiresIn,
      algorithm: JWT_CONFIG.algorithm
    }
  );
}

function verifyToken(token) {
  try {
    return jwt.verify(token, JWT_CONFIG.secret, {
      algorithms: [JWT_CONFIG.algorithm]
    });
  } catch (error) {
    throw new Error('Invalid token');
  }
}

module.exports = { generateToken, verifyToken };
```

### API Key Management

**Secure API Key Generation:**

```javascript
// utils/api-key.js
const crypto = require('crypto');

function generateApiKey() {
  // Generate 32 bytes of random data
  const key = crypto.randomBytes(32).toString('hex');
  return `agt_${key}`;
}

function hashApiKey(apiKey) {
  const salt = process.env.API_KEY_SALT;
  return crypto
    .createHmac('sha256', salt)
    .update(apiKey)
    .digest('hex');
}

function verifyApiKey(providedKey, storedHash) {
  const hash = hashApiKey(providedKey);
  return crypto.timingSafeEqual(
    Buffer.from(hash),
    Buffer.from(storedHash)
  );
}

module.exports = { generateApiKey, hashApiKey, verifyApiKey };
```

### OAuth 2.0 Security

**Secure OAuth Configuration:**

```javascript
// config/oauth.js
const OAUTH_CONFIG = {
  clientId: process.env.OAUTH_CLIENT_ID,
  clientSecret: process.env.OAUTH_CLIENT_SECRET,
  redirectUri: process.env.OAUTH_REDIRECT_URI,
  
  // Security settings
  tokenEndpoint: 'https://oauth.provider.com/token',
  authorizationEndpoint: 'https://oauth.provider.com/authorize',
  
  // Always use PKCE for added security
  usePKCE: true,
  
  // Scopes requested
  scopes: [
    'telemetry:read',
    'telemetry:write',
    'tasks:read',
    'tasks:write'
  ]
};

module.exports = OAUTH_CONFIG;
```

---

## Session Management

### Session Cleanup

**Automated Session Cleanup Job:**

```javascript
// jobs/session-cleanup.js
const cron = require('node-cron');

class SessionCleanup {
  constructor(sessionStore) {
    this.sessionStore = sessionStore;
  }

  start() {
    // Run every hour
    cron.schedule('0 * * * *', async () => {
      console.log('Running session cleanup...');
      await this.cleanup();
    });
  }

  async cleanup() {
    const now = Date.now();
    const sessions = await this.sessionStore.getAll();
    
    let cleaned = 0;
    for (const session of sessions) {
      // Remove expired sessions
      if (session.expiresAt < now) {
        await this.sessionStore.delete(session.id);
        cleaned++;
      }
      
      // Remove inactive sessions (no activity for 24 hours)
      const inactiveTime = 24 * 60 * 60 * 1000;
      if (now - session.lastActivity > inactiveTime) {
        await this.sessionStore.delete(session.id);
        cleaned++;
      }
    }
    
    console.log(`Cleaned up ${cleaned} sessions`);
    return cleaned;
  }

  async forceLogout(userId) {
    const sessions = await this.sessionStore.getByUser(userId);
    for (const session of sessions) {
      await this.sessionStore.delete(session.id);
    }
    console.log(`Logged out user ${userId} from ${sessions.length} sessions`);
  }
}

module.exports = SessionCleanup;
```

**Usage:**

```javascript
// app.js
const SessionCleanup = require('./jobs/session-cleanup');
const sessionStore = require('./store/session-store');

const sessionCleanup = new SessionCleanup(sessionStore);
sessionCleanup.start();
```

### Session Security Best Practices

1. **Short Session Timeouts:** 1-4 hours for regular users, 15-30 minutes for admins
2. **Activity Tracking:** Update last activity on each request
3. **Secure Session IDs:** Use cryptographically random session IDs
4. **HTTPOnly Cookies:** Prevent XSS attacks
5. **Secure Flag:** Only send cookies over HTTPS
6. **SameSite:** Prevent CSRF attacks

```javascript
// Session cookie configuration
app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,      // Prevent XSS
    secure: process.env.NODE_ENV === 'production',  // HTTPS only
    sameSite: 'strict',  // Prevent CSRF
    maxAge: 3600000      // 1 hour
  }
}));
```

---

## Secret Handling

### Environment Variables

**Required Secrets:**

```bash
# .env (NEVER commit this file!)

# Critical Secrets
JWT_SECRET=<64-char-random-hex>
SESSION_SECRET=<64-char-random-hex>
API_KEY_SALT=<32-char-random-hex>

# OAuth Credentials
OAUTH_CLIENT_ID=<from-oauth-provider>
OAUTH_CLIENT_SECRET=<from-oauth-provider>

# Database
DATABASE_URL=postgresql://user:password@host:5432/db
REDIS_URL=redis://host:6379

# Gmail OAuth (if used)
GMAIL_CLIENT_ID=<from-google-cloud>
GMAIL_CLIENT_SECRET=<from-google-cloud>
GMAIL_REFRESH_TOKEN=<from-oauth-flow>

# GGI Broadcast (if used)
GGI_BROADCAST_API_KEY=<from-ggi>
GGI_BROADCAST_WEBHOOK_SECRET=<from-ggi>
```

### Secret Rotation

**API Key Rotation Schedule:**

```javascript
// scripts/rotate-api-keys.js
const ApiKeyModel = require('../models/api-key');
const { generateApiKey, hashApiKey } = require('../utils/api-key');

async function rotateApiKey(keyId) {
  const oldKey = await ApiKeyModel.findById(keyId);
  
  // Generate new key
  const newKey = generateApiKey();
  const newHash = hashApiKey(newKey);
  
  // Update database
  await ApiKeyModel.findByIdAndUpdate(keyId, {
    keyHash: newHash,
    rotatedAt: new Date(),
    previousKeyHash: oldKey.keyHash,
    // Allow old key for 24 hours during transition
    gracePeriodEnds: new Date(Date.now() + 24 * 60 * 60 * 1000)
  });
  
  console.log('New API key (save this securely):');
  console.log(newKey);
  console.log('Old key will expire in 24 hours');
  
  return newKey;
}

// Rotate all keys older than 90 days
async function rotateOldKeys() {
  const ninetyDaysAgo = new Date(Date.now() - 90 * 24 * 60 * 60 * 1000);
  const oldKeys = await ApiKeyModel.find({
    rotatedAt: { $lt: ninetyDaysAgo }
  });
  
  console.log(`Found ${oldKeys.length} keys to rotate`);
  
  for (const key of oldKeys) {
    await rotateApiKey(key._id);
  }
}

module.exports = { rotateApiKey, rotateOldKeys };
```

### Secret Detection

**Pre-commit Hook to Prevent Secret Commits:**

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check for potential secrets
if git diff --cached | grep -E "(JWT_SECRET|API_KEY|CLIENT_SECRET|PASSWORD)=.+"; then
  echo "Error: Potential secret detected in commit!"
  echo "Remove secrets from code and use environment variables instead."
  exit 1
fi
```

---

## Rate Limiting

### Implementation

```javascript
// middleware/rate-limit.js
const redis = require('redis');
const client = redis.createClient(process.env.REDIS_URL);

async function rateLimit(req, res, next) {
  const userId = req.user?.id || req.ip;
  const tier = req.user?.tier || 'free';
  
  // Get rate limits for tier
  const limits = {
    free: { requests: 60, window: 60 },       // 60 req/min
    basic: { requests: 600, window: 60 },     // 600 req/min
    pro: { requests: 6000, window: 60 }       // 6000 req/min
  };
  
  const limit = limits[tier];
  const key = `rate_limit:${userId}:${Math.floor(Date.now() / 1000 / limit.window)}`;
  
  // Increment counter
  const count = await client.incr(key);
  
  // Set expiration on first request
  if (count === 1) {
    await client.expire(key, limit.window);
  }
  
  // Set headers
  res.setHeader('X-RateLimit-Limit', limit.requests);
  res.setHeader('X-RateLimit-Remaining', Math.max(0, limit.requests - count));
  res.setHeader('X-RateLimit-Reset', Math.floor(Date.now() / 1000) + limit.window);
  
  // Check if limit exceeded
  if (count > limit.requests) {
    return res.status(429).json({
      error: {
        code: 'RATE_LIMIT_EXCEEDED',
        message: 'Too many requests',
        retry_after: limit.window
      }
    });
  }
  
  next();
}

module.exports = rateLimit;
```

### Aggressive Rate Limiting for Auth Endpoints

```javascript
// Stricter limits for authentication endpoints
const authRateLimit = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 5,                     // 5 attempts
  message: 'Too many authentication attempts, please try again later'
});

app.post('/oauth/token', authRateLimit, handleOAuthToken);
app.post('/api/v1/sessions/create', authRateLimit, createSession);
```

---

## Input Validation

### Request Validation

```javascript
// middleware/validate.js
const { validationResult, body, param, query } = require('express-validator');

const validateRequest = (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({
      error: {
        code: 'VALIDATION_ERROR',
        message: 'Invalid request data',
        details: errors.array()
      }
    });
  }
  next();
};

// Example: Task creation validation
const validateTaskCreation = [
  body('title')
    .isString()
    .trim()
    .isLength({ min: 1, max: 200 })
    .withMessage('Title must be 1-200 characters'),
  
  body('type')
    .isIn(['data_processing', 'analysis', 'notification'])
    .withMessage('Invalid task type'),
  
  body('priority')
    .isIn(['low', 'medium', 'high', 'critical'])
    .withMessage('Invalid priority'),
  
  body('assigned_to')
    .optional()
    .matches(/^agent-[a-zA-Z0-9]+$/)
    .withMessage('Invalid agent ID format'),
  
  validateRequest
];

app.post('/api/v1/tasks', validateTaskCreation, createTask);
```

### SQL Injection Prevention

```javascript
// Always use parameterized queries
const { Pool } = require('pg');
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

// ✅ GOOD: Parameterized query
async function getTask(taskId) {
  const result = await pool.query(
    'SELECT * FROM tasks WHERE id = $1',
    [taskId]
  );
  return result.rows[0];
}

// ❌ BAD: String concatenation (vulnerable to SQL injection)
async function getTaskBad(taskId) {
  const result = await pool.query(
    `SELECT * FROM tasks WHERE id = '${taskId}'`
  );
  return result.rows[0];
}
```

---

## Audit Logging

### Audit Log Implementation

```javascript
// services/audit-log.js
const AuditLogModel = require('../models/audit-log');

class AuditLog {
  static async log(action, userId, details) {
    await AuditLogModel.create({
      action,
      userId,
      timestamp: new Date(),
      ipAddress: details.ipAddress,
      userAgent: details.userAgent,
      resource: details.resource,
      resourceId: details.resourceId,
      changes: details.changes,
      result: details.result
    });
  }

  static async logTaskCreated(userId, task, req) {
    await this.log('task_created', userId, {
      ipAddress: req.ip,
      userAgent: req.get('user-agent'),
      resource: 'task',
      resourceId: task.id,
      changes: { created: task },
      result: 'success'
    });
  }

  static async logFailedAuth(userId, req) {
    await this.log('auth_failed', userId, {
      ipAddress: req.ip,
      userAgent: req.get('user-agent'),
      result: 'failure'
    });
  }

  static async query(filters) {
    return await AuditLogModel.find(filters)
      .sort({ timestamp: -1 })
      .limit(100);
  }
}

module.exports = AuditLog;
```

### What to Log

**Always Log:**
- Authentication attempts (success and failure)
- Authorization failures
- API key generation/rotation
- Session creation/deletion
- Sensitive data access
- Configuration changes
- Security-relevant errors

**Never Log:**
- Passwords
- API keys or tokens
- Personal data (unless required for compliance)
- Full request/response bodies containing secrets

---

## Incident Response

### Security Incident Response Plan

**1. Detection & Triage**
- Monitor logs for suspicious activity
- Set up alerts for:
  - Multiple failed auth attempts
  - Unusual API usage patterns
  - Rate limit violations
  - SQL injection attempts
  - XSS attempts

**2. Containment**
- Immediately revoke compromised API keys
- Force logout affected users
- Block suspicious IP addresses
- Disable compromised features if needed

**3. Investigation**
- Review audit logs
- Identify scope of breach
- Determine what data was accessed
- Document timeline of events

**4. Recovery**
- Rotate all potentially compromised secrets
- Patch vulnerabilities
- Restore from backups if needed
- Notify affected users (if required by law)

**5. Post-Incident**
- Document lessons learned
- Update security procedures
- Implement additional controls
- Train team on new procedures

### Emergency Response Procedures

```javascript
// scripts/emergency-lockdown.js

async function emergencyLockdown() {
  console.log('🚨 EMERGENCY LOCKDOWN INITIATED');
  
  // 1. Disable all API access except admins
  await setMaintenanceMode(true);
  
  // 2. Revoke all active sessions
  await revokeAllSessions();
  
  // 3. Block all API keys except admin keys
  await disableNonAdminApiKeys();
  
  // 4. Alert admin team
  await notifyAdminTeam('EMERGENCY LOCKDOWN ACTIVATED');
  
  console.log('✅ Lockdown complete');
}

async function endLockdown() {
  console.log('Ending lockdown...');
  
  await setMaintenanceMode(false);
  await enableApiKeys();
  await notifyAdminTeam('LOCKDOWN ENDED');
  
  console.log('✅ Normal operations resumed');
}
```

---

## Regular Security Tasks

### Daily
- [ ] Review failed authentication attempts
- [ ] Check rate limit violations
- [ ] Monitor error logs for security issues

### Weekly
- [ ] Review audit logs
- [ ] Check for unusual API usage patterns
- [ ] Verify backup integrity
- [ ] Review active sessions

### Monthly
- [ ] Update dependencies
- [ ] Review and update firewall rules
- [ ] Check SSL certificate expiration
- [ ] Review user permissions
- [ ] Run security scans

### Quarterly
- [ ] Rotate API keys
- [ ] Security team training
- [ ] Review incident response plan
- [ ] Penetration testing
- [ ] Compliance audit

---

## Security Contacts

**Security Issues:**
- Email: security@euystacio.io
- Emergency: Use incident response plan

**Vulnerability Reporting:**
- Follow responsible disclosure
- Email details to security@euystacio.io
- Allow 90 days for patching before public disclosure

---

**Last Updated:** 2025-11-03
