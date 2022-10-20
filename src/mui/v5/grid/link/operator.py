from enum import unique

from mui.compat import StrEnum


@unique
class GridLinkOperator(StrEnum):
    And = "and"
    Or = "or"
