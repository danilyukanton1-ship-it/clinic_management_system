from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from core.models import BaseModel
from core import orm as orm_fields

class Disease(BaseModel):
    __tablename__ = 'diseases'

    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    name: Mapped[orm_fields.unique_str_128]
    description: Mapped[orm_fields.text_column]

