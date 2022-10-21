#!/usr/bin/env python
# examples/main.py

from flask import Flask, jsonify
from flask.wrappers import Response

from mui.integrations.flask import (
    grid_filter_model_from_request,
    grid_sort_model_from_request,
)

app = Flask(__name__)


@app.route("/")
def print_sorted_details() -> Response:
    sort_model = grid_sort_model_from_request(key="sort_model[]")
    filter_model = grid_filter_model_from_request(key="filter_model")
    return jsonify(
        {
            # sort_model is a list[GridSortItem]
            "sort_model[]": [model.dict() for model in sort_model],
            # filter_model is GridFilterModel
            "filter_model": filter_model.dict(),
        }
    )


if __name__ == "__main__":
    app.run()