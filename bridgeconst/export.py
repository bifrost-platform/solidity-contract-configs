import json
from .consts import EnumInterface, SUPPORTING_ENUMS


def _generate_dict_for_index(index_type: EnumInterface):
    index_dict = {
        "bsize": index_type.size(),
        "composed": index_type.is_composed(),
        "components": index_type.components()
    }

    for idx in index_type:
        index_dict[idx.name] = idx.formatted_hex()
    return index_dict


def export_enum_json(file_path: str = None):
    enum_dict = {}
    for _enum in SUPPORTING_ENUMS:
        enum_dict[_enum.__name__] = _generate_dict_for_index(_enum)

    if file_path is None:
        return json.dumps(enum_dict, indent=4)

    with open(file_path, "w") as f:
        json.dump(enum_dict, f, indent=4)
        print("success to export enums json")
