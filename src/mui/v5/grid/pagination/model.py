"""The pagination model is designed to abstract the pagination-related data grid state.
"""
from pydantic import Field, PositiveInt

from mui.v5.grid.base import GridBaseModel


class GridPaginationModel(GridBaseModel):
    """A normalized pagination model for Material-UI's data grid.

    Attributes:
        page (int): The current page number. Defaults to 0. First page is page zero.
        page_size (int): The size of each page. Defaults to 15.
    """

    page: int = Field(
        default=0,
        title="Starting Page",
        description="The starting page number (beginning with 0).",
        gte=0,
        example=0,
    )
    page_size: PositiveInt = Field(
        default=15,
        title="Page Size",
        description="The size of each results page",
        alias="pageSize",
        example=15,
    )
