from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, DateTime
from db import orm as orm_column
from db.database import Base

class BaseModel(Base):
    __abstract__ = True
    id: Mapped[orm_column.id_pk]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )