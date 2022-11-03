"""The apply_model module is responsible for applying a GridSortModel to a query."""
from operator import eq, ge, gt, le, lt, ne
from typing import Any, Callable, TypeVar, Optional

from sqlalchemy import and_, or_, any_
from sqlalchemy.orm import Query
from sqlalchemy.sql.elements import BooleanClauseList

from mui.v5.grid import GridFilterItem, GridFilterModel, GridLinkOperator
from mui.v5.integrations.sqlalchemy.resolver import Resolver

_Q = TypeVar("_Q")


def _get_link_operator(
    model: GridFilterModel,
) -> Callable[[Any], BooleanClauseList[Any]]:
    """Retrieves the correct filter operator for a model.

    If the link operator is None, `OR` is used by default.

    Args:
        model (GridFilterModel): The grid filter model which is being applied to the
            SQLAlchemy query.

    Returns:
        Callable[[Any], BooleanClauseList[Any]]: The `or_` and `and_` operators for
            application to SQLAlchemy filters.
    """
    if model.link_operator is None or model.link_operator == GridLinkOperator.Or:
        return or_
    else:
        return and_


def _get_operator_value(item: GridFilterItem) -> Callable[[Any, Any], Any]:
    """Retrieve the Python operator function from the filter item's operator value.

    As an example, this function converts strings such as "==", "!=", and ">=" to the
    functions operator.eq, operator.ne, operator.ge respectively.


    Args:
        item (GridFilterItem): The grid filter item being operated on.

    Raises:
        ValueError: Raised when the operator value is not supported by the integration.

    Returns:
        Callable[[Any, Any], Any]: The operator.
    """
    if item.operator_value == "==":
        # equal
        return eq
    elif item.operator_value == "!=":
        # not equal
        return ne
    elif item.operator_value == ">":
        # less than
        return gt
    elif item.operator_value == ">=":
        # less than or equal to
        return ge
    elif item.operator_value == "<":
        # greater than
        return lt
    elif item.operator_value == "<=":
        # greater than or equal to
        return le
    else:
        raise ValueError(f"Unsupported operator {item.operator_value}")


def apply_operator_to_column(item: GridFilterItem, resolver: Resolver) -> Any:
    column = resolver(item.column_field)
    operator: Optional[Callable[[Any, Any], Any]] = None
    if item.operator_value in {"==", "!=", ">", ">=", "<", "<="}:
        operator = _get_operator_value(item=item)
        return operator(column, item.value)
    elif item.operator_value == "isEmpty":
        return eq(column, None)
    elif item.operator_value == "isNotEmpty":
        return ne(column, None)
    elif item.operator_value == "isAnyOf":
        return eq(column, any_(item.value))


def apply_filter_items_to_query_from_items(
    query: "Query[_Q]", model: GridFilterModel, resolver: Resolver
) -> "Query[_Q]":
    """Applies a grid filter model's items section to a SQLAlchemy query.

    Args:
        query (Query[_Q]): The query to be filtered.
        model (GridFilterModel): The filter model being applied.
        resolver (Resolver): A resolver to convert field names from the model to
            SQLAlchemy column's or expressions.

    Returns:
        Query[_Q]: The filtered query.
    """
    if len(model.items) == 0:
        return query

    link_operator = _get_link_operator(model=model)
    # this is a bit gross, but is the easiest way to ensure it's applied properly
    return query.filter(
        # the link operator is either the and_ or or_ sqlalchemy function to determine
        # how the boolean clause list is applied
        link_operator(
            # the _get_operator_value returns a function which we immediately call.
            # The function is a comparison function supported by SQLAlchemy such as
            # eq, ne, le, lt, etc. which is applied to the model's resolved column
            # and the filter value.
            # Basically, it builds something like this, dynamically:
            # .filter(and_(gt(Request.id, 100), eq(Request.title, "Example"))
            apply_operator_to_column(item=item, resolver=resolver)
            for item in model.items
        )
    )