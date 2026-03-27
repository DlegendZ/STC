import { ethers } from "ethers";
import hre from "hardhat";

async function main() {
  const provider = new ethers.JsonRpcProvider("http://127.0.0.1:8545");

  const HARDHAT_TEST_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80";
  const signer = new ethers.Wallet(HARDHAT_TEST_KEY, provider);

  console.log("Deploying SpottyCoin with account:", signer.address);
  console.log("Account balance:", (await provider.getBalance(signer.address)).toString());

  const artifact = await hre.artifacts.readArtifact("SpottyCoin");
  const factory = new ethers.ContractFactory(artifact.abi, artifact.bytecode, signer);
  const token = await factory.deploy();
  await token.waitForDeployment();

  console.log("SpottyCoin deployed to:", await token.getAddress());
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
