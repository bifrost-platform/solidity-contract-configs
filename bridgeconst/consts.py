import json
import unittest
from typing import Union, List, cast, Tuple
from enum import Enum

from bridgeconst.utils import concat_as_int, parser, to_even_hex, zero_filled_hex


class EnumInterface(Enum):
    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return self.name

    @classmethod
    def from_name(cls, name):
        return cls.__dict__[name]

    @classmethod
    def str_with_size(cls):
        return cls.__name__ + "-{}".format(cls.size())

    @staticmethod
    def is_composed() -> bool:
        raise Exception("Not implemented")

    @staticmethod
    def components() -> List[str]:
        raise Exception("Not implemented")

    @staticmethod
    def size() -> int:
        raise Exception("Not implemented")

    def formatted_bytes(self) -> bytes:
        return self.value.to_bytes(self.size(), "big")

    def formatted_hex(self) -> str:
        return "0x" + self.formatted_bytes().hex()


class Chain(EnumInterface):
    """
    Name rule: <Native coin symbol> + "_" + <MAIN or TEST or name of testnet>
    Value rule: chain id (network id)
    """
    # BITCOIN-like chains
    NONE = 0
    # BTC_MAIN = 536887296  # version of header
    # BTC_TEST = 536870912  # version of header

    # BIFROST Networks
    BFC_MAIN = 0x0bfc
    BFC_TEST = 0xbfc0

    # Ethereums
    ETH_MAIN = 1
    ETH_GOERLI = 5
    ETH_SEPOLIA = 11155111

    # BNB chains
    BNB_MAIN = 56
    BNB_TEST = 97

    # Polygon chains
    MATIC_MAIN = 137
    MATIC_MUMBAI = 80001

    # Avalanche chains
    AVAX_MAIN = 43114
    AVAX_FUJI = 43113

    # Klaytn chains
    KLAY_MAIN = 8217
    KLAY_TEST = 1001

    # reserved
    RESERVED_01  = 0xffffffff
    RESERVED_02  = 0xfffffffe
    RESERVED_03  = 0xfffffffd
    RESERVED_04  = 0xfffffffc
    RESERVED_05  = 0xfffffffb

    @staticmethod
    def is_composed() -> bool:
        return False

    @staticmethod
    def components() -> List[str]:
        return []

    @staticmethod
    def size():
        return 4


class Symbol(EnumInterface):
    """
    Name rule: symbol of the asset
    Value rule: -
    """
    NONE = 0x00
    BFC = 0x01
    BIFI = 0x02
    BTC = 0x03
    ETH = 0x04
    BNB = 0x05
    MATIC = 0x06
    AVAX = 0x07
    USDC = 0x08
    BUSD = 0x09
    USDT = 0x0a
    DAI = 0x0b
    LINK = 0x0c
    KLAY = 0x0d

    @staticmethod
    def size():
        return 4

    @staticmethod
    def is_composed() -> bool:
        return False

    @staticmethod
    def components() -> List[str]:
        return []

    def is_coin_on(self, chain_index: Chain) -> bool:
        """ return True if the symbol is coin on the chain, or returns false """
        return True if self.name == chain_index.name.split("-")[0] else False

    @property
    def decimal(self):
        """ return a decimal of the asset (self) """
        return 6 if self == Symbol.USDC or self == Symbol.USDT else 18


class AssetType(EnumInterface):
    NONE = 0
    COIN = 1
    UNIFIED = 2
    BRIDGED = 3
    RESERVED = 0xffffffff

    @classmethod
    def size(cls) -> int:
        return 4

    @classmethod
    def is_composed(cls) -> bool:
        return False

    @classmethod
    def components(cls) -> List[str]:
        return []


ERC20_ADDRESS_BSIZE = 20
DISTINGUISH_NUM_BSIZE = 29
COIN_ADDRESS = "0x" + "ff" * 20


class Asset(EnumInterface):
    NONE = 0

    # # BTC
    # # ----------------------------------------------------------------------------------------------------------------
    # BTC_ON_BTC_MAIN = concat_as_int(
    #     Symbol.BTC, Chain.BTC_MAIN, COIN_ADDRESS
    # )
    # BTC_ON_BTC_TEST = concat_as_int(
    #     Symbol.BTC, Chain.BTC_TEST, COIN_ADDRESS
    # )
    # # ----------------------------------------------------------------------------------------------------------------
    # BTC_ON_ETH_MAIN = concat_as_int(
    #     Symbol.BTC, Chain.ETH_MAIN, 0
    # )
    # BTC_ON_ETH_GOERLI = concat_as_int(
    #     Symbol.BTC, Chain.ETH_GOERLI, 0
    # )
    # # ----------------------------------------------------------------------------------------------------------------
    # BRIDGED_BTC_MAIN_BTC_ON_BFC_MAIN = concat_as_int(
    #     Symbol.BTC, Chain.BFC_MAIN, 0
    # )
    # BRIDGED_BTC_MAIN_BTC_ON_BFC_TEST = concat_as_int(
    #     Symbol.BTC, Chain.BFC_TEST, 0
    # )
    # BRIDGED_BTC_TEST_BTC_ON_BFC_MAIN = concat_as_int(
    #     Symbol.BTC, Chain.BFC_MAIN, 0
    # )
    # BRIDGED_BTC_TEST_BTC_ON_BFC_TEST = concat_as_int(
    #     Symbol.BTC, Chain.BFC_TEST, 0
    # )
    # UNIFIED_BTC_ON_BFC_MAIN = concat_as_int(
    #     Symbol.BTC, Chain.BFC_MAIN, 0
    # )
    # UNIFIED_BTC_ON_BFC_TEST = concat_as_int(
    #     Symbol.BTC, Chain.BFC_TEST, 0
    # )
    # # ----------------------------------------------------------------------------------------------------------------

    # BFC
    # ------------------------------------------------------------------------------------------------------------------
    BFC_ON_BFC_MAIN = concat_as_int(Symbol.BFC, AssetType.COIN, Chain.BFC_MAIN, COIN_ADDRESS)
    BFC_ON_BFC_TEST = concat_as_int(Symbol.BFC, AssetType.COIN, Chain.BFC_TEST, COIN_ADDRESS)
    # ------------------------------------------------------------------------------------------------------------------
    BFC_ON_ETH_MAIN = concat_as_int(Symbol.BFC, AssetType.RESERVED, Chain.ETH_MAIN, "0x000000000000000000000000000000000000000")
    BFC_ON_ETH_GOERLI = concat_as_int(Symbol.BFC, AssetType.RESERVED, Chain.ETH_GOERLI, "0x3A815eBa66EaBE966a6Ae7e5Df9652eca24e9c54")
    # ------------------------------------------------------------------------------------------------------------------
    BRIDGED_ETH_MAIN_BFC_ON_BFC_MAIN = concat_as_int(
        Symbol.BFC, AssetType.BRIDGED, Chain.BFC_MAIN, "0x000000000000000000000000000000000000000"
    )
    BRIDGED_ETH_MAIN_BFC_ON_BFC_TEST = concat_as_int(
        Symbol.BFC, AssetType.BRIDGED, Chain.BFC_TEST, "0x000000000000000000000000000000000000000"
    )
    # BRIDGED_ETH_GOERLI_BFC_ON_BFC_MAIN = concat_as_int(
    #     Symbol.BFC, AssetType.BRIDGED, Chain.BFC_MAIN, "0x000000000000000000000000000000000000000"
    # )
    BRIDGED_ETH_GOERLI_BFC_ON_BFC_TEST = concat_as_int(
        Symbol.BFC, AssetType.BRIDGED, Chain.BFC_TEST, "0xfB5D65B8e8784ae3e004e1e476B05d408e6A1f2D"
    )
    UNIFIED_BFC_ON_BFC_MAIN = concat_as_int(
        Symbol.BFC, AssetType.UNIFIED, Chain.BFC_MAIN, "0x000000000000000000000000000000000000000"
    )
    UNIFIED_BFC_ON_BFC_TEST = concat_as_int(
        Symbol.BFC, AssetType.UNIFIED, Chain.BFC_TEST, "0xB0fF18CB2d0F3f51a9c54Af862ed98f3caa027A1"
    )
    # ------------------------------------------------------------------------------------------------------------------

    # BIFI
    # ------------------------------------------------------------------------------------------------------------------
    BIFI_ON_ETH_MAIN = concat_as_int(
        Symbol.BIFI, AssetType.RESERVED, Chain.ETH_MAIN, "0x000000000000000000000000000000000000000"
    )
    BIFI_ON_ETH_GOERLI = concat_as_int(
        Symbol.BIFI, AssetType.RESERVED, Chain.ETH_GOERLI, "0x055ED934c426855caB467FdF8441D4FD6a7D2659"
    )
    # ------------------------------------------------------------------------------------------------------------------
    BRIDGED_ETH_MAIN_BIFI_ON_BFC_MAIN = concat_as_int(
        Symbol.BIFI, AssetType.BRIDGED, Chain.BFC_MAIN, "0x000000000000000000000000000000000000000"
    )
    BRIDGED_ETH_MAIN_BIFI_ON_BFC_TEST = concat_as_int(
        Symbol.BIFI, AssetType.BRIDGED, Chain.BFC_TEST, "0x000000000000000000000000000000000000000"
    )
    # BRIDGED_ETH_GOERLI_BIFI_ON_BFC_MAIN = concat_as_int(
    #     Symbol.BIFI, AssetType.BRIDGED, Chain.BFC_MAIN, "0x000000000000000000000000000000000000000"
    # )
    BRIDGED_ETH_GOERLI_BIFI_ON_BFC_TEST = concat_as_int(
        Symbol.BIFI, AssetType.BRIDGED, Chain.BFC_TEST, "0xC4F1CcafCBeB0BE0F1CDBA499696603528655F29"
    )
    UNIFIED_BIFI_ON_BFC_MAIN = concat_as_int(
        Symbol.BIFI, AssetType.UNIFIED, Chain.BFC_MAIN, "0x000000000000000000000000000000000000000"
    )
    UNIFIED_BIFI_ON_BFC_TEST = concat_as_int(
        Symbol.BIFI, AssetType.UNIFIED, Chain.BFC_TEST, "0x8010a873d59719e895E20f15f9906B5a1F399C3A")
    # ------------------------------------------------------------------------------------------------------------------

    # ETH
    # ------------------------------------------------------------------------------------------------------------------
    ETH_ON_ETH_MAIN = concat_as_int(Symbol.ETH, AssetType.COIN, Chain.ETH_MAIN, COIN_ADDRESS)
    ETH_ON_ETH_GOERLI = concat_as_int(Symbol.ETH, AssetType.COIN, Chain.ETH_GOERLI, COIN_ADDRESS)
    # ------------------------------------------------------------------------------------------------------------------
    BRIDGED_ETH_MAIN_ETH_ON_BFC_MAIN = concat_as_int(
        Symbol.ETH, AssetType.BRIDGED, Chain.BFC_MAIN, "0x000000000000000000000000000000000000000"
    )
    BRIDGED_ETH_MAIN_ETH_ON_BFC_TEST = concat_as_int(
        Symbol.ETH, AssetType.BRIDGED, Chain.BFC_TEST, "0x000000000000000000000000000000000000000"
    )
    # BRIDGED_ETH_GOERLI_ETH_ON_BFC_MAIN = concat_as_int(
    #     Symbol.ETH, AssetType.BRIDGED, Chain.BFC_MAIN, 0
    # )
    BRIDGED_ETH_GOERLI_ETH_ON_BFC_TEST = concat_as_int(
        Symbol.ETH, AssetType.BRIDGED, Chain.BFC_TEST, "0xD089773D293F43440529e6cfa84639E0498A0277"
    )
    UNIFIED_ETH_ON_BFC_MAIN = concat_as_int(
        Symbol.ETH, AssetType.UNIFIED, Chain.BFC_MAIN, "0x000000000000000000000000000000000000000"
    )
    UNIFIED_ETH_ON_BFC_TEST = concat_as_int(
        Symbol.ETH, AssetType.UNIFIED, Chain.BFC_TEST, "0xc83EEd1bf5464eD5383bc3342b918E08f6815950"
    )
    # ------------------------------------------------------------------------------------------------------------------

    # BNB
    # ------------------------------------------------------------------------------------------------------------------
    BNB_ON_BNB_MAIN = concat_as_int(Symbol.BNB, AssetType.COIN, Chain.BNB_MAIN, COIN_ADDRESS)
    BNB_ON_BNB_TEST = concat_as_int(Symbol.BNB, AssetType.COIN, Chain.BNB_TEST, COIN_ADDRESS)
    # ------------------------------------------------------------------------------------------------------------------
    BRIDGED_BNB_MAIN_BNB_ON_BFC_MAIN = concat_as_int(
        Symbol.BNB, AssetType.BRIDGED, Chain.BFC_MAIN, "0x000000000000000000000000000000000000000"
    )
    BRIDGED_BNB_MAIN_BNB_ON_BFC_TEST = concat_as_int(
        Symbol.BNB, AssetType.BRIDGED, Chain.BFC_TEST, "0x000000000000000000000000000000000000000"
    )
    # BRIDGED_BNB_TEST_BNB_ON_BFC_MAIN = concat_as_int(
    #     Symbol.BNB, AssetType.BRIDGED, Chain.BFC_MAIN, 0
    # )
    BRIDGED_BNB_TEST_BNB_ON_BFC_TEST = concat_as_int(
        Symbol.BNB, AssetType.BRIDGED, Chain.BFC_TEST, "0x72D22DF54b86d25D9F9E0C10D516Ab22517b7051"
    )
    UNIFIED_BNB_ON_BFC_MAIN = concat_as_int(
        Symbol.BNB, AssetType.UNIFIED, Chain.BFC_MAIN, "0x000000000000000000000000000000000000000"
    )
    UNIFIED_BNB_ON_BFC_TEST = concat_as_int(
        Symbol.BNB, AssetType.UNIFIED, Chain.BFC_TEST, "0xCd8bf79fA84D551f2465C0a646cABc295d43Be5C"
    )
    # ------------------------------------------------------------------------------------------------------------------

    # AVAX
    # # ----------------------------------------------------------------------------------------------------------------
    # AVAX_ON_AVAX_MAIN = concat_as_int(Symbol.AVAX, AssetType.COIN, Chain.AVAX_MAIN, COIN_ADDRESS)
    # AVAX_ON_AVAX_FUJI = concat_as_int(Symbol.AVAX, AssetType.COIN, Chain.AVAX_FUJI, COIN_ADDRESS)
    # # ----------------------------------------------------------------------------------------------------------------
    # BRIDGE_AVAX_MAIN_AVAX_ON_BFC_MAIN = concat_as_int(Symbol.AVAX, AssetType.BRIDGED, Chain.BFC_MAIN, 48)
    # BRIDGE_AVAX_MAIN_AVAX_ON_BFC_TEST = concat_as_int(Symbol.AVAX, AssetType.BRIDGED, Chain.BFC_TEST, 49)
    # BRIDGE_AVAX_FUJI_AVAX_ON_BFC_MAIN = concat_as_int(Symbol.AVAX, AssetType.BRIDGED, Chain.BFC_MAIN, 50)
    # BRIDGE_AVAX_FUJI_AVAX_ON_BFC_TEST = concat_as_int(Symbol.AVAX, AssetType.BRIDGED, Chain.BFC_TEST, 51)
    # UNIFIED_AVAX_ON_BFC_MAIN = concat_as_int(Symbol.AVAX, AssetType.UNIFIED, Chain.BFC_MAIN, 52)
    # UNIFIED_AVAX_ON_BFC_TEST = concat_as_int(Symbol.AVAX, AssetType.UNIFIED, Chain.BFC_TEST, 53)
    # # ----------------------------------------------------------------------------------------------------------------
    #
    # # MATIC
    # # ----------------------------------------------------------------------------------------------------------------
    # MATIC_ON_MATIC_MAIN = concat_as_int(Symbol.MATIC, AssetType.COIN, Chain.MATIC_MAIN, COIN_ADDRESS)
    # MATIC_ON_MATIC_MUMBAI = concat_as_int(Symbol.MATIC, AssetType.COIN, Chain.MATIC_MUMBAI, COIN_ADDRESS)
    # # ----------------------------------------------------------------------------------------------------------------
    # BRIDGED_MATIC_MAIN_MATIC_ON_BFC_MAIN = concat_as_int(Symbol.MATIC, AssetType.BRIDGED, Chain.BFC_MAIN, 56)
    # BRIDGED_MATIC_MAIN_MATIC_ON_BFC_TEST = concat_as_int(Symbol.MATIC, AssetType.BRIDGED, Chain.BFC_TEST, 57)
    # BRIDGED_MATIC_MUMBAI_MATIC_ON_BFC_MAIN = concat_as_int(Symbol.MATIC, AssetType.BRIDGED, Chain.BFC_MAIN, 58)
    # BRIDGED_MATIC_MUMBAI_MATIC_ON_BFC_TEST = concat_as_int(Symbol.MATIC, AssetType.BRIDGED, Chain.BFC_TEST, 59)
    # UNIFIED_MATIC_ON_BFC_MAIN = concat_as_int(Symbol.MATIC, AssetType.UNIFIED, Chain.BFC_MAIN, 60)
    # UNIFIED_MATIC_ON_BFC_TEST = concat_as_int(Symbol.MATIC, AssetType.UNIFIED, Chain.BFC_TEST, 61)
    # # ----------------------------------------------------------------------------------------------------------------

    # USDC
    # ------------------------------------------------------------------------------------------------------------------
    USDC_ON_ETH_MAIN = concat_as_int(Symbol.USDC, AssetType.RESERVED, Chain.ETH_MAIN, "0x000000000000000000000000000000000000000")
    USDC_ON_ETH_GOERLI = concat_as_int(Symbol.USDC, AssetType.RESERVED, Chain.ETH_GOERLI, "0xD978Be30CE95D42DF7067b988f25bCa2b286Fb70")
    USDC_ON_BNB_MAIN = concat_as_int(Symbol.USDC, AssetType.RESERVED, Chain.BNB_MAIN, "0x000000000000000000000000000000000000000")
    USDC_ON_BNB_TEST = concat_as_int(Symbol.USDC, AssetType.RESERVED, Chain.BNB_TEST, "0xC9C0aD3179eE2f4801454926ED5D6A2Da30b56FB")
    # USDC_ON_MATIC_MAIN = concat_as_int(Symbol.USDC, AssetType.RESERVED, Chain.MATIC_MAIN, 64)
    # USDC_ON_MATIC_MUMBAI = concat_as_int(Symbol.USDC, AssetType.RESERVED, Chain.MATIC_MUMBAI, 64)
    # USDC_ON_AVAX_MAIN = concat_as_int(Symbol.USDC, AssetType.RESERVED, Chain.AVAX_MAIN, 64)
    # USDC_ON_AVAX_FUJI = concat_as_int(Symbol.USDC, AssetType.RESERVED, Chain.AVAX_FUJI, 64)
    # ------------------------------------------------------------------------------------------------------------------
    BRIDGED_ETH_MAIN_USDC_ON_BFC_MAIN = concat_as_int(
        Symbol.USDC, AssetType.BRIDGED, Chain.BFC_MAIN, "0x000000000000000000000000000000000000000"
    )
    BRIDGED_ETH_MAIN_USDC_ON_BFC_TEST = concat_as_int(
        Symbol.USDC, AssetType.BRIDGED, Chain.BFC_TEST, "0x000000000000000000000000000000000000000"
    )
    BRIDGED_ETH_GOERLI_USDC_ON_BFC_MAIN = concat_as_int(
        Symbol.USDC, AssetType.BRIDGED, Chain.BFC_MAIN, "0x000000000000000000000000000000000000000"
    )
    BRIDGED_ETH_GOERLI_USDC_ON_BFC_TEST = concat_as_int(
        Symbol.USDC, AssetType.BRIDGED, Chain.BFC_TEST, "0xa7bb0a2693fb4d1ab9a6C5acCf5C63f12fab1855"
    )
    # ------------------------------------------------------------------------------------------------------------------
    BRIDGED_BNB_MAIN_USDC_ON_BFC_MAIN = concat_as_int(
        Symbol.USDC, AssetType.BRIDGED, Chain.BFC_MAIN, "0x000000000000000000000000000000000000000"
    )
    BRIDGED_BNB_MAIN_USDC_ON_BFC_TEST = concat_as_int(
        Symbol.USDC, AssetType.BRIDGED, Chain.BFC_TEST, "0x000000000000000000000000000000000000000"
    )
    # BRIDGED_BNB_TEST_USDC_ON_BFC_MAIN = concat_as_int(
    #     Symbol.USDC, AssetType.BRIDGED, Chain.BFC_MAIN, "0x000000000000000000000000000000000000000"
    # )
    BRIDGED_BNB_TEST_USDC_ON_BFC_TEST = concat_as_int(
        Symbol.USDC, AssetType.BRIDGED, Chain.BFC_TEST, "0xC67f0b7c01f6888D43B563B3a8B851856BcfAB64"
    )
    # # ----------------------------------------------------------------------------------------------------------------
    # BRIDGED_MATIC_MAIN_USDC_ON_BFC_MAIN = concat_as_int(Symbol.USDC, AssetType.BRIDGED, Chain.BFC_MAIN, 80)
    # BRIDGED_MATIC_MAIN_USDC_ON_BFC_TEST = concat_as_int(Symbol.USDC, AssetType.BRIDGED, Chain.BFC_TEST, 81)
    # BRIDGED_MATIC_MUMBAI_USDC_ON_BFC_MAIN = concat_as_int(Symbol.USDC, AssetType.BRIDGED, Chain.BFC_MAIN, 82)
    # BRIDGED_MATIC_MUMBAI_USDC_ON_BFC_TEST = concat_as_int(Symbol.USDC, AssetType.BRIDGED, Chain.BFC_TEST, 83)
    # # ----------------------------------------------------------------------------------------------------------------
    # BRIDGED_AVAX_MAIN_USDC_ON_BFC_MAIN = concat_as_int(Symbol.USDC, AssetType.BRIDGED, Chain.BFC_MAIN, 88)
    # BRIDGED_AVAX_MAIN_USDC_ON_BFC_TEST = concat_as_int(Symbol.USDC, AssetType.BRIDGED, Chain.BFC_TEST, 89)
    # BRIDGED_AVAX_FUJI_USDC_ON_BFC_MAIN = concat_as_int(Symbol.USDC, AssetType.BRIDGED, Chain.BFC_MAIN, 91)
    # BRIDGED_AVAX_FUJI_USDC_ON_BFC_TEST = concat_as_int(Symbol.USDC, AssetType.BRIDGED, Chain.BFC_TEST, 92)
    # # ----------------------------------------------------------------------------------------------------------------
    UNIFIED_USDC_ON_BFC_MAIN = concat_as_int(
        Symbol.USDC, AssetType.UNIFIED, Chain.BFC_MAIN, "0x000000000000000000000000000000000000000"
    )
    UNIFIED_USDC_ON_BFC_TEST = concat_as_int(
        Symbol.USDC, AssetType.UNIFIED, Chain.BFC_TEST, "0x28661511CDA7119B2185c647F23106a637CC074f"
    )
    # ------------------------------------------------------------------------------------------------------------------

    # # BUSD
    # # ----------------------------------------------------------------------------------------------------------------
    # BUSD_ON_BNB_MAIN = concat_as_int(Symbol.BUSD, AssetType.RESERVED, Chain.BNB_MAIN, 97)
    # BUSD_ON_BNB_TEST = concat_as_int(Symbol.BUSD, AssetType.RESERVED, Chain.BNB_TEST, 98)
    # # ----------------------------------------------------------------------------------------------------------------
    # BRIDGED_BNB_MAIN_BUSD_ON_BFC_MAIN = concat_as_int(Symbol.BUSD, AssetType.BRIDGED, Chain.BFC_MAIN, 99)
    # BRIDGED_BNB_MAIN_BUSD_ON_BFC_TEST = concat_as_int(Symbol.BUSD, AssetType.BRIDGED, Chain.BFC_TEST, 99)
    # BRIDGED_BNB_TEST_BUSD_ON_BFC_MAIN = concat_as_int(Symbol.BUSD, AssetType.BRIDGED, Chain.BFC_MAIN, 100)
    # BRIDGED_BNB_TEST_BUSD_ON_BFC_TEST = concat_as_int(Symbol.BUSD, AssetType.BRIDGED, Chain.BFC_MAIN, 101)
    # UNIFIED_BUSD_ON_BFC_MAIN = concat_as_int(Symbol.BUSD, AssetType.UNIFIED, Chain.BFC_MAIN, 102)
    # UNIFIED_BUSD_ON_BFC_TEST = concat_as_int(Symbol.BUSD, AssetType.UNIFIED, Chain.BFC_TEST, 103)
    # # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def is_composed() -> bool:
        return True

    @staticmethod
    def components() -> List[str]:
        return [Symbol.str_with_size(), AssetType.str_with_size(), Chain.str_with_size(), "ADDRESS-{}".format(ERC20_ADDRESS_BSIZE)]

    def analyze(self) -> List[Union[int, type]]:
        """ symbol, related chain and erc20 address """
        return parser(self.formatted_hex(), [Symbol, AssetType, Chain, ERC20_ADDRESS_BSIZE])

    @staticmethod
    def size():
        return Symbol.size() + AssetType.size() + Chain.size() + ERC20_ADDRESS_BSIZE

    def symbol(self) -> Symbol:
        return cast(Symbol, self.analyze()[0])

    def is_coin_on(self) -> bool:
        return self.analyze()[1] == AssetType.COIN

    @property
    def decimal(self) -> int:
        return self.symbol().decimal

    @classmethod
    def from_components(cls, symbol: Symbol, asset_type: AssetType, chain: Chain, address: str):
        return cls(concat_as_int(symbol, asset_type, chain, to_even_hex(address)))


class OPCode(EnumInterface):
    NONE = 0x00
    WARP = 0x01
    UNIFY = 0x02
    SPLIT = 0x03
    UNIFY_SPLIT = 0x04
    DEPOSIT = 0x05
    WITHDRAW = 0x06
    BORROW = 0x07
    REPAY = 0x08
    X_OPEN = 0x09
    X_END = 0x0a
    SWAP = 0x0b
    CALL = 0x0c

    @staticmethod
    def size():
        return 1

    @staticmethod
    def is_composed() -> bool:
        return False

    @staticmethod
    def components() -> List[str]:
        return []


class RBCMethodDirection(EnumInterface):
    NONE = 0x00
    INBOUND = 0x01
    OUTBOUND = 0x02
    IN_AND_OUTBOUND = 0x03

    @staticmethod
    def is_composed() -> bool:
        return False

    @staticmethod
    def components() -> List[str]:
        return []

    @staticmethod
    def size() -> int:
        return OPCode.size()


RBC_METHOD_LENGTH_SIZE = 1


class RBCMethodV1(EnumInterface):
    NONE = 0x0000000000000000
    WARP_IN = concat_as_int(2, RBCMethodDirection.INBOUND, OPCode.WARP)
    WARP_UNIFY = concat_as_int(3, RBCMethodDirection.INBOUND, OPCode.WARP, OPCode.UNIFY)
    WARP_UNIFY_SPLIT = concat_as_int(3, RBCMethodDirection.INBOUND, OPCode.WARP, OPCode.UNIFY_SPLIT)
    WARP_UNIFY_DEPOSIT = concat_as_int(4, RBCMethodDirection.INBOUND, OPCode.WARP, OPCode.UNIFY, OPCode.DEPOSIT)
    WARP_UNIFY_REPAY = concat_as_int(4, RBCMethodDirection.INBOUND, OPCode.WARP, OPCode.UNIFY, OPCode.REPAY)
    WARP_UNIFY_SWAP = concat_as_int(4, RBCMethodDirection.INBOUND, OPCode.WARP, OPCode.UNIFY, OPCode.SWAP)
    WARP_XOPEN = concat_as_int(4, RBCMethodDirection.INBOUND, OPCode.WARP, OPCode.UNIFY, OPCode.X_OPEN)
    WARP_CALL = concat_as_int(3, RBCMethodDirection.INBOUND, OPCode.CALL, OPCode.WARP)

    WARP_OUT = concat_as_int(2, RBCMethodDirection.OUTBOUND, OPCode.WARP)
    SPLIT_WARP = concat_as_int(3, RBCMethodDirection.OUTBOUND, OPCode.SPLIT, OPCode.WARP)
    UNIFY_SPLIT_WARP = concat_as_int(3, RBCMethodDirection.OUTBOUND, OPCode.UNIFY_SPLIT, OPCode.WARP)
    BORROW_SPLIT_WARP = concat_as_int(4, RBCMethodDirection.OUTBOUND, OPCode.BORROW, OPCode.SPLIT, OPCode.WARP)
    BORROW_UNIFY_SPLIT_WARP = concat_as_int(
        4, RBCMethodDirection.OUTBOUND, OPCode.BORROW, OPCode.UNIFY_SPLIT, OPCode.WARP
    )
    WITHDRAW_SPLIT_WARP = concat_as_int(4, RBCMethodDirection.OUTBOUND, OPCode.WITHDRAW, OPCode.SPLIT, OPCode.WARP)
    WITHDRAW_UNIFY_SPLIT_WARP = concat_as_int(
        4, RBCMethodDirection.OUTBOUND, OPCode.WITHDRAW, OPCode.UNIFY_SPLIT, OPCode.WARP
    )
    SWAP_SPLIT_WARP = concat_as_int(4, RBCMethodDirection.OUTBOUND, OPCode.SWAP, OPCode.SPLIT, OPCode.WARP)
    SWAP_UNIFY_SPLIT_WARP = concat_as_int(
        4, RBCMethodDirection.OUTBOUND, OPCode.SWAP, OPCode.UNIFY_SPLIT, OPCode.WARP
    )
    XEND_SPLIT_WARP = concat_as_int(
        4, RBCMethodDirection.OUTBOUND, OPCode.X_END, OPCode.SPLIT, OPCode.WARP
    )
    XEND_UNIFY_SPLIT_WARP = concat_as_int(
        4, RBCMethodDirection.OUTBOUND, OPCode.X_END, OPCode.UNIFY_SPLIT, OPCode.WARP
    )
    CALL_WARP = concat_as_int(
        3, RBCMethodDirection.OUTBOUND, OPCode.CALL, OPCode.WARP
    )
    # in-and-out bound swap without the Unifier
    WARP_SWAP_WARP = concat_as_int(
        4, RBCMethodDirection.IN_AND_OUTBOUND, OPCode.WARP, OPCode.SWAP, OPCode.WARP
    )
    # in-and-out bound 1-1 exchange with the Unifier
    WARP_UNIFY_SPLIT_WARP = concat_as_int(
        4, RBCMethodDirection.IN_AND_OUTBOUND, OPCode.WARP, OPCode.UNIFY_SPLIT, OPCode.WARP
    )
    # in-and-out bound swap with the Unifier
    WARP_UNIFY_SWAP_SPLIT_WARP = concat_as_int(
        6, RBCMethodDirection.IN_AND_OUTBOUND, OPCode.WARP, OPCode.SPLIT, OPCode.SWAP, OPCode.UNIFY, OPCode.WARP
    )

    @staticmethod
    def is_composed() -> bool:
        return True

    @staticmethod
    def components() -> List[str]:
        return [
            "LENGTH-1",
            RBCMethodDirection.str_with_size(),
            "DYNAMIC_SIZE_ARRAY[{}]".format(OPCode.str_with_size())]

    def analyze(self) -> Tuple[int, List[OPCode]]:
        self_hex = self.formatted_hex().replace("0x", "")
        len_op, self_hex = int(self_hex[:2], 16), self_hex[2:]

        start, end = 0, 0
        op_code_list = list()
        for i in range(len_op):
            op_code_list.append(OPCode(int(self_hex[i * OPCode.size() * 2:(i + 1) * OPCode.size() * 2], 16)))
            self_hex = self_hex[end:]
        return len_op, op_code_list

    def formatted_hex(self) -> str:
        if self == self.__class__.NONE:
            return "0x" + "00" * self.size()

        hex_without_0x = to_even_hex(self.value).replace("0x", "")
        op_num = int(hex_without_0x[:RBC_METHOD_LENGTH_SIZE * 2], 16)
        zero_pad = "00" * (self.size() - op_num * OPCode.size() - RBC_METHOD_LENGTH_SIZE)
        return "0x" + hex_without_0x + zero_pad

    def formatted_bytes(self) -> bytes:
        return bytes.fromhex(self.formatted_hex().replace("0x", ""))

    @staticmethod
    def size():
        return 16

    @classmethod
    def from_components(cls, direction: RBCMethodDirection, op_codes: List[OPCode]):
        return cls(concat_as_int(len(op_codes) + 1, direction, op_codes))


class OracleType(EnumInterface):
    NONE = 0x00
    AGGREGATED = 0x01
    CONSENSUS = 0x02

    @staticmethod
    def size():
        """ bytes size """
        return 1

    @staticmethod
    def is_composed() -> bool:
        return False

    @staticmethod
    def components() -> List[str]:
        return []


class OracleSourceType(EnumInterface):
    NONE = 0x00
    ASSET_PRICE = 0x01
    BLOCK_HASH = 0x02

    @staticmethod
    def size():
        """ bytes size """
        return 2

    @staticmethod
    def is_composed() -> bool:
        return False

    @staticmethod
    def components() -> List[str]:
        return []


class Oracle(EnumInterface):
    NONE = 0
    BFC_PRICE = concat_as_int(
        OracleType.AGGREGATED, OracleSourceType.ASSET_PRICE, zero_filled_hex(Symbol.BFC.value, DISTINGUISH_NUM_BSIZE)
    )
    BIFI_PRICE = concat_as_int(
        OracleType.AGGREGATED, OracleSourceType.ASSET_PRICE, zero_filled_hex(Symbol.BIFI.value, DISTINGUISH_NUM_BSIZE)
    )
    BTC_PRICE = concat_as_int(
        OracleType.AGGREGATED, OracleSourceType.ASSET_PRICE, zero_filled_hex(Symbol.BTC.value, DISTINGUISH_NUM_BSIZE)
    )
    ETH_PRICE = concat_as_int(
        OracleType.AGGREGATED, OracleSourceType.ASSET_PRICE, zero_filled_hex(Symbol.ETH.value, DISTINGUISH_NUM_BSIZE)
    )
    BNB_PRICE = concat_as_int(
        OracleType.AGGREGATED, OracleSourceType.ASSET_PRICE, zero_filled_hex(Symbol.BNB.value, DISTINGUISH_NUM_BSIZE)
    )
    MATIC_PRICE = concat_as_int(
        OracleType.AGGREGATED, OracleSourceType.ASSET_PRICE, zero_filled_hex(Symbol.MATIC.value, DISTINGUISH_NUM_BSIZE)
    )
    AVAX_PRICE = concat_as_int(
        OracleType.AGGREGATED, OracleSourceType.ASSET_PRICE, zero_filled_hex(Symbol.AVAX.value, DISTINGUISH_NUM_BSIZE)
    )
    USDC_PRICE = concat_as_int(
        OracleType.AGGREGATED, OracleSourceType.ASSET_PRICE, zero_filled_hex(Symbol.USDC.value, DISTINGUISH_NUM_BSIZE)
    )
    BUSD_PRICE = concat_as_int(
        OracleType.AGGREGATED, OracleSourceType.ASSET_PRICE, zero_filled_hex(Symbol.BUSD.value, DISTINGUISH_NUM_BSIZE)
    )
    BITCOIN_BLOCK_HASH = concat_as_int(
        OracleType.CONSENSUS, OracleSourceType.BLOCK_HASH, zero_filled_hex(Symbol.BTC.value, DISTINGUISH_NUM_BSIZE)
    )

    @staticmethod
    def is_composed() -> bool:
        return True

    @staticmethod
    def components() -> List[str]:
        return [
            OracleType.str_with_size(),
            OracleSourceType.str_with_size(),
            "DISTINGUISHED_BYTES-{}".format(DISTINGUISH_NUM_BSIZE)
        ]

    def analyze(self) -> List[Union[int, type]]:
        return parser(self.formatted_hex(), [OracleType, OracleSourceType, DISTINGUISH_NUM_BSIZE])

    @staticmethod
    def size() -> int:
        return OracleType.size() + OracleSourceType.size() + DISTINGUISH_NUM_BSIZE

    @classmethod
    def build(cls, oracle_type: OracleType, oracle_source_type: OracleSourceType, distinguish_bytes: Union[bytes, str]):
        if isinstance(distinguish_bytes, str):
            distinguish_bytes = bytes.fromhex(distinguish_bytes)
        return cls(concat_as_int(oracle_type, oracle_source_type, distinguish_bytes))

    @classmethod
    def price_oracle_from_symbol(cls, symbol: Symbol):
        return cls(concat_as_int(
            OracleType.AGGREGATED,
            OracleSourceType.ASSET_PRICE,
            zero_filled_hex(symbol.value, DISTINGUISH_NUM_BSIZE)
        ))

    @classmethod
    def block_hash_oracle_from_symbol(cls, symbol: Symbol):
        if symbol != Symbol.BTC:
            raise Exception("Not supported block hash oracle: {}".format(symbol.name))
        return cls(concat_as_int(
            OracleType.CONSENSUS,
            OracleSourceType.BLOCK_HASH,
            zero_filled_hex(symbol.value, DISTINGUISH_NUM_BSIZE)
        ))


class ChainEventStatus(EnumInterface):
    NONE = 0
    REQUESTED = 1
    FAILED = 2
    EXECUTED = 3
    REVERTED = 4
    ACCEPTED = 5
    REJECTED = 6
    COMMITTED = 7
    ROLLBACKED = 8
    NEXT_AUTHORITY_RELAYED = 9
    NEXT_AUTHORITY_COMMITTED = 10

    @staticmethod
    def is_composed() -> bool:
        return False

    @staticmethod
    def components() -> List[str]:
        return []

    @staticmethod
    def size():
        return 1


class TestEnum(unittest.TestCase):
    @staticmethod
    def generate_dict_for_index(index_type):
        index_dict = {
            "bsize": index_type.size(),
            "composed": index_type.is_composed(),
            "components": index_type.components()
        }

        for idx in index_type:
            if idx.size() != index_dict["bsize"]:
                raise Exception("size error: {}".format(idx.name))
            if idx.is_composed():
                if idx.analyze() == []:
                    raise Exception("composed enum has no components: {}".format(idx.name))
                if idx not in RBCMethodV1:
                    comp_size = 0
                    for comp in idx.components():
                        comp_size += int(comp.split("-")[1].replace("]", ""))
                    if idx.size() != comp_size:
                        raise Exception("Not match enum size and the sum of components sizes")
                else:
                    pass

            index_dict[idx.name] = idx.formatted_hex()
        return index_dict

    def test_print_enum(self):
        enum_dict = {}
        enum_dict["Chain"] = TestEnum.generate_dict_for_index(Chain)
        enum_dict["Symbol"] = TestEnum.generate_dict_for_index(Symbol)
        enum_dict["AssetType"] = TestEnum.generate_dict_for_index(AssetType)
        enum_dict["Asset"] = TestEnum.generate_dict_for_index(Asset)

        enum_dict["OPCode"] = TestEnum.generate_dict_for_index(OPCode)
        enum_dict["RBCMethodDirection"] = TestEnum.generate_dict_for_index(RBCMethodDirection)
        enum_dict["RBCMethodV1"] = TestEnum.generate_dict_for_index(RBCMethodV1)

        enum_dict["OracleType"] = TestEnum.generate_dict_for_index(OracleType)
        enum_dict["OracleSourceType"] = TestEnum.generate_dict_for_index(OracleSourceType)
        enum_dict["Oracle"] = TestEnum.generate_dict_for_index(Oracle)
        enum_dict["ChainEventStatus"] = TestEnum.generate_dict_for_index(ChainEventStatus)

        print(json.dumps(enum_dict, indent=4))

    def test_analyze(self):
        result = Asset.BIFI_ON_ETH_GOERLI.analyze()
        print(result)
