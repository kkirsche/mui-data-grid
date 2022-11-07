from datetime import datetime, timedelta
from typing import Generator, Union

from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Query, Session

from mui.v5.integrations.sqlalchemy import Resolver
from tests.fixtures import Base, ChildModel, ParentModel, random_category

GENERATED_MODEL_COUNT = 1000
RESOLVABLE_FIELDS = (
    "created_at",
    "createdat",
    "grouping_id",
    "groupingid",
    "id",
    "name",
    "null_field",
    "nullfield",
)
FIRST_DATE_STR = "2022-11-01T12:00:00.000000+00:00"
FIRST_DATE_DATETIME = datetime.fromisoformat(FIRST_DATE_STR)


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
    normalized_field = field.lower()
    if normalized_field not in RESOLVABLE_FIELDS:
        raise ValueError("Incorrect configuration in RESOLVABLE_FIELDS constant")
    if normalized_field == "id":
        return ParentModel.id
    if field in {"grouping_id", "groupingid"}:
        return ParentModel.grouping_id
    if field in {"null_field", "nullfield"}:
        return ParentModel.null_field
    if field == "name":
        return ParentModel.name
    if field in {"created_at", "createdat"}:
        return ParentModel.created_at
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
        model = ParentModel(
            created_at=created,
            name=f"{ParentModel.__name__} {i}",
            grouping_id=group,
        )
        session.add(model)
        session.commit()
        session.refresh(model)
        for _ in range(1, model_count + 1):
            related_model = ChildModel(category=random_category(), parent_id=model.id)
            session.add(related_model)
    session.commit()
    yield session


@fixture(scope="module")
def query(session: Session) -> Generator["Query[ParentModel]", None, None]:
    """A fixture representing a SQLAlchemy query."""
    yield (session.query(ParentModel))


@fixture(scope="module")
def joined_query(session: Session) -> Generator["Query[ParentModel]", None, None]:
    """A fixture representing a SQLAlchemy query."""
    yield (session.query(ChildModel).join(ParentModel))


@fixture(scope="module")
def resolver() -> Resolver:
    return example_model_resolver
