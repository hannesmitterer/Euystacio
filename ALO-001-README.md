# ALO-001: Google OAuth Backend Enforcement

This implementation adds Google OAuth ID token verification to protect backend endpoints with role-based access control.

## Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and set:
   - `GOOGLE_CLIENT_ID`: Your Google OAuth client ID from Google Cloud Console
   - `COUNCIL_ALLOWLIST`: Comma-separated list of email addresses with Council access
   - `SEEDBRINGER_ALLOWLIST`: Comma-separated list of email addresses with Seedbringer access
   - `PORT`: Server port (default: 3000)

3. **Build the TypeScript:**
   ```bash
   npm run build
   ```

4. **Start the server:**
   ```bash
   npm start
   ```

## Protected Endpoints

### Council Access Required
- `GET /sfi` - Sacred Field Interface access
- `GET /mcl/live` - MCL Live access

### Seedbringer Access Required
- `POST /allocations` - Submit resource allocations

### Public Endpoints
- `GET /health` - Health check

## Frontend

Access the interface at `/pbl-001/` to:
1. Sign in with Google
2. Access protected endpoints with your credentials
3. View responses from authenticated API calls

## Google Cloud Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials (Web application)
5. Add authorized JavaScript origins:
   - `http://localhost:3000` (for local development)
   - Your production domain
6. Copy the Client ID and update:
   - `.env` file: `GOOGLE_CLIENT_ID`
   - `public/pbl-001/index.html`: Replace `YOUR_GOOGLE_CLIENT_ID` with your actual Client ID

## Architecture

- **Backend**: Node.js + Express + TypeScript
- **Authentication**: Google OAuth 2.0 (ID tokens)
- **Authorization**: Role-based allowlists (Council, Seedbringer)
- **Frontend**: HTML + JavaScript + Google Identity Services

## Security

- All protected endpoints require valid Google ID tokens
- Role verification via email allowlists loaded from environment
- No hardcoded credentials
- HTTPS recommended for production
- GitHub Actions workflow with minimal permissions

## CI/CD

The `.github/workflows/alo-001-ci.yml` workflow:
- Builds TypeScript on every push
- Verifies `.env.example` exists
- Validates required environment variables
- Checks build artifacts

## Development

```bash
# Development mode (build and run)
npm run dev
```

## License

See project root for license information.
