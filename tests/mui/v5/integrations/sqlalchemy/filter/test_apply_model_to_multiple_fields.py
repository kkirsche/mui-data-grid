from datetime import timedelta
from itertools import product
from typing import Optional

from pytest import mark
from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import Query
from typing_extensions import Literal

from mui.v5.grid import GridFilterModel, GridLinkOperator
from mui.v5.integrations.sqlalchemy.filter import apply_filter_to_query_from_model
from mui.v5.integrations.sqlalchemy.resolver import Resolver
from tests.conftest import FIRST_DATE_DATETIME, ExampleModel, calculate_grouping_id

LINK_OPERATOR_ARGVALUES = (GridLinkOperator.And, GridLinkOperator.Or, None)


def _sql_link_operator_from(
    link_operator: Optional[GridLinkOperator],
) -> Literal["AND", "OR"]:
    return "AND" if link_operator == GridLinkOperator.And else "OR"


@mark.parametrize(
    argnames=("link_operator"),
    argvalues=LINK_OPERATOR_ARGVALUES,
)
def test_apply_eq_apply_filter_to_query_from_model_multiple_fields(
    link_operator: Optional[GridLinkOperator],
    query: "Query[ExampleModel]",
    resolver: Resolver,
) -> None:
    TARGET_ID = 300
    TARGET_GROUP = calculate_grouping_id(model_id=TARGET_ID)
    model = GridFilterModel.parse_obj(
        {
            "items": [
                {
                    "column_field": "id",
                    "value": TARGET_ID,
                    "operator_value": "==",
                },
                {
                    "column_field": "grouping_id",
                    "value": TARGET_GROUP,
                    "operator_value": "==",
                },
            ],
            "link_operator": link_operator,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    sql_link_operator = _sql_link_operator_from(link_operator=link_operator)
    assert f"WHERE {ExampleModel.__tablename__}.id = ?" in compiled_str
    assert (
        f"{sql_link_operator} {ExampleModel.__tablename__}.grouping_id = ?"
        in compiled_str
    )
    assert compiled.params["id_1"] == TARGET_ID
    assert compiled.params["grouping_id_1"] == TARGET_GROUP

    row = filtered_query.first()
    assert row is not None
    if link_operator == GridLinkOperator.And:
        assert row.id == TARGET_ID
        assert row.grouping_id == TARGET_GROUP
    else:
        assert row.id == TARGET_ID or row.grouping_id == TARGET_GROUP


@mark.parametrize(
    argnames=("expected_id", "link_operator"),
    argvalues=((4, GridLinkOperator.And), (1, GridLinkOperator.Or), (1, None)),
)
def test_apply_is_datetime_apply_filter_to_query_from_model_single_field(
    expected_id: int,
    link_operator: Optional[GridLinkOperator],
    query: "Query[ExampleModel]",
    resolver: Resolver,
) -> None:
    THIRD_DAY = FIRST_DATE_DATETIME + timedelta(days=3)
    # sqlite doesn't support the concept of timezones, so we get a naive datetime
    # back from the database
    ROW_THIRD_DAY = THIRD_DAY.replace(tzinfo=None)
    model = GridFilterModel.parse_obj(
        {
            "items": [
                {
                    "column_field": "created_at",
                    "value": THIRD_DAY.isoformat(),
                    "operator_value": "is",
                },
                {
                    "column_field": "id",
                    "value": expected_id,
                    "operator_value": "is",
                },
            ],
            "link_operator": link_operator,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    sql_link_operator = _sql_link_operator_from(link_operator=link_operator)
    assert f"WHERE {ExampleModel.__tablename__}.created_at = ?" in compiled_str
    assert f"{sql_link_operator} {ExampleModel.__tablename__}.id = ?" in compiled_str
    assert compiled.params["created_at_1"] == THIRD_DAY
    assert compiled.params["id_1"] == expected_id

    rows = filtered_query.all()
    if link_operator == GridLinkOperator.And:
        assert len(rows) == 1
        row = rows[0]
        assert row is not None
        assert row.id == expected_id
        assert row.created_at == ROW_THIRD_DAY
    else:
        assert len(rows) == 2
        assert all(
            row.id == expected_id or row.created_at == ROW_THIRD_DAY for row in rows
        )


@mark.parametrize(argnames=("link_operator"), argvalues=LINK_OPERATOR_ARGVALUES)
def test_apply_ne_apply_filter_to_query_from_model_multiple_fields(
    link_operator: Optional[GridLinkOperator],
    query: "Query[ExampleModel]",
    resolver: Resolver,
) -> None:
    TARGET_ID = 300
    TARGET_GROUP = calculate_grouping_id(model_id=TARGET_ID)
    model = GridFilterModel.parse_obj(
        {
            "items": [
                {
                    "column_field": "id",
                    "value": TARGET_ID,
                    "operator_value": "!=",
                },
                {
                    "column_field": "grouping_id",
                    "value": TARGET_GROUP,
                    "operator_value": "!=",
                },
            ],
            "link_operator": link_operator,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    sql_link_operator = _sql_link_operator_from(link_operator=link_operator)
    assert f"WHERE {ExampleModel.__tablename__}.id != ?" in compiled_str
    assert (
        f"{sql_link_operator} {ExampleModel.__tablename__}.grouping_id != ?"
        in compiled_str
    )
    assert compiled.params["id_1"] == TARGET_ID
    assert compiled.params["grouping_id_1"] == TARGET_GROUP

    rows = filtered_query.all()
    if link_operator == GridLinkOperator.And:
        assert len(rows) == 900
        assert all(row.id != TARGET_ID for row in rows)
        assert all(row.grouping_id != TARGET_GROUP for row in rows)
    else:
        # because it's an `OR` clause, the != id ends up being the only
        # thing that evaluates, as it has both the ID and the group, while
        # the others at least have a differing ID.
        assert len(rows) == 999
        assert all(
            row.id != TARGET_ID or row.grouping_id != TARGET_GROUP for row in rows
        )


@mark.parametrize(
    argnames=("operator", "link_operator"),
    argvalues=(tuple(product(("<", ">"), LINK_OPERATOR_ARGVALUES))),
)
def test_apply_gt_lt_apply_filter_to_query_from_model_multiple_fields(
    operator: str,
    link_operator: Optional[GridLinkOperator],
    query: "Query[ExampleModel]",
    resolver: Resolver,
) -> None:
    TARGET_ID = 500
    TARGET_GROUP = calculate_grouping_id(model_id=TARGET_ID)
    model = GridFilterModel.parse_obj(
        {
            "items": [
                {
                    "column_field": "id",
                    "value": TARGET_ID,
                    "operator_value": operator,
                },
                {
                    "column_field": "grouping_id",
                    "value": TARGET_GROUP,
                    "operator_value": operator,
                },
            ],
            "link_operator": link_operator,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    sql_link_operator = _sql_link_operator_from(link_operator=link_operator)
    assert f"WHERE {ExampleModel.__tablename__}.id {operator} ?" in compiled_str
    assert (
        f"{sql_link_operator} {ExampleModel.__tablename__}.grouping_id {operator} ?"
        in compiled_str
    )
    assert compiled.params["id_1"] == TARGET_ID
    assert compiled.params["grouping_id_1"] == TARGET_GROUP

    rows = filtered_query.all()
    if operator == ">":
        if link_operator == GridLinkOperator.And:
            assert len(rows) == 401
            assert all(row.id > TARGET_ID for row in rows)  # pyright: ignore
            assert all(
                row.grouping_id > TARGET_GROUP for row in rows
            )  # pyright: ignore
        else:
            assert len(rows) == 500
            assert all(
                row.id > TARGET_ID or row.grouping_id > TARGET_GROUP for row in rows
            )  # pyright: ignore
    else:
        assert len(rows) == 499
        if link_operator == GridLinkOperator.And:
            assert all(row.id < TARGET_ID for row in rows)  # pyright: ignore
            assert all(
                row.grouping_id < TARGET_GROUP for row in rows
            )  # pyright: ignore
        else:
            assert all(
                row.id < TARGET_ID or row.grouping_id < TARGET_GROUP for row in rows
            )  # pyright: ignore


@mark.parametrize(
    argnames=("operator", "link_operator"),
    argvalues=(tuple(product(("<=", ">="), LINK_OPERATOR_ARGVALUES))),
)
def test_apply_ge_le_apply_filter_to_query_from_model_multiple_fields(
    operator: str,
    link_operator: Optional[GridLinkOperator],
    query: "Query[ExampleModel]",
    resolver: Resolver,
) -> None:
    TARGET_ID = 500
    TARGET_GROUP = calculate_grouping_id(model_id=TARGET_ID)
    model = GridFilterModel.parse_obj(
        {
            "items": [
                {
                    "column_field": "id",
                    "value": TARGET_ID,
                    "operator_value": operator,
                },
                {
                    "column_field": "grouping_id",
                    "value": TARGET_GROUP,
                    "operator_value": operator,
                },
            ],
            "link_operator": link_operator,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    sql_link_operator = _sql_link_operator_from(link_operator=link_operator)
    assert f"WHERE {ExampleModel.__tablename__}.id {operator} ?" in compiled_str
    assert (
        f"{sql_link_operator} {ExampleModel.__tablename__}.grouping_id {operator} ?"
        in compiled_str
    )
    assert compiled.params["id_1"] == TARGET_ID
    assert compiled.params["grouping_id_1"] == TARGET_GROUP

    rows = filtered_query.all()
    row_count = len(rows)
    if operator == ">=":
        assert row_count == 501
        if link_operator == GridLinkOperator.And:
            assert all(row.id >= TARGET_ID for row in rows)
            assert all(
                row.grouping_id >= TARGET_GROUP for row in rows
            )  # pyright: ignore
        else:
            assert all(
                row.id >= TARGET_ID or row.grouping_id >= TARGET_GROUP for row in rows
            )
    else:
        if link_operator == GridLinkOperator.And:
            assert row_count == 500
            assert all(row.id <= TARGET_ID for row in rows)
            assert all(
                row.grouping_id <= TARGET_GROUP for row in rows
            )  # pyright: ignore
        else:
            assert row_count == 599
            assert all(
                row.id <= TARGET_ID or row.grouping_id <= TARGET_GROUP for row in rows
            )  # pyright: ignore


@mark.parametrize(
    argnames=("field", "link_operator"),
    argvalues=tuple(product(("id", "null_field"), LINK_OPERATOR_ARGVALUES)),
)
def test_apply_is_empty_apply_filter_to_query_from_model_multiple_fields(
    field: str,
    link_operator: Optional[GridLinkOperator],
    model_count: int,
    query: "Query[ExampleModel]",
    resolver: Resolver,
) -> None:
    model = GridFilterModel.parse_obj(
        {
            "items": [
                {
                    "column_field": field,
                    "value": None,
                    "operator_value": "isEmpty",
                },
                {
                    "column_field": "grouping_id",
                    "value": None,
                    "operatorValue": "isEmpty",
                },
            ],
            "link_operator": link_operator,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    sql_link_operator = _sql_link_operator_from(link_operator=link_operator)
    assert f"WHERE {ExampleModel.__tablename__}.{field} IS NULL" in compiled_str
    assert (
        f"{sql_link_operator} {ExampleModel.__tablename__}.grouping_id IS NULL"
        in compiled_str
    )

    rows = filtered_query.all()
    row_count = len(rows)
    if link_operator == GridLinkOperator.And:
        # always zero because grouping_id is never empty
        assert row_count == 0
        assert all(row.null_field is None for row in rows)
        assert all(row.grouping_id is None for row in rows)
    else:
        if field == "null_field":
            assert row_count == model_count
        else:
            assert row_count == 0
        assert all(row.null_field is None or row.grouping_id is None for row in rows)


@mark.parametrize(
    argnames=("field", "link_operator"),
    argvalues=tuple(product(("id", "null_field"), LINK_OPERATOR_ARGVALUES)),
)
def test_apply_is_not_empty_apply_filter_to_query_from_model_multiple_fields(
    field: str,
    link_operator: Optional[GridLinkOperator],
    query: "Query[ExampleModel]",
    model_count: int,
    resolver: Resolver,
) -> None:
    model = GridFilterModel.parse_obj(
        {
            "items": [
                {
                    "column_field": field,
                    "value": None,
                    "operator_value": "isNotEmpty",
                },
                {
                    "column_field": "grouping_id",
                    "value": None,
                    "operator_value": "isNotEmpty",
                },
            ],
            "link_operator": link_operator,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    sql_link_operator = _sql_link_operator_from(link_operator=link_operator)
    assert f"WHERE {ExampleModel.__tablename__}.{field} IS NOT NULL" in compiled_str
    assert (
        f"{sql_link_operator} {ExampleModel.__tablename__}.grouping_id IS NOT NULL"
        in compiled_str
    )

    rows = filtered_query.all()
    row_count = len(rows)
    if link_operator == GridLinkOperator.And:
        if field == "id":
            assert row_count == model_count
        elif field == "null_field":
            assert row_count == 0
        assert all(row.grouping_id is not None for row in rows)
    else:
        # Or branch
        assert row_count == model_count
        assert all(
            row.null_field is not None or row.grouping_id is not None for row in rows
        )


@mark.parametrize(argnames=("link_operator"), argvalues=(LINK_OPERATOR_ARGVALUES))
def test_apply_is_any_of_apply_filter_to_query_from_model_multiple_fields(
    link_operator: Optional[GridLinkOperator],
    query: "Query[ExampleModel]",
    resolver: Resolver,
) -> None:
    TARGET_IDS = [1, 2, 3]
    TARGET_GROUPS = list(
        {calculate_grouping_id(model_id=TARGET_ID) for TARGET_ID in TARGET_IDS}
    )

    model = GridFilterModel.parse_obj(
        {
            "items": [
                {
                    "column_field": "id",
                    "value": TARGET_IDS,
                    "operator_value": "isAnyOf",
                },
                {
                    "column_field": "grouping_id",
                    "value": TARGET_GROUPS,
                    "operator_value": "isAnyOf",
                },
            ],
            "link_operator": link_operator,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    sql_link_operator = _sql_link_operator_from(link_operator=link_operator)
    assert (
        f"WHERE {ExampleModel.__tablename__}.id IN (__[POSTCOMPILE_id_1])"
        in compiled_str
    )
    assert (
        f"{sql_link_operator} {ExampleModel.__tablename__}.grouping_id IN "
        + "(__[POSTCOMPILE_grouping_id_1])"
        in compiled_str
    )
    assert compiled.params["id_1"] == [1, 2, 3]
    assert compiled.params["grouping_id_1"] == [0]

    rows = filtered_query.all()
    if link_operator == GridLinkOperator.And:
        assert len(rows) == len(TARGET_IDS)
        assert all(row.id in TARGET_IDS for row in rows)
        assert all(row.grouping_id in TARGET_GROUPS for row in rows)
    else:
        assert len(rows) == 99
        assert all(
            row.id in TARGET_IDS or row.grouping_id in TARGET_GROUPS for row in rows
        )


def test_apply_contains_apply_filter_to_query_from_model_multiple_fields(
    query: "Query[ExampleModel]",
    model_count: int,
    resolver: Resolver,
) -> None:
    model = GridFilterModel.parse_obj(
        {
            "items": [
                {
                    "column_field": "name",
                    "value": ExampleModel.__name__,
                    "operator_value": "contains",
                },
                {
                    "column_field": "grouping_id",
                    "value": 0,
                    "operator_value": "contains",
                },
            ],
            "link_operator": GridLinkOperator.And,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    assert (
        f"WHERE ({ExampleModel.__tablename__}.name LIKE '%' || ? || '%')"
        in compiled_str
    )
    assert (
        f"AND ({ExampleModel.__tablename__}.grouping_id LIKE '%' || ? || '%')"
        in compiled_str
    )
    assert compiled.params["name_1"] == ExampleModel.__name__
    assert compiled.params["grouping_id_1"] == 0

    rows = filtered_query.all()
    assert len(rows) == model_count / 10
    assert all(ExampleModel.__name__ in row.name for row in rows)
    assert all("0" in str(row.grouping_id) for row in rows)


def test_apply_starts_with_apply_filter_to_query_from_model_multiple_fields(
    query: "Query[ExampleModel]",
    model_count: int,
    resolver: Resolver,
) -> None:
    model = GridFilterModel.parse_obj(
        {
            "items": [
                {
                    "column_field": "name",
                    "value": ExampleModel.__name__,
                    "operator_value": "startsWith",
                },
                {
                    "column_field": "grouping_id",
                    "value": 0,
                    "operator_value": "startsWith",
                },
            ],
            "link_operator": GridLinkOperator.And,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    assert f"WHERE ({ExampleModel.__tablename__}.name LIKE ? || '%')" in compiled_str
    assert (
        f"AND ({ExampleModel.__tablename__}.grouping_id LIKE ? || '%')" in compiled_str
    )
    assert compiled.params["name_1"] == ExampleModel.__name__
    assert compiled.params["grouping_id_1"] == 0

    rows = filtered_query.all()
    groups = model_count / 10
    assert len(rows) == (groups - 1)
    assert all(ExampleModel.__name__ in row.name for row in rows)
    assert all(str(row.grouping_id).startswith("0") for row in rows)


def test_apply_ends_with_apply_filter_to_query_from_model_multiple_fields(
    query: "Query[ExampleModel]",
    model_count: int,
    resolver: Resolver,
) -> None:
    model = GridFilterModel.parse_obj(
        {
            "items": [
                {
                    "column_field": "name",
                    "value": "0",
                    "operator_value": "endsWith",
                },
                {
                    "column_field": "grouping_id",
                    "value": "0",
                    "operator_value": "endsWith",
                },
            ],
            "link_operator": GridLinkOperator.And,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    assert f"WHERE ({ExampleModel.__tablename__}.name LIKE '%' || ?)" in compiled_str
    assert (
        f"AND ({ExampleModel.__tablename__}.grouping_id LIKE '%' || ?)" in compiled_str
    )
    assert compiled.params["name_1"] == "0"
    assert compiled.params["grouping_id_1"] == "0"

    rows = filtered_query.all()
    assert len(rows) == 10
    assert all(ExampleModel.__name__ in row.name for row in rows)
    assert all(str(row.grouping_id).endswith("0") for row in rows)
