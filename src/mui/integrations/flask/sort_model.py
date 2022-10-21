"""The sort model Flask integration.

Supports parsing a GridSortModel from Flask's request.args
"""
from flask import request
from pydantic import parse_obj_as

from mui.v5.grid.sort.item import GridSortItem
from mui.v5.grid.sort.model import GridSortModel


def grid_sort_model_from_request(key: str = "sorl_model[]") -> GridSortModel:
    """Retrieves a GridSortModel from request.args.

    Args:
        key (str): The key in the request args where the sort model should be parsed
            from. Defaults to "sort_model[]".

    Raises:
        ValidationError: Raised when an invalid type was received.

    Returns:
        GridSortModel: The parsed sort model.
    """
    value = request.args.getlist(key=key, type=GridSortItem.parse_raw)
    return parse_obj_as(GridSortModel, value)
