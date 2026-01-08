# Workflows Directory

This directory contains all GitHub Actions workflows for the Euystacio repository.

## Workflow Files

### Primary Workflows

#### `ci.yml` - CI Pipeline
**Purpose**: Main continuous integration pipeline  
**Triggers**: Push to main/copilot/**/alo-001/**, PRs to main  
**Jobs**:
- TypeScript build and artifact upload
- Python build and validation
- Security audits (npm audit, pip-audit)
- Build status reporting

#### `test.yml` - Tests
**Purpose**: Automated testing  
**Triggers**: Push to main/copilot/**, PRs to main  
**Jobs**:
- TypeScript tests with Jest
- Python tests with pytest
- Integration tests
- Code coverage reporting

#### `lint.yml` - Code Quality & Linting
**Purpose**: Code quality checks  
**Triggers**: Push to main/copilot/**, PRs to main  
**Jobs**:
- ESLint for TypeScript/JavaScript
- Flake8, PyLint, Black for Python
- Prettier formatting checks
- Markdown linting

#### `deploy-pages.yml` - GitHub Pages Deployment
**Purpose**: Build and deploy documentation to GitHub Pages  
**Triggers**: Push to main, manual dispatch  
**Jobs**:
- Build site with TypeScript and Python components
- Convert Markdown to HTML
- Deploy to GitHub Pages

**Permissions Required**:
```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

#### `security.yml` - Security Scanning
**Purpose**: Comprehensive security scanning  
**Triggers**: Push to main, PRs to main, weekly schedule (Monday 00:00 UTC), manual dispatch  
**Jobs**:
- Gitleaks (secret scanning)
- Dependency Review (for PRs)
- CodeQL Analysis (JavaScript & Python)
- Semgrep SAST
- Supply chain security (npm/pip audits)

**Schedule**: `0 0 * * 1` (Weekly on Monday)

#### `uptime-monitor.yml` - Uptime Monitor
**Purpose**: Monitor GitHub Pages availability  
**Triggers**: Every 30 minutes, manual dispatch  
**Jobs**:
- HTTP status checks
- Response time monitoring
- Automated issue creation on failure

**Schedule**: `*/30 * * * *` (Every 30 minutes)

### Support Workflows

#### `alo-001-ci.yml` - ALO-001 CI
**Purpose**: Legacy CI for ALO-001 specific validation  
**Triggers**: Push to alo-001/** branches, PRs to main  
**Jobs**:
- Build and verify ALO-001 components
- Validate .env.example configuration

#### `badges.yml` - Update Badges
**Purpose**: Generate status badge data  
**Triggers**: Push to main, manual dispatch  
**Jobs**:
- Create badge data files
- Display badge URLs

#### `reusable-build.yml` - Reusable Build Workflow
**Purpose**: Reusable workflow for consistent builds  
**Type**: `workflow_call`  
**Inputs**:
- `node-version`: Node.js version (default: '18')
- `python-version`: Python version (default: '3.9')
- `skip-python`: Skip Python build steps (default: false)
- `skip-typescript`: Skip TypeScript build steps (default: false)

**Outputs**:
- `build-status`: Status of the build

### Usage Example

To call the reusable workflow:

```yaml
jobs:
  build:
    uses: ./.github/workflows/reusable-build.yml
    with:
      node-version: '18'
      python-version: '3.9'
      skip-python: false
      skip-typescript: false
```

## Workflow Triggers

### Push Events
- `main`: ci, test, lint, deploy-pages, security, badges
- `copilot/**`: ci, test, lint
- `alo-001/**`: ci, alo-001-ci

### Pull Request Events
- `main`: ci, test, lint, security (with dependency-review)

### Scheduled Events
- `security.yml`: Weekly on Monday at 00:00 UTC
- `uptime-monitor.yml`: Every 30 minutes

### Manual Triggers
All workflows support `workflow_dispatch` for manual execution.

## Workflow Dependencies

Some workflows depend on others:

```
ci.yml (builds artifacts)
  ↓
test.yml (may use artifacts)
  ↓
deploy-pages.yml (requires successful build)
  ↓
uptime-monitor.yml (monitors deployed site)
```

## Configuration Files

Related configuration files in the repository:

### Linting & Formatting
- `.eslintrc.json` - ESLint configuration
- `.prettierrc.json` - Prettier configuration
- `.prettierignore` - Prettier ignore patterns
- `.flake8` - Flake8 configuration

### Testing
- `jest.config.js` - Jest configuration
- `pytest.ini` - pytest configuration

### Code Ownership
- `.github/CODEOWNERS` - Code review assignments

### Dependency Management
- `.github/dependabot.yml` - Dependabot configuration

## Artifacts

Workflows generate various artifacts:

| Workflow | Artifact Name | Retention | Contents |
|----------|---------------|-----------|----------|
| ci.yml | `typescript-dist` | 7 days | Built TypeScript files |
| security.yml | `npm-audit-results` | Default | npm audit JSON |
| security.yml | `pip-audit-results` | Default | pip-audit JSON |
| uptime-monitor.yml | `monitoring-report-*` | 30 days | Uptime status reports |

## Best Practices

### Adding New Workflows

1. Create workflow file in `.github/workflows/`
2. Use descriptive name (e.g., `feature-name.yml`)
3. Add appropriate triggers
4. Document in this README
5. Test in a feature branch first
6. Add status badge to main README if applicable

### Modifying Existing Workflows

1. Test changes in a feature branch
2. Verify YAML syntax: `python -c "import yaml; yaml.safe_load(open('workflow.yml'))"`
3. Review workflow logs after changes
4. Update documentation if needed

### Security Considerations

- Never commit secrets to workflow files
- Use `${{ secrets.GITHUB_TOKEN }}` for GitHub API access
- Use `secrets.*` for sensitive data
- Review security scan results regularly
- Keep actions up to date (Dependabot helps with this)

### Performance Optimization

- Use caching for dependencies (`actions/cache` or built-in cache in setup actions)
- Use `continue-on-error: true` for non-critical jobs
- Configure appropriate artifact retention periods
- Use concurrency controls to prevent redundant runs

### Debugging Workflows

To debug workflow issues:

1. Check workflow logs in Actions tab
2. Add debug logging: `run: echo "Debug info: ${{ toJson(github) }}"`
3. Enable debug logging: Set `ACTIONS_STEP_DEBUG` secret to `true`
4. Test locally when possible
5. Use `act` tool for local workflow testing

## Maintenance

### Weekly Tasks
- Review security scan results
- Check for failed workflows
- Review Dependabot PRs

### Monthly Tasks
- Review workflow performance
- Update workflow documentation
- Clean up old artifacts (happens automatically)

### As Needed
- Update action versions
- Add new workflows for new features
- Optimize slow workflows

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Action Marketplace](https://github.com/marketplace?type=actions)
- [Security Hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)

## Support

For workflow-related issues:
- Check [WORKFLOW_STATUS.md](../../WORKFLOW_STATUS.md)
- See [CI_CD_DOCUMENTATION.md](../../CI_CD_DOCUMENTATION.md)
- Open an issue with label `workflow`
