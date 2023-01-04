import argparse
import json
import sys

from bridgeconst.consts import Chain, Symbol, Asset, OPCode, RBCMethodDirection, RBCMethodV1, OracleType, \
    OracleSourceType, Oracle, ChainEventStatus

parser = argparse.ArgumentParser(description="bridge enum exporter")
parser.add_argument("-p", "--path", type=str, help="insert configuration directory")

DEFAULT_ENUM_JSON_PATH = "./enums.json"


SUPPORTING_ENUMS = [
    Chain, Symbol, Asset,
    OPCode, RBCMethodDirection, RBCMethodV1,
    OracleType, OracleSourceType, Oracle,
    ChainEventStatus
]


def generate_dict_for_index(index_type):
    index_dict = {
        "bsize": index_type.size(),
        "composed": index_type.is_composed(),
        "components": index_type.components()
    }

    for idx in index_type:
        index_dict[idx.name] = idx.formatted_hex()
    return index_dict


def main(file_path: str):
    enum_dict = {}
    for _enum in SUPPORTING_ENUMS:
        enum_dict[_enum.__name__] = generate_dict_for_index(_enum)

    with open(file_path, "w") as f:
        json.dump(enum_dict, f, indent=4)
        print("success to export enums json")


if __name__ == "__main__":
    if not sys.argv[1:]:
        _path = DEFAULT_ENUM_JSON_PATH
    else:
        args = parser.parse_args()
        config = vars(args)["path"]
        _path = DEFAULT_ENUM_JSON_PATH if config.get("path") is None else config["path"]
    main(_path)
