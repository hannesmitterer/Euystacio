# Workflow Status Dashboard

Real-time status of all CI/CD workflows in the Euystacio project.

**Last Updated:** _Automatically updated on each workflow run_

---

## 🚀 Active Workflows

### Core Workflows

| Workflow | Status | Purpose | Frequency |
|----------|--------|---------|-----------|
| [CI/CD Pipeline](https://github.com/hannesmitterer/Euystacio/actions/workflows/ci-cd.yml) | ![CI/CD](https://github.com/hannesmitterer/Euystacio/actions/workflows/ci-cd.yml/badge.svg) | Full build, test, and validation | On push, PR |
| [ALO-001 CI](https://github.com/hannesmitterer/Euystacio/actions/workflows/alo-001-ci.yml) | ![ALO-001](https://github.com/hannesmitterer/Euystacio/actions/workflows/alo-001-ci.yml/badge.svg) | ALO-001 feature validation | On ALO-001 branches |
| [Release and Deploy](https://github.com/hannesmitterer/Euystacio/actions/workflows/main.yml) | ![Release](https://github.com/hannesmitterer/Euystacio/actions/workflows/main.yml/badge.svg) | Release management | On version tags |

### Security Workflows

| Workflow | Status | Purpose | Frequency |
|----------|--------|---------|-----------|
| [CodeQL Security Scan](https://github.com/hannesmitterer/Euystacio/actions/workflows/codeql-analysis.yml) | ![CodeQL](https://github.com/hannesmitterer/Euystacio/actions/workflows/codeql-analysis.yml/badge.svg) | Security vulnerability scanning | On push, Weekly |
| [Dependency Review](https://github.com/hannesmitterer/Euystacio/actions/workflows/dependency-review.yml) | ![Dependency](https://github.com/hannesmitterer/Euystacio/actions/workflows/dependency-review.yml/badge.svg) | PR dependency checking | On PR |

### Deployment Workflows

| Workflow | Status | Purpose | Frequency |
|----------|--------|---------|-----------|
| [Deploy to GitHub Pages](https://github.com/hannesmitterer/Euystacio/actions/workflows/deploy-pages.yml) | ![Pages](https://github.com/hannesmitterer/Euystacio/actions/workflows/deploy-pages.yml/badge.svg) | Documentation deployment | On main push |

### Quality Workflows

| Workflow | Status | Purpose | Frequency |
|----------|--------|---------|-----------|
| [PR Validation](https://github.com/hannesmitterer/Euystacio/actions/workflows/pr-validation.yml) | ![PR Validation](https://github.com/hannesmitterer/Euystacio/actions/workflows/pr-validation.yml/badge.svg) | Pull request quality checks | On PR |
| [Workflow Monitoring](https://github.com/hannesmitterer/Euystacio/actions/workflows/workflow-monitoring.yml) | ![Monitoring](https://github.com/hannesmitterer/Euystacio/actions/workflows/workflow-monitoring.yml/badge.svg) | Workflow health tracking | Daily, On completion |

---

## 📊 Success Rate Targets

| Metric | Target | Current Status |
|--------|--------|----------------|
| Overall Success Rate | ≥ 90% | _View in Monitoring Workflow_ |
| Build Time | < 10 min | _View individual runs_ |
| Test Coverage | ≥ 80% | _View CI/CD logs_ |
| Security Issues | 0 Critical | _View CodeQL results_ |

---

## 🔄 Recent Activity

View recent workflow runs:
- [All Workflows](https://github.com/hannesmitterer/Euystacio/actions)
- [CI/CD Runs](https://github.com/hannesmitterer/Euystacio/actions/workflows/ci-cd.yml)
- [Security Scans](https://github.com/hannesmitterer/Euystacio/actions/workflows/codeql-analysis.yml)
- [Deployments](https://github.com/hannesmitterer/Euystacio/actions/workflows/deploy-pages.yml)

---

## 🎯 Quick Links

### For Developers
- [Workflow Documentation](./workflows/README.md)
- [Usage Examples](./WORKFLOW_USAGE_EXAMPLES.md)
- [Troubleshooting Guide](./WORKFLOW_TROUBLESHOOTING.md)

### For Maintainers
- [Dependabot Dashboard](https://github.com/hannesmitterer/Euystacio/network/updates)
- [Security Alerts](https://github.com/hannesmitterer/Euystacio/security)
- [Code Scanning Alerts](https://github.com/hannesmitterer/Euystacio/security/code-scanning)

### Documentation
- [GitHub Pages Site](https://hannesmitterer.github.io/Euystacio/)
- [API Documentation](https://hannesmitterer.github.io/Euystacio/NEXUS_API_SPEC.md)
- [Deployment Guide](https://hannesmitterer.github.io/Euystacio/DEPLOY_INSTRUCTIONS.md)

---

## 🚨 Active Issues

Check for known workflow issues:
- [Open Issues: workflow](https://github.com/hannesmitterer/Euystacio/issues?q=is%3Aissue+is%3Aopen+label%3Aworkflow)
- [Open Issues: ci/cd](https://github.com/hannesmitterer/Euystacio/issues?q=is%3Aissue+is%3Aopen+label%3Aci)

---

## 📈 Performance Metrics

### Average Workflow Duration

```
CI/CD Pipeline:          ~5-8 minutes
CodeQL Security Scan:    ~8-12 minutes
Deploy to GitHub Pages:  ~3-5 minutes
PR Validation:           ~1-2 minutes
```

### Resource Usage

```
Build Artifacts:  ~10 MB
Cache Size:       ~100 MB (npm + pip)
Retention:        7 days
```

---

## 🔔 Notifications

### Workflow Failure Alerts

Maintainers are notified of:
- ❌ Failed CI/CD builds on main
- 🔴 Critical security vulnerabilities
- ⚠️ Deployment failures
- 📉 Success rate below 80%

### Dependabot Updates

Automatic PRs for:
- 📦 npm package updates (Weekly, Monday 08:00 UTC)
- 🐍 pip package updates (Weekly, Monday 08:00 UTC)
- ⚙️ GitHub Actions updates (Monthly)

---

## 🛠️ Maintenance Schedule

| Task | Frequency | Last Run | Next Run |
|------|-----------|----------|----------|
| CodeQL Scan | Weekly | _View workflow_ | Every Monday 08:00 UTC |
| Workflow Monitoring | Daily | _View workflow_ | Every day 09:00 UTC |
| Dependency Updates | Weekly | _View Dependabot_ | Every Monday 08:00 UTC |
| Actions Updates | Monthly | _View Dependabot_ | Monthly |

---

## 📝 Change Log

### Recent Workflow Changes

**2025-12-08:**
- ✨ Added comprehensive CI/CD pipeline
- ✨ Implemented GitHub Pages deployment
- ✨ Added CodeQL security scanning
- ✨ Created dependency review workflow
- ✨ Added PR validation
- ✨ Implemented workflow monitoring
- ✨ Added Dependabot configuration
- ✨ Created workflow documentation

---

## 🤝 Contributing

### Modifying Workflows

1. Create a feature branch
2. Edit workflow files in `.github/workflows/`
3. Test changes thoroughly
4. Submit PR with:
   - Clear description of changes
   - Reason for modification
   - Testing evidence
5. Update this status page if needed

### Reporting Issues

Found a workflow issue? [Create an issue](https://github.com/hannesmitterer/Euystacio/issues/new) with:
- Workflow name
- Run ID and link
- Error message
- Expected vs actual behavior

---

## 📚 Additional Resources

### Internal Documentation
- [Workflow README](./workflows/README.md) - Complete workflow documentation
- [Usage Examples](./WORKFLOW_USAGE_EXAMPLES.md) - Common scenarios and examples
- [Troubleshooting](./WORKFLOW_TROUBLESHOOTING.md) - Debug common issues

### External Resources
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [GitHub Actions Community](https://github.community/c/code-to-cloud/github-actions/)

---

## 🎖️ Workflow Badges

Use these badges in documentation:

```markdown
<!-- All workflows -->
![CI/CD](https://github.com/hannesmitterer/Euystacio/actions/workflows/ci-cd.yml/badge.svg)
![CodeQL](https://github.com/hannesmitterer/Euystacio/actions/workflows/codeql-analysis.yml/badge.svg)
![Pages](https://github.com/hannesmitterer/Euystacio/actions/workflows/deploy-pages.yml/badge.svg)

<!-- With links -->
[![CI/CD](https://github.com/hannesmitterer/Euystacio/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/hannesmitterer/Euystacio/actions/workflows/ci-cd.yml)
```

---

**Maintained by:** Euystacio Development Team  
**Contact:** [Create an issue](https://github.com/hannesmitterer/Euystacio/issues) for workflow questions

---

_This page is updated automatically. For manual updates, edit `.github/WORKFLOW_STATUS.md`_
