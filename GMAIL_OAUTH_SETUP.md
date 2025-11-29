# Gmail OAuth 2.0 Setup Guide

This guide walks you through setting up Gmail OAuth 2.0 for the Nexus API to send notifications and emails.

---

## Overview

Gmail OAuth 2.0 allows your application to send emails on behalf of users without storing passwords. This guide covers:

1. Creating a Google Cloud Project
2. Enabling Gmail API
3. Configuring OAuth 2.0 credentials
4. Obtaining refresh tokens
5. Configuring environment variables

---

## Prerequisites

- A Google account
- Access to Google Cloud Console
- Admin access to your application

---

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **Select a project** → **New Project**
3. Enter project details:
   - **Project name:** `Euystacio Nexus`
   - **Organization:** (optional)
4. Click **Create**
5. Wait for project creation to complete

---

## Step 2: Enable Gmail API

1. In the Google Cloud Console, select your project
2. Navigate to **APIs & Services** → **Library**
3. Search for **Gmail API**
4. Click **Gmail API** in the results
5. Click **Enable**
6. Wait for API to be enabled

---

## Step 3: Configure OAuth Consent Screen

1. Navigate to **APIs & Services** → **OAuth consent screen**
2. Select user type:
   - **Internal:** Only for Google Workspace organization users
   - **External:** For all users (select this for public apps)
3. Click **Create**
4. Fill in application information:

   **App Information:**
   - **App name:** `Euystacio Nexus`
   - **User support email:** Your email address
   - **App logo:** (optional) Upload your logo

   **App Domain:**
   - **Application home page:** `https://nexus.euystacio.io`
   - **Application privacy policy:** `https://nexus.euystacio.io/privacy`
   - **Application terms of service:** `https://nexus.euystacio.io/terms`

   **Authorized domains:**
   - Add: `euystacio.io`

   **Developer contact:**
   - Your email address

5. Click **Save and Continue**

---

## Step 4: Configure Scopes

1. On the **Scopes** page, click **Add or Remove Scopes**
2. Add the following Gmail scopes:

   **Required Scopes:**
   - `https://www.googleapis.com/auth/gmail.send` - Send email on behalf of user
   - `https://www.googleapis.com/auth/gmail.readonly` - Read email metadata (optional)
   - `https://www.googleapis.com/auth/userinfo.email` - Get user email address
   - `https://www.googleapis.com/auth/userinfo.profile` - Get user profile info

3. Click **Update**
4. Click **Save and Continue**

---

## Step 5: Create OAuth 2.0 Credentials

1. Navigate to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. Select application type:
   - **Application type:** `Web application`
   - **Name:** `Euystacio Nexus Web Client`

4. Configure authorized redirect URIs:

   **Authorized JavaScript origins:**
   ```
   https://nexus.euystacio.io
   http://localhost:8080
   ```

   **Authorized redirect URIs:**
   ```
   https://nexus.euystacio.io/oauth/callback
   https://nexus.euystacio.io/oauth/gmail/callback
   http://localhost:8080/oauth/callback
   http://localhost:8080/oauth/gmail/callback
   ```

5. Click **Create**
6. **Save your credentials:**
   - **Client ID:** `abc123.apps.googleusercontent.com`
   - **Client Secret:** `GOCSPX-abc123xyz...`

   ⚠️ **Important:** Store these securely! Never commit to Git.

---

## Step 6: Obtain Refresh Token

You need a refresh token to make API calls without user interaction.

### Method 1: Using OAuth Playground

1. Go to [OAuth 2.0 Playground](https://developers.google.com/oauthplayground/)
2. Click settings (gear icon) → Check **Use your own OAuth credentials**
3. Enter your:
   - **OAuth Client ID:** `your_client_id`
   - **OAuth Client Secret:** `your_client_secret`
4. In **Step 1**, select scopes:
   - `https://www.googleapis.com/auth/gmail.send`
   - `https://www.googleapis.com/auth/userinfo.email`
5. Click **Authorize APIs**
6. Sign in with Google and grant permissions
7. In **Step 2**, click **Exchange authorization code for tokens**
8. **Save the Refresh Token** displayed

### Method 2: Using Custom Script

Create `get_refresh_token.js`:

```javascript
const { OAuth2Client } = require('google-auth-library');
const readline = require('readline');

const CLIENT_ID = 'your_client_id_here';
const CLIENT_SECRET = 'your_client_secret_here';
const REDIRECT_URI = 'http://localhost:8080/oauth/callback';

const SCOPES = [
  'https://www.googleapis.com/auth/gmail.send',
  'https://www.googleapis.com/auth/userinfo.email'
];

const oauth2Client = new OAuth2Client(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI);

// Generate auth URL
const authUrl = oauth2Client.generateAuthUrl({
  access_type: 'offline',
  scope: SCOPES,
  prompt: 'consent'
});

console.log('Authorize this app by visiting this URL:');
console.log(authUrl);

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question('Enter the authorization code: ', async (code) => {
  try {
    const { tokens } = await oauth2Client.getToken(code);
    console.log('\nYour refresh token:');
    console.log(tokens.refresh_token);
  } catch (error) {
    console.error('Error retrieving token:', error);
  }
  rl.close();
});
```

Run the script:
```bash
npm install google-auth-library
node get_refresh_token.js
```

Follow the prompts and save the refresh token.

---

## Step 7: Configure Environment Variables

Add the following to your `.env` file:

```bash
# Gmail OAuth 2.0 Configuration
GMAIL_CLIENT_ID=abc123.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=GOCSPX-abc123xyz...
GMAIL_REFRESH_TOKEN=1//0abc123xyz...

# Email Configuration
GMAIL_FROM_EMAIL=noreply@euystacio.io
GMAIL_FROM_NAME=Euystacio Nexus

# Optional: Rate Limiting
GMAIL_MAX_EMAILS_PER_DAY=500
GMAIL_MAX_EMAILS_PER_HOUR=50
```

**⚠️ Security Note:** Never commit these values to version control!

---

## Step 8: Test the Integration

### Test Script (Node.js)

Create `test_gmail.js`:

```javascript
const { google } = require('googleapis');
require('dotenv').config();

const oauth2Client = new google.auth.OAuth2(
  process.env.GMAIL_CLIENT_ID,
  process.env.GMAIL_CLIENT_SECRET
);

oauth2Client.setCredentials({
  refresh_token: process.env.GMAIL_REFRESH_TOKEN
});

const gmail = google.gmail({ version: 'v1', auth: oauth2Client });

async function sendTestEmail() {
  const message = [
    'From: Euystacio Nexus <noreply@euystacio.io>',
    'To: your-email@example.com',
    'Subject: Test Email from Nexus API',
    '',
    'This is a test email sent via Gmail OAuth 2.0.'
  ].join('\n');

  const encodedMessage = Buffer.from(message)
    .toString('base64')
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');

  try {
    const result = await gmail.users.messages.send({
      userId: 'me',
      requestBody: {
        raw: encodedMessage
      }
    });
    console.log('Email sent successfully!');
    console.log('Message ID:', result.data.id);
  } catch (error) {
    console.error('Error sending email:', error);
  }
}

sendTestEmail();
```

Run the test:
```bash
npm install googleapis
node test_gmail.js
```

### Test Script (Python)

Create `test_gmail.py`:

```python
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

def send_test_email():
    creds = Credentials.from_authorized_user_info({
        'client_id': os.environ['GMAIL_CLIENT_ID'],
        'client_secret': os.environ['GMAIL_CLIENT_SECRET'],
        'refresh_token': os.environ['GMAIL_REFRESH_TOKEN']
    })

    service = build('gmail', 'v1', credentials=creds)

    message = MIMEText('This is a test email from Nexus API')
    message['to'] = 'your-email@example.com'
    message['from'] = 'noreply@euystacio.io'
    message['subject'] = 'Test Email from Nexus API'

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    
    try:
        result = service.users().messages().send(
            userId='me',
            body={'raw': raw}
        ).execute()
        print('Email sent successfully!')
        print('Message ID:', result['id'])
    except Exception as error:
        print('Error sending email:', error)

if __name__ == '__main__':
    send_test_email()
```

Run the test:
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
python test_gmail.py
```

---

## API Integration Example

### Sending Notification Emails

```javascript
// services/gmail.js
const { google } = require('googleapis');

class GmailService {
  constructor() {
    this.oauth2Client = new google.auth.OAuth2(
      process.env.GMAIL_CLIENT_ID,
      process.env.GMAIL_CLIENT_SECRET
    );

    this.oauth2Client.setCredentials({
      refresh_token: process.env.GMAIL_REFRESH_TOKEN
    });

    this.gmail = google.gmail({ version: 'v1', auth: this.oauth2Client });
  }

  async sendEmail({ to, subject, body, isHtml = false }) {
    const message = [
      `From: ${process.env.GMAIL_FROM_NAME} <${process.env.GMAIL_FROM_EMAIL}>`,
      `To: ${to}`,
      `Subject: ${subject}`,
      isHtml ? 'Content-Type: text/html; charset=utf-8' : '',
      '',
      body
    ].join('\n');

    const encodedMessage = Buffer.from(message)
      .toString('base64')
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=+$/, '');

    try {
      const result = await this.gmail.users.messages.send({
        userId: 'me',
        requestBody: { raw: encodedMessage }
      });
      return { success: true, messageId: result.data.id };
    } catch (error) {
      console.error('Gmail send error:', error);
      return { success: false, error: error.message };
    }
  }

  async sendTaskCompletionEmail(task) {
    return this.sendEmail({
      to: task.notifyEmail,
      subject: `Task Completed: ${task.title}`,
      body: `
        Your task "${task.title}" has been completed successfully.
        
        Task ID: ${task.id}
        Status: ${task.status}
        Completed at: ${task.completedAt}
        
        View details: https://nexus.euystacio.io/tasks/${task.id}
      `
    });
  }
}

module.exports = new GmailService();
```

---

## Scope Reference

### Available Gmail Scopes

| Scope | Description | Use Case |
|-------|-------------|----------|
| `gmail.send` | Send email only | Notifications |
| `gmail.readonly` | Read email | Email ingestion |
| `gmail.modify` | Read and modify | Full email management |
| `gmail.compose` | Create drafts | Draft creation |
| `gmail.labels` | Manage labels | Organization |
| `gmail.metadata` | Read metadata | Headers only |

### Recommended Scopes for Nexus API

```
https://www.googleapis.com/auth/gmail.send
https://www.googleapis.com/auth/userinfo.email
https://www.googleapis.com/auth/userinfo.profile
```

---

## Troubleshooting

### Common Issues

**"Invalid grant" error:**
- Refresh token may have expired
- Regenerate refresh token using OAuth Playground
- Ensure `access_type: 'offline'` when generating tokens

**"Insufficient permissions" error:**
- Check scopes are correctly configured
- Regenerate consent with all required scopes
- Ensure user has granted permissions

**"Daily sending quota exceeded":**
- Gmail has daily sending limits (500-2000 emails/day)
- Implement rate limiting
- Consider using SendGrid/Mailgun for high volume

**Token refresh fails:**
- Verify CLIENT_ID and CLIENT_SECRET are correct
- Check refresh token hasn't been revoked
- Ensure credentials match OAuth consent screen

---

## Security Best Practices

### Do's ✅
- Store credentials in environment variables
- Use HTTPS for redirect URIs
- Implement rate limiting
- Log all email sends for audit
- Rotate refresh tokens periodically
- Validate recipient email addresses

### Don'ts ❌
- Never commit credentials to Git
- Don't expose client secret in frontend
- Don't send emails without user consent
- Don't store passwords
- Don't share refresh tokens between apps

---

## Sample Environment Entries

Add these to your `.env` file (with actual values):

```bash
# Gmail OAuth 2.0
GMAIL_CLIENT_ID=123456789-abc123xyz.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=GOCSPX-AbCdEfGhIjKlMnOpQrStUvWxYz
GMAIL_REFRESH_TOKEN=1//0abcdefghijklmnopqrstuvwxyz1234567890

# Email Settings
GMAIL_FROM_EMAIL=noreply@euystacio.io
GMAIL_FROM_NAME=Euystacio Nexus
GMAIL_MAX_EMAILS_PER_DAY=500
GMAIL_MAX_EMAILS_PER_HOUR=50

# Optional: Template Settings
EMAIL_TEMPLATE_DIR=./templates/email
EMAIL_LOGO_URL=https://nexus.euystacio.io/logo.png
```

---

## Resources

- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [OAuth 2.0 Guide](https://developers.google.com/identity/protocols/oauth2)
- [Google Cloud Console](https://console.cloud.google.com/)
- [OAuth 2.0 Playground](https://developers.google.com/oauthplayground/)

---

**Last Updated:** 2025-11-03
