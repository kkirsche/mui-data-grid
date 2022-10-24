from typing import Literal, Union, cast

from hypothesis import given
from hypothesis.strategies import builds, from_type, lists, one_of
from pytest import mark
from typing_extensions import TypeAlias

from mui.v5.grid.filter.item import GridFilterItem
from mui.v5.grid.filter.model import (
    GridFilterModel,
    Items,
    ItemsLiterals,
    LinkOperator,
    LinkOperatorLiterals,
    QuickFilterLogicOperator,
    QuickFilterLogicOperatorLiterals,
    QuickFilterValues,
)
from mui.v5.grid.link.operator import GridLinkOperator

columns = "items,link_operator,quick_filter_logic_operator,quick_filter_values"
GridFilterModelTestCase: TypeAlias = tuple[
    Items | ItemsLiterals,
    LinkOperator | LinkOperatorLiterals,
    QuickFilterLogicOperator | QuickFilterLogicOperatorLiterals,
    QuickFilterValues,
]
GridFilterModelTestCases: TypeAlias = list[GridFilterModelTestCase]
ValidItems: TypeAlias = Union[Items, ItemsLiterals]
ValidLinkOperator: TypeAlias = Union[LinkOperator, LinkOperatorLiterals]
ValidQuickFilterLogicOperator: TypeAlias = Union[LinkOperator, LinkOperatorLiterals]

valid_items: list[Items | ItemsLiterals] = [
    # contains optional keys
    [{"columnField": "id", "operatorValue": "!=", "id": 85484, "value": "1234"}],
    # missing one optional key
    [{"columnField": "id", "id": 85484, "value": "1234"}],
    [{"columnField": "id", "operatorValue": "!=", "value": "1234"}],
    # missing two optional keys
    [{"columnField": "id", "id": 85484}],
    [{"columnField": "id", "operatorValue": "!="}],
    [{"columnField": "id", "value": "1234"}],
    # missing all optional keys
    [{"columnField": "id"}],
    # empty list
    cast(Items, []),
]
valid_link_operator_values: list[LinkOperator | LinkOperatorLiterals] = [
    "and",
    "or",
    GridLinkOperator.And,
    GridLinkOperator.Or,
    None,
]
valid_quick_filter_logic_operators: list[LinkOperator | LinkOperatorLiterals] = [
    "and",
    "or",
    GridLinkOperator.And,
    GridLinkOperator.Or,
    None,
]
valid_filter_values: list[QuickFilterValues] = [[], None]


def generate_valid_test_cases() -> GridFilterModelTestCases:
    valid_test_cases: GridFilterModelTestCases = []
    for items in valid_items:
        for link_operator in valid_link_operator_values:
            for quick_filter_logic_operator in valid_quick_filter_logic_operators:
                for quick_filter_values in valid_filter_values:
                    test_case: GridFilterModelTestCase = (
                        items,
                        link_operator,
                        quick_filter_logic_operator,
                        quick_filter_values,
                    )
                    valid_test_cases.append(test_case)
    return valid_test_cases


valid_test_cases = generate_valid_test_cases()


@given(builds(GridFilterModel, items=lists(from_type(ValidItems))))
def test_valid_grid_filter_model_items(instance: GridFilterModel) -> None:
    assert isinstance(instance.items, Items)
    assert all(isinstance(item, GridFilterItem) for item in instance.items)


@given(builds(GridFilterModel, link_operator=one_of(from_type(ValidLinkOperator))))
def test_valid_grid_filter_model_link_operators(instance: GridFilterModel) -> None:
    assert isinstance(instance.link_operator, GridLinkOperator)


@given(
    builds(
        GridFilterModel,
        quick_filter_logic_operator=one_of(ValidQuickFilterLogicOperator),
    )
)
def test_valid_grid_filter_model_quick_filter_logic_operators(
    instance: GridFilterModel,
) -> None:
    assert isinstance(instance.quick_filter_logic_operator, GridLinkOperator)


@mark.parametrize(columns, valid_test_cases)
def test_valid_grid_filter_models_camel_case_parse(
    items: Items,
    link_operator: LinkOperator | Literal["asc", "desc"],
    quick_filter_logic_operator: QuickFilterLogicOperator | Literal["asc", "desc"],
    quick_filter_values: QuickFilterValues,
) -> None:
    GridFilterModel.parse_obj(
        {
            "items": items,
            "linkOperator": link_operator,
            "quickFilterLogicOperator": quick_filter_logic_operator,
            "quickFilterValues": quick_filter_values,
        }
    )


@mark.parametrize(columns, valid_test_cases)
def test_valid_grid_filter_models_camel_case_parse_missing_keys(
    items: Items,
    link_operator: LinkOperator | Literal["asc", "desc"],
    quick_filter_logic_operator: QuickFilterLogicOperator | Literal["asc", "desc"],
    quick_filter_values: QuickFilterValues,
) -> None:
    for key_tuple in GridFilterModel._optional_keys:
        for k in key_tuple:
            d = {
                "items": items,
                "linkOperator": link_operator,
                "quickFilterLogicOperator": quick_filter_logic_operator,
                "quickFilterValues": quick_filter_values,
            }
            if k in d:
                del d[k]
            GridFilterModel.parse_obj(d)


@mark.parametrize(columns, valid_test_cases)
def test_valid_grid_filter_models_snake_case_parse(
    items: Items,
    link_operator: LinkOperator | Literal["asc", "desc"],
    quick_filter_logic_operator: QuickFilterLogicOperator | Literal["asc", "desc"],
    quick_filter_values: QuickFilterValues,
) -> None:
    GridFilterModel.parse_obj(
        {
            "items": items,
            "link_operator": link_operator,
            "quick_filter_logic_operator": quick_filter_logic_operator,
            "quick_filter_values": quick_filter_values,
        }
    )


@mark.parametrize(columns, valid_test_cases)
def test_valid_grid_filter_models_snake_case_parse_missing_keys(
    items: Items,
    link_operator: LinkOperator | Literal["asc", "desc"],
    quick_filter_logic_operator: QuickFilterLogicOperator | Literal["asc", "desc"],
    quick_filter_values: QuickFilterValues,
) -> None:
    for key_tuple in GridFilterModel._optional_keys:
        for k in key_tuple:
            d = {
                "items": items,
                "link_operator": link_operator,
                "quick_filter_logic_operator": quick_filter_logic_operator,
                "quick_filter_values": quick_filter_values,
            }
            if k in d:
                del d[k]
            GridFilterModel.parse_obj(d)
