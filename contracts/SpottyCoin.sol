// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

/**
 * @title SpottyCoin
 * @dev A simple fixed-supply ERC-20 token.
 *      All 1,000,000 STC tokens are minted once at deployment.
 *      No more can ever be created.
 */
contract SpottyCoin is ERC20 {

    /**
     * @dev Constructor — runs once when the contract is deployed.
     *      Mints the entire supply to the deployer's wallet.
     */
    constructor() ERC20("SpottyCoin", "STC") {
        // 1_000_000 tokens × 10^18 (18 decimal places)
        _mint(msg.sender, 1_000_000 * 10 ** decimals());
    }
}
