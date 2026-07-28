from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from db import orm as orm_fields
from db.base import BaseModel


class PrescriptionItem(BaseModel):
    __tablename__ = "prescription_items"

    __table_args__ = (
        CheckConstraint("duration_days > 0", name="ck_duration_days_positive"),
    )

    prescription_id: Mapped[int] = mapped_column(
        ForeignKey("prescriptions.id", ondelete="CASCADE"),
        nullable=False,
    )

    drug_id: Mapped[int] = mapped_column(
        ForeignKey("drugs.id", ondelete="RESTRICT"),
        nullable=False,
    )

    dosage: Mapped[orm_fields.not_nullable_str_128]
    frequency: Mapped[orm_fields.not_nullable_str_128]
    duration_days: Mapped[orm_fields.not_nullable_int]
