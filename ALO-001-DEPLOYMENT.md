# ALO-001 Deployment Guide

This guide explains how to deploy the Euystacio ALO-001 RBAC system with Google OAuth authentication.

## Prerequisites

1. **Google Cloud Project** with OAuth 2.0 configured
2. **Node.js** version 18 or higher
3. **npm** or **yarn** package manager

## Google OAuth Setup

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API (for user info access)

### 2. Configure OAuth Consent Screen

1. Navigate to **APIs & Services** > **OAuth consent screen**
2. Choose **External** user type
3. Fill in required information:
   - App name: "Euystacio Sacred Access"
   - User support email: Your email
   - Developer contact: Your email
4. Add scopes:
   - `https://www.googleapis.com/auth/userinfo.email`
   - `https://www.googleapis.com/auth/userinfo.profile`
5. Add test users if still in testing mode

### 3. Create OAuth 2.0 Credentials

1. Navigate to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **OAuth client ID**
3. Choose **Web application**
4. Configure:
   - **Name**: "Euystacio Web Client"
   - **Authorized JavaScript origins**: 
     - `http://localhost:8080` (for local testing)
     - `https://your-production-domain.com`
   - **Authorized redirect URIs**: Leave empty (using ID token flow)
5. Copy the **Client ID** (format: `xxxxx.apps.googleusercontent.com`)

## Backend Deployment

### 1. Configure Environment

Copy `.env.example` to `.env` and update values:

```bash
cp .env.example .env
```

Edit `.env` with your actual values:

```env
GOOGLE_CLIENT_ID=your-actual-client-id.apps.googleusercontent.com
SEEDBRINGER_EMAILS=hannes.mitterer@gmail.com
COUNCIL_EMAILS=dietmar.zuegg@gmail.com,bioarchitettura.rivista@gmail.com,consultant.laquila@gmail.com
REQUIRED_SCOPES_SEEDBRINGER=https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile
REQUIRED_SCOPES_COUNCIL=https://www.googleapis.com/auth/userinfo.email
PORT=3000
NODE_ENV=production
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Build TypeScript

```bash
npm run build
```

### 4. Start Server

For production:
```bash
npm start
```

For development (with auto-reload):
```bash
npm run dev
```

The server will start on port 3000 (or the port specified in `.env`).

### 5. Production Deployment Options

#### Option A: Heroku

1. Create `Procfile` (already exists):
   ```
   web: npm start
   ```

2. Deploy:
   ```bash
   heroku create euystacio-backend
   heroku config:set GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
   heroku config:set SEEDBRINGER_EMAILS=hannes.mitterer@gmail.com
   # ... set other env vars
   git push heroku main
   ```

#### Option B: Railway / Render

1. Connect your GitHub repository
2. Set environment variables in the dashboard
3. Set build command: `npm run build`
4. Set start command: `npm start`

#### Option C: VPS (Ubuntu/Debian)

1. Install Node.js:
   ```bash
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt-get install -y nodejs
   ```

2. Clone repository and setup:
   ```bash
   git clone https://github.com/hannesmitterer/Euystacio.git
   cd Euystacio
   npm install
   npm run build
   ```

3. Use PM2 for process management:
   ```bash
   sudo npm install -g pm2
   pm2 start dist/server.js --name euystacio-api
   pm2 startup
   pm2 save
   ```

4. Configure nginx as reverse proxy (optional).

## Frontend Deployment

### Update Google Client ID

Edit `public/pbl-001/index.html` and replace the placeholder:

```html
<div id="g_id_onload"
     data-client_id="YOUR_GOOGLE_CLIENT_ID"  <!-- Replace this -->
     data-callback="handleCredentialResponse"
     data-auto_prompt="false">
</div>
```

With your actual Client ID:

```html
<div id="g_id_onload"
     data-client_id="123456789-abcdefg.apps.googleusercontent.com"
     data-callback="handleCredentialResponse"
     data-auto_prompt="false">
</div>
```

### Update Backend API URL

Users can configure the backend URL in the UI, or you can set a default by editing the HTML:

```html
<input 
    type="text" 
    id="api-base-url" 
    value="https://your-backend-api.com"  <!-- Update this -->
    ...
/>
```

### Deploy Frontend

#### Option A: GitHub Pages

1. Ensure `public/pbl-001/index.html` is updated with correct Client ID
2. Go to repository **Settings** > **Pages**
3. Set source to `main` branch, `/public` folder (or root)
4. Your site will be available at `https://username.github.io/Euystacio/pbl-001/`

#### Option B: Netlify

1. Create a `netlify.toml`:
   ```toml
   [build]
     publish = "public"
   ```
2. Connect repository to Netlify
3. Deploy

#### Option C: Vercel

1. Import project
2. Set root directory to `public`
3. Deploy

## Testing the Deployment

1. Open the frontend URL in a browser
2. Click the Google Sign-In button
3. Authenticate with an authorized email (Seedbringer or Council)
4. Test the API endpoints:
   - **GET /sfi** - Should work for both roles
   - **GET /mcl/live** - Should work for both roles
   - **POST /allocations** - Should only work for Seedbringer

## Role-Based Access Control (RBAC)

### Roles

- **Seedbringer**: Full access (read + write)
  - Can access: GET /sfi, GET /mcl/live, POST /allocations
  - Email: hannes.mitterer@gmail.com

- **Council**: Read-only access
  - Can access: GET /sfi, GET /mcl/live
  - Emails: dietmar.zuegg@gmail.com, bioarchitettura.rivista@gmail.com, consultant.laquila@gmail.com

### Adding/Removing Users

Edit the `.env` file and restart the server:

```env
SEEDBRINGER_EMAILS=email1@gmail.com,email2@gmail.com
COUNCIL_EMAILS=email3@gmail.com,email4@gmail.com,email5@gmail.com
```

## API Endpoints

### Public Endpoints

- `GET /health` - Health check (no auth required)

### Protected Endpoints

All require `Authorization: Bearer <google-id-token>` header.

- `GET /sfi` - Seedbringer Financial Interface (Council or Seedbringer)
- `GET /mcl/live` - Master Control Live data (Council or Seedbringer)
- `POST /allocations` - Create allocation (Seedbringer only)

## Troubleshooting

### "Invalid or expired token" error

- Ensure the Google Client ID in `.env` matches the one in the HTML
- Check that the OAuth consent screen is configured correctly
- Verify that the requesting user's email is in an allowlist

### CORS errors

- The backend uses CORS middleware with open access
- For production, consider restricting to specific origins in `src/server.ts`

### Port already in use

- Change the PORT in `.env`
- Or kill the existing process: `pkill -f "node dist/server.js"`

## Security Notes

1. **Never commit `.env`** - It's already in `.gitignore`
2. **Use HTTPS in production** - Required by Google Sign-In
3. **Restrict CORS** - Update `src/server.ts` to limit origins
4. **Keep dependencies updated** - Run `npm audit` regularly
5. **Monitor access logs** - The server logs all authentication attempts
6. **Rate Limiting (Recommended)** - For production deployments, consider adding rate limiting middleware (e.g., `express-rate-limit`) to prevent DoS attacks on authentication endpoints
7. **Token Expiration** - Google ID tokens expire after 1 hour; implement token refresh logic for long-running sessions

## Support

For issues or questions, please open an issue in the GitHub repository.
