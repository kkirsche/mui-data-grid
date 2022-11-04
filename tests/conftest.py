from datetime import datetime, timedelta
from typing import Generator, Optional, Union

from pytest import fixture
from sqlalchemy import Column, DateTime, Integer, String, create_engine, func
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeMeta, Mapped, Query, Session, registry

from mui.v5.integrations.sqlalchemy import Resolver

GENERATED_MODEL_COUNT = 1000
RESOLVABLE_FIELDS = (
    "id",
    "grouping_id",
    "groupingId",
    "groupingID",
    "null_field",
    "nullField",
    "name",
    "created_at",
    "createdAt",
)
FIRST_DATE_STR = "2022-11-01T12:00:00.000000+00:00"
FIRST_DATE_DATETIME = datetime.fromisoformat(FIRST_DATE_STR)
mapper_registry = registry()


class Base(metaclass=DeclarativeMeta):
    __abstract__ = True

    registry = mapper_registry
    metadata = mapper_registry.metadata

    __init__ = mapper_registry.constructor


class ExampleModel(Base):
    __tablename__ = "test_model"

    def __hash__(self) -> int:
        return hash((self.id,))

    id: Mapped[int] = Column(  # pyright: ignore
        Integer(),
        autoincrement=True,
        comment="Identifier",
        primary_key=True,
    )
    created_at: Mapped[datetime] = Column(  # pyright:ignore
        DateTime(timezone=True),
        comment="When the row was created.",
        nullable=False,
        # equivalent to MariaDB's UTC_TIMESTAMP
        server_default=func.DATETIME("now"),
    )
    grouping_id: Mapped[int] = Column(  # pyright: ignore
        Integer(),
        comment="A number to more easily group results to test multi-directional sort",
        nullable=False,
    )
    null_field: Mapped[Optional[int]] = Column(  # pyright: ignore
        Integer(),
        comment="A null field",
        default=None,
        nullable=True,
    )
    name: Mapped[str] = Column(  # pyright: ignore
        String(),
        nullable=False,
        comment="The name of the model",
    )


def example_model_resolver(field: str) -> Union[int, str]:
    """Resolves the model's field names to the corresponding column names.

    Args:
        field (str): The field name being resolved.

    Raises:
        ValueError: Raised when the field is not a resolvable field.
        ValueError: Raised when the resolver doesn't support the field even though
            it was considered a resolvable field. This is considered a programming
            error, but ensures MyPy is satisfied.

    Returns:
        Union[int, str]: The column (which mypy thinks is actually it's value)
    """
    if field not in RESOLVABLE_FIELDS:
        raise ValueError("Incorrect configuration in RESOLVABLE_FIELDS constant")
    if field == "id":
        return ExampleModel.id
    if field in {"grouping_id", "groupingId", "groupingID"}:
        return ExampleModel.grouping_id
    if field in {"null_field", "nullField"}:
        return ExampleModel.null_field
    if field == "name":
        return ExampleModel.name
    if field in {"created_at", "createdAt"}:
        return ExampleModel.created_at
    raise ValueError("Resolver does not support this field name")


def calculate_grouping_id(model_id: int) -> int:
    """Calculate a grouping ID from the model's ID.

    Formula:
        int(abs(model_id / 100))

    Args:
        model_id (int): The model's ID.

    Returns:
        int: The model's grouping ID.
    """
    return int(abs(model_id / 100))


@fixture(scope="session")
def model_count() -> int:
    """The number of models that were committed to the database.

    Returns:
        int: The model count.
    """
    return GENERATED_MODEL_COUNT


@fixture(scope="session")
def engine() -> Generator[Engine, None, None]:
    """The SQLAlchemy engine, after creating the metadata.

    Yields:
        Engine: The SQLAlchemy engine
    """
    engine = create_engine(url="sqlite:///:memory:", future=True)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@fixture(scope="session")
def session(engine: Engine, model_count: int) -> Generator[Session, None, None]:
    """The SQLAlchemy session, after committing models to the database.

    Yields:
        Session: The SQLAlchemy session
    """
    session = Session(bind=engine, future=True)
    for i in range(1, model_count + 1):
        group = calculate_grouping_id(model_id=i)
        created = FIRST_DATE_DATETIME + timedelta(days=i - 1)
        # faked for testing of `is` equality operator and other date-time operators
        model = ExampleModel(
            created_at=created,
            name=f"{ExampleModel.__name__} {i}",
            grouping_id=group,
        )
        session.add(model)
    session.commit()
    yield session


@fixture(scope="module")
def query(session: Session) -> Generator["Query[ExampleModel]", None, None]:
    """A fixture representing a SQLAlchemy query."""
    yield (session.query(ExampleModel))


@fixture(scope="module")
def resolver() -> Resolver:
    return example_model_resolver
