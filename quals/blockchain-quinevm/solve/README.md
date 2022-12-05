Using [Foundry](https://getfoundry.sh/).

## Local test

- Run `anvil`, make note of a provided private key
- `foundry script quine --rpc-url http://localhost:8545 --private-key <see above> --broadcast`
- Make note of the created contract address
- The contract address should be in checksum format for the remote, so use `cast ta`

## Against the remote

Do the same thing, but with a different rpc url and private key (make sure to get some test ether to your address first).
