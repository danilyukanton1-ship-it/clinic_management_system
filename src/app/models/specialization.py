from core.models import BaseModel
from core import orm as orm_column

class Specialization(BaseModel):
    __tablename__ = 'specializations'

    name: orm_column.unique_str_128
    description: orm_column.text_column
