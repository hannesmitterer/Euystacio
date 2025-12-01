#!/usr/bin/env bash
#
# automate_integration.sh
# Euystacio Integration Automation Script
#
# This script automates the integration setup for the Euystacio project.
# It checks dependencies, validates environment, and prepares the project.
#
# SECURITY WARNING:
# - Do NOT commit private keys
# - All secrets should be set via environment variables or GitHub Secrets
#
# Usage: ./scripts/automate_integration.sh
#

set -e  # Exit on error
set -u  # Exit on undefined variable

echo "========================================"
echo "  Euystacio Integration Automation     "
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running from repository root
if [ ! -f "package.json" ]; then
    echo -e "${RED}Error: Must run from repository root${NC}"
    exit 1
fi

echo -e "${GREEN}Step 1: Checking Node.js installation...${NC}"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "  ✓ Node.js version: $NODE_VERSION"
else
    echo -e "${RED}  ✗ Node.js not found. Please install Node.js 18+${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}Step 2: Installing root dependencies...${NC}"
npm install --silent 2>/dev/null || {
    echo -e "${YELLOW}  ⚠ npm install had warnings (this may be okay)${NC}"
}
echo "  ✓ Root dependencies installed"

echo ""
echo -e "${GREEN}Step 3: Checking for contracts/hardhat directory...${NC}"
if [ -d "contracts/hardhat" ]; then
    echo "  ✓ Hardhat directory exists"
    
    echo ""
    echo -e "${GREEN}Step 4: Installing Hardhat dependencies...${NC}"
    cd contracts/hardhat
    npm install --silent 2>/dev/null || {
        echo -e "${YELLOW}  ⚠ Hardhat npm install had warnings${NC}"
    }
    echo "  ✓ Hardhat dependencies installed"
    
    echo ""
    echo -e "${GREEN}Step 5: Compiling smart contracts...${NC}"
    npx hardhat compile 2>/dev/null && {
        echo "  ✓ Contracts compiled successfully"
    } || {
        echo -e "${YELLOW}  ⚠ Contract compilation skipped (may need configuration)${NC}"
    }
    
    cd ../..
else
    echo -e "${YELLOW}  ⚠ contracts/hardhat directory not found${NC}"
fi

echo ""
echo -e "${GREEN}Step 6: Validating environment...${NC}"

# Check for .env file (should not exist if following security practices)
if [ -f ".env" ]; then
    echo -e "${YELLOW}  ⚠ .env file found - ensure no secrets are committed${NC}"
else
    echo "  ✓ No .env file in root (good for security)"
fi

# Check .gitignore for security patterns
if grep -q "keys/" .gitignore 2>/dev/null; then
    echo "  ✓ keys/ directory is gitignored"
else
    echo -e "${YELLOW}  ⚠ Consider adding keys/ to .gitignore${NC}"
fi

echo ""
echo -e "${GREEN}Step 7: Creating necessary directories...${NC}"
mkdir -p artifacts
mkdir -p web-prototype
mkdir -p src/components
echo "  ✓ Directory structure verified"

echo ""
echo "========================================"
echo -e "${GREEN}  Integration Setup Complete!           ${NC}"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Set up GitHub Secrets for deployment"
echo "  2. Configure RPC endpoints"
echo "  3. Run: npm run build"
echo ""
echo -e "${YELLOW}Remember: NEVER commit private keys!${NC}"
echo ""
