# GitHub Actions Workflows

This directory contains all automation workflows for the Euystacio project.

## 📋 Workflows Overview

### Core CI/CD Workflows

#### 1. **CI/CD Pipeline** (`ci-cd.yml`)
Comprehensive continuous integration and deployment pipeline.

- **Triggers:** Push to main, alo-001/**, copilot/** branches; Pull requests to main
- **Jobs:**
  - `lint-and-analyze`: Runs linting for TypeScript and Python
  - `build-and-test`: Builds and tests both Node.js and Python code
  - `security-scan`: Performs npm audit and Python safety checks
  - `validate-env`: Verifies environment configuration files
  - `ci-success`: Summary job that confirms all checks passed

**Features:**
- ✅ Parallel execution for TypeScript and Python
- ✅ Build caching for faster execution
- ✅ Test coverage reporting
- ✅ Security vulnerability scanning

#### 2. **ALO-001 CI** (`alo-001-ci.yml`)
Specialized workflow for ALO-001 feature branches.

- **Triggers:** Push to alo-001/** and copilot/alo-001** branches; Pull requests to main
- **Features:**
  - Google OAuth backend enforcement validation
  - Environment variable verification
  - Build artifact caching and uploading

#### 3. **Release and Deploy** (`main.yml`)
Handles releases and deployment preparation.

- **Triggers:** Version tags (v*.*.*), release publications, manual dispatch
- **Features:**
  - Automated changelog generation
  - Release archive creation
  - Asset uploading to GitHub releases

### GitHub Pages Deployment

#### 4. **Deploy to GitHub Pages** (`deploy-pages.yml`)
Automatically builds and deploys documentation to GitHub Pages.

- **Triggers:** Push to main, manual dispatch
- **Features:**
  - Builds documentation site
  - Creates navigation index
  - Deploys to GitHub Pages with proper permissions

**Deployed Content:**
- API documentation (README, NEXUS_API_SPEC, etc.)
- Integration guides (WebSocket, GGI, Gmail OAuth)
- Security documentation
- Public manifesto and PBL-001 content

### Security Workflows

#### 5. **CodeQL Security Scan** (`codeql-analysis.yml`)
Automated security vulnerability detection.

- **Triggers:** Push to main/branches, Pull requests, Weekly schedule (Mondays 08:00 UTC)
- **Languages:** JavaScript/TypeScript, Python
- **Features:**
  - Static code analysis
  - Security vulnerability detection
  - Scheduled weekly scans

#### 6. **Dependency Review** (`dependency-review.yml`)
Reviews dependencies in pull requests for security issues.

- **Triggers:** Pull requests to main
- **Features:**
  - Scans for vulnerable dependencies
  - Checks for license compliance
  - Identifies outdated packages
  - Comments on PRs with findings

### Quality & Validation

#### 7. **PR Validation** (`pr-validation.yml`)
Validates pull request quality before merge.

- **Triggers:** PR opened, synchronized, reopened, ready for review
- **Checks:**
  - PR title format (conventional commits)
  - Adequate PR description
  - Merge conflict detection
  - File change analysis
  - Sensitive file detection
  - Automatic size labeling

#### 8. **Workflow Monitoring** (`workflow-monitoring.yml`)
Monitors workflow health and performance.

- **Triggers:** Workflow completion, Daily at 09:00 UTC, Manual dispatch
- **Features:**
  - Success rate tracking (fails if < 80%)
  - Failed workflow reporting
  - Slow workflow detection (> 10 minutes)
  - Health metrics summary

## 🔧 Configuration Files

### Dependabot (`dependabot.yml`)
Automated dependency updates for:
- **npm packages:** Weekly updates on Mondays
- **pip packages:** Weekly updates on Mondays
- **GitHub Actions:** Monthly updates

## 📊 Workflow Status Badges

Add these badges to your README to show workflow status:

```markdown
[![CI/CD Pipeline](https://github.com/hannesmitterer/Euystacio/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/hannesmitterer/Euystacio/actions/workflows/ci-cd.yml)
[![CodeQL](https://github.com/hannesmitterer/Euystacio/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/hannesmitterer/Euystacio/actions/workflows/codeql-analysis.yml)
[![Deploy Pages](https://github.com/hannesmitterer/Euystacio/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/hannesmitterer/Euystacio/actions/workflows/deploy-pages.yml)
```

## 🚀 Best Practices

### For Contributors

1. **Pull Requests:**
   - Use conventional commit format in PR titles
   - Provide detailed descriptions
   - Keep PRs focused and reasonably sized
   - Ensure all CI checks pass

2. **Branch Naming:**
   - Feature branches: `feature/description`
   - Bug fixes: `fix/description`
   - ALO-001 work: `alo-001/description`

3. **Security:**
   - Never commit secrets or credentials
   - Keep dependencies up to date
   - Address security scan findings promptly

### For Maintainers

1. **Workflow Management:**
   - Monitor workflow success rates
   - Optimize slow-running workflows
   - Keep actions up to date via Dependabot

2. **Security:**
   - Review CodeQL findings weekly
   - Approve or merge Dependabot PRs promptly
   - Maintain security documentation

3. **Documentation:**
   - Keep workflow documentation current
   - Update this README when adding workflows
   - Document any workflow-specific secrets

## 🔐 Required Secrets

The following secrets need to be configured in repository settings:

- `GITHUB_TOKEN`: Automatically provided (for releases and Pages)

Optional secrets for enhanced features:
- `CODECOV_TOKEN`: For code coverage reporting
- `SLACK_WEBHOOK`: For workflow notifications (future)

## 📈 Performance Optimization

Current optimizations in place:

1. **Caching:**
   - npm dependencies cached
   - pip dependencies cached
   - Build artifacts cached

2. **Parallelization:**
   - TypeScript and Python jobs run in parallel
   - Lint, build, and security scans run concurrently

3. **Conditional Execution:**
   - Skip draft PRs
   - Language-specific steps only run when needed
   - Smart artifact retention (7 days)

## 🛠️ Troubleshooting

### Workflow Failures

1. **Build failures:** Check build logs in the workflow run
2. **Security scan failures:** Review CodeQL results and address findings
3. **Deployment failures:** Verify GitHub Pages settings and permissions

### Common Issues

**Issue:** npm audit failures
- **Solution:** Run `npm audit fix` locally and commit changes

**Issue:** GitHub Pages not updating
- **Solution:** Check Pages settings, ensure workflow has proper permissions

**Issue:** PR validation blocking merge
- **Solution:** Add adequate PR description and resolve conflicts

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [CodeQL Documentation](https://codeql.github.com/docs/)
- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)

## 🤝 Contributing

To add or modify workflows:

1. Create/edit workflow files in `.github/workflows/`
2. Test changes in a feature branch
3. Update this README with changes
4. Submit a PR with clear description

---

**Last Updated:** 2025-12-08
**Maintained by:** Euystacio Development Team
