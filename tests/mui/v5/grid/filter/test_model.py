from typing import TypeAlias

from pytest import mark

from mui.v5.grid.filter.model import (
    GridFilterModel,
    _LinkOperator,
    _QuickFilterLogicOperator,
    _QuickFilterValues,
)
from mui.v5.grid.link.operator import GridLinkOperator

GridFilterModelTestCase: TypeAlias = tuple[
    _LinkOperator, _QuickFilterLogicOperator, _QuickFilterValues
]
GridFilterModelTestCases: TypeAlias = list[GridFilterModelTestCase]

valid_filter_values: list[_QuickFilterValues] = [[], None]


def generate_valid_test_cases() -> GridFilterModelTestCases:
    valid_test_cases: GridFilterModelTestCases = []
    for link_operator in [GridLinkOperator.And, GridLinkOperator.Or, None]:
        for quick_filter_logic_operator in [
            GridLinkOperator.And,
            GridLinkOperator.Or,
            None,
        ]:
            for quick_filter_values in valid_filter_values:
                test_case: GridFilterModelTestCase = (
                    link_operator,
                    quick_filter_logic_operator,
                    quick_filter_values,
                )
                valid_test_cases.append(test_case)
    return valid_test_cases


valid_test_cases = generate_valid_test_cases()


@mark.parametrize(
    "link_operator,quick_filter_logic_operator,quick_filter_values", valid_test_cases
)
def test_valid_grid_filter_models_camel_case_parse(
    link_operator: _LinkOperator,
    quick_filter_logic_operator: _QuickFilterLogicOperator,
    quick_filter_values: _QuickFilterValues,
) -> None:
    GridFilterModel.parse_obj(
        {
            "linkOperator": link_operator,
            "quickFilterLogicOperator": quick_filter_logic_operator,
            "quickFilterValues": quick_filter_values,
        }
    )


@mark.parametrize(
    "link_operator,quick_filter_logic_operator,quick_filter_values", valid_test_cases
)
def test_valid_grid_filter_models_camel_case_parse_missing_keys(
    link_operator: _LinkOperator,
    quick_filter_logic_operator: _QuickFilterLogicOperator,
    quick_filter_values: _QuickFilterValues,
) -> None:
    for key_tuple in GridFilterModel._optional_keys:
        for k in key_tuple:
            d = {
                "linkOperator": link_operator,
                "quickFilterLogicOperator": quick_filter_logic_operator,
                "quickFilterValues": quick_filter_values,
            }
            if k in d:
                del d[k]
            GridFilterModel.parse_obj(d)


@mark.parametrize(
    "link_operator,quick_filter_logic_operator,quick_filter_values", valid_test_cases
)
def test_valid_grid_filter_models_snake_case_parse(
    link_operator: _LinkOperator,
    quick_filter_logic_operator: _QuickFilterLogicOperator,
    quick_filter_values: _QuickFilterValues,
) -> None:
    GridFilterModel.parse_obj(
        {
            "link_operator": link_operator,
            "quick_filter_logic_operator": quick_filter_logic_operator,
            "quick_filter_values": quick_filter_values,
        }
    )


@mark.parametrize(
    "link_operator,quick_filter_logic_operator,quick_filter_values", valid_test_cases
)
def test_valid_grid_filter_models_snake_case_parse_missing_keys(
    link_operator: _LinkOperator,
    quick_filter_logic_operator: _QuickFilterLogicOperator,
    quick_filter_values: _QuickFilterValues,
) -> None:
    for key_tuple in GridFilterModel._optional_keys:
        for k in key_tuple:
            d = {
                "link_operator": link_operator,
                "quick_filter_logic_operator": quick_filter_logic_operator,
                "quick_filter_values": quick_filter_values,
            }
            if k in d:
                del d[k]
            GridFilterModel.parse_obj(d)
