from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from core.models import BaseModel
from core import orm as orm_column

class User(BaseModel):
    __tablename__ = "users"

    email: orm_column.email_column
    phone: orm_column.phone_column
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)

    first_name: orm_column.str_64
    last_name: orm_column.str_64
    middle_name: Mapped[str | None] = mapped_column(String(64), nullable=True)

    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_verified: orm_column.bool_column
