from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, relationship

from tests.fixtures.sqlalchemy.models.base import Base

if TYPE_CHECKING:
    from tests.fixtures.sqlalchemy.models.child import ChildModel


class ParentModel(Base):
    __tablename__ = "test_model"

    def __hash__(self) -> int:
        return hash(
            (
                self.id,
                self.created_at.isoformat(),
                self.grouping_id,
                self.null_field,
                self.name,
            )
        )

    id: Mapped[int] = sa.Column(  # pyright: ignore
        sa.Integer(),
        autoincrement=True,
        comment="Identifier",
        primary_key=True,
    )
    created_at: Mapped[datetime] = sa.Column(  # pyright:ignore
        sa.DateTime(timezone=True),
        comment="When the row was created.",
        nullable=False,
        # equivalent to MariaDB's UTC_TIMESTAMP
        server_default=sa.func.DATETIME("now"),
    )
    grouping_id: Mapped[int] = sa.Column(  # pyright: ignore
        sa.Integer(),
        comment="A number to more easily group results to test multi-directional sort",
        nullable=False,
    )
    null_field: Mapped[Optional[int]] = sa.Column(  # pyright: ignore
        sa.Integer(),
        comment="A null field",
        default=None,
        nullable=True,
    )
    name: Mapped[str] = sa.Column(  # pyright: ignore
        sa.String(),
        nullable=False,
        comment="The name of the model",
    )

    children: Mapped[List["ChildModel"]] = relationship(  # pyright: ignore
        "ChildModel", back_populates="parent", uselist=True
    )
