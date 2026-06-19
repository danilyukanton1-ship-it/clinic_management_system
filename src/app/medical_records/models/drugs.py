from sqlalchemy.orm import Mapped

from db.base import BaseModel
from db import orm as orm_fields


class Drugs(BaseModel):
    __tablename__ = 'drugs'

    name: Mapped[orm_fields.unique_str_128]

    description: Mapped[orm_fields.text_column]