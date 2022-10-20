from typing import Any, TypeAlias

from pydantic import Field

from mui.v5.grid.base import GridBaseModel
from mui.v5.grid.link.operator import GridLinkOperator

_LinkOperator: TypeAlias = GridLinkOperator | None
_QuickFilterLogicOperator: TypeAlias = GridLinkOperator | None
_QuickFilterValues: TypeAlias = list[Any] | None


class GridFilterModel(GridBaseModel):
    """A grid filter model.

    Documentation:
        https://mui.com/x/api/data-grid/grid-filter-model/

    Attributes:
        link_operator (GridLinkOperator | None | not set):
            - GridLinkOperator.And: the row must pass all the filter items.
            - GridLinkOperator.Or: the row must pass at least on filter item.
            - Alias: linkOperator
        quick_filter_logic_operator (GridLinkOperator | None | not set):
            - GridLinkOperator.And: the row must pass all the values.
            - GridLinkOperator.Or: the row must pass at least one value.
            - Alias: quickFilteringLogicOperator
        quick_filter_values (list[Any] | None | not set): values used to quick
            filter rows.
            - Alias: quickFilterValues
    """

    link_operator: _LinkOperator = Field(
        default=None,
        title="Link Operator",
        description="Whether the row row must pass all filter items.",
        alias="linkOperator",
    )
    quick_filter_logic_operator: _QuickFilterLogicOperator = Field(
        default=None,
        title="Quick Filter Logic Operator",
        description="Whether the row must pass all values or at least one value.",
        alias="quickFilterLogicOperator",
    )
    quick_filter_values: _QuickFilterValues = Field(
        default=None,
        title="Quick Filter Values",
        description="Values used to quick filter rows.",
        alias="quickFilterValues",
    )

    _optional_keys = {
        ("linkOperator", "link_operator"),
        ("quickFilterLogicOperator", "quick_filter_logic_operator"),
        ("quickFilterValues", "quick_filter_values"),
    }
