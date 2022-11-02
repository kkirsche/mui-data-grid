from random import randrange
from typing import Generator, cast

from pytest import fixture
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeMeta, Query, Session, registry

from mui.v5.integrations.sqlalchemy import Resolver

GENERATED_MODEL_COUNT = 1000
RESOLVABLE_FIELDS = ("id", "random_number", "randomNumber")
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

    id = Column(
        Integer(),
        autoincrement=True,
        primary_key=True,
        comment="Identifier",
    )
    random_number = Column(Integer(), comment="A random number")


def example_model_resolver(field: str) -> "Column[Integer]":
    if field == "id":
        return cast("Column[Integer]", ExampleModel.id)
    if field in {"random_number", "randomNumber"}:
        return cast("Column[Integer]", ExampleModel.random_number)
    raise ValueError("Resolver does not support this field name")


@fixture(scope="session")
def model_count() -> int:
    return GENERATED_MODEL_COUNT


@fixture(scope="session")
def engine() -> Generator[Engine, None, None]:
    engine = create_engine(url="sqlite:///:memory:", future=True)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@fixture(scope="session")
def session(engine: Engine, model_count: int) -> Generator[Session, None, None]:
    session = Session(bind=engine)
    for _ in range(1, model_count + 1):
        session.add(ExampleModel(random_number=randrange(model_count + 1)))
    session.commit()
    yield session


@fixture(scope="module")
def query(session: Session) -> Generator["Query[ExampleModel]", None, None]:
    """A fixture representing a SQLAlchemy query."""
    yield (session.query(ExampleModel))


@fixture(scope="module")
def resolver() -> Resolver:
    return example_model_resolver
