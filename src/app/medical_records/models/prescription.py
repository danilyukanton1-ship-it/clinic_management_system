from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db import orm as orm_fields
from db.base import BaseModel

class Prescription(BaseModel):
    __tablename__ = 'prescriptions'

    appointment_id: Mapped[int] = mapped_column(
        ForeignKey('appointments.id'),
        nullable=False,
    )

    recommendations: Mapped[orm_fields.nullable_text_column]