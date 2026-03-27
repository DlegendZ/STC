import hre from "hardhat";

async function main() {
  const [deployer] = await hre.ethers.getSigners();

  const address = await deployer.getAddress();
  const balanceWei = await hre.ethers.provider.getBalance(address);
  const balanceEth = hre.ethers.formatEther(balanceWei);

  console.log("Deploying SpottyCoin to Sepolia...");
  console.log("  Deployer address :", address);
  console.log("  Deployer balance :", balanceEth, "ETH");

  if (balanceWei === 0n) {
    throw new Error(
      "Deployer has 0 ETH. Get free Sepolia ETH from https://sepoliafaucet.com"
    );
  }

  const SpottyCoin = await hre.ethers.getContractFactory("SpottyCoin");
  console.log("\nSending deployment transaction...");
  const token = await SpottyCoin.deploy();

  console.log("  Tx hash          :", token.deploymentTransaction()?.hash);
  console.log("  Waiting for confirmation...");

  await token.waitForDeployment();
  const contractAddress = await token.getAddress();

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
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
