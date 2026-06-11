from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core import orm as orm_fields
from core.models import BaseModel

class Diagnosis(BaseModel):
    __tablename__ = 'diagnoses'

    appointment_id: Mapped[int] = mapped_column(
        ForeignKey('appointments.id'),
        nullable=False,
    )

    disease_id: Mapped[int] = mapped_column(
        ForeignKey('diseases.id'),
        nullable=False,
    )

    notes: Mapped[orm_fields.nullable_text_column]