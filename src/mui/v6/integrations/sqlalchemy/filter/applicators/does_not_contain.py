"""The does not contain applicator applies the contains method to the data.

Does not contain is meant as in "Jonathan" does not contain "Matt".
"""

from typing import Any

from sqlalchemy import not_


def apply_does_not_contain_operator(column: Any, value: Any) -> Any:
    """Handles applying the doesNotContain x-data-grid operator to a column.

    Args:
        column (Any): The column the operator is being applied to, or equivalent
            property, expression, subquery, etc.
        value (Any): The value being filtered.

    Returns:
        Any: The column after applying the is any of filter using the provided value.
    """
    # https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.contains # noqa: E501
    # Per SQLAlchemy 1.4.43:
    # only '=', '!=', 'is_()', 'is_not()', 'is_distinct_from()',
    # 'is_not_distinct_from()' operators can be used with None/True/False
    # so below have to special case them.
    return not_(column.contains(value if value is not None else ""))
