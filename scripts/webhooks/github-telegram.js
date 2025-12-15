/**
 * GitHub to Telegram Webhook Integration
 * 
 * This script enables real-time synchronization of GitHub events to Telegram channels.
 * Supports: Issues, Pull Requests, Commits, Releases, and more.
 * 
 * Setup:
 * 1. Create a Telegram bot via @BotFather
 * 2. Get your bot token
 * 3. Add bot to your channel and get channel ID
 * 4. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables
 * 5. Configure GitHub webhook to point to this endpoint
 * 6. Deploy as serverless function or Express app
 */

const crypto = require('crypto');

/**
 * Configuration
 */
const CONFIG = {
  telegramBotToken: process.env.TELEGRAM_BOT_TOKEN || '',
  telegramChatId: process.env.TELEGRAM_CHAT_ID || '',
  githubWebhookSecret: process.env.GITHUB_WEBHOOK_SECRET || '',
  telegramApiUrl: 'https://api.telegram.org/bot',
};

/**
 * Verify GitHub webhook signature
 */
function verifySignature(payload, signature) {
  if (!CONFIG.githubWebhookSecret) {
    console.warn('No webhook secret configured - skipping verification');
    return true;
  }

  const hmac = crypto.createHmac('sha256', CONFIG.githubWebhookSecret);
  const digest = 'sha256=' + hmac.update(payload).digest('hex');
  return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(digest));
}

/**
 * Send message to Telegram
 */
async function sendToTelegram(message, parseMode = 'Markdown') {
  if (!CONFIG.telegramBotToken || !CONFIG.telegramChatId) {
    throw new Error('TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not configured');
  }

  const url = `${CONFIG.telegramApiUrl}${CONFIG.telegramBotToken}/sendMessage`;
  
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      chat_id: CONFIG.telegramChatId,
      text: message,
      parse_mode: parseMode,
      disable_web_page_preview: false,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(`Telegram API error: ${error.description}`);
  }

  return response.json();
}

/**
 * Escape Markdown special characters for Telegram
 * Note: This uses Markdown format. For MarkdownV2, additional escaping may be needed.
 * Consider using a library like 'telegram-escape-markdown' for production use.
 */
function escapeMarkdown(text) {
  if (!text) return '';
  // Basic escaping for Telegram Markdown (not MarkdownV2)
  // For production, consider using: npm install telegram-escape-markdown
  return text.replace(/([_*\[\]()~`>#+\-=|{}.!\\])/g, '\\$1');
}

/**
 * Format issue event for Telegram
 */
function formatIssueEvent(event) {
  const { action, issue, repository } = event;
  
  const emoji = action === 'opened' ? '🆕' : action === 'closed' ? '✅' : '📝';
  const labels = issue.labels.length > 0 
    ? `\n🏷 Labels: ${issue.labels.map(l => `\`${l.name}\``).join(', ')}`
    : '';

  return `${emoji} *Issue ${action}*

📋 [#${issue.number}](${issue.html_url}) ${escapeMarkdown(issue.title)}
👤 by [${escapeMarkdown(issue.user.login)}](${issue.user.html_url})
📦 Repository: [${escapeMarkdown(repository.full_name)}](${repository.html_url})
🔖 State: \`${issue.state}\`${labels}

${issue.body ? escapeMarkdown(issue.body.substring(0, 200)) + '...' : 'No description'}`;
}

/**
 * Format pull request event for Telegram
 */
function formatPullRequestEvent(event) {
  const { action, pull_request, repository } = event;
  
  const emoji = action === 'opened' ? '🔀' 
    : action === 'closed' && pull_request.merged ? '✅' 
    : action === 'closed' ? '❌' 
    : '📝';

  const status = pull_request.merged ? '✅ Merged' : `\`${pull_request.state}\``;

  return `${emoji} *Pull Request ${action}*

🔀 [#${pull_request.number}](${pull_request.html_url}) ${escapeMarkdown(pull_request.title)}
👤 by [${escapeMarkdown(pull_request.user.login)}](${pull_request.user.html_url})
📦 Repository: [${escapeMarkdown(repository.full_name)}](${repository.html_url})
🔖 State: ${status}
📊 Changes: \`+${pull_request.additions} -${pull_request.deletions}\`

${pull_request.body ? escapeMarkdown(pull_request.body.substring(0, 200)) + '...' : 'No description'}`;
}

/**
 * Format push event for Telegram
 */
function formatPushEvent(event) {
  const { commits, repository, pusher, ref } = event;
  
  const branch = ref.replace('refs/heads/', '');
  const commitList = commits.slice(0, 5).map(commit => {
    const shortId = commit.id.substring(0, 7);
    const message = escapeMarkdown(commit.message.split('\n')[0]);
    return `  • [\`${shortId}\`](${commit.url}) ${message}`;
  }).join('\n');

  let message = `📤 *${commits.length} new commit${commits.length > 1 ? 's' : ''}* pushed to \`${branch}\`

👤 by ${escapeMarkdown(pusher.name)}
📦 Repository: [${escapeMarkdown(repository.full_name)}](${repository.html_url})

*Commits:*
${commitList}`;

  if (commits.length > 5) {
    message += `\n\n... and ${commits.length - 5} more commits`;
  }

  return message;
}

/**
 * Format release event for Telegram
 */
function formatReleaseEvent(event) {
  const { action, release, repository } = event;
  
  const prerelease = release.prerelease ? '⚠️ Pre-release' : '✅ Stable';

  return `🚀 *Release ${action}*

📦 [${escapeMarkdown(release.name || release.tag_name)}](${release.html_url})
👤 by [${escapeMarkdown(release.author.login)}](${release.author.html_url})
📦 Repository: [${escapeMarkdown(repository.full_name)}](${repository.html_url})
🏷 Tag: \`${release.tag_name}\`
🔖 Type: ${prerelease}

*Release Notes:*
${release.body ? escapeMarkdown(release.body.substring(0, 300)) + '...' : 'No release notes provided'}`;
}

/**
 * Format star event for Telegram
 */
function formatStarEvent(event) {
  const { action, repository, sender } = event;
  
  if (action !== 'created') return null; // Only notify on new stars

  return `⭐ *New Star!*

👤 [${escapeMarkdown(sender.login)}](${sender.html_url}) starred [${escapeMarkdown(repository.full_name)}](${repository.html_url})
✨ Total stars: *${repository.stargazers_count}*`;
}

/**
 * Format fork event for Telegram
 */
function formatForkEvent(event) {
  const { forkee, repository, sender } = event;

  return `🍴 *Repository Forked!*

👤 [${escapeMarkdown(sender.login)}](${sender.html_url}) forked [${escapeMarkdown(repository.full_name)}](${repository.html_url})
📦 New fork: [${escapeMarkdown(forkee.full_name)}](${forkee.html_url})
🍴 Total forks: *${repository.forks_count}*`;
}

/**
 * Format watch event for Telegram
 */
function formatWatchEvent(event) {
  const { action, repository, sender } = event;
  
  if (action !== 'started') return null; // Only notify on new watches

  return `👁 *New Watcher!*

👤 [${escapeMarkdown(sender.login)}](${sender.html_url}) is watching [${escapeMarkdown(repository.full_name)}](${repository.html_url})
👁 Total watchers: *${repository.watchers_count}*`;
}

/**
 * Format issue comment event for Telegram
 */
function formatIssueCommentEvent(event) {
  const { action, issue, comment, repository } = event;
  
  if (action !== 'created') return null; // Only notify on new comments

  return `💬 *New Comment on Issue*

📋 [#${issue.number}](${issue.html_url}) ${escapeMarkdown(issue.title)}
👤 by [${escapeMarkdown(comment.user.login)}](${comment.user.html_url})
📦 Repository: [${escapeMarkdown(repository.full_name)}](${repository.html_url})

*Comment:*
${escapeMarkdown(comment.body.substring(0, 200))}${comment.body.length > 200 ? '...' : ''}

[View Comment](${comment.html_url})`;
}

/**
 * Format deployment event for Telegram
 */
function formatDeploymentEvent(event) {
  const { deployment, repository } = event;

  return `🚀 *New Deployment*

📦 Repository: [${escapeMarkdown(repository.full_name)}](${repository.html_url})
🌍 Environment: \`${deployment.environment}\`
🔀 Ref: \`${deployment.ref}\`
👤 by [${escapeMarkdown(deployment.creator.login)}](${deployment.creator.html_url})

${deployment.description ? escapeMarkdown(deployment.description) : 'No description'}`;
}

/**
 * Main webhook handler
 */
async function handleWebhook(event, eventType, signature, rawBody) {
  // Verify signature
  if (!verifySignature(rawBody, signature)) {
    throw new Error('Invalid webhook signature');
  }

  let message = null;

  // Route based on event type
  switch (eventType) {
    case 'issues':
      message = formatIssueEvent(event);
      break;
    
    case 'pull_request':
      message = formatPullRequestEvent(event);
      break;
    
    case 'push':
      message = formatPushEvent(event);
      break;
    
    case 'release':
      message = formatReleaseEvent(event);
      break;
    
    case 'star':
      message = formatStarEvent(event);
      break;
    
    case 'fork':
      message = formatForkEvent(event);
      break;
    
    case 'watch':
      message = formatWatchEvent(event);
      break;
    
    case 'issue_comment':
      message = formatIssueCommentEvent(event);
      break;
    
    case 'deployment':
      message = formatDeploymentEvent(event);
      break;
    
    default:
      console.log(`Unsupported event type: ${eventType}`);
      return { success: true, message: 'Event type not configured' };
  }

  if (message) {
    await sendToTelegram(message);
    return { success: true, message: 'Event forwarded to Telegram' };
  }

  return { success: true, message: 'No action taken' };
}

/**
 * Express.js integration example
 */
function createExpressHandler() {
  const express = require('express');
  const app = express();

  app.use(express.json({
    verify: (req, res, buf) => {
      req.rawBody = buf.toString();
    }
  }));

  app.post('/webhook/github', async (req, res) => {
    try {
      const eventType = req.headers['x-github-event'];
      const signature = req.headers['x-hub-signature-256'];
      
      const result = await handleWebhook(
        req.body,
        eventType,
        signature,
        req.rawBody
      );

      res.json(result);
    } catch (error) {
      console.error('Webhook error:', error);
      res.status(500).json({ 
        success: false, 
        error: error.message 
      });
    }
  });

  app.get('/health', (req, res) => {
    res.json({ status: 'healthy' });
  });

  return app;
}

/**
 * Serverless function example (Vercel, Netlify, etc.)
 */
async function serverlessHandler(req) {
  if (req.method !== 'POST') {
    return {
      statusCode: 405,
      body: JSON.stringify({ error: 'Method not allowed' }),
    };
  }

  try {
    const eventType = req.headers['x-github-event'];
    const signature = req.headers['x-hub-signature-256'];
    const event = JSON.parse(req.body);

    const result = await handleWebhook(event, eventType, signature, req.body);

    return {
      statusCode: 200,
      body: JSON.stringify(result),
    };
  } catch (error) {
    console.error('Webhook error:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ 
        success: false, 
        error: error.message 
      }),
    };
  }
}

// Export handlers
module.exports = {
  handleWebhook,
  createExpressHandler,
  serverlessHandler,
  CONFIG,
};

// CLI usage example
if (require.main === module) {
  const PORT = process.env.PORT || 3001;
  const app = createExpressHandler();
  
  app.listen(PORT, () => {
    console.log(`GitHub-Telegram webhook server running on port ${PORT}`);
    console.log(`Webhook endpoint: http://localhost:${PORT}/webhook/github`);
  });
}
