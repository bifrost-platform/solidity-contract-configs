import argparse
import sys

from bridgeconst.export import export_enum_json

parser = argparse.ArgumentParser(description="bridge enum exporter")
parser.add_argument("-p", "--path", type=str, help="insert configuration directory")

DEFAULT_ENUM_JSON_PATH = "./enums.json"


if __name__ == "__main__":
    if not sys.argv[1:]:
        _path = DEFAULT_ENUM_JSON_PATH
    else:
        args = parser.parse_args()
        config = vars(args)["path"]
        _path = DEFAULT_ENUM_JSON_PATH if config.get("path") is None else config["path"]
    export_enum_json(_path)
