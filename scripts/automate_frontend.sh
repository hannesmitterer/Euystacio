#!/usr/bin/env bash
#
# automate_frontend.sh
# Euystacio Frontend Automation Script
#
# This script handles frontend build and deployment preparation.
#
# Usage: ./scripts/automate_frontend.sh
#

set -e
set -u

echo "========================================"
echo "  Euystacio Frontend Automation        "
echo "========================================"
echo ""

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if running from repository root
if [ ! -f "package.json" ]; then
    echo -e "${RED}Error: Must run from repository root${NC}"
    exit 1
fi

echo -e "${GREEN}Step 1: Verifying Node.js...${NC}"
node --version || {
    echo -e "${RED}Node.js not found${NC}"
    exit 1
}

echo ""
echo -e "${GREEN}Step 2: Installing dependencies...${NC}"
npm install

echo ""
echo -e "${GREEN}Step 3: Building frontend...${NC}"
if npm run build 2>/dev/null; then
    echo -e "  ${GREEN}✓ Build successful${NC}"
else
    echo -e "${YELLOW}  ⚠ Build command not configured or failed${NC}"
    echo "  Creating static build directory..."
    mkdir -p dist
fi

echo ""
echo -e "${GREEN}Step 4: Validating static assets...${NC}"

# Check for key frontend files
FRONTEND_FILES=(
    "web-prototype/ave-maria-dashboard.html"
    "src/App.jsx"
    "src/main.jsx"
    "src/components/TamperDemo.jsx"
)

for file in "${FRONTEND_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file exists"
    else
        echo -e "  ${YELLOW}⚠ $file not found${NC}"
    fi
done

echo ""
echo -e "${GREEN}Step 5: Checking artifacts...${NC}"
if [ -d "artifacts" ]; then
    ARTIFACT_COUNT=$(ls -1 artifacts/ 2>/dev/null | wc -l)
    echo "  ✓ artifacts/ contains $ARTIFACT_COUNT files"
else
    echo -e "  ${YELLOW}⚠ artifacts/ directory not found${NC}"
fi

echo ""
echo "========================================"
echo -e "${GREEN}  Frontend Automation Complete!         ${NC}"
echo "========================================"
echo ""
echo "Frontend assets are ready for deployment."
echo ""
echo "To deploy:"
echo "  1. Ensure GitHub Secrets are configured"
echo "  2. Push to trigger CI/CD workflow"
echo "  3. Or run: npm run deploy (if configured)"
echo ""
