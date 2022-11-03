from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import Query

from mui.v5.grid import GridFilterItem, GridFilterModel
from mui.v5.integrations.sqlalchemy.filter import apply_filter_to_query_from_model
from mui.v5.integrations.sqlalchemy.resolver import Resolver
from tests.conftest import ExampleModel


def test_apply_sort_to_query_from_model_single_field(
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
