from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db import orm as orm_fields
from db.base import BaseModel

class Attachment(BaseModel):
    __tablename__ = 'attachments'

    patient_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='RESTRICT'),
        nullable=False,
    )

    appointment_id: Mapped[int] = mapped_column(
        ForeignKey('appointments.id', ondelete='CASCADE'),
        nullable=False,
    )

    uploaded_by_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='RESTRICT'),
        nullable=False,
    )
    filename: Mapped[orm_fields.not_nullable_str_128]
    file_path: Mapped[orm_fields.not_nullable_str_512]
    file_mime_type: Mapped[orm_fields.not_nullable_str_128]
    file_size: Mapped[orm_fields.not_nullable_int]