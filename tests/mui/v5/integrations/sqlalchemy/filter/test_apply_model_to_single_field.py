from datetime import timedelta

from pytest import mark
from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import Query

from mui.v5.grid import GridFilterItem, GridFilterModel
from mui.v5.integrations.sqlalchemy.filter import apply_filter_to_query_from_model
from mui.v5.integrations.sqlalchemy.resolver import Resolver
from tests.conftest import FIRST_DATE_DATETIME, ExampleModel


@mark.parametrize("operator", ("==", "equals", "is"))
def test_apply_eq_apply_filter_to_query_from_model_single_field(
    operator: str,
    query: "Query[ExampleModel]",
    resolver: Resolver,
) -> None:
    EXPECTED_ID = 300
    model = GridFilterModel.parse_obj(
        {
            "items": [
                GridFilterItem.parse_obj(
                    {
                        "column_field": "id",
                        "value": EXPECTED_ID,
                        "operator_value": operator,
                    },
                )
            ],
            "link_operator": None,  # defaults to `or_`
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    assert f"WHERE {ExampleModel.__tablename__}.id = ?" in compiled_str
    assert compiled.params["id_1"] == EXPECTED_ID

    row = filtered_query.first()
    assert row is not None
    assert row.id == EXPECTED_ID


def test_apply_is_datetime_apply_filter_to_query_from_model_single_field(
    query: "Query[ExampleModel]",
    resolver: Resolver,
) -> None:
    THIRD_DAY = FIRST_DATE_DATETIME + timedelta(days=3)
    model = GridFilterModel.parse_obj(
        {
            "items": [
                {
                    "column_field": "created_at",
                    "value": THIRD_DAY.isoformat(),
                    "operator_value": "is",
                },
            ],
            "link_operator": None,  # defaults to `or_`
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    assert f"WHERE {ExampleModel.__tablename__}.created_at = ?" in compiled_str
    assert compiled.params["created_at_1"] == THIRD_DAY

    rows = filtered_query.all()
    assert len(rows) == 1
    row = rows[0]
    assert row is not None
    assert row.created_at == THIRD_DAY.replace(tzinfo=None)


def test_apply_ne_apply_filter_to_query_from_model_single_field(
    query: "Query[ExampleModel]",
    model_count: int,
    resolver: Resolver,
) -> None:
    TARGET_ID = 300
    model = GridFilterModel.parse_obj(
        {
            "items": [
                {
                    "column_field": "id",
                    "value": TARGET_ID,
                    "operator_value": "!=",
                },
            ],
            "link_operator": None,  # defaults to `or_`
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    assert f"WHERE {ExampleModel.__tablename__}.id != ?" in compiled_str
    assert compiled.params["id_1"] == TARGET_ID

    rows = filtered_query.all()
    assert len(rows) == (model_count - 1)
    assert all(row.id != TARGET_ID for row in rows)


@mark.parametrize("operator", ("<", ">"))
def test_apply_gt_lt_apply_filter_to_query_from_model_single_field(
    operator: str,
    query: "Query[ExampleModel]",
    resolver: Resolver,
) -> None:
    TARGET_ID = 500
    model = GridFilterModel.parse_obj(
        {
            "items": [
                {
                    "column_field": "id",
                    "value": TARGET_ID,
                    "operator_value": operator,
                },
            ],
            "link_operator": None,  # defaults to `or_`
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    assert f"WHERE {ExampleModel.__tablename__}.id {operator} ?" in compiled_str
    assert compiled.params["id_1"] == TARGET_ID

    rows = filtered_query.all()
    if operator == ">":
        assert len(rows) == 500
        assert all(row.id > TARGET_ID for row in rows)  # pyright: ignore
    else:
        assert len(rows) == 499
        assert all(row.id < TARGET_ID for row in rows)  # pyright: ignore


@mark.parametrize("operator", (">=", "<="))
def test_apply_ge_le_apply_filter_to_query_from_model_single_field(
    operator: str,
    query: "Query[ExampleModel]",
    resolver: Resolver,
) -> None:
    TARGET_ID = 500
    model = GridFilterModel.parse_obj(
        {
            "items": [
                {
                    "column_field": "id",
                    "value": TARGET_ID,
                    "operator_value": operator,
                },
            ],
            "link_operator": None,  # defaults to `or_`
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    assert f"WHERE {ExampleModel.__tablename__}.id {operator} ?" in compiled_str
    assert compiled.params["id_1"] == TARGET_ID

    rows = filtered_query.all()
    row_count = len(rows)
    if operator == ">=":
        assert row_count == 501
        assert all(row.id >= TARGET_ID for row in rows)
    else:
        assert row_count == 500
        assert all(row.id <= TARGET_ID for row in rows)


@mark.parametrize("field", ("id", "null_field"))
def test_apply_is_empty_apply_filter_to_query_from_model_single_field(
    field: str,
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
                    "operator_value": "isEmpty",
                },
            ],
            "link_operator": None,  # defaults to `or_`
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    assert f"WHERE {ExampleModel.__tablename__}.{field} IS NULL" in compiled_str

    rows = filtered_query.all()
    row_count = len(rows)
    if field == "null_field":
        assert row_count == model_count
    elif field == "id":
        assert row_count == 0
    assert all(row.null_field is None for row in rows)


@mark.parametrize("field", ("id", "null_field"))
def test_apply_is_not_empty_apply_filter_to_query_from_model_single_field(
    field: str,
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
            ],
            "link_operator": None,  # defaults to `or_`
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    assert f"WHERE {ExampleModel.__tablename__}.{field} IS NOT NULL" in compiled_str

    rows = filtered_query.all()
    row_count = len(rows)
    if field == "id":
        assert row_count == model_count
    elif field == "null_field":
        assert row_count == 0
    assert all(row.null_field is None for row in rows)


def test_apply_is_any_of_apply_filter_to_query_from_model_single_field(
    query: "Query[ExampleModel]",
    resolver: Resolver,
) -> None:
    TARGET_IDS = [1, 2, 3]
    model = GridFilterModel.parse_obj(
        {
            "items": [
                {
                    "column_field": "id",
                    "value": TARGET_IDS,
                    "operator_value": "isAnyOf",
                },
            ],
            "link_operator": None,  # defaults to `or_`
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
        f"WHERE {ExampleModel.__tablename__}.id IN (__[POSTCOMPILE_id_1])"
        in compiled_str
    )
    assert compiled.params["id_1"] == [1, 2, 3]

    rows = filtered_query.all()
    assert len(rows) == len(TARGET_IDS)
    assert all(row.id in TARGET_IDS for row in rows)


def test_apply_contains_apply_filter_to_query_from_model_single_field(
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
            ],
            "link_operator": None,  # defaults to `or_`
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
    assert compiled.params["name_1"] == ExampleModel.__name__

    rows = filtered_query.all()
    assert len(rows) == model_count
    assert all(ExampleModel.__name__ in row.name for row in rows)


def test_apply_starts_with_apply_filter_to_query_from_model_single_field(
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
            ],
            "link_operator": None,  # defaults to `or_`
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
    assert compiled.params["name_1"] == ExampleModel.__name__

    rows = filtered_query.all()
    assert len(rows) == model_count
    assert all(ExampleModel.__name__ in row.name for row in rows)


def test_apply_ends_with_apply_filter_to_query_from_model_single_field(
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
            ],
            "link_operator": None,  # defaults to `or_`
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
    assert compiled.params["name_1"] == "0"

    rows = filtered_query.all()
    assert len(rows) == (model_count / 10)
    assert all(ExampleModel.__name__ in row.name for row in rows)
