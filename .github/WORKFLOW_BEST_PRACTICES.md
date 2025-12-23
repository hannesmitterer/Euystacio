# Workflow Best Practices

Guidelines for creating, maintaining, and optimizing GitHub Actions workflows in the Euystacio project.

---

## 🎯 Design Principles

### 1. **Modularity**
Break workflows into focused, reusable jobs.

✅ **Good:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps: [...]
  
  test:
    needs: build
    runs-on: ubuntu-latest
    steps: [...]
```

❌ **Avoid:**
```yaml
jobs:
  build-test-deploy-everything:
    steps: [50 steps doing everything]
```

### 2. **Fail Fast**
Detect issues early to save time and resources.

✅ **Good:**
```yaml
strategy:
  fail-fast: true  # Stop all jobs if one fails
  matrix:
    node-version: [16, 18, 20]
```

### 3. **Clear Naming**
Use descriptive names for workflows, jobs, and steps.

✅ **Good:**
```yaml
name: CI/CD Pipeline
jobs:
  lint-and-analyze:
    name: Lint & Static Analysis
    steps:
      - name: Run ESLint on TypeScript files
```

❌ **Avoid:**
```yaml
name: Workflow1
jobs:
  job1:
    steps:
      - name: Do stuff
```

---

## 🚀 Performance Optimization

### 1. **Use Caching Effectively**

**npm dependencies:**
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '18'
    cache: 'npm'  # Built-in caching
```

**Custom caching:**
```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.npm
      ~/.cache/pip
      **/node_modules
    key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json', 'requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-deps-
```

### 2. **Parallelize Independent Jobs**

```yaml
jobs:
  test-node:
    runs-on: ubuntu-latest
    # Runs in parallel
  
  test-python:
    runs-on: ubuntu-latest
    # Runs in parallel
  
  deploy:
    needs: [test-node, test-python]
    # Waits for both
```

### 3. **Use Concurrency Groups**

Prevent duplicate runs:
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true  # Cancel old runs
```

### 4. **Skip Unnecessary Runs**

**Path filters:**
```yaml
on:
  push:
    paths:
      - 'src/**'
      - 'package.json'
    paths-ignore:
      - '**.md'
      - 'docs/**'
```

**Commit message filters:**
```yaml
- name: Check skip conditions
  if: "!contains(github.event.head_commit.message, '[skip ci]')"
```

---

## 🔒 Security Best Practices

### 1. **Minimize Permissions**

Use least privilege principle:
```yaml
permissions:
  contents: read  # Only what's needed
  pull-requests: write  # For commenting
```

### 2. **Pin Action Versions**

✅ **Good:**
```yaml
- uses: actions/checkout@v4  # Pinned to major version
- uses: actions/setup-node@a1b2c3d  # Pinned to commit SHA (most secure)
```

❌ **Avoid:**
```yaml
- uses: actions/checkout@main  # Unpredictable
```

### 3. **Never Commit Secrets**

Use GitHub Secrets:
```yaml
- name: Deploy
  env:
    API_KEY: ${{ secrets.API_KEY }}
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
  run: ./deploy.sh
```

### 4. **Validate External Input**

```yaml
- name: Validate PR title
  run: |
    TITLE="${{ github.event.pull_request.title }}"
    # Sanitize before using
    CLEAN_TITLE=$(echo "$TITLE" | tr -cd '[:alnum:][:space:]-_')
```

---

## 📝 Code Quality

### 1. **DRY (Don't Repeat Yourself)**

**Use composite actions:**
```yaml
# .github/actions/setup-environment/action.yml
name: Setup Environment
runs:
  using: "composite"
  steps:
    - uses: actions/setup-node@v4
    - run: npm ci

# In workflow:
- uses: ./.github/actions/setup-environment
```

**Use reusable workflows:**
```yaml
# .github/workflows/reusable-build.yml
on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string

# In another workflow:
jobs:
  build:
    uses: ./.github/workflows/reusable-build.yml
    with:
      node-version: '18'
```

### 2. **Add Helpful Comments**

```yaml
# This job runs only on main branch to avoid double deployments
deploy:
  if: github.ref == 'refs/heads/main'
  steps: [...]
```

### 3. **Use Job Summaries**

```yaml
- name: Generate summary
  run: |
    echo "## Test Results" >> $GITHUB_STEP_SUMMARY
    echo "✅ 42 tests passed" >> $GITHUB_STEP_SUMMARY
    echo "❌ 2 tests failed" >> $GITHUB_STEP_SUMMARY
```

---

## 🐛 Debugging and Monitoring

### 1. **Add Debug Information**

```yaml
- name: Debug workflow context
  run: |
    echo "Event: ${{ github.event_name }}"
    echo "Ref: ${{ github.ref }}"
    echo "SHA: ${{ github.sha }}"
    echo "Actor: ${{ github.actor }}"
```

### 2. **Use Continue on Error Wisely**

```yaml
# For optional steps
- name: Upload coverage
  uses: codecov/codecov-action@v4
  continue-on-error: true

# NOT for critical steps
- name: Run tests
  run: npm test
  # Don't use continue-on-error here!
```

### 3. **Set Timeouts**

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 10  # Prevent hanging
```

---

## 🎨 Workflow Organization

### Directory Structure

```
.github/
├── workflows/
│   ├── ci-cd.yml              # Main CI/CD
│   ├── deploy-pages.yml       # Deployment
│   ├── codeql-analysis.yml    # Security
│   ├── dependency-review.yml  # Dependencies
│   └── README.md              # Documentation
├── actions/
│   └── setup-environment/     # Custom actions
│       └── action.yml
├── dependabot.yml
├── WORKFLOW_STATUS.md
└── WORKFLOW_USAGE_EXAMPLES.md
```

### Naming Conventions

**Workflows:**
- Use kebab-case: `ci-cd.yml`, `deploy-pages.yml`
- Be descriptive: `deploy-production.yml` not `deploy.yml`

**Jobs:**
- Use snake_case: `build_and_test`, `deploy_to_production`
- Group related jobs: `test_unit`, `test_integration`

**Steps:**
- Use sentence case: "Setup Node.js", "Run tests"
- Start with action verb: "Build", "Deploy", "Validate"

---

## 📊 Workflow Metrics

### Track Important Metrics

```yaml
- name: Record metrics
  run: |
    echo "BUILD_TIME=${{ job.duration }}" >> metrics.txt
    echo "TEST_COUNT=$(grep -c 'test' test-results.xml)" >> metrics.txt
```

### Use Badges

Add to README:
```markdown
[![CI/CD](https://github.com/owner/repo/actions/workflows/ci-cd.yml/badge.svg)](...)
```

---

## 🧪 Testing Workflows

### 1. **Test in Feature Branches**

```yaml
on:
  push:
    branches:
      - main
      - 'feature/**'  # Test workflow changes
```

### 2. **Use Act for Local Testing**

```bash
# Install act
brew install act

# Test workflow locally
act push
act pull_request -j build
```

### 3. **Gradual Rollout**

```yaml
- name: Deploy to staging
  if: github.ref == 'refs/heads/develop'
  
- name: Deploy to production
  if: github.ref == 'refs/heads/main'
```

---

## 🔄 Maintenance

### Regular Reviews

**Weekly:**
- Check workflow success rates
- Review failed runs
- Update outdated actions

**Monthly:**
- Analyze workflow performance
- Optimize slow workflows
- Review and update documentation

**Quarterly:**
- Major version updates
- Architecture review
- Security audit

### Version Updates

**Use Dependabot:**
```yaml
# .github/dependabot.yml
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "monthly"
```

---

## 📚 Documentation Standards

### Workflow Documentation

Each workflow should have:

1. **Header comment:**
```yaml
# CI/CD Pipeline
# Purpose: Build, test, and validate code changes
# Triggers: Push to main/branches, Pull requests
# Maintainer: @username
```

2. **README entry:**
Document in `.github/workflows/README.md`

3. **Usage examples:**
Add to `.github/WORKFLOW_USAGE_EXAMPLES.md`

### Change Documentation

When modifying workflows:
- Update README
- Add to CHANGELOG
- Update status page
- Notify team

---

## ⚠️ Common Pitfalls

### 1. **Don't Use `${{ }}` in `if` Conditions**

✅ **Good:**
```yaml
if: github.ref == 'refs/heads/main'
```

❌ **Avoid:**
```yaml
if: ${{ github.ref == 'refs/heads/main' }}
```

### 2. **Quote Complex Expressions**

✅ **Good:**
```yaml
if: "!contains(github.event.head_commit.message, '[skip ci]')"
```

### 3. **Use Checkout Before Everything**

```yaml
steps:
  - uses: actions/checkout@v4  # FIRST
  - name: Do things with code
```

### 4. **Don't Hardcode Values**

✅ **Good:**
```yaml
env:
  NODE_VERSION: '18'
  
jobs:
  build:
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
```

---

## 🎓 Learning Resources

### Official Documentation
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Contexts](https://docs.github.com/en/actions/reference/context-and-expression-syntax-for-github-actions)

### Community Resources
- [Awesome Actions](https://github.com/sdras/awesome-actions)
- [Actions Marketplace](https://github.com/marketplace?type=actions)
- [GitHub Community Forum](https://github.community/)

### Internal Resources
- [Workflow README](.github/workflows/README.md)
- [Usage Examples](.github/WORKFLOW_USAGE_EXAMPLES.md)
- [Troubleshooting](.github/WORKFLOW_TROUBLESHOOTING.md)

---

## ✅ Checklist for New Workflows

Before merging a new workflow:

- [ ] Clear, descriptive name
- [ ] Proper trigger conditions
- [ ] Minimal required permissions
- [ ] Timeout set on jobs
- [ ] Caching implemented
- [ ] Error handling in place
- [ ] Documentation added
- [ ] Tested in feature branch
- [ ] Status badge created
- [ ] Team notified

---

## 🤝 Contributing Guidelines

### Making Changes

1. **Small, focused changes:**
   - One workflow per PR
   - Clear purpose and scope

2. **Test thoroughly:**
   - Run locally with `act`
   - Test in feature branch
   - Verify all scenarios

3. **Document changes:**
   - Update README
   - Add examples if needed
   - Update troubleshooting guide

4. **Review process:**
   - Request review from maintainers
   - Address feedback
   - Wait for approval

---

**Last Updated:** 2025-12-08  
**Maintained by:** Euystacio Development Team
