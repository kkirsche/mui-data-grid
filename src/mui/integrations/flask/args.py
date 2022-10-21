from collections.abc import Iterable
from typing import TypeAlias, TypeVar

from pydantic import parse_obj_as, parse_raw_as

from mui.v5.grid.filter.model import (
    LinkOperator,
    QuickFilterLogicOperator,
    QuickFilterValues,
)
from mui.v5.grid.link.operator import GridLinkOperator

_T = TypeVar("_T")

FilterModel: TypeAlias = dict[str, str | list[str]]


def multi_get(model: FilterModel, keys: Iterable[str], type_: type[_T]) -> _T | None:
    result: list[str] | str | None = None
    for key in keys:
        value = model.get(key, "")
        if value != "" and result is None:
            result = value
    return (
        result
        if result is None
        else parse_obj_as(
            type_=type_,
            obj=result,
        )
    )


def multi_getlist(
    model: FilterModel, keys: Iterable[str], contained_type: type[_T]
) -> list[_T]:
    result: list[_T] = []
    for key in keys:
        value = model.get(key, [])
        if isinstance(value, list):
            result.extend(parse_raw_as(type_=contained_type, b=item) for item in value)
    return result


def get_link_operator(model: FilterModel) -> LinkOperator:
    return multi_get(
        model=model,
        keys=("linkOperator", "link_operator"),
        type_=GridLinkOperator,
    )


def get_quick_filter_logic_operator(model: FilterModel) -> QuickFilterLogicOperator:
    return multi_get(
        model=model,
        keys=("linkOperator", "link_operator"),
        type_=GridLinkOperator,
    )


def get_quick_filter_values(model: FilterModel) -> QuickFilterValues:
    return multi_getlist(
        model=model,
        keys=("quickFilterValues", "quick_filter_values"),
        contained_type=dict[str, object],
    )
