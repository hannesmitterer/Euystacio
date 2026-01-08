# EuystacioSTAnchor Deployment Guide

## ⚠️ SECURITY WARNING

**NEVER commit private keys or service account JSON files to this repository!**

All secrets must be configured via:
- **GitHub Secrets** (for CI/CD workflows)
- **Environment variables** (for local development)

---

## Prerequisites

1. Node.js 18.x or higher
2. npm or yarn
3. An Ethereum wallet with ETH for gas fees
4. RPC endpoint (Infura, Alchemy, or public RPC)

---

## Local Development Setup

### 1. Install Dependencies

```bash
cd contracts/hardhat
npm install
```

### 2. Create Environment File

Create a `.env` file (this file is gitignored):

```bash
# .env - DO NOT COMMIT THIS FILE
DEPLOYER_PRIVATE_KEY=your_private_key_here
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/your-api-key
MAINNET_RPC_URL=https://eth-mainnet.g.alchemy.com/v2/your-api-key
POLYGON_RPC_URL=https://polygon-mainnet.g.alchemy.com/v2/your-api-key
ETHERSCAN_API_KEY=your_etherscan_api_key
POLYGONSCAN_API_KEY=your_polygonscan_api_key
```

### 3. Compile Contract

```bash
npm run compile
```

### 4. Run Tests (if available)

```bash
npm run test
```

---

## Deployment

### Deploy to Sepolia (Testnet)

```bash
npm run deploy:sepolia
```

### Deploy to Mainnet

```bash
npm run deploy:mainnet
```

### Deploy to Polygon

```bash
npm run deploy:polygon
```

---

## GitHub Secrets Setup

For CI/CD deployment via GitHub Actions, set these secrets:

### Using GitHub CLI

```bash
# Set the deployer private key
gh secret set DEPLOYER_PRIVATE_KEY --body "your_private_key"

# Set RPC URLs
gh secret set SEPOLIA_RPC_URL --body "https://eth-sepolia.g.alchemy.com/v2/your-api-key"
gh secret set MAINNET_RPC_URL --body "https://eth-mainnet.g.alchemy.com/v2/your-api-key"

# Set API keys for verification
gh secret set ETHERSCAN_API_KEY --body "your_api_key"
gh secret set POLYGONSCAN_API_KEY --body "your_api_key"
```

### Using GitHub Web Interface

1. Navigate to your repository settings
2. Go to **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret:
   - `DEPLOYER_PRIVATE_KEY`
   - `SEPOLIA_RPC_URL`
   - `MAINNET_RPC_URL`
   - `POLYGON_RPC_URL`
   - `ETHERSCAN_API_KEY`
   - `POLYGONSCAN_API_KEY`

---

## Required Secrets List

| Secret Name | Description | Required For |
|-------------|-------------|--------------|
| `DEPLOYER_PRIVATE_KEY` | Private key of deployer wallet | All deployments |
| `SEPOLIA_RPC_URL` | Sepolia RPC endpoint | Testnet deploy |
| `MAINNET_RPC_URL` | Mainnet RPC endpoint | Mainnet deploy |
| `POLYGON_RPC_URL` | Polygon RPC endpoint | Polygon deploy |
| `ETHERSCAN_API_KEY` | Etherscan API key | Contract verification |
| `POLYGONSCAN_API_KEY` | Polygonscan API key | Polygon verification |

---

## Contract Verification

After deployment, verify the contract:

```bash
npx hardhat verify --network sepolia DEPLOYED_CONTRACT_ADDRESS
```

---

## Post-Deployment Steps

1. **Save the contract address** - Store it securely
2. **Verify the contract** - Run verification command
3. **Anchor documents** - Use the contract to anchor sacred documents
4. **Seal when complete** - Call `sealContract()` to make immutable

---

## Troubleshooting

### "Insufficient funds"
Ensure your deployer wallet has enough ETH for gas.

### "Invalid private key"
Check that your private key is properly formatted (with or without 0x prefix).

### "Network connection error"
Verify your RPC URL is correct and accessible.

---

## Support

For issues, create a GitHub issue in the Euystacio repository.

---

*"Der Unveränderliche Eid" - The Immutable Oath*
