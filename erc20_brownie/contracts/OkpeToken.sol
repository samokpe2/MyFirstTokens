// contracts/OkpeToken.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract OkpeToken is ERC20 {

     event Bought(uint256 amount);
    // wei
    constructor(uint256 initialSupply) ERC20("OkpeToken", "OKPE") {
        _mint(msg.sender, initialSupply);
    }

    function buyToken(address reciever, uint256 amount) payable public {
    uint256 Balance = this.balanceOf(address(this));
    require(amount > 0, "You need to send some ether");
    
    require(amount <= Balance, "Not enough tokens in the reserve");

    amount = 1000 * amount;
    this.transfer(reciever, amount);
    emit Bought(amount);
    }
}
