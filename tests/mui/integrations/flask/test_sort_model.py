from json import dumps
from urllib.parse import quote

from flask import Flask
from pydantic import parse_obj_as
from pytest import mark

from mui.v5.grid.sort import GridSortModel
from mui.v5.integrations.flask.sort.model import get_grid_sort_model_from_request
from tests.mui.v5.grid.sort.test_model import COLUMNS, valid_test_cases

app = Flask(__name__)


@mark.parametrize(COLUMNS, valid_test_cases)
def test_sort_models(sort_model: GridSortModel | list[dict[str, object]]) -> None:
    key = "sort_model[]"
    with app.app_context():
        model = parse_obj_as(
            type_=GridSortModel,
            obj=sort_model,
        )
        json = dumps([item.dict() for item in model])
        query_str = quote(json)
        with app.test_request_context(
            path=(f"/?{key}={query_str}"),
        ):
            model = get_grid_sort_model_from_request()
