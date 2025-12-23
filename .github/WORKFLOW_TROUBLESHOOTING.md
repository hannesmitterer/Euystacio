# Workflow Troubleshooting Guide

Quick reference for diagnosing and fixing common workflow issues.

## Quick Diagnosis

```
Is the workflow running? → Check Actions tab
Is it failing? → Check which job failed
Is it slow? → Review job duration
Is it not triggered? → Check trigger conditions
```

---

## Common Issues and Solutions

### 🔴 Build Failures

#### TypeScript Build Errors

**Symptoms:**
- `npm run build` fails
- Type errors in logs
- Module not found errors

**Solutions:**

```bash
# Clean build
rm -rf dist node_modules package-lock.json
npm install
npm run build

# Check TypeScript config
npx tsc --showConfig

# Verify all dependencies installed
npm ci
```

**Prevention:**
- Run `npm run build` before committing
- Use pre-commit hooks
- Keep dependencies up to date

#### Python Build Errors

**Symptoms:**
- Import errors
- Module not found
- Syntax errors

**Solutions:**

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python version
python --version

# Verify virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

---

### 🔴 Test Failures

#### Flaky Tests

**Symptoms:**
- Tests pass locally but fail in CI
- Intermittent failures
- Timeout issues

**Solutions:**

1. **Add retries:**
   ```yaml
   - name: Run tests
     uses: nick-fields/retry@v2
     with:
       timeout_minutes: 10
       max_attempts: 3
       command: npm test
   ```

2. **Increase timeouts:**
   ```yaml
   - name: Run tests
     timeout-minutes: 15
     run: npm test
   ```

3. **Fix timing issues:**
   ```javascript
   // Bad: Hard-coded delays
   await sleep(1000);
   
   // Good: Wait for conditions
   await waitFor(() => element.isVisible());
   ```

#### Missing Test Dependencies

**Symptoms:**
- "Cannot find module" errors
- Mock data not found
- Environment issues

**Solutions:**

```bash
# Install dev dependencies
npm ci --include=dev

# Verify test data
ls -la test/fixtures/

# Check environment variables
cat .env.test
```

---

### 🔴 Linting Failures

#### ESLint Errors

**Symptoms:**
- Code style violations
- Unused variables
- Missing semicolons

**Solutions:**

```bash
# Auto-fix many issues
npx eslint src --ext .ts --fix

# Check configuration
npx eslint --print-config src/server.ts

# Ignore specific rules (use sparingly)
// eslint-disable-next-line no-console
console.log('debug');
```

#### Python Linting Errors

**Symptoms:**
- PEP 8 violations
- Import order issues
- Line too long

**Solutions:**

```bash
# Auto-format with black
pip install black
black .

# Auto-fix imports
pip install isort
isort .

# Check specific file
flake8 app.py --show-source
```

---

### 🔴 Security Scan Issues

#### npm audit Vulnerabilities

**Severity Levels:**
- 🔴 **Critical/High:** Fix immediately
- 🟡 **Moderate:** Fix in next release
- 🟢 **Low:** Fix when convenient

**Solutions:**

```bash
# View details
npm audit

# Auto-fix (safe updates)
npm audit fix

# Force updates (may break things)
npm audit fix --force

# Update specific package
npm update package-name@latest

# Manual override (last resort)
npm audit --audit-level=high  # Ignore low/moderate
```

#### CodeQL False Positives

**When to Dismiss:**
- Code is not actually vulnerable
- Vulnerability is mitigated elsewhere
- Issue is in test code only

**How to Dismiss:**
1. Go to Security → Code scanning alerts
2. Select the alert
3. Click "Dismiss alert"
4. Choose reason and add comment

**Example reasons:**
- "Won't fix" - Code is intentional
- "False positive" - Not actually vulnerable
- "Used in tests" - Test code only

---

### 🔴 Deployment Issues

#### GitHub Pages Not Updating

**Symptoms:**
- Pages deploy succeeds but content unchanged
- Old content still showing
- 404 errors on new pages

**Solutions:**

1. **Check deployment succeeded:**
   ```
   Actions → Deploy to GitHub Pages → Verify green checkmark
   ```

2. **Verify Pages settings:**
   ```
   Settings → Pages → Source: GitHub Actions
   ```

3. **Clear cache:**
   ```bash
   # Browser: Ctrl+Shift+R (force refresh)
   # CDN: Wait 10 minutes for cache expiry
   ```

4. **Check build artifacts:**
   ```yaml
   - name: Debug site contents
     run: ls -R _site/
   ```

5. **Force redeploy:**
   - Manually trigger workflow
   - Or push small change to main

#### Missing Files in Deployment

**Symptoms:**
- Some files not appearing on Pages
- Broken links
- Missing assets

**Solutions:**

```yaml
# Ensure files are copied in deploy-pages.yml
- name: Copy missing files
  run: |
    cp -r additional-files/ _site/
    ls -la _site/
```

---

### 🔴 Permission Issues

#### Token Permissions

**Symptoms:**
- "Resource not accessible by token"
- "Permission denied"
- "Insufficient permissions"

**Solutions:**

1. **Update workflow permissions:**
   ```yaml
   permissions:
     contents: write
     pages: write
     id-token: write
   ```

2. **Check repository settings:**
   ```
   Settings → Actions → General → Workflow permissions
   Enable: Read and write permissions
   ```

3. **Use GITHUB_TOKEN correctly:**
   ```yaml
   - name: Create release
     env:
       GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
     run: gh release create v1.0.0
   ```

---

### 🔴 Dependency Issues

#### Cache Issues

**Symptoms:**
- Dependencies not found
- Old dependencies being used
- Inconsistent builds

**Solutions:**

```bash
# Clear local cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install

# Clear CI cache (in workflow)
```

```yaml
- name: Clear cache
  run: |
    rm -rf ~/.npm
```

#### Lock File Conflicts

**Symptoms:**
- package-lock.json conflicts
- Merge conflicts in dependencies
- Version mismatches

**Solutions:**

```bash
# Regenerate lock file
rm package-lock.json
npm install
git add package-lock.json
git commit -m "Regenerate lock file"
```

---

### 🔴 Performance Issues

#### Slow Workflows

**Symptoms:**
- Workflows take > 10 minutes
- Timeout errors
- Queue delays

**Solutions:**

1. **Optimize dependencies:**
   ```yaml
   # Use cache
   - uses: actions/cache@v4
     with:
       path: |
         ~/.npm
         ~/.cache/pip
       key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json') }}
   ```

2. **Parallelize jobs:**
   ```yaml
   jobs:
     test-node:
       runs-on: ubuntu-latest
     test-python:
       runs-on: ubuntu-latest
       # These run in parallel
   ```

3. **Skip unnecessary steps:**
   ```yaml
   - name: Skip on docs changes
     if: "!contains(github.event.head_commit.message, '[skip ci]')"
     run: npm test
   ```

4. **Use matrix efficiently:**
   ```yaml
   strategy:
     matrix:
       node: [18]  # Only test main version in PRs
   ```

#### Out of Memory

**Symptoms:**
- "JavaScript heap out of memory"
- Process killed
- OOM errors

**Solutions:**

```yaml
- name: Build with more memory
  env:
    NODE_OPTIONS: --max-old-space-size=4096
  run: npm run build
```

---

### 🔴 Workflow Not Triggering

#### Check Trigger Conditions

**Common issues:**

1. **Branch mismatch:**
   ```yaml
   on:
     push:
       branches: [main]  # Won't trigger on feature/branch
   ```

2. **Path filters:**
   ```yaml
   on:
     push:
       paths:
         - 'src/**'  # Won't trigger for docs changes
   ```

3. **Event type:**
   ```yaml
   on:
     pull_request:
       types: [opened]  # Won't trigger on sync
   ```

**Solutions:**

```yaml
# More inclusive triggers
on:
  push:
    branches:
      - main
      - 'feature/**'
  pull_request:
    types: [opened, synchronize, reopened]
```

#### Workflow Disabled

**Check:**
```
Actions → Workflows → Select workflow
If disabled, click "Enable workflow"
```

---

## Debugging Techniques

### Add Debug Logging

```yaml
- name: Debug info
  run: |
    echo "Event: ${{ github.event_name }}"
    echo "Branch: ${{ github.ref }}"
    echo "SHA: ${{ github.sha }}"
    env
    ls -la
```

### Use tmate for Interactive Debugging

```yaml
- name: Setup tmate session
  if: failure()
  uses: mxschmitt/action-tmate@v3
  timeout-minutes: 15
```

### Local Workflow Testing

```bash
# Install act
brew install act  # macOS
# or
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run workflow locally
act push
act pull_request
act -j build-and-test
```

### View Detailed Logs

```yaml
- name: Enable debug logging
  env:
    ACTIONS_STEP_DEBUG: true
  run: npm test
```

Or set repository secret: `ACTIONS_STEP_DEBUG=true`

---

## Escalation Path

### Level 1: Self-Service
1. Check this troubleshooting guide
2. Review workflow logs
3. Search GitHub Community
4. Check Stack Overflow

### Level 2: Team Support
1. Create issue with:
   - Workflow name
   - Run ID
   - Error message
   - What you've tried
2. Tag relevant team members
3. Include reproduction steps

### Level 3: GitHub Support
1. Critical infrastructure issues
2. GitHub Actions platform problems
3. Quota or billing issues

---

## Prevention Best Practices

### Before Committing

```bash
# Run full validation suite
npm run build
npm test
npm run lint
npm audit

# Check git status
git status
git diff
```

### Pre-commit Hooks

Install Husky for automatic checks:

```bash
npm install --save-dev husky
npx husky install
npx husky add .husky/pre-commit "npm run build && npm test"
```

### Workflow Testing

Test workflow changes:
1. Create test branch
2. Modify workflow
3. Push to test branch
4. Verify workflow runs correctly
5. Merge to main

---

## Useful Commands

### GitHub CLI

```bash
# View workflow runs
gh run list

# View specific run
gh run view 12345

# Rerun failed jobs
gh run rerun 12345

# Download logs
gh run download 12345

# Watch running workflow
gh run watch
```

### Git

```bash
# View recent commits
git log --oneline -10

# Check which workflows would run
git diff --name-only origin/main

# View file history
git log --follow -- .github/workflows/ci-cd.yml
```

---

## Emergency Procedures

### Workflow Causing Major Issues

1. **Disable workflow immediately:**
   ```
   Actions → Workflows → Select workflow → Disable
   ```

2. **Cancel running workflows:**
   ```bash
   gh run list --workflow=ci-cd.yml --json databaseId --jq '.[].databaseId' | \
     xargs -I {} gh run cancel {}
   ```

3. **Revert changes:**
   ```bash
   git revert <commit-sha>
   git push
   ```

### Recovery Checklist

- [ ] Identify the problem workflow
- [ ] Disable problematic workflow
- [ ] Cancel running instances
- [ ] Assess impact
- [ ] Fix issue locally
- [ ] Test fix thoroughly
- [ ] Re-enable workflow
- [ ] Monitor closely
- [ ] Document incident

---

**Last Updated:** 2025-12-08  
**Need Help?** Create an issue: https://github.com/hannesmitterer/Euystacio/issues
