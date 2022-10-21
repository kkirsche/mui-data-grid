from flask import request
from pydantic import parse_obj_as

from mui.v5.grid.sort.item import GridSortItem
from mui.v5.grid.sort.model import GridSortModel


def grid_sort_model_from_request(key: str = "sorl_model[]") -> GridSortModel:
    """Returns a grid sort model from a Flask request."""
    value = request.args.getlist(key=key, type=GridSortItem.parse_raw)
    return parse_obj_as(GridSortModel, value)
