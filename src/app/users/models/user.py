from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from sqlalchemy import Enum as SQLEnum
from db.base import BaseModel
from db import orm as orm_column
from common.enums.user_role import UserRole

if TYPE_CHECKING:
    from app.users.models.specialization import Specialization


class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[orm_column.email_column]
    phone: Mapped[orm_column.phone_column]
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)

    first_name: Mapped[orm_column.str_64]
    last_name: Mapped[orm_column.str_64]
    middle_name: Mapped[str | None] = mapped_column(String(64), nullable=True)

    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, name="user_role"), nullable=False
    )

    specialization_id: Mapped[int] = mapped_column(
        ForeignKey("specializations.id"), nullable=True
    )
    specialization: Mapped["Specialization"] = relationship(
        "Specialization", back_populates="users"
    )

    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_verified: Mapped[orm_column.bool_column]
