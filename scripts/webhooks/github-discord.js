/**
 * GitHub to Discord Webhook Integration
 * 
 * This script enables real-time synchronization of GitHub events to Discord channels.
 * Supports: Issues, Pull Requests, Commits, Releases, and more.
 * 
 * Setup:
 * 1. Create a Discord webhook URL in your server settings
 * 2. Set the DISCORD_WEBHOOK_URL environment variable
 * 3. Configure GitHub webhook to point to this endpoint
 * 4. Deploy as serverless function or Express app
 */

const crypto = require('crypto');

/**
 * Configuration
 */
const CONFIG = {
  discordWebhookUrl: process.env.DISCORD_WEBHOOK_URL || '',
  githubWebhookSecret: process.env.GITHUB_WEBHOOK_SECRET || '',
  colors: {
    issue: 0xFFA500,      // Orange
    pullRequest: 0x6F42C1, // Purple
    commit: 0x28A745,     // Green
    release: 0x0366D6,    // Blue
    error: 0xDC3545       // Red
  }
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
 * Send message to Discord
 */
async function sendToDiscord(payload) {
  if (!CONFIG.discordWebhookUrl) {
    throw new Error('DISCORD_WEBHOOK_URL not configured');
  }

  const response = await fetch(CONFIG.discordWebhookUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`Discord webhook failed: ${response.statusText}`);
  }

  return response;
}

/**
 * Format issue event for Discord
 */
function formatIssueEvent(event) {
  const { action, issue, repository } = event;
  
  const embed = {
    title: `Issue ${action}: #${issue.number} ${issue.title}`,
    url: issue.html_url,
    description: issue.body?.substring(0, 300) || 'No description provided',
    color: CONFIG.colors.issue,
    author: {
      name: issue.user.login,
      icon_url: issue.user.avatar_url,
      url: issue.user.html_url,
    },
    fields: [
      {
        name: 'Repository',
        value: repository.full_name,
        inline: true,
      },
      {
        name: 'State',
        value: issue.state,
        inline: true,
      },
    ],
    timestamp: new Date(issue.created_at).toISOString(),
  };

  if (issue.labels.length > 0) {
    embed.fields.push({
      name: 'Labels',
      value: issue.labels.map(l => l.name).join(', '),
      inline: false,
    });
  }

  return {
    username: 'GitHub Bot',
    avatar_url: 'https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png',
    embeds: [embed],
  };
}

/**
 * Format pull request event for Discord
 */
function formatPullRequestEvent(event) {
  const { action, pull_request, repository } = event;
  
  const embed = {
    title: `PR ${action}: #${pull_request.number} ${pull_request.title}`,
    url: pull_request.html_url,
    description: pull_request.body?.substring(0, 300) || 'No description provided',
    color: CONFIG.colors.pullRequest,
    author: {
      name: pull_request.user.login,
      icon_url: pull_request.user.avatar_url,
      url: pull_request.user.html_url,
    },
    fields: [
      {
        name: 'Repository',
        value: repository.full_name,
        inline: true,
      },
      {
        name: 'State',
        value: pull_request.state,
        inline: true,
      },
      {
        name: 'Changes',
        value: `+${pull_request.additions} -${pull_request.deletions}`,
        inline: true,
      },
    ],
    timestamp: new Date(pull_request.created_at).toISOString(),
  };

  if (pull_request.merged) {
    embed.fields.push({
      name: 'Status',
      value: '✅ Merged',
      inline: true,
    });
  }

  return {
    username: 'GitHub Bot',
    avatar_url: 'https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png',
    embeds: [embed],
  };
}

/**
 * Format push event for Discord
 */
function formatPushEvent(event) {
  const { commits, repository, pusher, ref } = event;
  
  const branch = ref.replace('refs/heads/', '');
  const commitList = commits.slice(0, 5).map(commit => {
    return `[\`${commit.id.substring(0, 7)}\`](${commit.url}) ${commit.message.split('\n')[0]}`;
  }).join('\n');

  const embed = {
    title: `${commits.length} new commit${commits.length > 1 ? 's' : ''} to ${branch}`,
    url: `${repository.html_url}/tree/${branch}`,
    description: commitList,
    color: CONFIG.colors.commit,
    author: {
      name: pusher.name,
    },
    fields: [
      {
        name: 'Repository',
        value: repository.full_name,
        inline: true,
      },
      {
        name: 'Branch',
        value: branch,
        inline: true,
      },
    ],
    timestamp: new Date().toISOString(),
  };

  if (commits.length > 5) {
    embed.description += `\n\n... and ${commits.length - 5} more commits`;
  }

  return {
    username: 'GitHub Bot',
    avatar_url: 'https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png',
    embeds: [embed],
  };
}

/**
 * Format release event for Discord
 */
function formatReleaseEvent(event) {
  const { action, release, repository } = event;
  
  const embed = {
    title: `🚀 Release ${action}: ${release.name || release.tag_name}`,
    url: release.html_url,
    description: release.body?.substring(0, 500) || 'No release notes provided',
    color: CONFIG.colors.release,
    author: {
      name: release.author.login,
      icon_url: release.author.avatar_url,
      url: release.author.html_url,
    },
    fields: [
      {
        name: 'Repository',
        value: repository.full_name,
        inline: true,
      },
      {
        name: 'Tag',
        value: release.tag_name,
        inline: true,
      },
    ],
    timestamp: new Date(release.published_at).toISOString(),
  };

  if (release.prerelease) {
    embed.fields.push({
      name: 'Type',
      value: '⚠️ Pre-release',
      inline: true,
    });
  }

  return {
    username: 'GitHub Bot',
    avatar_url: 'https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png',
    embeds: [embed],
  };
}

/**
 * Format star event for Discord
 */
function formatStarEvent(event) {
  const { action, repository, sender } = event;
  
  if (action !== 'created') return null; // Only notify on new stars

  return {
    username: 'GitHub Bot',
    avatar_url: 'https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png',
    content: `⭐ **${sender.login}** starred [${repository.full_name}](${repository.html_url})! Total stars: ${repository.stargazers_count}`,
  };
}

/**
 * Main webhook handler
 */
async function handleWebhook(event, eventType, signature, rawBody) {
  // Verify signature
  if (!verifySignature(rawBody, signature)) {
    throw new Error('Invalid webhook signature');
  }

  let discordPayload = null;

  // Route based on event type
  switch (eventType) {
    case 'issues':
      discordPayload = formatIssueEvent(event);
      break;
    
    case 'pull_request':
      discordPayload = formatPullRequestEvent(event);
      break;
    
    case 'push':
      discordPayload = formatPushEvent(event);
      break;
    
    case 'release':
      discordPayload = formatReleaseEvent(event);
      break;
    
    case 'star':
      discordPayload = formatStarEvent(event);
      break;
    
    default:
      console.log(`Unsupported event type: ${eventType}`);
      return { success: true, message: 'Event type not configured' };
  }

  if (discordPayload) {
    await sendToDiscord(discordPayload);
    return { success: true, message: 'Event forwarded to Discord' };
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
  const PORT = process.env.PORT || 3000;
  const app = createExpressHandler();
  
  app.listen(PORT, () => {
    console.log(`GitHub-Discord webhook server running on port ${PORT}`);
    console.log(`Webhook endpoint: http://localhost:${PORT}/webhook/github`);
  });
}
