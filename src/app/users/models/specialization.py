from sqlalchemy.orm import Mapped
from db.base import BaseModel
from db import orm as orm_column


class Specialization(BaseModel):
    __tablename__ = 'specializations'

    name: Mapped[orm_column.unique_str_128]
    description: Mapped[orm_column.text_column]
