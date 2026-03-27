import "dotenv/config";
import { ethers } from "ethers";
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __dirname = dirname(fileURLToPath(import.meta.url));

const { PRIVATE_KEY, SEPOLIA_RPC_URL } = process.env;

if (!PRIVATE_KEY || PRIVATE_KEY.includes("PASTE")) {
  console.error("ERROR: Set PRIVATE_KEY in your .env file (64 hex chars, no 0x prefix).");
  process.exit(1);
}
if (!SEPOLIA_RPC_URL || SEPOLIA_RPC_URL.includes("PASTE")) {
  console.error("ERROR: Set SEPOLIA_RPC_URL in your .env file.");
  process.exit(1);
}

const artifactPath = join(
  __dirname,
  "artifacts/contracts/SpottyCoin.sol/SpottyCoin.json"
);
let artifact;
try {
  artifact = JSON.parse(readFileSync(artifactPath, "utf8"));
} catch {
  console.error(
    "ERROR: Artifact not found. Run `npx hardhat compile` first.\n",
    artifactPath
  );
  process.exit(1);
}

const provider = new ethers.JsonRpcProvider(SEPOLIA_RPC_URL);
const wallet = new ethers.Wallet(
  `0x${PRIVATE_KEY.replace(/^0x/, "")}`,
  provider
);

const address = wallet.address;
const balanceWei = await provider.getBalance(address);
const balanceEth = ethers.formatEther(balanceWei);

console.log("Deploying SpottyCoin to Sepolia...");
console.log("  Deployer address :", address);
console.log("  Deployer balance :", balanceEth, "ETH");

if (balanceWei === 0n) {
  console.error(
    "\nERROR: Deployer has 0 ETH. Get free Sepolia ETH from https://sepoliafaucet.com"
  );
  process.exit(1);
}

const factory = new ethers.ContractFactory(
  artifact.abi,
  artifact.bytecode,
  wallet
);

console.log("\nSending deployment transaction...");
const contract = await factory.deploy();
const txHash = contract.deploymentTransaction()?.hash;
console.log("  Tx hash          :", txHash);
console.log("  Waiting for confirmation (this may take ~15 s on Sepolia)...");

await contract.waitForDeployment();
const contractAddress = await contract.getAddress();

console.log("\n✔ SpottyCoin deployed!");
console.log("  Contract address :", contractAddress);
console.log(
  "  Sepolia Etherscan:",
  `https://sepolia.etherscan.io/address/${contractAddress}`
);
console.log("\nNext steps:");
console.log(
  "  1. Verify:  npx hardhat verify --network sepolia",
  contractAddress
);
console.log(
  "  2. MetaMask: import token at address",
  contractAddress,
  "(symbol: STC, decimals: 18)"
);
