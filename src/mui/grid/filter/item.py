from collections.abc import MutableMapping, Sequence
from typing import Any, ClassVar, Optional, TypeAlias

from pydantic import BaseModel, Field, root_validator

_ColumnField: TypeAlias = str
_Id: TypeAlias = int | str | None
_OperatorValue: TypeAlias = str | None
_Value: TypeAlias = Optional[Any]


class GridFilterItem(BaseModel):
    """A grid filter item.

    Documentation:
        https://mui.com/x/api/data-grid/grid-filter-item/

    Attributes:
        column_field (str): The column from which we want to filter the rows.
            - Alias: columnField
        id (str | int | not set): Must be unique. Only useful when the model contains
            several items.
        operator_value (str | None | not set): The name of the operator we want to
            apply. Will become required on @mui/x-data-grid@6.X.
            - Alias: operatorValue
        value: (Any | None | not set): The filtering value.
            The operator filtering function will decide for each row if the row values
            is correct compared to this value.
    """

    column_field: _ColumnField = Field(
        default=...,
        title="Column Field",
        description="The column from which we want to filter the rows.",
        alias="columnField",
    )
    id: _Id = Field(
        default=None,
        title="Identifier",
        description="A unique identifier if a model contains several items",
    )
    operator_value: _OperatorValue = Field(
        default=None,
        title="Operator Value",
        description="The name of the operator we want to apply.",
        alias="operatorValue",
    )
    value: _Value = Field(
        default=None, title="Value", description="The filtering value"
    )

    _optional_keys: ClassVar[set[Sequence[str]]] = {
        # be careful, this is a tuple because of the trailing comma
        ("id",),
        ("operatorValue", "operator_value"),
        # be careful, this is a tuple because of the trailing comma
        ("value",),
    }

    @root_validator(pre=True)
    def ensure_optional_keys_exist(cls, haystack: object) -> object:
        """A validator that runs before validating the attribute's values.

        This validator ensures that at least one key per tuple exists if the received
        object is a mutable mapping, such as a dictionary.

        Arguments:
            haystack (object): The haystack, or incoming value, being evaluated to
                identify if it has at least one of the optional keys (needles).
                The name comes from looking for a needle in a haystack.

        Returns:
            object: The haystack, with the keys added to the mapping, if it was an
                object we could mutate.
        """
        if isinstance(haystack, MutableMapping):
            for keys in cls._optional_keys:
                found_needle = any(needle in haystack for needle in keys)
                if not found_needle:
                    key = keys[0]
                    haystack[key] = None
        return haystack

    class Config:
        allow_population_by_field_name = True
