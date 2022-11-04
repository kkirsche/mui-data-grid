from typing import Generator, Optional, Union

from pytest import fixture
from sqlalchemy import Column, Integer, String, create_engine
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
)
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
        primary_key=True,
        comment="Identifier",
    )
    grouping_id: Mapped[int] = Column(  # pyright: ignore
        Integer(),
        nullable=False,
        comment="A number to more easily group results to test multi-directional sort",
    )
    null_field: Mapped[Optional[int]] = Column(  # pyright: ignore
        Integer(),
        nullable=True,
        comment="A null field",
        default=None,
    )
    name: Mapped[str] = Column(  # pyright: ignore
        String(),
        nullable=False,
        comment="The name of the model",
    )


def example_model_resolver(field: str) -> Union[int, str]:
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
    raise ValueError("Resolver does not support this field name")


def calculate_grouping_id(model_id: int) -> int:
    return int(abs(model_id / 100))


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
        group = int(abs(i / 100))
        session.add(
            ExampleModel(name=f"{ExampleModel.__name__} {i}", grouping_id=group)
        )
    session.commit()
    yield session


@fixture(scope="module")
def query(session: Session) -> Generator["Query[ExampleModel]", None, None]:
    """A fixture representing a SQLAlchemy query."""
    yield (session.query(ExampleModel))


@fixture(scope="module")
def resolver() -> Resolver:
    return example_model_resolver
