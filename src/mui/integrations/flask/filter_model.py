"""The filter model Flask integration.

Supports parsing a GridFilterModel from Flask's request.args
"""
from flask import request

from mui.v5.grid.filter import GridFilterModel


def grid_filter_model_from_request(key: str = "filter_model") -> GridFilterModel:
    """Retrieves a GridFilterModel from request.args.

    Args:
        key (str): The key in the request args where the filter model should be parsed
            from. Defaults to "filter_model".

    Raises:
        ValidationError: Raised when an invalid type was received.

    Returns:
        GridFilterModel: The parsed filter model.
    """
    return request.args.get(
        key=key, default=GridFilterModel(items=[]), type=GridFilterModel.parse_raw
    )
