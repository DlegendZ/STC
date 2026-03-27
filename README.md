# SpottyCoin (STC)

A fixed-supply ERC-20 token built with Hardhat v3 + TypeScript + ESM.
1,000,000 STC tokens are minted once at deployment — no more can ever be created.

---

## Requirements

- Node.js 18+
- A MetaMask wallet (use a **dedicated dev wallet**, not your main one)
- Free Sepolia ETH — get some at [sepoliafaucet.com](https://sepoliafaucet.com)
- Free accounts at [Alchemy](https://alchemy.com) and [Etherscan](https://etherscan.io)

---

## Setup

### 1. Install dependencies

```bash
npm install
```

### 2. Configure environment

Copy the example file and fill in your values:

```bash
cp env.example .env
```

Open `.env` and set:

| Variable | Where to get it |
|---|---|
| `PRIVATE_KEY` | MetaMask → Account → three dots → Account Details → Export Private Key (64 hex chars, **no** `0x` prefix) |
| `SEPOLIA_RPC_URL` | [Alchemy](https://alchemy.com) → Create App → Ethereum → Sepolia → copy HTTPS URL |
| `ETHERSCAN_API_KEY` | [Etherscan](https://etherscan.io) → Sign in → API Keys → Add |

> **Never commit `.env` to Git.** It is already in `.gitignore`.

---

## Compile

```bash
npx hardhat compile
```

Artifacts are written to `artifacts/contracts/SpottyCoin.sol/SpottyCoin.json`.

---

## Deploy to Sepolia

```bash
node deploy-direct.mjs
```

The script will print your contract address when done. Copy it — you need it for the next steps.

Example output:
```
✔ SpottyCoin deployed!
  Contract address : 0xABC...
  Sepolia Etherscan: https://sepolia.etherscan.io/address/0xABC...
```

---

## Verify on Etherscan

```bash
npx hardhat verify --network sepolia <CONTRACT_ADDRESS>
```

Replace `<CONTRACT_ADDRESS>` with the address printed during deployment.
Wait ~30 seconds after deployment before running this — Etherscan needs time to index the bytecode.

---

## Import into MetaMask

1. Open MetaMask → switch network to **Sepolia Testnet**
2. Scroll down → **Import tokens**
3. Paste your contract address
4. MetaMask auto-fills: symbol `STC`, decimals `18`
5. Click **Add custom token** → **Import tokens**

You should now see **1,000,000 STC** in your wallet.

---

## Project structure

```
contracts/
  SpottyCoin.sol          # ERC-20 token contract (OpenZeppelin)
scripts/
  deploy.ts               # Hardhat deploy script (local/testing)
  deploy-sepolia.ts       # Hardhat deploy script (Sepolia via config)
deploy-direct.mjs         # Direct ethers.js deploy (bypasses Hardhat network config)
hardhat.config.ts         # Hardhat v3 configuration
env.example               # Environment variable template
spottycoin_icon.png       # Token icon (512×512, use in MetaMask)
```

---

## Token details

| Property | Value |
|---|---|
| Name | SpottyCoin |
| Symbol | STC |
| Decimals | 18 |
| Total supply | 1,000,000 STC |
| Network | Sepolia testnet |
| Compiler | solc 0.8.28 |
| Standard | ERC-20 (OpenZeppelin v5) |
