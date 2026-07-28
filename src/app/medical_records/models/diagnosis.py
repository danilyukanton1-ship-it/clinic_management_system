from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db import orm as orm_fields
from db.base import BaseModel

class Diagnosis(BaseModel):
    __tablename__ = 'diagnoses'

    prescription_id: Mapped[int] = mapped_column(
        ForeignKey('prescriptions.id', ondelete='CASCADE'),
        nullable=False,
    )

    disease_id: Mapped[int] = mapped_column(
        ForeignKey('diseases.id', ondelete='RESTRICT'),
        nullable=False,
    )

    notes: Mapped[orm_fields.nullable_text_column]