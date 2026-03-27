import "dotenv/config";
import { HardhatUserConfig } from "hardhat/config";
import hardhatEthers from "@nomicfoundation/hardhat-ethers";
import hardhatVerify from "@nomicfoundation/hardhat-verify";

const PRIVATE_KEY = process.env.PRIVATE_KEY ?? "";
const SEPOLIA_RPC_URL = process.env.SEPOLIA_RPC_URL ?? "";
const ETHERSCAN_API_KEY = process.env.ETHERSCAN_API_KEY ?? "";

const config: HardhatUserConfig = {
  plugins: [hardhatEthers, hardhatVerify],
  solidity: {
    version: "0.8.28",
  },
  paths: {
    sources: "./contracts",
    artifacts: "./artifacts",
    cache: "./cache",
  },
  networks: {
    hardhat: {
      type: "edr-simulated",
    },
    sepolia: {
      type: "http",
      url: SEPOLIA_RPC_URL,
      accounts: PRIVATE_KEY ? [`0x${PRIVATE_KEY.replace(/^0x/, "")}`] : [],
    },
  },
  verify: {
    etherscan: {
      apiKey: ETHERSCAN_API_KEY,
    },
  },
};

export default config;
