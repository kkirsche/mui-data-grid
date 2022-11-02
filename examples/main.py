#!/usr/bin/env python
"""An example script demonstrating how to use this library."""
# examples/main.py

from flask import Flask, jsonify
from flask.wrappers import Response

from mui.v5.integrations.flask import get_grid_models_from_request

app = Flask(__name__)

FILTER_MODEL_KEY = "filter_model"
SORT_MODEL_KEY = "sort_model[]"
PAGINATION_MODEL_KEY = None  # stored inline in the query string, not encoded as an obj


@app.route("/")
def print_sorted_details() -> Response:
    """This method will act as an echo server for the caller.

    Query Parameters:
        filter_model: The Material-UI Data Grid Filter Model.
        page: The current page number.
        pageSize: The size of each page.
        sort_model[]: The Material-UI Data Grid Sort Model.
    """
    models = get_grid_models_from_request(
        filter_model_key=FILTER_MODEL_KEY,
        pagination_model_key=PAGINATION_MODEL_KEY,
        sort_model_key=SORT_MODEL_KEY,
    )
    return jsonify(
        {
            # sort_model is a list[GridSortItem]
            SORT_MODEL_KEY: [model.dict() for model in models.sort_model],
            # filter_model is GridFilterModel
            FILTER_MODEL_KEY: models.filter_model.dict(),
            # pagination_model is a GridPaginationModel
            # providing a consistent interface to pagination parameters
            PAGINATION_MODEL_KEY: models.pagination_model,
        }
    )


if __name__ == "__main__":
    app.run()
