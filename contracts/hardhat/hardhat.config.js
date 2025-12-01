/**
 * Hardhat Configuration for EuystacioSTAnchor Deployment
 * 
 * SECURITY WARNING:
 * - NEVER commit private keys to version control
 * - Use environment variables or GitHub Secrets for all sensitive data
 * - See README_DEPLOY.md for setup instructions
 */

require("dotenv").config();
require("@nomicfoundation/hardhat-toolbox");

// Validate required environment variables
const PRIVATE_KEY = process.env.DEPLOYER_PRIVATE_KEY || "0x0000000000000000000000000000000000000000000000000000000000000001";
const ETHERSCAN_API_KEY = process.env.ETHERSCAN_API_KEY || "";
const POLYGONSCAN_API_KEY = process.env.POLYGONSCAN_API_KEY || "";

// RPC URLs - use public endpoints or your own
const SEPOLIA_RPC_URL = process.env.SEPOLIA_RPC_URL || "https://rpc.sepolia.org";
const MAINNET_RPC_URL = process.env.MAINNET_RPC_URL || "https://eth.llamarpc.com";
const POLYGON_RPC_URL = process.env.POLYGON_RPC_URL || "https://polygon-rpc.com";

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: {
    version: "0.8.19",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
    },
  },
  networks: {
    hardhat: {
      chainId: 31337,
    },
    localhost: {
      url: "http://127.0.0.1:8545",
    },
    sepolia: {
      url: SEPOLIA_RPC_URL,
      accounts: [PRIVATE_KEY],
      chainId: 11155111,
      gasPrice: "auto",
    },
    mainnet: {
      url: MAINNET_RPC_URL,
      accounts: [PRIVATE_KEY],
      chainId: 1,
      gasPrice: "auto",
    },
    polygon: {
      url: POLYGON_RPC_URL,
      accounts: [PRIVATE_KEY],
      chainId: 137,
      gasPrice: "auto",
    },
  },
  etherscan: {
    apiKey: {
      mainnet: ETHERSCAN_API_KEY,
      sepolia: ETHERSCAN_API_KEY,
      polygon: POLYGONSCAN_API_KEY,
    },
  },
  paths: {
    sources: "../",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts",
  },
  mocha: {
    timeout: 60000,
  },
};
