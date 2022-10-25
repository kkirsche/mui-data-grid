from enum import Enum
from typing import Any, List, Tuple


class StrEnum(str, Enum):
    """Enum where members are also (and must be) strings

    Backport of Python 3.11 feature

    Taken at:
    https://github.com/python/cpython/blob/b44372e03c5461b6ad3d89763a9eb6cb82df07a4/Lib/enum.py#L1221

    Future?:
    https://github.com/python/cpython/blob/main/Lib/enum.py#L1221
    """

    def __new__(cls, *values: Tuple[str, ...]) -> "StrEnum":
        "values must already be of type `str`"
        if len(values) > 3:
            raise TypeError("too many arguments for str(): {!r}".format(values))
        if len(values) == 1 and not isinstance(values[0], str):
            raise TypeError("{!r} is not a string".format(values[0]))
        if len(values) >= 2 and not isinstance(values[1], str):
            raise TypeError("encoding must be a string, not {!r}".format(values[1]))
        if len(values) == 3 and not isinstance(values[2], str):
            raise TypeError("errors must be a string, not {!r}".format(values[2]))
        value = str(*values)
        member = str.__new__(cls, value)
        member._value_ = value
        return member

    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: List[Any]
    ) -> Any:
        """Return the lower-cased version of the member name."""
        return name.lower()
