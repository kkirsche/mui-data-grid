from urllib.parse import quote

from flask import Flask
from pytest import mark

from mui.integrations.flask.filter_model import grid_filter_model_from_request
from mui.v5.grid.filter import (
    Items,
    LinkOperator,
    QuickFilterLogicOperator,
    QuickFilterValues,
)
from mui.v5.grid.filter.model import GridFilterModel
from tests.mui.v5.grid.filter.test_model import columns, generate_valid_test_cases

app = Flask(__name__)


valid_test_cases = generate_valid_test_cases()


@mark.parametrize(columns, valid_test_cases)
def test_filter_models(
    items: Items,
    link_operator: LinkOperator,
    quick_filter_logic_operator: QuickFilterLogicOperator,
    quick_filter_values: QuickFilterValues,
) -> None:
    key = "filter_model"
    with app.app_context():
        model = GridFilterModel(
            items=items,
            link_operator=link_operator,
            quick_filter_logic_operator=quick_filter_logic_operator,
            quick_filter_values=quick_filter_values,
        )
        query_str = quote(model.json())
        with app.test_request_context(
            path=(f"/?{key}={query_str}"),
        ):
            model = grid_filter_model_from_request()
