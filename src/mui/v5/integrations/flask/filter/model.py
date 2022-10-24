"""The model module contains the Grid Filter Model Flask integration.

Supports parsing a GridFilterModel from Flask's request.args
"""
from flask import request

from mui.v5.grid.filter import GridFilterModel


def get_grid_filter_model_from_request(
    key: str = "filter_model",
) -> GridFilterModel:
    """Retrieves a GridFilterModel from request.args.

    Args:
        key (str): The key in the request args where the filter model should be parsed
            from. Defaults to "filter_model".

    Raises:
        ValidationError: Raised when an invalid type was received.

    Returns:
        GridFilterModel: The parsed filter model, if found. If no filter model is
            found, an empty GridFilterModel instance is returned.
    """
    # get swallows `KeyError` and `ValueError`, which is why we don't allow this to
    # raise an exception
    # https://github.com/pallets/werkzeug/blob/main/src/werkzeug/datastructures.py#L919
    return request.args.get(
        key=key, default=GridFilterModel(), type=GridFilterModel.parse_raw
    )
