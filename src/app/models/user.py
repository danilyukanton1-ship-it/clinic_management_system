from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from sqlalchemy import Enum as SQLEnum
from core.models import BaseModel
from core import orm as orm_column
from app.enums.user_role import UserRole

class User(BaseModel):
    __tablename__ = "users"

    email: orm_column.email_column
    phone: orm_column.phone_column
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)

    first_name: orm_column.str_64
    last_name: orm_column.str_64
    middle_name: Mapped[str | None] = mapped_column(String(64), nullable=True)

    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole, name='user_role'), nullable=False)

    specialization_id: Mapped[int] = mapped_column(ForeignKey('specializations.id'), nullable=True)

    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_verified: orm_column.bool_column
