"""The query module contains the DataGridQuery data structure.

This structure is used to provide helpers related to pagination, such as
total row counts.
"""
from typing import Generic, List, Optional, TypeVar

from sqlalchemy.orm import Query

from mui.v5.grid import GridFilterModel, GridPaginationModel, GridSortModel
from mui.v5.integrations.sqlalchemy.filter import apply_filter_to_query_from_model
from mui.v5.integrations.sqlalchemy.pagination import (
    apply_limit_offset_to_query_from_model,
)
from mui.v5.integrations.sqlalchemy.resolver import Resolver
from mui.v5.integrations.sqlalchemy.sort import apply_sort_to_query_from_model

_T = TypeVar("_T")


class DataGridQuery(Generic[_T]):
    """A data grid query handles utilities related to our query.

    Args:
        Generic (_type_): The model being retrieved by the query.
    """

    _query: "Query[_T]"
    column_resovler: Resolver
    filter_model: Optional[GridFilterModel]
    pagination_model: Optional[GridPaginationModel]
    query: "Query[_T]"
    sort_model: Optional[GridSortModel]

    def __init__(
        self,
        query: "Query[_T]",
        column_resolver: Resolver,
        filter_model: Optional[GridFilterModel] = None,
        sort_model: Optional[GridSortModel] = None,
        pagination_model: Optional[GridPaginationModel] = None,
    ) -> None:
        """Initialize a new data grid query.

        Args:
            query (Query[_T]): The base query which the models will be applied to.
            column_resolver (Resolver): The field resolver which converts a UI field
                to the corresponding SQLAlchemy column, column property, etc.
            filter_model (Optional[GridFilterModel], optional): The filter model to
                apply, if provided. Defaults to None.
            sort_model (Optional[GridSortModel], optional): The sort model to apply,
                if provided. Defaults to None.
            pagination_model (Optional[GridPaginationModel], optional): The pagination
                model to apply, if provided. Defaults to None.
        """
        self.column_resovler = column_resolver
        self.filter_model = filter_model
        self.sort_model = sort_model
        self.pagination_model = pagination_model
        query = self._filter_query(query=query)
        # we filter it first, so that our total is accurate
        self._query = query
        # then we apply the order and pagination limits
        query = self._order_query(query=query)
        query = self._paginate_query(query=query)
        self.query = query

    def _filter_query(self, query: "Query[_T]") -> "Query[_T]":
        """Applies the filter model to the query.

        Args:
            query (Query[_T]): The query being filtered.

        Returns:
            Query[_T]: The filtered query.
        """
        if self.filter_model is None:
            return query
        return apply_filter_to_query_from_model(
            query=query, model=self.filter_model, resolver=self.column_resovler
        )

    def _order_query(self, query: "Query[_T]") -> "Query[_T]":
        """Applies the sort model to the query.

        Args:
            query (Query[_T]): The query being ordered / sorted.

        Returns:
            Query[_T]: The sorted / ordered query.
        """
        if self.sort_model is None:
            return query
        return apply_sort_to_query_from_model(
            query=query, model=self.sort_model, resolver=self.column_resovler
        )

    def _paginate_query(self, query: "Query[_T]") -> "Query[_T]":
        """Applies the pagination model to the query.

        Args:
            query (Query[_T]): The query being paginated (limit / offset).

        Returns:
            Query[_T]: The paginated (limited) query.
        """
        if self.pagination_model is None:
            return query
        return apply_limit_offset_to_query_from_model(
            query=query, model=self.pagination_model
        )

    def total(self) -> int:
        """Returns the total number of rows that exist with the filter.

        Returns:
            int: _description_
        """
        return self._query.order_by(None).count()

    def items(self) -> List[_T]:
        """Returns the results of the query.

        Returns:
            List[_T]: The list of individual items located by the query after all
                models have been applied.
        """
        return self.query.all()
