from pytest import mark
from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import Query

from mui.v5.grid import GridFilterItem, GridFilterModel
from mui.v5.integrations.sqlalchemy.filter import apply_filter_to_query_from_model
from mui.v5.integrations.sqlalchemy.resolver import Resolver
from tests.conftest import ExampleModel


def test_apply_eq_sort_to_query_from_model_single_field(
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
                        "operator_value": "==",
                    },
                )
            ],
            "link_operator": None,
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
    assert compiled.params["id_1"] == EXPECTED_ID

    row = sorted_query.first()
    assert row is not None
    assert row.id == EXPECTED_ID


def test_apply_ne_sort_to_query_from_model_single_field(
    query: "Query[ExampleModel]",
    model_count: int,
    resolver: Resolver,
) -> None:
    TARGET_ID = 300
    model = GridFilterModel.parse_obj(
        {
            "items": [
                GridFilterItem.parse_obj(
                    {
                        "column_field": "id",
                        "value": TARGET_ID,
                        "operator_value": "!=",
                    },
                )
            ],
            "link_operator": None,
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
    assert compiled.params["id_1"] == TARGET_ID

    rows = sorted_query.all()
    assert len(rows) == (model_count - 1)
    assert all(row.id != TARGET_ID for row in rows)


@mark.parametrize("operator", ("<", ">"))
def test_apply_gt_lt_sort_to_query_from_model_single_field(
    operator: str,
    query: "Query[ExampleModel]",
    resolver: Resolver,
) -> None:
    TARGET_ID = 500
    model = GridFilterModel.parse_obj(
        {
            "items": [
                GridFilterItem.parse_obj(
                    {
                        "column_field": "id",
                        "value": TARGET_ID,
                        "operator_value": operator,
                    },
                )
            ],
            "link_operator": None,
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
    assert compiled.params["id_1"] == TARGET_ID

    rows = sorted_query.all()
    if operator == ">":
        assert len(rows) == 500
        assert all(row.id > TARGET_ID for row in rows)
    else:
        assert len(rows) == 499
        assert all(row.id < TARGET_ID for row in rows)


@mark.parametrize("operator", (">=", "<="))
def test_apply_ge_le_sort_to_query_from_model_single_field(
    operator: str,
    query: "Query[ExampleModel]",
    resolver: Resolver,
) -> None:
    TARGET_ID = 500
    model = GridFilterModel.parse_obj(
        {
            "items": [
                GridFilterItem.parse_obj(
                    {
                        "column_field": "id",
                        "value": TARGET_ID,
                        "operator_value": operator,
                    },
                )
            ],
            "link_operator": None,
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
    assert compiled.params["id_1"] == TARGET_ID

    rows = sorted_query.all()
    row_count = len(rows)
    if operator == ">=":
        assert row_count == 501
        assert all(row.id >= TARGET_ID for row in rows)
    else:
        assert row_count == 500
        assert all(row.id <= TARGET_ID for row in rows)


def test_apply_is_empty_sort_to_query_from_model_single_field(
    query: "Query[ExampleModel]",
    model_count: int,
    resolver: Resolver,
) -> None:
    model = GridFilterModel.parse_obj(
        {
            "items": [
                GridFilterItem.parse_obj(
                    {
                        "column_field": "null_field",
                        "value": None,
                        "operator_value": "isEmpty",
                    },
                )
            ],
            "link_operator": None,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    sorted_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = sorted_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    assert f"WHERE {ExampleModel.__tablename__}.null_field IS NULL" in compiled_str

    rows = sorted_query.all()
    assert len(rows) == model_count
    assert all(row.null_field is None for row in rows)
