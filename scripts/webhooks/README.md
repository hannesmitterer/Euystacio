# Webhook Integration Scripts

This directory contains webhook integration scripts for automatically propagating Framework Euystacio updates across multiple platforms.

## Available Integrations

### 1. GitHub to Discord (`github-discord.js`)

Forwards GitHub events to Discord channels in real-time.

**Supported Events:**
- Issues (opened, closed, edited)
- Pull Requests (opened, merged, closed)
- Commits (push events)
- Releases (published, created)
- Stars (new stars)

**Setup:**

1. Create a Discord webhook:
   - Go to your Discord server settings
   - Navigate to Integrations → Webhooks
   - Create a new webhook
   - Copy the webhook URL

2. Set environment variables:
   ```bash
   export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
   export GITHUB_WEBHOOK_SECRET="your_secret_here"  # Optional but recommended
   ```

3. Deploy the webhook handler:
   
   **Option A: Express Server**
   ```bash
   cd scripts/webhooks
   npm install express
   node github-discord.js
   # Server runs on http://localhost:3000
   ```

   **Option B: Serverless (Vercel)**
   ```bash
   # Deploy to Vercel
   vercel deploy
   ```

4. Configure GitHub webhook:
   - Go to your repository settings
   - Navigate to Webhooks → Add webhook
   - Set Payload URL to your deployed endpoint (e.g., `https://your-domain.com/webhook/github`)
   - Content type: `application/json`
   - Secret: (same as GITHUB_WEBHOOK_SECRET)
   - Select events to trigger: Issues, Pull requests, Pushes, Releases, Stars

---

### 2. GitHub to Telegram (`github-telegram.js`)

Forwards GitHub events to Telegram channels in real-time.

**Supported Events:**
- Issues (opened, closed, edited)
- Pull Requests (opened, merged, closed)
- Commits (push events)
- Releases (published)
- Stars (new stars)
- Forks (new forks)
- Watches (new watchers)
- Issue comments
- Deployments

**Setup:**

1. Create a Telegram bot:
   - Message @BotFather on Telegram
   - Send `/newbot` and follow instructions
   - Copy the bot token

2. Get your channel/chat ID:
   - Add your bot to your channel
   - Send a message to the channel
   - Visit `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Find the chat ID in the response

3. Set environment variables:
   ```bash
   export TELEGRAM_BOT_TOKEN="your_bot_token_here"
   export TELEGRAM_CHAT_ID="your_chat_id_here"  # Can be channel ID or chat ID
   export GITHUB_WEBHOOK_SECRET="your_secret_here"  # Optional but recommended
   ```

4. Deploy the webhook handler:
   
   **Option A: Express Server**
   ```bash
   cd scripts/webhooks
   npm install express
   node github-telegram.js
   # Server runs on http://localhost:3001
   ```

   **Option B: Serverless (Vercel)**
   ```bash
   # Deploy to Vercel
   vercel deploy
   ```

5. Configure GitHub webhook:
   - Same as Discord setup above
   - Point to your Telegram webhook endpoint

---

## Security Best Practices

### 1. Use Webhook Secrets

Always configure a webhook secret in GitHub and verify signatures:

```bash
# Generate a strong secret
openssl rand -hex 32

# Set as environment variable
export GITHUB_WEBHOOK_SECRET="your_generated_secret"
```

**Important:** Store webhook secrets securely:
- Use environment variables (never commit to git)
- Use a secrets manager (AWS Secrets Manager, HashiCorp Vault, etc.)
- Rotate secrets every 90 days or after suspected compromise
- Document secret rotation procedures

### 2. Use HTTPS

Always use HTTPS for webhook endpoints:
- ✅ `https://your-domain.com/webhook/github`
- ❌ `http://your-domain.com/webhook/github`

### 3. Restrict IP Access

Consider restricting webhook access to GitHub's IP ranges:
- https://api.github.com/meta

### 4. Monitor Logs

Regularly review webhook logs for:
- Failed signature verifications
- Unusual activity patterns
- Error rates

### 5. Rotate Secrets

Rotate webhook secrets periodically (e.g., every 90 days).

---

## Deployment Options

### Option 1: Express Server on VPS

```bash
# Install dependencies
npm install express

# Run with PM2 for production
npm install -g pm2
pm2 start github-discord.js --name "github-discord-webhook"
pm2 start github-telegram.js --name "github-telegram-webhook"
pm2 save
pm2 startup
```

### Option 2: Serverless (Vercel)

Create `api/webhook-discord.js`:
```javascript
const { serverlessHandler } = require('../scripts/webhooks/github-discord');

module.exports = serverlessHandler;
```

Create `api/webhook-telegram.js`:
```javascript
const { serverlessHandler } = require('../scripts/webhooks/github-telegram');

module.exports = serverlessHandler;
```

Deploy:
```bash
vercel deploy --prod
```

### Option 3: Serverless (Netlify)

Create `netlify/functions/webhook-discord.js`:
```javascript
const { serverlessHandler } = require('../../scripts/webhooks/github-discord');

exports.handler = async (event) => {
  return await serverlessHandler({
    method: event.httpMethod,
    headers: event.headers,
    body: event.body,
  });
};
```

Deploy:
```bash
netlify deploy --prod
```

### Option 4: Docker

Create `Dockerfile`:
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install --production

COPY scripts/webhooks ./scripts/webhooks

ENV NODE_ENV=production
ENV PORT=3000

EXPOSE 3000

CMD ["node", "scripts/webhooks/github-discord.js"]
```

Build and run:
```bash
docker build -t euystacio-webhooks .
docker run -d \
  -p 3000:3000 \
  -e DISCORD_WEBHOOK_URL="your_webhook_url" \
  -e GITHUB_WEBHOOK_SECRET="your_secret" \
  euystacio-webhooks
```

---

## Testing

### Test Discord Webhook

```bash
curl -X POST https://discord.com/api/webhooks/YOUR_WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -d '{"content": "Test message from Framework Euystacio!"}'
```

### Test Telegram Webhook

```bash
curl -X POST https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage \
  -H "Content-Type: application/json" \
  -d '{"chat_id": "<YOUR_CHAT_ID>", "text": "Test message from Framework Euystacio!"}'
```

### Test GitHub Webhook Locally

```bash
# Install webhook testing tool
npm install -g smee-client

# Start smee proxy
smee --url https://smee.io/YOUR_UNIQUE_URL --path /webhook/github --port 3000

# Configure GitHub webhook to point to smee.io URL
# Trigger events in GitHub and see them forwarded to local server
```

---

## Troubleshooting

### Discord Webhook Not Working

1. **Check webhook URL:**
   ```bash
   echo $DISCORD_WEBHOOK_URL
   # Should start with https://discord.com/api/webhooks/
   ```

2. **Test webhook directly:**
   ```bash
   curl -X POST $DISCORD_WEBHOOK_URL \
     -H "Content-Type: application/json" \
     -d '{"content": "Test"}'
   ```

3. **Check Discord webhook settings:**
   - Webhook should be active
   - Channel should allow webhooks

### Telegram Webhook Not Working

1. **Check bot token:**
   ```bash
   curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe
   # Should return bot information
   ```

2. **Check chat ID:**
   ```bash
   curl https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
   # Find your chat ID in the response
   ```

3. **Ensure bot is admin in channel:**
   - Bot must be added to channel
   - Bot must have post permissions

### GitHub Webhook Not Triggering

1. **Check webhook configuration:**
   - URL is correct and accessible
   - Content type is `application/json`
   - SSL verification is enabled

2. **Check recent deliveries:**
   - Go to repository settings → Webhooks
   - Click on your webhook
   - Check "Recent Deliveries" for errors

3. **Verify signature:**
   - Ensure GITHUB_WEBHOOK_SECRET matches
   - Check server logs for signature errors

---

## Customization

### Add Custom Event Handlers

Edit `github-discord.js` or `github-telegram.js`:

```javascript
// Add new event handler
function formatCustomEvent(event) {
  // Your custom formatting logic
  return {
    username: 'GitHub Bot',
    embeds: [{
      title: 'Custom Event',
      description: 'Your custom content',
      color: 0x00FF00,
    }],
  };
}

// Add to main handler
case 'custom_event':
  discordPayload = formatCustomEvent(event);
  break;
```

### Filter Events

Add filtering logic before sending:

```javascript
// Only notify for specific branches
function formatPushEvent(event) {
  const branch = event.ref.replace('refs/heads/', '');
  
  // Only notify for main/master/develop
  if (!['main', 'master', 'develop'].includes(branch)) {
    return null;
  }
  
  // ... rest of formatting
}
```

### Add Multiple Channels

Send to multiple Discord channels:

```javascript
const CHANNELS = {
  issues: process.env.DISCORD_WEBHOOK_ISSUES,
  pullRequests: process.env.DISCORD_WEBHOOK_PRS,
  releases: process.env.DISCORD_WEBHOOK_RELEASES,
};

// Route based on event type
switch (eventType) {
  case 'issues':
    await sendToDiscord(payload, CHANNELS.issues);
    break;
  case 'pull_request':
    await sendToDiscord(payload, CHANNELS.pullRequests);
    break;
  // ...
}
```

---

## Monitoring

### Health Checks

Both scripts expose a `/health` endpoint:

```bash
curl http://localhost:3000/health
# Response: {"status":"healthy"}
```

### Logging

Enable detailed logging:

```bash
# Set log level
export LOG_LEVEL=debug

# Run with logging
node github-discord.js | tee webhook.log
```

### Metrics

Track webhook performance:

```javascript
// Add to handlers
let metrics = {
  eventsReceived: 0,
  eventsProcessed: 0,
  eventsFailed: 0,
};

// Increment in handler
metrics.eventsReceived++;
// ... process event ...
metrics.eventsProcessed++;

// Expose metrics endpoint
app.get('/metrics', (req, res) => {
  res.json(metrics);
});
```

---

## Framework Euystacio Specific Configuration

### Recommended Event Subscriptions

For Framework Euystacio propagation, subscribe to:

✅ **High Priority:**
- Releases (announce new versions)
- Pull Requests (community contributions)
- Issues (bug reports, feature requests)
- Stars (community growth)

✅ **Medium Priority:**
- Pushes (development activity)
- Forks (adoption metrics)

✅ **Optional:**
- Issue comments (community discussions)
- Deployments (infrastructure updates)

### Recommended Channels

**Discord:**
- `#announcements` - Releases, major updates
- `#dev-updates` - Commits, PRs
- `#community` - Stars, forks, discussions

**Telegram:**
- Main channel - All important updates
- Dev channel - Development activity

---

## Support

For issues or questions:
- **GitHub Issues:** https://github.com/hannesmitterer/Euystacio/issues
- **Discord:** Join the Framework Euystacio Discord
- **Documentation:** https://github.com/hannesmitterer/Euystacio

---

**Built for Framework Euystacio - The Holy Bridge for AI Coordination**
