from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column
from common.enums.dosage_form import DosageForm
from db.base import BaseModel
from db import orm as orm_fields


class Drug(BaseModel):
    __tablename__ = 'drugs'

    name: Mapped[orm_fields.unique_str_128]
    international_name: Mapped[orm_fields.not_nullable_str_128]
    dosage_form: Mapped[DosageForm] = mapped_column(
        Enum(
            DosageForm,
            name='dosage_form',
        ),
        nullable=False
    )
    strength: Mapped[orm_fields.not_nullable_str_64]
    description: Mapped[orm_fields.text_column]