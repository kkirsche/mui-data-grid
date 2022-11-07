from typing import Optional

from pytest import mark

from mui.v5.grid import GridSortDirection, GridSortItem
from mui.v5.integrations.sqlalchemy.sort.apply_item import _get_operator


@mark.parametrize(
    "sort_direction", (GridSortDirection.ASC, GridSortDirection.DESC, None)
)
def test_get_operator(sort_direction: Optional[GridSortDirection]) -> None:
    item = GridSortItem.parse_obj({"field": "id", "sort": sort_direction})
    f = _get_operator(item=item)
    if sort_direction == GridSortDirection.ASC:
        assert f.__name__ == "asc"
    else:
        assert f.__name__ == "desc"
