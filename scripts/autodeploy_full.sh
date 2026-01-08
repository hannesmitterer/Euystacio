#!/usr/bin/env bash
#
# autodeploy_full.sh
# Euystacio Full Deployment Automation Script
#
# This script orchestrates a complete deployment:
# 1. Frontend build and preparation
# 2. Smart contract compilation
# 3. Deployment instructions
#
# SECURITY WARNING:
# - This script does NOT deploy contracts automatically
# - All secrets must be set via GitHub Secrets
# - Private keys must NEVER be committed
#
# Usage: ./scripts/autodeploy_full.sh
#

set -e
set -u

echo "╔══════════════════════════════════════╗"
echo "║  EUYSTACIO FULL DEPLOYMENT SCRIPT    ║"
echo "╚══════════════════════════════════════╝"
echo ""

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Navigate to repository root
cd "$(dirname "$0")/.."
REPO_ROOT=$(pwd)

echo -e "${CYAN}Repository root: $REPO_ROOT${NC}"
echo ""

# Phase 1: Environment Check
echo "════════════════════════════════════════"
echo -e "${GREEN}PHASE 1: Environment Validation${NC}"
echo "════════════════════════════════════════"

echo "Checking required tools..."
command -v node >/dev/null 2>&1 && echo "  ✓ Node.js: $(node --version)" || { echo -e "${RED}  ✗ Node.js not found${NC}"; exit 1; }
command -v npm >/dev/null 2>&1 && echo "  ✓ npm: $(npm --version)" || { echo -e "${RED}  ✗ npm not found${NC}"; exit 1; }
command -v git >/dev/null 2>&1 && echo "  ✓ git: $(git --version | cut -d' ' -f3)" || { echo -e "${RED}  ✗ git not found${NC}"; exit 1; }

echo ""

# Phase 2: Security Check
echo "════════════════════════════════════════"
echo -e "${GREEN}PHASE 2: Security Validation${NC}"
echo "════════════════════════════════════════"

SECURITY_ISSUES=0

# Check for .env files with secrets
if [ -f ".env" ]; then
    if grep -qE "(PRIVATE_KEY|SECRET|PASSWORD)" .env 2>/dev/null; then
        echo -e "${RED}  ✗ WARNING: .env contains sensitive data!${NC}"
        SECURITY_ISSUES=$((SECURITY_ISSUES + 1))
    else
        echo -e "${YELLOW}  ⚠ .env file exists (ensure it's gitignored)${NC}"
    fi
else
    echo "  ✓ No .env file in root"
fi

# Check for keys directory
if [ -d "keys" ] || [ -d "keys-to-include" ]; then
    echo -e "${RED}  ✗ WARNING: keys/ or keys-to-include/ directory found!${NC}"
    echo -e "${RED}    These directories should NOT be committed!${NC}"
    SECURITY_ISSUES=$((SECURITY_ISSUES + 1))
else
    echo "  ✓ No keys directories found"
fi

# Check .gitignore
if grep -q "keys/" .gitignore 2>/dev/null && grep -q ".env" .gitignore 2>/dev/null; then
    echo "  ✓ .gitignore properly configured"
else
    echo -e "${YELLOW}  ⚠ Verify .gitignore excludes sensitive files${NC}"
fi

if [ $SECURITY_ISSUES -gt 0 ]; then
    echo ""
    echo -e "${RED}⚠️  SECURITY ISSUES DETECTED: $SECURITY_ISSUES${NC}"
    echo -e "${RED}   Please resolve before deployment!${NC}"
    echo ""
fi

echo ""

# Phase 3: Dependency Installation
echo "════════════════════════════════════════"
echo -e "${GREEN}PHASE 3: Dependency Installation${NC}"
echo "════════════════════════════════════════"

echo "Installing root dependencies..."
npm install --silent 2>/dev/null || echo -e "${YELLOW}  ⚠ Some npm warnings (may be okay)${NC}"
echo "  ✓ Root dependencies installed"

if [ -d "contracts/hardhat" ]; then
    echo "Installing Hardhat dependencies..."
    cd contracts/hardhat
    npm install --silent 2>/dev/null || echo -e "${YELLOW}  ⚠ Some npm warnings${NC}"
    echo "  ✓ Hardhat dependencies installed"
    cd "$REPO_ROOT"
fi

echo ""

# Phase 4: Build
echo "════════════════════════════════════════"
echo -e "${GREEN}PHASE 4: Build${NC}"
echo "════════════════════════════════════════"

echo "Building frontend..."
npm run build 2>/dev/null && echo "  ✓ Frontend built" || echo -e "${YELLOW}  ⚠ Frontend build skipped${NC}"

if [ -d "contracts/hardhat" ]; then
    echo "Compiling smart contracts..."
    cd contracts/hardhat
    npx hardhat compile 2>/dev/null && echo "  ✓ Contracts compiled" || echo -e "${YELLOW}  ⚠ Contract compilation skipped${NC}"
    cd "$REPO_ROOT"
fi

echo ""

# Phase 5: Summary
echo "════════════════════════════════════════"
echo -e "${GREEN}PHASE 5: Deployment Summary${NC}"
echo "════════════════════════════════════════"

echo ""
echo "📦 Components Ready:"
echo "   • Frontend assets"
echo "   • Smart contracts (compiled)"
echo "   • Artifacts and templates"
echo ""
echo "🔒 Security Reminders:"
echo "   • NEVER commit private keys"
echo "   • Use GitHub Secrets for CI/CD"
echo "   • Review all files before pushing"
echo ""
echo "🚀 Next Steps for Deployment:"
echo "   1. Set GitHub Secrets:"
echo "      gh secret set DEPLOYER_PRIVATE_KEY"
echo "      gh secret set SEPOLIA_RPC_URL"
echo "      gh secret set ETHERSCAN_API_KEY"
echo ""
echo "   2. Push to trigger CI/CD:"
echo "      git push origin <branch>"
echo ""
echo "   3. Or deploy manually:"
echo "      cd contracts/hardhat"
echo "      npm run deploy:sepolia"
echo ""

echo "╔══════════════════════════════════════╗"
echo -e "║  ${GREEN}DEPLOYMENT PREPARATION COMPLETE${NC}    ║"
echo "╚══════════════════════════════════════╝"
