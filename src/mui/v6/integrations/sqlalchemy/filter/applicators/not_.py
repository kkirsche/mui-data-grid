"""The is not applicator applies the is not operator to the data."""

from __future__ import annotations

from datetime import date, datetime, time
from datetime import timezone as dt_timezone
from operator import ne
from typing import Any
from zoneinfo import ZoneInfo

from mui.v6.integrations.sqlalchemy.utils import (
    apply_timezone_to_datetime,
    get_python_type_from_column,
)


def apply_not_operator(
    column: Any, value: Any, timezone: ZoneInfo | dt_timezone | None
) -> Any:
    """Handles applying the not x-data-grid operator to a column.

    The not operator exists on enum selections as well as datetimes. Care
    needs to be given as a result.

    Args:
        column (Any): The column the operator is being applied to, or equivalent
            property, expression, subquery, etc.
        value (Any): The value being filtered.

    Returns:
        Any: The column after applying the is filter using the provided value.
    """
    python_type = get_python_type_from_column(column=column)

    if python_type in {datetime, time, date} and value is not None:
        parsed = datetime.fromisoformat(value)
        parsed = apply_timezone_to_datetime(dt=parsed, timezone=timezone)
        return ne(column, parsed)
    return ne(column, value)
