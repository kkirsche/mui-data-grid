from typing import Literal, Union

from pytest import mark
from typing_extensions import TypeAlias

from mui.v5.grid.sort.direction import GridSortDirection
from mui.v5.grid.sort.item import Field, GridSortItem, Sort

SortTest: TypeAlias = Union[Sort, Literal["asc", "desc"]]
GridSortModelItemTestCase: TypeAlias = tuple[Field, SortTest]
GridSortItemTestCases: TypeAlias = list[GridSortModelItemTestCase]
COLUMNS = "field,sort"


valid_field_values: list[Field] = ["field1", "field2.nested_field3"]
valid_sort_values: list[SortTest] = [
    "asc",
    "desc",
    GridSortDirection.ASC,
    GridSortDirection.DESC,
    None,
]


def generate_valid_test_cases() -> GridSortItemTestCases:
    valid_test_cases: GridSortItemTestCases = []
    for field in valid_field_values:
        for sort in valid_sort_values:
            test_case: GridSortModelItemTestCase = (field, sort)
            valid_test_cases.append(test_case)
    return valid_test_cases


valid_test_cases = generate_valid_test_cases()


@mark.parametrize(COLUMNS, valid_test_cases)
def test_valid_grid_sort_item_parse(field: Field, sort: SortTest) -> None:
    GridSortItem.parse_obj(
        {
            "field": field,
            "sort": sort,
        }
    )


@mark.parametrize(COLUMNS, valid_test_cases)
def test_valid_grid_sort_item_parse_missing_keys(field: Field, sort: SortTest) -> None:
    for key_tuple in GridSortItem._optional_keys:
        for k in key_tuple:
            d = {
                "field": field,
                "sort": sort,
            }
            if k in d:
                del d[k]
            GridSortItem.parse_obj(d)
