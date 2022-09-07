### ABI json naming rule
```python
abi.<contract_name>.<chain_name>.json
```

### Contract Config json
```python
# contractconfig.json
{
    "<chain_name>": {
        "contracts": [
            {"name": "<contract_name>", "address": "<address in hex>", "abi_file": "<abi json file name>", "deploy_height": "<height_in_int>"},
            {"name": "<contract_name>", "address": "<address in hex>", "abi_file": "<abi json file name>", "deploy_height": "<height_in_int>"},
        ]
    },
    "bifrost": {
        "contracts": [
            {"name": "authority", "address": "0x0000000000000000000000000000000000000400", "abi_file": "abi.authority.json", "deploy_height": 0},
            {"name": "vault", "address": "0x59d1216D2AEACBf1666307417b57d3979d9cd5bB", "abi_file": "abi.vault.json", "deploy_height": 5441},
            {"name": "socket", "address": "0xe5464242b6572507240B8d6BC86f2f6d4a98f14D", "abi_file": "abi.socket.json", "deploy_height": 5443},
            {"name": "oracle_manager", "address": "0x7175D85658600D71B4feF32D8EC4aE8D2EB2b4B7", "abi_file": "abi.oracle_manager.json", "deploy_height": 5439}
        ]
    }    
}

```
