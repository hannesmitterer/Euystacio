# Workflow Status

This page provides an overview of all automated workflows in the Euystacio repository.

## Build & Test Status

| Workflow | Status | Description |
|----------|--------|-------------|
| CI Pipeline | [![CI](https://github.com/hannesmitterer/Euystacio/actions/workflows/ci.yml/badge.svg)](https://github.com/hannesmitterer/Euystacio/actions/workflows/ci.yml) | Main CI pipeline for TypeScript and Python builds |
| Tests | [![Tests](https://github.com/hannesmitterer/Euystacio/actions/workflows/test.yml/badge.svg)](https://github.com/hannesmitterer/Euystacio/actions/workflows/test.yml) | Jest and pytest test execution |
| Code Quality | [![Lint](https://github.com/hannesmitterer/Euystacio/actions/workflows/lint.yml/badge.svg)](https://github.com/hannesmitterer/Euystacio/actions/workflows/lint.yml) | ESLint, Flake8, PyLint, Prettier checks |
| ALO-001 CI | [![ALO-001](https://github.com/hannesmitterer/Euystacio/actions/workflows/alo-001-ci.yml/badge.svg)](https://github.com/hannesmitterer/Euystacio/actions/workflows/alo-001-ci.yml) | ALO-001 specific build validation |

## Security

| Workflow | Status | Description |
|----------|--------|-------------|
| Security Scanning | [![Security](https://github.com/hannesmitterer/Euystacio/actions/workflows/security.yml/badge.svg)](https://github.com/hannesmitterer/Euystacio/actions/workflows/security.yml) | CodeQL, Semgrep, Gitleaks, dependency audits |

## Deployment

| Workflow | Status | Description |
|----------|--------|-------------|
| GitHub Pages | [![Deploy](https://github.com/hannesmitterer/Euystacio/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/hannesmitterer/Euystacio/actions/workflows/deploy-pages.yml) | Automated deployment to GitHub Pages |
| Uptime Monitor | [![Uptime](https://github.com/hannesmitterer/Euystacio/actions/workflows/uptime-monitor.yml/badge.svg)](https://github.com/hannesmitterer/Euystacio/actions/workflows/uptime-monitor.yml) | Monitors GitHub Pages availability |

## Workflow Details

### Scheduled Workflows

- **Security Scanning**: Runs weekly on Monday at 00:00 UTC
- **Uptime Monitor**: Runs every 30 minutes

### On-Demand Workflows

All workflows can be triggered manually via workflow_dispatch:
1. Go to the [Actions tab](https://github.com/hannesmitterer/Euystacio/actions)
2. Select the workflow
3. Click "Run workflow"

### Workflow Triggers

#### Push Triggers
- `ci.yml`: main, copilot/**, alo-001/**
- `test.yml`: main, copilot/**
- `lint.yml`: main, copilot/**
- `deploy-pages.yml`: main only

#### Pull Request Triggers
- All build, test, lint, and security workflows trigger on PRs to main

## Recent Workflow Runs

View all workflow runs: [Actions Dashboard](https://github.com/hannesmitterer/Euystacio/actions)

## Workflow Artifacts

Workflows generate various artifacts:

### Build Artifacts
- **TypeScript Build**: `typescript-dist/` (7-day retention)
- Available from successful CI runs

### Test Reports
- **Coverage Reports**: Available from test workflow runs
- Includes HTML and XML coverage data

### Security Reports
- **npm Audit**: JSON format (from supply-chain security)
- **pip Audit**: JSON format (from supply-chain security)
- Available from security workflow runs

### Monitoring Reports
- **Uptime Reports**: Text format (30-day retention)
- Generated every 30 minutes

## Accessing Artifacts

1. Go to the [Actions tab](https://github.com/hannesmitterer/Euystacio/actions)
2. Click on a workflow run
3. Scroll to the "Artifacts" section
4. Download the desired artifact

## Troubleshooting

### Workflow Failures

If a workflow fails:

1. **Check the logs**: Click on the failed workflow run to view detailed logs
2. **Identify the failed job**: Look for red X marks
3. **Review the error messages**: Expand the failed step
4. **Fix locally**: Reproduce and fix the issue locally
5. **Push the fix**: The workflow will automatically re-run

### Common Issues

#### Build Failures
- **Cause**: TypeScript compilation errors or missing dependencies
- **Solution**: Run `npm run build` locally to identify issues

#### Test Failures
- **Cause**: Failing tests or import errors
- **Solution**: Run `npm test` or `pytest` locally

#### Lint Failures
- **Cause**: Code style violations
- **Solution**: Run `npm run lint:fix` or `black *.py` to auto-fix

#### Security Alerts
- **Cause**: Vulnerable dependencies detected
- **Solution**: Update dependencies via Dependabot PRs

#### Deployment Failures
- **Cause**: GitHub Pages configuration or build errors
- **Solution**: Check Pages settings and workflow logs

## Maintenance

### Updating Workflows

To update workflows:

1. Edit the workflow file in `.github/workflows/`
2. Test the changes in a feature branch
3. Create a PR for review
4. Merge to main after approval

### Adding New Workflows

To add new workflows:

1. Create a new YAML file in `.github/workflows/`
2. Define triggers, jobs, and steps
3. Test thoroughly
4. Document in this file

### Disabling Workflows

To temporarily disable a workflow:

1. Go to the [Actions tab](https://github.com/hannesmitterer/Euystacio/actions)
2. Select the workflow
3. Click the "..." menu
4. Select "Disable workflow"

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [CI/CD Documentation](./CI_CD_DOCUMENTATION.md)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## Support

For workflow issues or questions:
- Open an issue: https://github.com/hannesmitterer/Euystacio/issues
- Review existing runs: https://github.com/hannesmitterer/Euystacio/actions
- Check documentation: [CI_CD_DOCUMENTATION.md](./CI_CD_DOCUMENTATION.md)
