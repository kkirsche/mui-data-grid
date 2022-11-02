from pytest import mark
from sqlalchemy.orm import Query

from mui.v5.grid import GridSortDirection, GridSortItem, GridSortModel
from mui.v5.integrations.sqlalchemy.resolver import Resolver
from mui.v5.integrations.sqlalchemy.sort import apply_sort_to_query_from_model
from tests.conftest import RESOLVABLE_FIELDS, ExampleModel


def _assert_desc_order(
    last_model: ExampleModel, next_model: ExampleModel, key: str
) -> None:
    assert hasattr(last_model, key)
    assert hasattr(next_model, key)
    assert getattr(last_model, key) > getattr(next_model, key)


def _assert_asc_order(
    last_model: ExampleModel, next_model: ExampleModel, key: str
) -> None:
    assert hasattr(last_model, key)
    assert hasattr(next_model, key)
    assert getattr(last_model, key) < getattr(next_model, key)


@mark.parametrize("direction", (GridSortDirection.ASC, GridSortDirection.DESC, None))
def test_apply_sort_to_query_from_model_single_field(
    direction: GridSortDirection,
    query: "Query[ExampleModel]",
    resolver: Resolver,
) -> None:
    item = GridSortItem(field="id", sort=direction)
    assert item.field in RESOLVABLE_FIELDS
    model: GridSortModel = [item]
    sorted_results = apply_sort_to_query_from_model(
        query=query, model=model, resolver=resolver
    ).all()
    assert len(sorted_results) > 0

    for i, current_row in enumerate(sorted_results[1:]):
        prev_row = sorted_results[i]
        if item.sort == GridSortDirection.ASC:
            _assert_asc_order(
                last_model=prev_row, next_model=current_row, key=item.field
            )
        elif item.sort == GridSortDirection.DESC or item.sort is None:
            # None defaults the operator to DESC
            # see src/mui/v5/integrations/sqlalchemy/sort/apply_item.py:_get_operator
            # for more details.
            _assert_desc_order(
                last_model=prev_row, next_model=current_row, key=item.field
            )
