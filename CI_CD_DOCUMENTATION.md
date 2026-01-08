# CI/CD Documentation

This document describes the comprehensive CI/CD automation setup for the Euystacio repository.

## Overview

The repository uses GitHub Actions for automated building, testing, deployment, and maintenance. All workflows are designed to be modular, secure, and efficient.

## Status Badges

![CI Status](https://github.com/hannesmitterer/Euystacio/actions/workflows/ci.yml/badge.svg)
![Tests](https://github.com/hannesmitterer/Euystacio/actions/workflows/test.yml/badge.svg)
![Lint](https://github.com/hannesmitterer/Euystacio/actions/workflows/lint.yml/badge.svg)
![Security](https://github.com/hannesmitterer/Euystacio/actions/workflows/security.yml/badge.svg)
![Deploy Pages](https://github.com/hannesmitterer/Euystacio/actions/workflows/deploy-pages.yml/badge.svg)

## Workflows

### 1. CI Pipeline (`ci.yml`)

**Triggers:**
- Push to `main`, `copilot/**`, `alo-001/**` branches
- Pull requests to `main`

**Jobs:**
- **TypeScript Build**: Compiles TypeScript, stores artifacts
- **Python Build**: Validates Python components
- **Security Audit**: Runs npm audit and pip-audit
- **Build Status**: Reports overall build status

**Artifacts:**
- TypeScript build artifacts (7-day retention)

### 2. Code Quality & Linting (`lint.yml`)

**Triggers:**
- Push to `main`, `copilot/**` branches
- Pull requests to `main`

**Jobs:**
- **ESLint**: Lints TypeScript/JavaScript code
- **Python Lint**: Runs Flake8, PyLint, and Black formatting checks
- **Prettier**: Checks code formatting
- **Markdownlint**: Validates Markdown files

**Note:** All linting jobs are non-blocking (continue-on-error: true)

### 3. Tests (`test.yml`)

**Triggers:**
- Push to `main`, `copilot/**` branches
- Pull requests to `main`

**Jobs:**
- **TypeScript Tests**: Runs Jest tests
- **Python Tests**: Runs pytest with coverage
- **Integration Tests**: End-to-end testing

**Features:**
- Code coverage reporting
- Import validation
- Server startup verification

### 4. Deploy to GitHub Pages (`deploy-pages.yml`)

**Triggers:**
- Push to `main` branch
- Manual workflow dispatch

**Jobs:**
- **Build Site**: 
  - Compiles TypeScript and Python components
  - Copies static HTML files
  - Converts Markdown to HTML
  - Generates navigation
- **Deploy**: Publishes to GitHub Pages

**Permissions:**
- contents: read
- pages: write
- id-token: write

**Deployment URL:** https://hannesmitterer.github.io/Euystacio/

### 5. Security Scanning (`security.yml`)

**Triggers:**
- Push to `main`
- Pull requests to `main`
- Weekly schedule (Monday 00:00 UTC)
- Manual workflow dispatch

**Jobs:**
- **Gitleaks**: Secret scanning
- **Dependency Review**: Checks for vulnerable dependencies in PRs
- **CodeQL**: Static code analysis (JavaScript & Python)
- **Semgrep**: SAST scanning
- **Supply Chain**: npm and pip security audits

**Features:**
- Automated weekly security scans
- Pull request security reviews
- Vulnerability reports as artifacts

### 6. Uptime Monitor (`uptime-monitor.yml`)

**Triggers:**
- Every 30 minutes (scheduled)
- Manual workflow dispatch

**Jobs:**
- **Monitor**: Checks GitHub Pages availability
- **Notify on Failure**: Creates/updates issues on downtime

**Monitoring:**
- HTTP status checks
- Response time monitoring
- Automated issue creation for failures

### 7. Reusable Build Workflow (`reusable-build.yml`)

A reusable workflow that can be called by other workflows for consistent build processes.

**Inputs:**
- `node-version`: Node.js version (default: '18')
- `python-version`: Python version (default: '3.9')
- `skip-python`: Skip Python build steps
- `skip-typescript`: Skip TypeScript build steps

**Outputs:**
- `build-status`: Status of the build

### 8. ALO-001 CI (`alo-001-ci.yml`)

Legacy CI workflow for ALO-001 specific builds. Validates ALO-001 requirements including .env.example validation.

## Configuration Files

### ESLint (`.eslintrc.json`)
- TypeScript-specific rules
- Error on unused variables
- Code style enforcement

### Prettier (`.prettierrc.json`)
- Single quotes
- 100 character line width
- 2-space indentation
- Unix line endings

### Flake8 (`.flake8`)
- 100 character line length
- Extends ignore list for E203, W503
- Excludes common directories

### Jest (`jest.config.js`)
- TypeScript preset
- Coverage reporting
- Test pattern matching

### Pytest (`pytest.ini`)
- Verbose output
- Coverage reporting (term, HTML, XML)
- Test markers for categorization

## Dependabot Configuration

Automated dependency updates are configured for:
- **npm**: Weekly on Monday
- **pip**: Weekly on Monday
- **GitHub Actions**: Weekly on Monday

Configuration: `.github/dependabot.yml`

## Code Owners

Defined in `.github/CODEOWNERS`:
- Default owner: @hannesmitterer
- Specific ownership for workflows, TypeScript, Python, and documentation

## Local Development

### Setup

```bash
# Install Node.js dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install flake8 pylint black pytest pytest-cov
npm install --save-dev eslint prettier jest ts-jest @types/jest
```

### Build

```bash
# Build TypeScript
npm run build

# Verify Python
python -c "import app; import euystacio_core"
```

### Linting

```bash
# Lint TypeScript
npm run lint

# Fix TypeScript lint issues
npm run lint:fix

# Check formatting
npm run format:check

# Fix formatting
npm run format

# Lint Python
flake8 *.py
pylint *.py
black --check *.py
```

### Testing

```bash
# Run TypeScript tests
npm test

# Run with coverage
npm run test:coverage

# Run Python tests
pytest

# Run with coverage
pytest --cov
```

### Type Checking

```bash
# Check TypeScript types without emitting
npm run typecheck
```

## Security Best Practices

1. **Never commit secrets**: Use environment variables
2. **Use GITHUB_TOKEN**: Workflows use built-in token
3. **Scan dependencies**: Automated via Dependabot and security workflows
4. **Regular audits**: Weekly CodeQL and security scans
5. **Review PRs**: CODEOWNERS ensures proper review

## Deployment Process

### Automatic Deployment

1. Push to `main` branch
2. CI workflows run (build, test, lint)
3. If all pass, deploy-pages workflow triggers
4. Site builds and deploys to GitHub Pages
5. Uptime monitor begins checking availability

### Manual Deployment

```bash
# Trigger manual deployment
gh workflow run deploy-pages.yml
```

Or use the GitHub UI: Actions → Deploy to GitHub Pages → Run workflow

## Monitoring and Alerts

### Uptime Monitoring
- Runs every 30 minutes
- Checks HTTP status and response time
- Creates issues on failure
- Reports stored as artifacts

### Build Status
- All workflows report status via badges
- Failed builds prevent deployment
- Security issues flagged in PRs

## Troubleshooting

### Build Failures

1. Check CI workflow logs
2. Verify dependencies are up to date
3. Run locally: `npm run build`
4. Check for TypeScript errors: `npm run typecheck`

### Test Failures

1. Check test workflow logs
2. Run locally: `npm test` or `pytest`
3. Check coverage reports
4. Verify imports work

### Deployment Issues

1. Check deploy-pages workflow logs
2. Verify GitHub Pages is enabled in repository settings
3. Check that main branch is protected
4. Verify GITHUB_TOKEN permissions

### Security Alerts

1. Review security workflow results
2. Check Dependabot PRs
3. Review CodeQL alerts
4. Update vulnerable dependencies

## Workflow Optimization

### Caching
- Node modules cached by actions/setup-node
- Python packages cached by actions/setup-python
- Reduces build times significantly

### Concurrency Control
- Pages deployment prevents concurrent runs
- Other workflows allow parallel execution
- Reduces resource usage

### Artifact Management
- Build artifacts retained for 7 days
- Monitoring reports retained for 30 days
- Security reports stored as artifacts

## Future Enhancements

Planned improvements:
- [ ] Add E2E testing with Playwright
- [ ] Implement performance testing
- [ ] Add API integration tests
- [ ] Configure Slack/Discord notifications
- [ ] Add deployment previews for PRs
- [ ] Implement blue-green deployments
- [ ] Add canary deployment strategy
- [ ] Configure SonarCloud integration

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [CodeQL Documentation](https://codeql.github.com/docs/)
- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)

## Support

For issues or questions:
- Open an issue: https://github.com/hannesmitterer/Euystacio/issues
- Check discussions: https://github.com/hannesmitterer/Euystacio/discussions
- Email: support@euystacio.io
