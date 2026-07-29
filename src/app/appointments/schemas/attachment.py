from datetime import datetime
from pydantic import BaseModel, ConfigDict
from pydantic import PositiveInt, Field
from fastapi import Form


class AttachmentCreateSchema(BaseModel):
    patient_id: PositiveInt
    appointment_id: PositiveInt

    @classmethod
    def as_form(
        cls,
        patient_id: PositiveInt = Form(...),
        appointment_id: PositiveInt = Form(...),
    ) -> "AttachmentCreateSchema":
        return cls(
            patient_id=patient_id,
            appointment_id=appointment_id,
        )


class AttachmentUpdateSchema(BaseModel):
    filename: str = Field(
        min_length=1,
        max_length=255,
    )


class AttachmentResponseSchema(BaseModel):
    id: PositiveInt
    filename: str
    patient_id: PositiveInt
    appointment_id: PositiveInt
    uploaded_by_id: PositiveInt
    file_size: PositiveInt
    file_mime_type: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(
        from_attributes=True,
    )


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
    patient_id: PositiveInt
    appointment_id: PositiveInt
