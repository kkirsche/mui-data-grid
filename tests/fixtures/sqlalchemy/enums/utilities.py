from typing import List, Type

from mui.compat import StrEnum


def values_callable(enum: Type[StrEnum]) -> List[str]:
    return [member.value for member in enum]
