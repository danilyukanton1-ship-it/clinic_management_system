from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic import PositiveInt, Field


class AttachmentSchema(BaseModel):

    filename: str = Field(
        min_length=1,
        max_length=255,
    )
    file_path: str = Field(
        min_length=1,
        max_length=1024,
    )
    file_size: PositiveInt
    file_mime_type: str = Field(
        min_length=3,
        max_length=100,
    )


class AttachmentCreateSchema(AttachmentSchema):
    patient_id: PositiveInt
    appointment_id: PositiveInt


class AttachmentUpdateSchema(AttachmentSchema):
    pass


class AttachmentResponseSchema(AttachmentSchema):
    id: PositiveInt
    patient_id: PositiveInt
    appointment_id: PositiveInt
    uploaded_by_id: PositiveInt
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(
        from_attributes=True,
    )
