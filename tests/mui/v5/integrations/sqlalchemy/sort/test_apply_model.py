from pytest import mark
from sqlalchemy.orm import Query

from mui.v5.grid import GridSortDirection, GridSortItem, GridSortModel
from mui.v5.integrations.sqlalchemy.resolver import Resolver
from mui.v5.integrations.sqlalchemy.sort import apply_sort_to_query_from_model
from tests.conftest import RESOLVABLE_FIELDS, ExampleModel


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
            assert prev_row.id < current_row.id
        elif item.sort in {GridSortDirection.DESC, None}:
            # None defaults the operator to DESC
            # see src/mui/v5/integrations/sqlalchemy/sort/apply_item.py:_get_operator
            # for more details.
            assert prev_row.id > current_row.id


@mark.parametrize(
    "direction",
    (
        GridSortDirection.ASC,
        GridSortDirection.DESC,
        None,
    ),
)
def test_apply_sort_to_query_from_model_multiple_fields(
    direction: GridSortDirection,
    query: "Query[ExampleModel]",
    resolver: Resolver,
) -> None:
    # order matters with how we're using the fields!
    model: GridSortModel = [
        GridSortItem(field="grouping_id", sort=direction),
        GridSortItem(field="id", sort=direction),
    ]
    for item in model:
        assert item.field in RESOLVABLE_FIELDS

    sorted_results = apply_sort_to_query_from_model(
        query=query, model=model, resolver=resolver
    ).all()
    assert len(sorted_results) > 0

    for i, current_row in enumerate(sorted_results[1:]):
        prev_row = sorted_results[i]
        if direction == GridSortDirection.ASC:
            assert prev_row.id < current_row.id
            if prev_row.grouping_id != current_row.grouping_id:
                assert prev_row.grouping_id < current_row.grouping_id
        elif direction in {GridSortDirection.DESC, None}:
            # None defaults the operator to DESC
            # see src/mui/v5/integrations/sqlalchemy/sort/apply_item.py:_get_operator
            # for more details.
            assert prev_row.id > current_row.id
            if prev_row.grouping_id != current_row.grouping_id:
                assert prev_row.grouping_id > current_row.grouping_id
