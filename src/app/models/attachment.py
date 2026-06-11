from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core import orm as orm_fields
from core.models import BaseModel

class Attachment(BaseModel):
    __tablename__ = 'attachments'

    patient_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='RESTRICT'),
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