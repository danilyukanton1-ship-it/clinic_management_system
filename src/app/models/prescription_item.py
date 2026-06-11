from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core import orm as orm_fields
from core.models import BaseModel

class PrescriptionItem(BaseModel):
    __tablename__ = 'prescription_items'

    __table_args__ = (
        CheckConstraint(
            'duration_days > 0',
            name='ck_duration_days_positive'
        ),
    )

    prescription_id: Mapped[int] = mapped_column(
        ForeignKey('prescriptions.id'),
        nullable=False,
    )

    drug_id: Mapped[int] = mapped_column(
        ForeignKey('drugs.id'),
        nullable=False,
    )

    dosage: Mapped[orm_fields.not_nullable_str_128]
    frequency: Mapped[orm_fields.not_nullable_str_128]
    duration_days: Mapped[orm_fields.not_nullable_int]