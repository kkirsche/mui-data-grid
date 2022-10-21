from pytest import mark
from typing_extensions import TypeAlias

from mui.v5.grid.filter.item import (
    ColumnField,
    GridFilterItem,
    Id,
    OperatorValue,
    Value,
)

GridFilterModelItemTestCase: TypeAlias = tuple[ColumnField, Id, OperatorValue, Value]
GridFilterItemTestCases: TypeAlias = list[GridFilterModelItemTestCase]

valid_id_types: list[Id] = ["str", 1, None]
valid_operator_values: list[OperatorValue] = ["str", None]
valid_values: list[Value] = ["str", None, True, [], {}, 1, 1.1]


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
def test_valid_grid_filter_item_camel_case_parse(
    column_field: ColumnField,
    identifier: Id,
    operator_value: OperatorValue,
    value: Value,
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
def test_valid_grid_filter_item_camel_case_parse_missing_keys(
    column_field: ColumnField,
    identifier: Id,
    operator_value: OperatorValue,
    value: Value,
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
def test_valid_grid_filter_item_snake_case_parse(
    column_field: ColumnField,
    identifier: Id,
    operator_value: OperatorValue,
    value: Value,
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
def test_valid_grid_filter_item_snake_case_parse_missing_keys(
    column_field: ColumnField,
    identifier: Id,
    operator_value: OperatorValue,
    value: Value,
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
            GridFilterItem.parse_obj(d)
