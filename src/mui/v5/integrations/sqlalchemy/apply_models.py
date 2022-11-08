"""The apply_models module is used to apply the X-Data-Grid state models, such as the
GridFilterModel, GridSortModel, and GridPaginationModel to a SQLAlchemy ORM query.
"""
from typing import Optional, TypeVar

from sqlalchemy.orm import Query

from mui.v5.grid import (
    GridFilterModel,
    GridPaginationModel,
    GridSortModel,
    RequestGridModels,
)
from mui.v5.integrations.sqlalchemy.filter import apply_filter_to_query_from_model
from mui.v5.integrations.sqlalchemy.pagination import (
    apply_limit_offset_to_query_from_model,
)
from mui.v5.integrations.sqlalchemy.resolver import Resolver
from mui.v5.integrations.sqlalchemy.sort import apply_sort_to_query_from_model

T = TypeVar("T")


def apply_request_grid_models_to_query(
    query: "Query[T]",
    request_model: RequestGridModels,
    column_resolver: Resolver,
) -> "Query[T]":
    """Applies a RequestGridModels object to a query.

    This is a utility function to ensure that the models are applied in a SQLAlchemy
    compatible order.

    Args:
        query (Query[T]): The base query which will be filtered, ordered,
            and paginated.
        request_model (RequestGridModels): The X-Data-Grid state models being applied
            to the query.
        column_resolver (Resolver): The resolver responsible for taking an X-Data-Grid
            field name (from the UI configuration) and resolving it to the appropriate
            SQLAlchemy model column.

    Returns:
        Query[T]: The query, after it's paginated, ordered, and paginated. The caller
            should call the .all(), .first(), .count(), or other method to retrieve the
            final result(s).
    """
    return apply_data_grid_models_to_query(
        query=query,
        column_resolver=column_resolver,
        filter_model=request_model.filter_model,
        sort_model=request_model.sort_model,
        pagination_model=request_model.pagination_model,
    )


def apply_data_grid_models_to_query(
    query: "Query[T]",
    column_resolver: Resolver,
    filter_model: Optional[GridFilterModel] = None,
    sort_model: Optional[GridSortModel] = None,
    pagination_model: Optional[GridPaginationModel] = None,
) -> "Query[T]":
    """Applies the provided X-Data-Grid state models to the SQLAlchemy ORM Query.

    This method is provided to allow for implementing support for only specific
    server-side features rather than the trio of filter, sort, and pagination.

    Args:
        query (Query[T]): The base query which will be filtered, ordered,
            and paginated.
        column_resolver (Resolver): The resolver responsible for taking an X-Data-Grid
            field name (from the UI configuration) and resolving it to the appropriate
            SQLAlchemy model column.
        filter_model (Optional[GridFilterModel], optional): The filter model to apply
            to the query. If None, this stage will be skipped. Defaults to None.
        sort_model (Optional[GridSortModel], optional): The sort model to apply to the
            query. If None, this stage will be skipped. Defaults to None.
        pagination_model (Optional[GridPaginationModel], optional): The pagination
            model to apply to the query. If None, this stage will be skipped.
            Defaults to None.

    Returns:
        Query[T]: The query, with the filter, sort, and/or pagination models applied.
    """
    # order matters!
    if filter_model is not None:
        query = apply_filter_to_query_from_model(
            query=query, model=filter_model, resolver=column_resolver
        )
    if sort_model is not None:
        query = apply_sort_to_query_from_model(
            query=query, model=sort_model, resolver=column_resolver
        )
    if pagination_model is not None:
        query = apply_limit_offset_to_query_from_model(
            query=query, model=pagination_model
        )
    return query
