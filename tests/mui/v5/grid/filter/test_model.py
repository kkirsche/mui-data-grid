from typing import Any, Literal, TypeAlias, cast

from pytest import mark

from mui.v5.grid.filter.model import (
    GridFilterModel,
    Items,
    LinkOperator,
    QuickFilterLogicOperator,
    QuickFilterValues,
)
from mui.v5.grid.link.operator import GridLinkOperator

columns = "items,link_operator,quick_filter_logic_operator,quick_filter_values"
GridFilterModelTestCase: TypeAlias = tuple[
    Items | list[dict[str, Any]],
    LinkOperator | Literal["and", "or"],
    QuickFilterLogicOperator | Literal["and", "or"],
    QuickFilterValues,
]
GridFilterModelTestCases: TypeAlias = list[GridFilterModelTestCase]

valid_items: list[Items | list[dict[str, Any]]] = [
    cast(Items, []),
    [{"columnField": "id", "operatorValue": "!=", "id": 85484, "value": "1234"}],
]
valid_link_operator_values: list[LinkOperator | Literal["and", "or"]] = [
    "and",
    "or",
    GridLinkOperator.And,
    GridLinkOperator.Or,
    None,
]
valid_quick_filter_logic_operators: list[
    QuickFilterLogicOperator | Literal["and", "or"]
] = [
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
