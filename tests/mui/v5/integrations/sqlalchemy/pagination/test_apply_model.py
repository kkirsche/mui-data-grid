from datetime import datetime, timezone
from typing import Generator

from hypothesis import given
from hypothesis import strategies as st
from pytest import fixture
from sqlalchemy import Column, DateTime, Integer, create_engine
from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import DeclarativeMeta, Query, Session, registry

from mui.v5.grid import GridPaginationModel
from mui.v5.integrations.sqlalchemy.pagination import (
    apply_limit_offset_to_query_from_model,
)

mapper_registry = registry()


class Base(metaclass=DeclarativeMeta):
    __abstract__ = True

    registry = mapper_registry
    metadata = mapper_registry.metadata

    __init__ = mapper_registry.constructor


class TestModel(Base):
    __tablename__ = "test_model"

    id = Column(Integer(), primary_key=True, autoincrement=True, comment="Identifier")
    date = Column(DateTime, onupdate=datetime.now(tz=timezone.utc))


@fixture(scope="module")
def query() -> Generator["Query[TestModel]", None, None]:
    """A fixture representing a SQLAlchemy query."""
    engine = create_engine("sqlite:///:memory:")
    session = Session(engine)
    Base.metadata.create_all(engine)
    yield (session.query(TestModel))
    Base.metadata.drop_all(engine)


@given(model=st.builds(GridPaginationModel, page=st.integers(min_value=0)))
def test_apply_limit_offset_to_query_from_model(
    model: GridPaginationModel, query: "Query[TestModel]"
) -> None:
    paginated = apply_limit_offset_to_query_from_model(query=query, model=model)
    compiled = paginated.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    assert "LIMIT ?" in compiled_str
    assert "OFFSET ?" in compiled_str
    assert compiled.params["param_1"] == 15
    assert compiled.params["param_2"] == 0
