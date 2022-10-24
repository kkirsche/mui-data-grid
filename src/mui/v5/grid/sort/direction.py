from enum import unique
from typing import Literal

from typing_extensions import TypeAlias

from mui.compat import StrEnum

GridSortDirectionLiterals: TypeAlias = Literal["asc", "desc"]


@unique
class GridSortDirection(StrEnum):
    """The direction to sort a column.

    export declare type GridSortDirection = 'asc' | 'desc' | null | undefined;
    """

    ASC = "asc"
    DESC = "desc"
