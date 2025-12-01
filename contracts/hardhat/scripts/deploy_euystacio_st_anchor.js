/**
 * Deploy Script for EuystacioSTAnchor
 * 
 * Usage:
 *   npx hardhat run scripts/deploy_euystacio_st_anchor.js --network sepolia
 * 
 * Required Environment Variables:
 *   - DEPLOYER_PRIVATE_KEY: Private key of the deploying wallet
 *   - SEPOLIA_RPC_URL: (optional) RPC endpoint for Sepolia
 * 
 * SECURITY WARNING:
 *   Never commit private keys. Use environment variables or GitHub Secrets.
 */

const hre = require("hardhat");

async function main() {
  console.log("========================================");
  console.log("  EuystacioSTAnchor Deployment Script  ");
  console.log("========================================\n");

  // Get deployer info
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying with account:", deployer.address);
  
  const balance = await hre.ethers.provider.getBalance(deployer.address);
  console.log("Account balance:", hre.ethers.formatEther(balance), "ETH\n");

  // Check for sufficient balance
  if (balance === 0n) {
    throw new Error("Deployer account has no ETH. Please fund the account first.");
  }

  // Deploy contract
  console.log("Deploying EuystacioSTAnchor...");
  const EuystacioSTAnchor = await hre.ethers.getContractFactory("EuystacioSTAnchor");
  const anchor = await EuystacioSTAnchor.deploy();

  await anchor.waitForDeployment();
  
  const contractAddress = await anchor.getAddress();
  console.log("\n✓ EuystacioSTAnchor deployed to:", contractAddress);

  // Get contract info
  const [keeper, coronationTimestamp, anchorCount, sealed] = await anchor.getContractInfo();
  console.log("\nContract Info:");
  console.log("  - Keeper:", keeper);
  console.log("  - Coronation Timestamp:", new Date(Number(coronationTimestamp) * 1000).toISOString());
  console.log("  - Anchor Count:", anchorCount.toString());
  console.log("  - Sealed:", sealed);

  // Output deployment info
  console.log("\n========================================");
  console.log("  Deployment Complete!                  ");
  console.log("========================================");
  console.log("\nSave this contract address for verification:");
  console.log(contractAddress);
  
  // Verification instructions
  console.log("\n--- Verification Instructions ---");
  console.log(`To verify on Etherscan/Polygonscan, run:`);
  console.log(`npx hardhat verify --network ${hre.network.name} ${contractAddress}`);
  
  // Return for testing purposes
  return {
    address: contractAddress,
    keeper,
    coronationTimestamp: coronationTimestamp.toString()
  };
}

main()
  .then((result) => {
    console.log("\nDeployment result:", result);
    process.exit(0);
  })
  .catch((error) => {
    console.error("\n✗ Deployment failed:", error);
    process.exit(1);
  });
