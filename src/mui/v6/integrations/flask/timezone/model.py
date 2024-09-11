"""The sort model Flask integration.

Supports parsing a GridSortModel from Flask's request.args
"""

from datetime import timezone
from typing import Optional, Union
from zoneinfo import ZoneInfo

from flask import request
from typing_extensions import Literal


def get_grid_timezone_from_request(
    key: str = "timezone",
    model_format: Literal["json"] = "json",
    default: Optional[Union[ZoneInfo, timezone]] = None,
) -> Optional[Union[ZoneInfo, timezone]]:
    """Retrieves a timezone from request.args.

    Currently, this only supports a JSON encoded model, but in the future the plan is
    to write a custom querystring parser to support nested arguments as JavaScript
    libraries like Axios create out of the box.

    Args:
        key (str): The key in the request args where the sort model should be parsed
            from. Defaults to "timezone".

    Raises:
        ValidationError: Raised when an invalid type was received.
        ValueError: Raised when an invalid model format was received.

    Returns:
        ZoneInfo: The parsed timezone.
    """
    if model_format == "json":
        value = request.args.get(key=key)
        if value is not None:
            return ZoneInfo(value)
        if default is not None:
            return default
        return None
    raise ValueError(f"Invalid model format: {model_format}")
