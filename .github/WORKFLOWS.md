# GitHub Actions Workflows Documentation

This document describes the CI/CD automation workflows for the Euystacio repository.

## Overview

The repository uses multiple GitHub Actions workflows to ensure code quality, security, and reliable deployment.

## Workflows

### 1. CI/CD Pipeline (`ci-cd.yml`)

**Triggers:**
- Push to `main` branch
- Pull requests to `main` branch
- Manual dispatch

**Jobs:**

#### Lint & Test
- Installs Node.js and Python dependencies
- Runs linting for TypeScript/JavaScript and Python code
- Builds the TypeScript project
- Verifies build artifacts
- Uploads build artifacts for 7 days

#### Security Scan
- Runs `npm audit` for dependency vulnerabilities
- Performs dependency review for PRs
- Identifies potential security issues

#### Build Verification
- Performs a clean build of the project
- Verifies environment configuration (.env.example)
- Tests Python app imports
- Validates all components

#### Workflow Status
- Reports the status of all jobs
- Runs always, even if previous jobs fail

**Concurrency:** 
- Cancels in-progress runs for the same branch

---

### 2. GitHub Pages Deployment (`github-pages.yml`)

**Triggers:**
- Push to `main` branch
- Manual dispatch

**Jobs:**

#### Build Site
- Prepares static site content
- Copies `index.html` and HTML files
- Includes static assets and images
- Uploads Pages artifact

#### Deploy to Pages
- Deploys to GitHub Pages
- Requires successful build
- Updates environment with deployment URL

**Permissions:**
- `contents: read`
- `pages: write`
- `id-token: write`

**Deployment URL:** `https://hannesmitterer.github.io/Euystacio`

---

### 3. ALO-001 CI (`alo-001-ci.yml`)

**Triggers:**
- Push to branches matching `alo-001/**` or `copilot/alo-001**`
- Pull requests to `main`
- Manual dispatch

**Jobs:**

#### Build and Verify
- Sets up Node.js environment using composite action
- Builds TypeScript code
- Verifies `.env.example` exists and contains required variables
- Checks build artifacts
- Runs security audit
- Uploads build artifacts

**Required Environment Variables:**
- `GOOGLE_CLIENT_ID`
- `COUNCIL_ALLOWLIST`
- `SEEDBRINGER_ALLOWLIST`

---

### 4. Main Branch CI (`main.yml`)

**Triggers:**
- Push to `main` branch
- Manual dispatch

**Jobs:**

#### Validate & Build
- Sets up Node.js and Python environments using composite actions
- Builds TypeScript project
- Validates Python apps
- Performs repository health check

**Purpose:** 
- Ensures main branch is always in a deployable state
- Validates both Node.js and Python components

---

### 5. Dependency Review (`dependency-review.yml`)

**Triggers:**
- Pull requests to `main` branch

**Jobs:**

#### Review Dependencies
- Reviews dependencies added in PRs
- Checks for known vulnerabilities
- Fails on moderate+ severity issues
- Comments summary in PR
- Denies problematic licenses (AGPL, GPL)

**Purpose:**
- Prevents introduction of vulnerable dependencies
- Ensures license compliance
- Provides automated security review

---

### 6. PR Auto-Labeler (`pr-labeler.yml`)

**Triggers:**
- Pull request opened, synchronized, or reopened

**Jobs:**

#### Label Pull Request
- Automatically labels PRs based on changed files
- Uses configuration from `.github/labeler.yml`

**Labels Applied:**
- `documentation` - Markdown or docs changes
- `workflows` - GitHub Actions changes
- `typescript` - TypeScript code changes
- `python` - Python code changes
- `configuration` - Config file changes
- `frontend` - HTML/CSS changes
- `dependencies` - Dependency updates
- `security` - Security-related changes

---

### 7. Scheduled Health Checks (`scheduled-checks.yml`)

**Triggers:**
- Daily at 6 AM UTC (cron schedule)
- Manual dispatch

**Jobs:**

#### Health Check
- Performs daily build verification
- Runs security audits
- Checks Python dependencies
- Verifies critical files exist
- Tests GitHub Pages URL
- Creates GitHub issue on failure

#### Dependency Updates
- Checks for outdated npm packages
- Checks for outdated pip packages
- Reports available updates

**Purpose:**
- Catches regressions early
- Monitors dependency health
- Ensures continuous deployability

---

## Composite Actions

### Setup Node.js Environment (`.github/actions/setup-node-env`)

Reusable action for Node.js setup with caching.

**Inputs:**
- `node-version` (default: '18')
- `install-deps` (default: 'true')

**Steps:**
1. Setup Node.js with npm cache
2. Install dependencies with `npm ci`
3. Display Node.js and npm versions

**Usage:**
```yaml
- name: Setup Node.js
  uses: ./.github/actions/setup-node-env
  with:
    node-version: '18'
    install-deps: 'true'
```

### Setup Python Environment (`.github/actions/setup-python-env`)

Reusable action for Python setup with caching.

**Inputs:**
- `python-version` (default: '3.9')
- `install-deps` (default: 'true')

**Steps:**
1. Setup Python with pip cache
2. Install dependencies from `requirements.txt`
3. Display Python and pip versions

**Usage:**
```yaml
- name: Setup Python
  uses: ./.github/actions/setup-python-env
  with:
    python-version: '3.9'
    install-deps: 'true'
```

---

## Best Practices

### Caching
- Node.js dependencies are cached automatically using `cache: 'npm'`
- Python dependencies are cached automatically using `cache: 'pip'`
- Reduces workflow execution time significantly

### Concurrency
- Workflows use concurrency groups to prevent duplicate runs
- `cancel-in-progress: true` cancels outdated runs automatically
- Saves CI minutes and provides faster feedback

### Security
- All workflows run with minimal required permissions
- Security scans run on every PR and push
- Dependencies are audited for vulnerabilities
- Build artifacts are stored for 7 days

### Artifacts
- Build outputs are uploaded as artifacts
- Available for debugging and deployment
- Retention period: 7 days

---

## Monitoring

### Workflow Status Badges

Add these badges to your README.md:

```markdown
![CI/CD Pipeline](https://github.com/hannesmitterer/Euystacio/actions/workflows/ci-cd.yml/badge.svg)
![GitHub Pages](https://github.com/hannesmitterer/Euystacio/actions/workflows/github-pages.yml/badge.svg)
![ALO-001 CI](https://github.com/hannesmitterer/Euystacio/actions/workflows/alo-001-ci.yml/badge.svg)
```

### Viewing Workflow Runs
1. Go to the "Actions" tab in the repository
2. Select the workflow you want to view
3. Click on a specific run to see details
4. Review job logs for debugging

### Downloading Artifacts
1. Navigate to a completed workflow run
2. Scroll to the "Artifacts" section
3. Click to download build artifacts

---

## Troubleshooting

### Common Issues

#### Build Failures
- Ensure all dependencies are listed in `package.json` or `requirements.txt`
- Check that the Node.js and Python versions match local development
- Review build logs for specific error messages

#### Permission Errors
- Verify repository settings under Settings → Actions → General
- Ensure required permissions are granted for Pages deployment
- Check branch protection rules

#### Cache Issues
- Clear caches by re-running workflows
- Update action versions if caching behavior changes

### Getting Help
- Check workflow logs for detailed error messages
- Review GitHub Actions documentation
- Open an issue with workflow run ID

---

## Configuration Files

### `.github/workflows/`
- Contains all workflow YAML files
- Each workflow has specific triggers and jobs

### `.github/actions/`
- Contains reusable composite actions
- Simplifies workflow maintenance

### `_config.yml`
- Jekyll configuration for GitHub Pages
- Specifies included/excluded files
- Defines site metadata

---

## Future Enhancements

Potential improvements for the CI/CD pipeline:

1. **Testing**
   - Add unit tests for TypeScript code
   - Add integration tests for Python apps
   - Add E2E tests for web interfaces

2. **Coverage Reports**
   - Generate code coverage reports
   - Upload coverage to Codecov or similar

3. **Performance Monitoring**
   - Track build times
   - Monitor deployment performance
   - Set up alerts for slow builds

4. **Advanced Deployment**
   - Add staging environment
   - Implement blue-green deployments
   - Add rollback capabilities

5. **Notifications**
   - Slack or Discord notifications
   - Email alerts for failures
   - Custom webhook integrations

---

## Maintenance

### Updating Actions
- Keep action versions up to date
- Review changelogs before updating
- Test changes in a separate branch

### Dependency Updates
- Run `npm audit fix` regularly
- Update Python packages in `requirements.txt`
- Monitor Dependabot alerts

### Workflow Reviews
- Review workflow efficiency quarterly
- Optimize for speed and cost
- Remove unused workflows

---

## Support

For questions or issues with workflows:
- Open an issue in the repository
- Tag with `ci/cd` label
- Provide workflow run ID and logs

---

**Last Updated:** December 2025
**Maintained by:** Euystacio Development Team
