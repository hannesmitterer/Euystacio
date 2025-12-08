# Workflow Usage Examples

This guide provides practical examples for common workflow scenarios in the Euystacio project.

## Table of Contents

- [Running Workflows Manually](#running-workflows-manually)
- [Monitoring Workflow Status](#monitoring-workflow-status)
- [Debugging Failed Workflows](#debugging-failed-workflows)
- [Working with Dependabot](#working-with-dependabot)
- [Security Scan Responses](#security-scan-responses)
- [GitHub Pages Deployment](#github-pages-deployment)

---

## Running Workflows Manually

### Deploying to GitHub Pages

You can manually trigger a GitHub Pages deployment:

1. Go to **Actions** tab in GitHub
2. Select **Deploy to GitHub Pages** workflow
3. Click **Run workflow**
4. Select branch (usually `main`)
5. Click **Run workflow** button

**Use Case:** Redeploy documentation after fixing issues without pushing new commits.

### Running Workflow Monitoring

Check the health of your CI/CD pipelines:

1. Go to **Actions** tab
2. Select **Workflow Monitoring** workflow
3. Click **Run workflow**
4. Review the generated health report

**Use Case:** Get a quick overview of workflow success rates and identify problematic workflows.

---

## Monitoring Workflow Status

### Via GitHub UI

1. **Real-time Monitoring:**
   ```
   Repository → Actions → Select workflow → View run
   ```

2. **Check Recent Runs:**
   ```
   Repository → Actions → Filter by workflow name
   ```

3. **View Logs:**
   ```
   Click on workflow run → Select job → View logs
   ```

### Via Badges in README

The README includes status badges that show current workflow status:

```markdown
[![CI/CD Pipeline](https://github.com/hannesmitterer/Euystacio/actions/workflows/ci-cd.yml/badge.svg)](...)
```

Click on badges to view detailed workflow information.

---

## Debugging Failed Workflows

### Step 1: Identify the Failure

Check the workflow run page for:
- Which job failed
- Which step in the job failed
- Error messages in logs

### Step 2: Common Failure Scenarios

#### Build Failures

**Symptom:** TypeScript build fails

```bash
# Local reproduction
npm ci
npm run build
```

**Common Causes:**
- Type errors in TypeScript
- Missing dependencies
- Configuration issues

**Solution:**
```bash
# Fix type errors
npx tsc --noEmit

# Update dependencies
npm update
```

#### Test Failures

**Symptom:** Tests fail in CI

```bash
# Local reproduction
npm test  # or pytest for Python
```

**Common Causes:**
- Breaking changes
- Environment differences
- Missing test data

**Solution:**
- Run tests locally first
- Check test logs for specific failures
- Ensure test data is available

#### Linting Failures

**Symptom:** ESLint or flake8 errors

```bash
# Local reproduction
npx eslint src --ext .ts  # TypeScript
flake8 .                   # Python
```

**Solution:**
```bash
# Auto-fix where possible
npx eslint src --ext .ts --fix
```

#### Security Scan Failures

**Symptom:** npm audit or CodeQL finds vulnerabilities

```bash
# Check locally
npm audit
npm audit fix  # Auto-fix if possible
```

**Solution:**
- Review security advisory
- Update vulnerable packages
- Apply patches if available

### Step 3: Test Fixes Locally

Before pushing:

```bash
# Full local validation
npm ci
npm run build
npm test
npm audit
npx eslint src --ext .ts
```

---

## Working with Dependabot

### Reviewing Dependabot PRs

When Dependabot creates a PR:

1. **Check PR Description:**
   - What's being updated
   - Changelog link
   - Compatibility notes

2. **Review Changes:**
   - Look at package.json or requirements.txt
   - Check for breaking changes
   - Review release notes

3. **Validate Locally (Optional):**
   ```bash
   git fetch origin
   git checkout dependabot/npm_and_yarn/...
   npm ci
   npm run build
   npm test
   ```

4. **Merge Strategy:**
   - ✅ Patch versions: Usually safe to auto-merge
   - ⚠️ Minor versions: Review changelog
   - ⛔ Major versions: Careful review required

### Handling Failed Dependabot PRs

If Dependabot PRs fail CI:

1. Checkout the branch locally
2. Investigate the failure
3. Fix issues if needed
4. Push fixes to the Dependabot branch
5. CI will re-run automatically

### Configuring Dependabot

Edit `.github/dependabot.yml`:

```yaml
# Increase PR limit
open-pull-requests-limit: 20

# Change schedule
schedule:
  interval: "daily"  # or "weekly", "monthly"
```

---

## Security Scan Responses

### CodeQL Alerts

When CodeQL finds issues:

1. **Review Alert:**
   ```
   Security → Code scanning alerts → Select alert
   ```

2. **Understand the Issue:**
   - What vulnerability was detected
   - Where in the code
   - Potential impact

3. **Fix the Issue:**
   - Follow CodeQL recommendations
   - Test fix locally
   - Push changes

4. **Dismiss False Positives:**
   ```
   Alert → Dismiss alert → Select reason
   ```

### Dependency Vulnerabilities

For npm audit findings:

```bash
# Check severity
npm audit

# Auto-fix (use with caution)
npm audit fix

# Force update (may break things)
npm audit fix --force
```

For Python dependencies:

```bash
# Install safety
pip install safety

# Check for vulnerabilities
safety check

# Update vulnerable package
pip install --upgrade package-name
```

---

## GitHub Pages Deployment

### First-Time Setup

1. **Enable GitHub Pages:**
   ```
   Repository → Settings → Pages
   Source: GitHub Actions
   ```

2. **Trigger First Deployment:**
   - Push to main branch, or
   - Manually run deployment workflow

3. **Verify Deployment:**
   ```
   Check: https://hannesmitterer.github.io/Euystacio/
   ```

### Updating Documentation

Any change to these files triggers redeployment:

- `index.html`
- `README.md`
- Documentation markdown files
- `public/` directory contents

### Custom Domain (Optional)

To use a custom domain:

1. Add `CNAME` file to repository root
2. Configure DNS settings
3. Enable in GitHub Pages settings

### Troubleshooting Pages

**Issue:** Pages not updating

**Solution:**
1. Check workflow run succeeded
2. Verify Pages is enabled
3. Clear browser cache
4. Check deployment URL in workflow logs

**Issue:** 404 errors

**Solution:**
1. Verify file paths are correct
2. Check file is included in `_site/` directory
3. Review build step logs

---

## Advanced Workflows

### Workflow Dependencies

Workflows can depend on each other:

```yaml
jobs:
  deploy:
    needs: [build, test]  # Runs only if both succeed
```

### Conditional Steps

Run steps based on conditions:

```yaml
- name: Deploy to production
  if: github.ref == 'refs/heads/main'
  run: ./deploy.sh
```

### Matrix Strategies

Test across multiple versions:

```yaml
strategy:
  matrix:
    node-version: [16, 18, 20]
    os: [ubuntu-latest, macos-latest]
```

### Secrets Management

Use secrets in workflows:

```yaml
- name: Deploy
  env:
    API_KEY: ${{ secrets.API_KEY }}
  run: ./deploy.sh
```

---

## Performance Tips

### Optimize Workflow Execution

1. **Use Caching:**
   ```yaml
   - uses: actions/cache@v4
     with:
       path: node_modules
       key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
   ```

2. **Parallel Jobs:**
   - Split independent jobs
   - Use matrix strategies
   - Avoid unnecessary dependencies

3. **Skip Redundant Runs:**
   ```yaml
   on:
     push:
       paths-ignore:
         - '**.md'
         - 'docs/**'
   ```

4. **Fail Fast:**
   ```yaml
   strategy:
     fail-fast: true
   ```

### Reduce Workflow Costs

1. **Self-hosted Runners:** For high-volume projects
2. **Concurrency Groups:** Prevent duplicate runs
3. **Scheduled Jobs:** Run heavy tasks during off-peak hours

---

## Getting Help

### Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Actions Marketplace](https://github.com/marketplace?type=actions)

### Debugging Tools

```bash
# Validate workflow locally with act
act -l  # List workflows
act pull_request  # Simulate PR event

# GitHub CLI
gh workflow list
gh workflow view ci-cd.yml
gh run list --workflow=ci-cd.yml
gh run view <run-id>
```

### Community Support

- [GitHub Community Forum](https://github.community/)
- [Stack Overflow: github-actions tag](https://stackoverflow.com/questions/tagged/github-actions)
- Project Issues: [Report workflow issues](https://github.com/hannesmitterer/Euystacio/issues)

---

**Last Updated:** 2025-12-08  
**Maintained by:** Euystacio Development Team
