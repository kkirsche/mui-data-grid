from typing import TypeAlias

from pytest import mark

from mui.grid.filter.item import (
    GridFilterItem,
    _ColumnField,
    _Id,
    _OperatorValue,
    _Value,
)

GridFilterModelItemTestCase: TypeAlias = tuple[
    _ColumnField, _Id, _OperatorValue, _Value
]
GridFilterItemTestCases: TypeAlias = list[GridFilterModelItemTestCase]

valid_id_types: list[_Id] = ["str", 1, None]
valid_operator_values: list[_OperatorValue] = ["str", None]
valid_values: list[_Value] = ["str", None, True, [], {}, 1, 1.1]


def generate_valid_test_cases() -> GridFilterItemTestCases:
    valid_test_cases: GridFilterItemTestCases = []
    for id_type in valid_id_types:
        for operator_value in valid_operator_values:
            for value in valid_values:
                test_case: GridFilterModelItemTestCase = (
                    "Column Field",
                    id_type,
                    operator_value,
                    value,
                )
                valid_test_cases.append(test_case)
    return valid_test_cases


valid_test_cases = generate_valid_test_cases()


@mark.parametrize("column_field,identifier,operator_value,value", valid_test_cases)
def test_valid_grid_filter_models_camel_case_parse(
    column_field: _ColumnField,
    identifier: _Id,
    operator_value: _OperatorValue,
    value: _Value,
) -> None:
    GridFilterItem.parse_obj(
        {
            "columnField": column_field,
            "id": identifier,
            "operatorValue": operator_value,
            "value": value,
        }
    )


@mark.parametrize("column_field,identifier,operator_value,value", valid_test_cases)
def test_valid_grid_filter_models_camel_case_parse_missing_keys(
    column_field: _ColumnField,
    identifier: _Id,
    operator_value: _OperatorValue,
    value: _Value,
) -> None:
    for key_tuple in GridFilterItem._optional_keys:
        for k in key_tuple:
            d = {
                "columnField": column_field,
                "id": identifier,
                "operatorValue": operator_value,
                "value": value,
            }
            if k in d:
                del d[k]
            GridFilterItem.parse_obj(d)


@mark.parametrize("column_field,identifier,operator_value,value", valid_test_cases)
def test_valid_grid_filter_models_snake_case_parse(
    column_field: _ColumnField,
    identifier: _Id,
    operator_value: _OperatorValue,
    value: _Value,
) -> None:
    GridFilterItem.parse_obj(
        {
            "column_field": column_field,
            "id": identifier,
            "operator_value": operator_value,
            "value": value,
        }
    )


@mark.parametrize("column_field,identifier,operator_value,value", valid_test_cases)
def test_valid_grid_filter_items_snake_case_parse_missing_keys(
    column_field: _ColumnField,
    identifier: _Id,
    operator_value: _OperatorValue,
    value: _Value,
) -> None:
    for key_tuple in GridFilterItem._optional_keys:
        for k in key_tuple:
            d = {
                "column_field": column_field,
                "id": identifier,
                "operator_value": operator_value,
                "value": value,
            }
            if k in d:
                del d[k]
            print("SENDING", d)
            GridFilterItem.parse_obj(d)
