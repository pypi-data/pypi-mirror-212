from enum import Enum
from typing import Type, Union


def from_str(obj: Type["Enum"], val: str) -> Union["Enum", None]:
    try:
        return obj(val)
    except Exception:
        """"""


def get_members(obj: Type["Enum"]) -> list[Enum]:
    return list(obj.__members__.values())
