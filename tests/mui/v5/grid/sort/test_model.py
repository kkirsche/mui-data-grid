from typing import TypeAlias

from pydantic import parse_obj_as
from pytest import mark

from mui.v5.grid.sort.model import GridSortModel
from tests.mui.v5.grid.sort.test_item import generate_valid_test_cases

columns = "sort_model"
TestGridSortModel: TypeAlias = GridSortModel | list[dict[str, object]]
GridSortModelTestCase: TypeAlias = tuple[TestGridSortModel]
GridSortModelTestCases: TypeAlias = list[GridSortModelTestCase]


valid_test_cases: list[TestGridSortModel] = [
    [{"field": test_case[0], "sort": test_case[1]}]
    for test_case in generate_valid_test_cases()
]


@mark.parametrize(columns, valid_test_cases)
def test_valid_grid_sort_model_parse(
    sort_model: TestGridSortModel,
) -> None:
    parse_obj_as(GridSortModel, sort_model)
