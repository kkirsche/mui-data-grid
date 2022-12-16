"""The is not applicator applies the is not operator to the data.
"""
from datetime import datetime
from operator import ne
from typing import Any


def apply_not_operator(column: Any, value: Any) -> Any:
    """Handles applying the not x-data-grid operator to a column.

    Args:
        column (Any): The column the operator is being applied to, or equivalent
            property, expression, subquery, etc.
        value (Any): The value being filtered.

    Returns:
        Any: The column after applying the is filter using the provided value.
    """
    return ne(column, datetime.fromisoformat(value))
