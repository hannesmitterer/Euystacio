#!/usr/bin/env bash
#
# run_deploy_locally.sh
# Euystacio Local Deployment Runner
#
# This script helps run deployments locally for testing.
# It guides through the deployment process without exposing secrets.
#
# SECURITY WARNING:
# - Requires environment variables to be set
# - NEVER hardcode private keys in this script
# - For production, use GitHub Actions CI/CD
#
# Usage: ./scripts/run_deploy_locally.sh [network]
#   network: sepolia (default), mainnet, polygon
#

set -e

echo "========================================"
echo "  Euystacio Local Deployment Runner    "
echo "========================================"
echo ""

NETWORK=${1:-sepolia}

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Validate network
case $NETWORK in
    sepolia|mainnet|polygon)
        echo -e "${GREEN}Target network: $NETWORK${NC}"
        ;;
    *)
        echo -e "${RED}Invalid network: $NETWORK${NC}"
        echo "Valid options: sepolia, mainnet, polygon"
        exit 1
        ;;
esac

echo ""

# Check for required environment variables
echo "Checking required environment variables..."

MISSING_VARS=0

if [ -z "${DEPLOYER_PRIVATE_KEY:-}" ]; then
    echo -e "${RED}  ✗ DEPLOYER_PRIVATE_KEY not set${NC}"
    MISSING_VARS=$((MISSING_VARS + 1))
else
    echo "  ✓ DEPLOYER_PRIVATE_KEY is set"
fi

RPC_VAR="${NETWORK^^}_RPC_URL"
if [ -z "${!RPC_VAR:-}" ]; then
    echo -e "${YELLOW}  ⚠ ${RPC_VAR} not set (will use default)${NC}"
else
    echo "  ✓ ${RPC_VAR} is set"
fi

if [ $MISSING_VARS -gt 0 ]; then
    echo ""
    echo -e "${RED}Missing required environment variables!${NC}"
    echo ""
    echo "Set them using:"
    echo "  export DEPLOYER_PRIVATE_KEY='your_private_key'"
    echo "  export ${NETWORK^^}_RPC_URL='your_rpc_url'"
    echo ""
    echo "Or create a .env file in contracts/hardhat/"
    echo "(Make sure .env is gitignored!)"
    exit 1
fi

echo ""

# Navigate to hardhat directory
cd "$(dirname "$0")/../contracts/hardhat"

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Compile contracts
echo "Compiling contracts..."
npx hardhat compile

echo ""
echo -e "${GREEN}Ready to deploy to $NETWORK${NC}"
echo ""
echo -e "${YELLOW}⚠️  DEPLOYMENT WARNING ⚠️${NC}"
echo ""
echo "You are about to deploy EuystacioSTAnchor to $NETWORK."
echo ""

if [ "$NETWORK" = "mainnet" ]; then
    echo -e "${RED}⚠️  THIS IS MAINNET - REAL FUNDS WILL BE USED ⚠️${NC}"
    echo ""
fi

read -p "Do you want to proceed? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Deployment cancelled."
    exit 0
fi

echo ""
echo "Deploying..."
echo ""

# Run deployment
npm run deploy:$NETWORK

echo ""
echo -e "${GREEN}Deployment script completed!${NC}"
echo ""
echo "Next steps:"
echo "  1. Save the contract address"
echo "  2. Verify the contract on Etherscan/Polygonscan"
echo "  3. Update the dashboard with the contract address"
echo ""
