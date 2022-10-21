from collections.abc import Sequence
from typing import ClassVar, TypeAlias

from pydantic import Field

from mui.v5.grid.base import GridBaseModel
from mui.v5.grid.sort.direction import GridSortDirection

_Field: TypeAlias = str
_Sort: TypeAlias = GridSortDirection | None


class GridSortItem(GridBaseModel):
    """Object that represents the column sorted data, part of the GridSortModel.

    Documentation:
        N/A

    Code:
        https://github.com/mui/mui-x/blob/0cdee3369bbf6df792c9228ef55ea1a61a246ff3/packages/grid/x-data-grid/src/models/gridSortModel.ts#L27-L39

    Attributes:
        field (str): The column field identifier.
        sort (GridSortDirection): The direction of the column that the grid should sort.
    """

    field: _Field = Field(
        default=...,
        title="Field",
        description="The direction of the column that the grid should sort.",
    )

    sort: _Sort = Field(
        default=...,
        title="Sort",
        description="The direction of the column that the grid should sort.",
    )

    _optional_keys: ClassVar[set[Sequence[str]]] = set()
