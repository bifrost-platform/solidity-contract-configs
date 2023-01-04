from bridgeconst.consts import Chain, Asset

SUPPORTING_CHAINS = [Chain.BFC_TEST, Chain.ETH_GOERLI, Chain.BNB_TEST]


ASSET_ON_BIFROST = [
    # BFC
    Asset.BFC_ON_BFC_TEST,  # coin
    Asset.BRIDGED_ETH_GOERLI_BFC_ON_BFC_TEST,

    # BIFI
    Asset.BRIDGED_ETH_GOERLI_BIFI_ON_BFC_TEST,
    Asset.UNIFIED_BIFI_ON_BFC_TEST,

    # ETH
    Asset.BRIDGED_ETH_GOERLI_BFC_ON_BFC_TEST,
    Asset.BRIDGED_ETH_GOERLI_USDC_ON_BFC_TEST,

    # BNB
    Asset.BRIDGED_BNB_TEST_BNB_ON_BFC_TEST,
    Asset.BRIDGED_BNB_TEST_USDC_ON_BFC_TEST,

    Asset.UNIFIED_BFC_ON_BFC_TEST,  # wbfc
    Asset.UNIFIED_BIFI_ON_BFC_TEST,
    Asset.UNIFIED_ETH_ON_BFC_TEST,
    Asset.UNIFIED_BNB_ON_BFC_TEST,
    Asset.UNIFIED_USDC_ON_BFC_TEST
]

ASSET_ON_ETHEREUM = [
    Asset.BFC_ON_ETH_GOERLI,
    Asset.BIFI_ON_ETH_GOERLI,
    Asset.USDC_ON_ETH_GOERLI
]

ASSET_ON_BINANCE = [
    Asset.BNB_ON_BNB_TEST,
    Asset.USDC_ON_BNB_TEST
]

SUPPORTING_ASSETS = ASSET_ON_BIFROST + ASSET_ON_ETHEREUM + ASSET_ON_BINANCE
