from collections.abc import MutableMapping, Sequence
from typing import Any, ClassVar, TypeAlias

from pydantic import BaseModel, Field, root_validator

from mui.grid.link.operator import GridLinkOperator

_LinkOperator: TypeAlias = GridLinkOperator | None
_QuickFilterLogicOperator: TypeAlias = GridLinkOperator | None
_QuickFilterValues: TypeAlias = list[Any] | None


class GridFilterModel(BaseModel):
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

    _optional_keys: ClassVar[set[Sequence[str]]] = {
        ("linkOperator", "link_operator"),
        ("quickFilterLogicOperator", "quick_filter_logic_operator"),
        ("quickFilterValues", "quick_filter_values"),
    }

    @root_validator(pre=True)
    def ensure_optional_keys_exist(cls, haystack: object) -> object:
        """A validator that runs before validating the attribute's values.

        This validator ensures that at least one key per tuple exists if the received
        object is a mutable mapping, such as a dictionary.

        Arguments:
            haystack (object): The haystack, or incoming value, being evaluated to
                identify if it has at least one of the optional keys (needles).
                The name comes from looking for a needle in a haystack.

        Returns:
            object: The haystack, with the keys added to the mapping, if it was an
                object we could mutate.
        """
        if isinstance(haystack, MutableMapping):
            for keys in cls._optional_keys:
                found_needle = any(needle in haystack for needle in keys)
                if not found_needle:
                    key = keys[0]
                    haystack[key] = None
        return haystack

    class Config:
        allow_population_by_field_name = True
