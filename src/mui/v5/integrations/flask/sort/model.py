"""The sort model Flask integration.

Supports parsing a GridSortModel from Flask's request.args
"""
from flask import request
from pydantic import parse_obj_as

from mui.v5.grid.sort import GridSortItem, GridSortModel


def get_grid_sort_model_from_request(key: str = "sorl_model[]") -> GridSortModel:
    """Retrieves a GridSortModel from request.args.

    Args:
        key (str): The key in the request args where the sort model should be parsed
            from. Defaults to "sort_model[]".

    Raises:
        ValidationError: Raised when an invalid type was received.

    Returns:
        GridSortModel: The parsed sort model.
    """
    # getlist returns [] as a default when the key doesn't exist
    # https://github.com/pallets/werkzeug/blob/main/src/werkzeug/datastructures.py#L395
    value = request.args.getlist(key=key, type=GridSortItem.parse_raw)
    return parse_obj_as(GridSortModel, value)
