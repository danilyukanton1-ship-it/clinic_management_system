from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship
from db.base import BaseModel
from db import orm as orm_column

if TYPE_CHECKING:
    from app.users.models.user import User


class Specialization(BaseModel):
    __tablename__ = "specializations"

    name: Mapped[orm_column.unique_str_128]
    users: Mapped[list["User"]] = relationship(
        "User",
        back_populates="specialization",
    )
    description: Mapped[orm_column.text_column]
