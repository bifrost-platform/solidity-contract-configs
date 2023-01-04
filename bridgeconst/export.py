import json
from typing import List
from .consts import EnumInterface, Chain, Symbol, Asset, OPCode, RBCMethodDirection, RBCMethodV1, OracleType, Oracle, \
    OracleSourceType, ChainEventStatus


SUPPORTING_ENUMS = {
    Chain, Symbol, Asset,
    OPCode, RBCMethodDirection, RBCMethodV1,
    OracleType, OracleSourceType, Oracle,
    ChainEventStatus
}


def _generate_dict_for_index(index_type: EnumInterface):
    index_dict = {
        "bsize": index_type.size(),
        "composed": index_type.is_composed(),
        "components": index_type.components()
    }

    for idx in index_type:
        index_dict[idx.name] = idx.formatted_hex()
    return index_dict


def export_enum_json(supporting_enums: List[EnumInterface], file_path: str = None):
    enum_dict = {}
    for _enum in supporting_enums:
        enum_dict[_enum.__name__] = _generate_dict_for_index(_enum)

    if file_path is None:
        return json.dumps(enum_dict, indent=4)

    with open(file_path, "w") as f:
        json.dump(enum_dict, f, indent=4)
        print("success to export enums json")
