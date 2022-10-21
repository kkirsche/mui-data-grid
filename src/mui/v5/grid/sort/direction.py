from enum import unique

from mui.compat import StrEnum


@unique
class GridSortDirection(StrEnum):
    """The direction to sort a column.

    export declare type GridSortDirection = 'asc' | 'desc' | null | undefined;
    """

    ASC = "asc"
    DESC = "desc"
