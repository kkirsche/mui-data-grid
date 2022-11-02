from typing import Generator
from uuid import uuid4

from pytest import fixture
from sqlalchemy import Column, DateTime, String, create_engine, func
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeMeta, Query, Session, registry
from mui.v5.integrations.sqlalchemy import Resolver

GENERATED_MODEL_COUNT = 1000
mapper_registry = registry()


class Base(metaclass=DeclarativeMeta):
    __abstract__ = True

    registry = mapper_registry
    metadata = mapper_registry.metadata

    __init__ = mapper_registry.constructor


class ExampleModel(Base):
    __tablename__ = "test_model"

    id = Column(
        String(length=255),
        comment="Identifier",
        nullable=False,
        primary_key=True,
    )
    created_at = Column(
        DateTime(timezone=True),
        comment="Created At Time",
        nullable=False,
        server_default=func.datetime("now"),
    )
    name = Column(String(length=255), nullable=False, comment="The model's name.")


def example_model_resolver(field: str) -> "Column[String] | Column[DateTime]":
    match field:
        case "id":
            return ExampleModel.id
        case "created_at":
            return ExampleModel.created_at
        case "createdAt":
            return ExampleModel.created_at
        case "name":
            return ExampleModel.name
        case _:
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
    for i in range(1, model_count + 1):
        session.add(ExampleModel(id=str(uuid4()), name=f"model {i}"))
    session.commit()
    yield session


@fixture(scope="module")
def query(session: Session) -> Generator["Query[ExampleModel]", None, None]:
    """A fixture representing a SQLAlchemy query."""
    yield (session.query(ExampleModel))


@fixture(scope="module")
def resolver() -> Resolver:
    return example_model_resolver
