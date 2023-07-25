from bridgeconst.consts import Chain, Asset

SUPPORTING_TEST_CHAINS = [Chain.BFC_TEST, Chain.ETH_GOERLI, Chain.BNB_TEST, Chain.MATIC_MUMBAI]


ASSET_ON_BFC_TEST = [
    # BFC
    Asset.BFC_ON_BFC_TEST,  # coin
    Asset.BRIDGED_ETH_GOERLI_BFC_ON_BFC_TEST,
    Asset.UNIFIED_BFC_ON_BFC_TEST,  # wbfc

    # BIFI
    Asset.BRIDGED_ETH_GOERLI_BIFI_ON_BFC_TEST,
    Asset.UNIFIED_BIFI_ON_BFC_TEST,

    # ETH
    Asset.BRIDGED_ETH_GOERLI_ETH_ON_BFC_TEST,
    Asset.UNIFIED_ETH_ON_BFC_TEST,

    # BNB
    Asset.BRIDGED_BNB_TEST_BNB_ON_BFC_TEST,
    Asset.UNIFIED_BNB_ON_BFC_TEST,

    # MATIC
    Asset.BRIDGED_MATIC_MUMBAI_MATIC_ON_BFC_TEST,
    Asset.UNIFIED_MATIC_ON_BFC_TEST,

    # USDC
    Asset.BRIDGED_BNB_TEST_USDC_ON_BFC_TEST,
    Asset.BRIDGED_ETH_GOERLI_USDC_ON_BFC_TEST,
    Asset.UNIFIED_USDC_ON_BFC_TEST,
    Asset.BRIDGED_MATIC_MUMBAI_USDC_ON_BFC_TEST,

    # USDT
    Asset.BRIDGED_ETH_GOERLI_USDT_ON_BFC_TEST,
    Asset.BRIDGED_BNB_TEST_USDT_ON_BFC_TEST,
    Asset.BRIDGED_MATIC_MUMBAI_USDT_ON_BFC_TEST,
    Asset.UNIFIED_USDT_ON_BFC_TEST,

    # SAT
    Asset.BRIDGED_ETH_GOERLI_SAT_ON_BFC_TEST,
    Asset.UNIFIED_SAT_ON_BFC_TEST,

    # WITCH
    Asset.BRIDGED_ETH_GOERLI_WITCH_ON_BFC_TEST,
    Asset.UNIFIED_WITCH_ON_BFC_TEST,

    # P2D
    Asset.BRIDGED_BNB_TEST_P2D_ON_BFC_TEST,
    Asset.UNIFIED_P2D_ON_BFC_TEST
]

ASSET_ON_ETH_GOERLI = [
    Asset.BFC_ON_ETH_GOERLI,
    Asset.BIFI_ON_ETH_GOERLI,
    Asset.ETH_ON_ETH_GOERLI,
    Asset.USDC_ON_ETH_GOERLI,
    Asset.USDT_ON_ETH_GOERLI,
    Asset.SAT_ON_ETH_GOERLI,
    Asset.WITCH_ON_ETH_GOERLI
]

ASSET_ON_BNB_TEST = [
    Asset.BNB_ON_BNB_TEST,
    Asset.USDC_ON_BNB_TEST,
    Asset.USDT_ON_BNB_TEST,
    Asset.P2D_ON_BNB_TEST
]

ASSET_ON_MATIC_MUMBAI = [
    Asset.MATIC_ON_MATIC_MUMBAI,
    Asset.USDT_ON_MATIC_MUMBAI,
    Asset.USDC_ON_MATIC_MUMBAI
]

SUPPORTING_ASSETS = ASSET_ON_BFC_TEST + ASSET_ON_ETH_GOERLI + ASSET_ON_BNB_TEST + ASSET_ON_MATIC_MUMBAI
