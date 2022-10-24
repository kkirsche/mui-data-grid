from hypothesis import given
from hyptothesis.strategies import builds
from typing_extensions import TypeAlias

from mui.v5.grid.sort.model import GridSortModel
from tests.mui.v5.grid.sort.test_item import generate_valid_test_cases

COLUMNS = "sort_model"
SortModelParameter: TypeAlias = GridSortModel | list[dict[str, object]]

GridSortModelTestCase: TypeAlias = tuple[SortModelParameter]
GridSortModelTestCases: TypeAlias = list[GridSortModelTestCase]


valid_test_cases: GridSortModelTestCases = [
    [{"field": test_case[0], "sort": test_case[1]}]
    for test_case in generate_valid_test_cases()
]


@given(builds(GridSortModel))
def test_valid_grid_sort_model_parse(instance: GridSortModel) -> None:
    assert isinstance(instance, list)
