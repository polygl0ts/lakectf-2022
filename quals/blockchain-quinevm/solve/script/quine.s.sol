// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-std/Script.sol";
import "forge-std/console.sol";

contract quine is Script {
    function setUp() public {}

    function run() public {
        vm.startBroadcast();

        bytes memory bytecode = hex"383481818039f3";
        address res;
        assembly {
            res := create(0, add(bytecode, 0x20), 7)
        }

        vm.stopBroadcast();
        require(keccak256(res.code) == keccak256(bytecode), "Correctness");
    }
}
