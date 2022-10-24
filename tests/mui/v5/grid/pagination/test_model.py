from hypothesis import given
from hypothesis.strategies import builds

from mui.v5.grid import GridPaginationModel


@given(builds(GridPaginationModel))
def test_valid_grid_pagination_model_parse(instance: GridPaginationModel) -> None:
    assert instance.page >= 0
    assert instance.page_size >= 1
