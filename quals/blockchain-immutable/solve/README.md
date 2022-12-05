Using [Foundry](https://getfoundry.sh/).

## Local test

- Run `anvil`, make note of a provided private key
- `foundry script step1 --rpc-url http://localhost:8545 --private-key <see above> --broadcast`
- Make note of the created contract addresses
- Get your endorsement from the server
- `CHILD=<see above> PWN=<see above> forge script step2 --rpc-url http://localhost:8545  --private-key <same as above --broadcast`
- Get your flag from the server`

## Against the remote

Do the same thing, but with a different rpc url and private key (make sure to get some test ether to your address first).
