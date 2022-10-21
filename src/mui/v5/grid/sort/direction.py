from enum import Enum, unique


@unique
class GridSortDirection(Enum):
    """The direction to sort a column.

    export declare type GridSortDirection = 'asc' | 'desc' | null | undefined;
    """

    ASC = "asc"
    DESC = "desc"
