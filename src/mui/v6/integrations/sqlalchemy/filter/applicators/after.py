"""The is after applicator applies the is after operator to the data."""

from __future__ import annotations

from datetime import datetime
from datetime import timezone as dt_timezone
from operator import gt
from typing import Any
from zoneinfo import ZoneInfo

from mui.v6.integrations.sqlalchemy.utils import apply_timezone_to_datetime


def apply_after_operator(
    column: Any, value: Any, timezone: ZoneInfo | dt_timezone | None
) -> Any:
    """Handles applying the after x-data-grid operator to a column.

    Args:
        column (Any): The column the operator is being applied to, or equivalent
            property, expression, subquery, etc.
        value (Any): The value being filtered.

    Returns:
        Any: The column after applying the after filter using the provided value.
    """
    if value is None:
        return column
    # if the column is after the received date, it will be greater than the
    # received date
    parsed = datetime.fromisoformat(value)
    parsed = apply_timezone_to_datetime(dt=parsed, timezone=timezone)
    return gt(column, parsed)
