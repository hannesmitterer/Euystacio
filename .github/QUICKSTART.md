# Developer Quick Start Guide

Quick reference for developers working on the Euystacio project.

## 🚀 Getting Started

### Prerequisites
```bash
# Required
- Node.js 18+
- Python 3.9+
- npm
- git

# Optional
- Docker (for containerized development)
```

### Initial Setup
```bash
# Clone the repository
git clone https://github.com/hannesmitterer/Euystacio.git
cd Euystacio

# Install Node.js dependencies
npm ci

# Install Python dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Build the project
npm run build
```

## 📋 Common Commands

### Node.js / TypeScript
```bash
npm run build       # Build TypeScript to JavaScript
npm run dev         # Build and run in development mode
npm start           # Run the built application
npm audit           # Check for vulnerabilities
npm audit fix       # Fix vulnerabilities automatically
```

### Python
```bash
python app.py       # Run Flask app
python main.py      # Run FastAPI app
pip list --outdated # Check for outdated packages
flake8 .           # Lint Python code
```

### Git Workflow
```bash
git checkout -b feature/my-feature    # Create feature branch
git add .                             # Stage changes
git commit -m "Description"           # Commit changes
git push origin feature/my-feature    # Push to GitHub

# After PR is created and approved
git checkout main
git pull origin main                  # Update main branch
```

## 🔧 Development Workflow

### 1. Create a Branch
- Branch naming: `feature/`, `fix/`, `docs/`, `refactor/`
- Example: `feature/add-new-endpoint`

### 2. Make Changes
- Write code
- Test locally
- Lint your code
- Update documentation if needed

### 3. Commit Changes
```bash
# Good commit messages
git commit -m "Add user authentication endpoint"
git commit -m "Fix memory leak in telemetry processing"
git commit -m "Update deployment documentation"

# Bad commit messages (avoid these)
git commit -m "fix"
git commit -m "updates"
git commit -m "changes"
```

### 4. Push and Create PR
```bash
git push origin your-branch-name
```
- Go to GitHub and create a Pull Request
- Fill in the PR template
- Wait for CI/CD checks to pass
- Request reviews if needed

### 5. After Approval
- Merge the PR
- Delete the branch
- Pull latest main

## 🧪 Testing

### Run Tests Locally
```bash
# Node.js tests (when available)
npm test

# Python tests (when available)
pytest

# Linting
npm run lint          # TypeScript/JavaScript
flake8 .             # Python
```

### Before Pushing
1. ✅ Build succeeds locally
2. ✅ Tests pass (if available)
3. ✅ Code is linted
4. ✅ No console errors
5. ✅ Documentation updated

## 🔍 CI/CD Checks

When you push or create a PR, these checks run automatically:

### Build & Lint
- TypeScript compilation
- Python syntax check
- Code linting
- Build artifact verification

### Security
- Dependency vulnerability scan
- License compliance check
- Security audit

### Deployment (main branch only)
- GitHub Pages deployment
- Static site generation

## 📊 Monitoring Your PR

### Check Workflow Status
1. Go to your PR on GitHub
2. Scroll to "Checks" section
3. Click on failed checks to see logs
4. Fix issues and push again

### Common CI Failures

**Build Failure:**
```bash
# Reproduce locally
npm run build

# Fix and push
git add .
git commit -m "Fix build errors"
git push
```

**Linting Errors:**
```bash
# See errors
npm run lint

# Fix automatically (some)
npm run lint -- --fix

# Commit fixes
git commit -am "Fix linting errors"
```

**Dependency Issues:**
```bash
# Update dependencies
npm ci
npm audit fix

# Commit lockfile
git add package-lock.json
git commit -m "Update dependencies"
```

## 📦 Dependencies

### Adding Node.js Packages
```bash
# Install package
npm install package-name

# Or for dev dependencies
npm install --save-dev package-name

# Commit both files
git add package.json package-lock.json
git commit -m "Add package-name dependency"
```

### Adding Python Packages
```bash
# Install package
pip install package-name

# Update requirements
pip freeze > requirements.txt

# Commit
git add requirements.txt
git commit -m "Add package-name dependency"
```

### Security Note
All dependency changes are automatically scanned for vulnerabilities!

## 🎯 Code Owners

Files automatically request review from:
- Workflows: `@hannesmitterer`
- TypeScript: `@hannesmitterer`
- Python: `@hannesmitterer`
- Documentation: `@hannesmitterer`

## 🏷️ PR Labels

PRs are automatically labeled based on changed files:
- `documentation` - Markdown files
- `workflows` - GitHub Actions
- `typescript` - `.ts` files
- `python` - `.py` files
- `frontend` - HTML/CSS
- `dependencies` - Package files
- `configuration` - Config files

## 🐛 Troubleshooting

### Build Issues
```bash
# Clean and rebuild
rm -rf node_modules dist
npm ci
npm run build
```

### Dependency Issues
```bash
# Clear npm cache
npm cache clean --force
npm ci

# Or reinstall everything
rm -rf node_modules package-lock.json
npm install
```

### Python Issues
```bash
# Recreate virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Git Issues
```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard all local changes
git reset --hard HEAD
git clean -fd

# Update branch with main
git checkout main
git pull
git checkout your-branch
git merge main
```

## 📚 Additional Resources

- [Full Workflow Documentation](.github/WORKFLOWS.md)
- [Deployment Status](.github/DEPLOYMENT_STATUS.md)
- [Security Runbook](../SECURITY_RUNBOOK.md)
- [API Documentation](../NEXUS_API_SPEC.md)
- [Main README](../README.md)

## 🆘 Getting Help

1. **Check Documentation** - Most answers are in the docs
2. **Search Issues** - Someone may have had the same problem
3. **Ask the Team** - Create an issue or discussion
4. **Review Logs** - Workflow logs contain detailed error info

## ✨ Best Practices

### Code Quality
- Write clear, self-documenting code
- Add comments for complex logic
- Keep functions small and focused
- Use meaningful variable names

### Commits
- Commit often, with clear messages
- One logical change per commit
- Reference issues when relevant

### PRs
- Keep PRs focused and small
- Update documentation with code changes
- Respond to review comments promptly
- Resolve conflicts before requesting review

### Security
- Never commit secrets or API keys
- Use environment variables
- Keep dependencies updated
- Report security issues privately

---

**Happy Coding! 🎉**

For questions, open an issue or discussion on GitHub.
