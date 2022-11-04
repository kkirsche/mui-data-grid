from pytest import mark
from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import Query

from mui.v5.grid import GridFilterItem, GridFilterModel, GridLinkOperator
from mui.v5.integrations.sqlalchemy.filter import apply_filter_to_query_from_model
from mui.v5.integrations.sqlalchemy.resolver import Resolver
from tests.conftest import ExampleModel, calculate_grouping_id


def test_apply_eq_apply_filter_to_query_from_model_multiple_fields(
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
            "link_operator": GridLinkOperator.And,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    sorted_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = sorted_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    assert f"WHERE {ExampleModel.__tablename__}.id = ?" in compiled_str
    assert f"AND {ExampleModel.__tablename__}.grouping_id = ?" in compiled_str
    assert compiled.params["id_1"] == TARGET_ID
    assert compiled.params["grouping_id_1"] == TARGET_GROUP

    row = sorted_query.first()
    assert row is not None
    assert row.id == TARGET_ID
    assert row.grouping_id == TARGET_GROUP


def test_apply_ne_apply_filter_to_query_from_model_multiple_fields(
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
            "link_operator": GridLinkOperator.And,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    sorted_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = sorted_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    assert f"WHERE {ExampleModel.__tablename__}.id != ?" in compiled_str
    assert f"AND {ExampleModel.__tablename__}.grouping_id != ?" in compiled_str
    assert compiled.params["id_1"] == TARGET_ID
    assert compiled.params["grouping_id_1"] == TARGET_GROUP

    rows = sorted_query.all()
    assert len(rows) == 900
    assert all(row.id != TARGET_ID for row in rows)
    assert all(row.grouping_id != TARGET_GROUP for row in rows)


@mark.parametrize("operator", ("<", ">"))
def test_apply_gt_lt_apply_filter_to_query_from_model_multiple_fields(
    operator: str,
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
            "link_operator": GridLinkOperator.And,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    sorted_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = sorted_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    assert f"WHERE {ExampleModel.__tablename__}.id {operator} ?" in compiled_str
    assert f"AND {ExampleModel.__tablename__}.grouping_id {operator} ?" in compiled_str
    assert compiled.params["id_1"] == TARGET_ID
    assert compiled.params["grouping_id_1"] == TARGET_GROUP

    rows = sorted_query.all()
    if operator == ">":
        assert len(rows) == 401
        assert all(row.id > TARGET_ID for row in rows)  # pyright: ignore
        assert all(row.grouping_id > TARGET_GROUP for row in rows)  # pyright: ignore
    else:
        assert len(rows) == 499
        assert all(row.id < TARGET_ID for row in rows)  # pyright: ignore
        assert all(row.grouping_id < TARGET_GROUP for row in rows)  # pyright: ignore


@mark.parametrize("operator", (">=", "<="))
def test_apply_ge_le_apply_filter_to_query_from_model_multiple_fields(
    operator: str,
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
            "link_operator": GridLinkOperator.And,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    sorted_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = sorted_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    assert f"WHERE {ExampleModel.__tablename__}.id {operator} ?" in compiled_str
    assert f"AND {ExampleModel.__tablename__}.grouping_id {operator} ?" in compiled_str
    assert compiled.params["id_1"] == TARGET_ID
    assert compiled.params["grouping_id_1"] == TARGET_GROUP

    rows = sorted_query.all()
    row_count = len(rows)
    if operator == ">=":
        assert row_count == 501
        assert all(row.id >= TARGET_ID for row in rows)
        assert all(row.grouping_id >= TARGET_GROUP for row in rows)  # pyright: ignore
    else:
        assert row_count == 500
        assert all(row.id <= TARGET_ID for row in rows)
        assert all(row.grouping_id <= TARGET_GROUP for row in rows)  # pyright: ignore


@mark.parametrize("field", ("id", "null_field"))
def test_apply_is_empty_apply_filter_to_query_from_model_multiple_fields(
    field: str,
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
            "link_operator": GridLinkOperator.And,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    sorted_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = sorted_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    assert f"WHERE {ExampleModel.__tablename__}.{field} IS NULL" in compiled_str
    assert f"AND {ExampleModel.__tablename__}.grouping_id IS NULL" in compiled_str

    rows = sorted_query.all()
    row_count = len(rows)
    # always zero because grouping_id is never empty
    assert row_count == 0
    assert all(row.null_field is None for row in rows)
    assert all(row.grouping_id is None for row in rows)


@mark.parametrize("field", ("id", "null_field"))
def test_apply_is_not_empty_apply_filter_to_query_from_model_multiple_fields(
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
                {
                    "column_field": "grouping_id",
                    "value": None,
                    "operator_value": "isNotEmpty",
                },
            ],
            "link_operator": GridLinkOperator.And,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    sorted_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = sorted_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    assert f"WHERE {ExampleModel.__tablename__}.{field} IS NOT NULL" in compiled_str
    assert f"AND {ExampleModel.__tablename__}.grouping_id IS NOT NULL" in compiled_str

    rows = sorted_query.all()
    row_count = len(rows)
    if field == "id":
        assert row_count == model_count
    elif field == "null_field":
        assert row_count == 0
    assert all(row.null_field is None for row in rows)
    assert all(row.grouping_id is not None for row in rows)


def test_apply_is_any_of_apply_filter_to_query_from_model_multiple_fields(
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
            "link_operator": GridLinkOperator.And,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    sorted_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = sorted_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    assert (
        f"WHERE {ExampleModel.__tablename__}.id IN (__[POSTCOMPILE_id_1])"
        in compiled_str
    )
    assert (
        f"AND {ExampleModel.__tablename__}.grouping_id IN (__[POSTCOMPILE_grouping_id_1])"  # noqa
        in compiled_str
    )
    assert compiled.params["id_1"] == [1, 2, 3]
    assert compiled.params["grouping_id_1"] == [0]

    rows = sorted_query.all()
    assert len(rows) == len(TARGET_IDS)
    assert all(row.id in TARGET_IDS for row in rows)
    assert all(row.grouping_id in TARGET_GROUPS for row in rows)


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
    sorted_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = sorted_query.statement.compile(dialect=sqlite.dialect())
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

    rows = sorted_query.all()
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
    sorted_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = sorted_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    assert f"WHERE ({ExampleModel.__tablename__}.name LIKE ? || '%')" in compiled_str
    assert (
        f"AND ({ExampleModel.__tablename__}.grouping_id LIKE ? || '%')" in compiled_str
    )
    assert compiled.params["name_1"] == ExampleModel.__name__
    assert compiled.params["grouping_id_1"] == 0

    rows = sorted_query.all()
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
    sorted_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = sorted_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    assert f"WHERE ({ExampleModel.__tablename__}.name LIKE '%' || ?)" in compiled_str
    assert (
        f"AND ({ExampleModel.__tablename__}.grouping_id LIKE '%' || ?)" in compiled_str
    )
    assert compiled.params["name_1"] == "0"
    assert compiled.params["grouping_id_1"] == "0"

    rows = sorted_query.all()
    assert len(rows) == 10
    assert all(ExampleModel.__name__ in row.name for row in rows)
    assert all(str(row.grouping_id).endswith("0") for row in rows)
