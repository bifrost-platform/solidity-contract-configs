# Using the Bridge Enums on your python code


#### installation
``` shell
$ pip install git+https://github.com/bifrost-platform/solidity-contract-configs@230104
```

#### Getting Bridge Service Spec.
```python
from bridgeconst.testbridgespec import SUPPORTING_ASSETS, SUPPORTING_CHAINS
# You can get service spec. of the bridge service. (currently TESTNET ONLY)
print(SUPPORTING_CHAINS)
print(SUPPORTING_ASSETS)
```



#### Basic Example
```python
from bridgeconst.consts import Chain, Asset, Symbol, RBCMethodV1, RBCMethodDirection, OPCode
from bridgeconst.consts import OracleSourceType, OracleType, Oracle
from bridgeconst.export import SUPPORTING_ENUMS

# You can check the list of supporting enum
print("supporting enums: {}".format(SUPPORTING_ENUMS))

# common member function (both composed-enum and non-composed-enum)
print("bytes-size of the enum: {}".format(Chain.size()))
print("sized hex: {}".format(Chain.ETH_GOERLI.formatted_hex()))
print("sized bytes: {}".format(Chain.ETH_GOERLI.formatted_bytes()))
print("is composed? :{}".format(Chain.is_composed()))
print("components of the enum: {}".format(Chain.components()))

# In case of the non-composed, the enum has no components
print("the enum is composed of other enums".format(Chain.is_composed()))  # False
print("components: {}".format(Chain.components()))  # []

# In case of the composed, the enum has the own components
print("the enum is composed of other enums".format(Asset.is_composed()))  # True
print("components: {}".format(Asset.components()))  # [Symbol-4, Chain-8, ADDRESS-20]
# A composed enum can be analyzed (decompose)
# it returns [Symbol.BFC, Chain.BFC_TEST, 0xffffffffffffffffffffffffffffffffffffffff]
print("decomposed: {}".format(Asset.BFC_ON_BFC_TEST))

# A composed enum has "build-functions"
actual = Asset.from_components(Symbol.BFC, Chain.BFC_TEST, "0xffffffffffffffffffffffffffffffffffffffff")
expected = Asset.BFC_ON_BFC_TEST
print(actual == expected)  # True

actual = RBCMethodV1.from_components(RBCMethodDirection.INBOUND, [OPCode.WARP])
expected = RBCMethodV1.WARP_IN
print(actual == expected)  # True

actual = Oracle.price_oracle_from_symbol(Symbol.BFC)
expected = Oracle.BFC_PRICE
print(actual == expected)  # True

actual = Oracle.block_hash_oracle_from_symbol(Symbol.BTC)
expected = Oracle.BITCOIN_BLOCK_HASH
print(actual == expected)  # True
```

#### Export Enums as a json file
```python
from bridgeconst.export import export_enum_json

json_path = "./enums.json"
export_enum_json(json_path)  # write every enums to the json file
export_enum_json()  # print every enum to the console (stdout)
```
