from datetime import datetime, time
from typing import Any, Optional, Union
from zoneinfo import ZoneInfo


def get_python_type_from_column(column: Any) -> Any:
    """Retrieve the python_type value for a SQLAlchemy column.

    This is used to ensure that we can retrieve the python_type from both native
    datatypes in SQLAlchemy as well as custom data types implemented using the
    TypeDecorator class, as described in the documentation:

    https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator
    """
    # built-in types and type decorators
    if hasattr(column.type, "python_type"):
        python_type = column.type.python_type
    # if implementing a type decorator without a python type
    elif hasattr(column.type, "impl") and hasattr(column.type.impl, "python_type"):
        python_type = column.type.impl.python_type
    else:
        python_type = None

    return python_type


def is_timezone_aware(value: Union[datetime, time]) -> bool:
    # https://docs.python.org/3/library/datetime.html#determining-if-an-object-is-aware-or-naive
    if value.tzinfo is not None:
        if isinstance(value, datetime):
            return value.tzinfo.utcoffset(value) is not None
        return value.tzinfo.utcoffset(None) is not None
    # naive
    return False


def apply_timezone_to_datetime(dt: datetime, timezone: Optional[ZoneInfo]) -> datetime:
    if is_timezone_aware(value=dt):
        # don't convert an aware timezone to a naive one
        if timezone is None:
            return dt
        return dt.astimezone(tz=timezone)
    # if it's not timezone aware, None will still be None, so we don't need to check
    return dt.replace(tzinfo=timezone)
