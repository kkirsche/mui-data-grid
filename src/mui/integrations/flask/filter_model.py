from flask import request

from mui.v5.grid.filter import GridFilterModel


def grid_filter_model_from_request(key: str = "filter_model") -> GridFilterModel:
    """Retrieves a GridFilterModel

    Args:
        key (str, optional): _description_. Defaults to "filter_model".

    Returns:
        GridFilterModel: _description_
    """
    return request.args.get(
        key=key, default=GridFilterModel(), type=GridFilterModel.parse_raw
    )
