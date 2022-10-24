from enum import unique
from typing import Literal

from typing_extensions import TypeAlias

from mui.compat import StrEnum

GridLinkOperatorLiterals: TypeAlias = Literal["and", "or"]


@unique
class GridLinkOperator(StrEnum):
    And = "and"
    Or = "or"
