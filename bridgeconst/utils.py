import json
from enum import Enum
from typing import Union, List, TYPE_CHECKING
if TYPE_CHECKING:
    from .consts import EnumInterface


def to_even_hex(a: Union[str, int]) -> str:
    if isinstance(a, str):
        hex_value = "0x" + a if not a.startswith("0x") else a
    elif isinstance(a, int):
        hex_value = hex(a)
    else:
        raise Exception("Input with unexpected typed: {}".format(type(a)))

    return "0x0" + hex_value.replace("0x", "") if len(hex_value) % 2 == 1 else hex_value


def zero_filled_hex(a: int, a_size: int) -> str:
    limit = 2 ** (a_size << 3) - 1
    if a > limit:
        raise Exception("overflow")
    return "0x" + hex(a).replace("0x", "").zfill(a_size * 2)


def concat_hexes(*args) -> str:
    ret_hex = ""
    for arg in args:
        if ret_hex == "":
            ret_hex = to_even_hex(arg)
        else:
            ret_hex += arg.replace("0x", "")
    return ret_hex


def concat_as_hex(*args) -> str:
    hexes = list()
    for arg in args:
        if issubclass(type(arg), Enum):
            arg_hex = zero_filled_hex(arg.value, arg.size())
            hexes.append(arg_hex)
        elif isinstance(arg, int) or isinstance(arg, str):
            arg_hex = to_even_hex(arg)
            hexes.append(arg_hex)
        else:
            raise Exception("Input with unexpected typed: {}".format(type(arg)))
    return concat_hexes(*hexes)


def concat_as_int(*args) -> int:
    return int(concat_as_hex(*args), 16)


def parser(hex_str: str, element_types: List[Union[int, type]]) -> List[Union[int, type]]:
    hex_without_0x = hex_str.replace("0x", "")

    start, end = 0, 0
    elements = list()

    for _type in element_types:
        if isinstance(_type, int):
            start, end = end, end + _type * 2
            enc = lambda x: to_even_hex(x)
        elif issubclass(_type, Enum):
            start, end = end, end + _type.size() * 2
            enc = lambda x: _type(x)
        else:
            raise Exception()
        elements.append(enc(int(hex_without_0x[start:end], 16)))

    return elements
