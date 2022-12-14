import sqlalchemy as sa
from sqlalchemy.orm import Mapped, relationship

from tests.fixtures.sqlalchemy.enums import Category, values_callable
from tests.fixtures.sqlalchemy.models.base import Base
from tests.fixtures.sqlalchemy.models.parent import ParentModel


class ChildModel(Base):
    __tablename__ = "test_related_model"

    def __hash__(self) -> int:
        """Returns a unique identifier for the object"""
        return hash((self.id, self.parent_id))

    id: Mapped[int] = sa.Column(  # pyright: ignore
        sa.Integer(),
        autoincrement=True,
        comment="Identifier",
        primary_key=True,
    )
    parent_id: Mapped[int] = sa.Column(  # pyright: ignore
        sa.Integer(),
        sa.ForeignKey(f"{ParentModel.__tablename__}.id"),
        nullable=False,
    )
    category: Mapped[Category] = sa.Column(  # pyright: ignore
        sa.Enum(Category, create_constraint=True, values_callable=values_callable),
        nullable=False,
    )

    parent: Mapped["ParentModel"] = relationship(  # pyright: ignore
        "ParentModel", back_populates="children", uselist=False
    )
