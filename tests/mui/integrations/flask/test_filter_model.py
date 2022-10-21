from flask import Flask, request

from mui.integrations.flask.filter_model import grid_filter_model_from_request

app = Flask(__name__)


def test_filter_models() -> None:
    key = "filter_model"
    with app.app_context():
        with app.test_request_context(
            path=(
                f"/?{key}"
                + r"=%7B%22items%22:["
                + r"%7B%22columnField%22:%22id%22,%22operatorValue%22:%22!%3D%22,"
                + r"%22id%22:85484,%22value%22:%221234%22%7D]%7D"
            ),
        ):
            print(request.args)
            model = grid_filter_model_from_request()
            assert len(model.items) == 1
            assert model.link_operator is None
            assert model.quick_filter_logic_operator is None
            assert model.quick_filter_values is None
