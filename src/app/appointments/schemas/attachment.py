from datetime import datetime

from fastapi import Form
from pydantic import BaseModel, ConfigDict, Field, PositiveInt


class AttachmentCreateSchema(BaseModel):
    patient_id: PositiveInt = Field(
        description="Patient identifier.",
        examples=[15],
    )

    appointment_id: PositiveInt = Field(
        description="Appointment identifier.",
        examples=[42],
    )

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
        description="Attachment filename.",
        examples=["blood_test_results.pdf"],
    )


class AttachmentResponseSchema(BaseModel):
    id: PositiveInt = Field(
        description="Attachment identifier.",
        examples=[1],
    )

    filename: str = Field(
        description="Attachment filename.",
        examples=["blood_test_results.pdf"],
    )

    patient_id: PositiveInt = Field(
        description="Patient identifier.",
        examples=[15],
    )

    appointment_id: PositiveInt = Field(
        description="Appointment identifier.",
        examples=[42],
    )

    uploaded_by_id: PositiveInt = Field(
        description="Identifier of the user who uploaded the attachment.",
        examples=[3],
    )

    file_size: PositiveInt = Field(
        description="Attachment size in bytes.",
        examples=[524288],
    )

    file_mime_type: str = Field(
        description="MIME type of the uploaded file.",
        examples=["application/pdf"],
    )

    created_at: datetime = Field(
        description="Timestamp when the attachment was created.",
        examples=["2026-08-03T14:25:31Z"],
    )

    updated_at: datetime = Field(
        description="Timestamp when the attachment was last updated.",
        examples=["2026-08-03T15:02:18Z"],
    )

    model_config = ConfigDict(
        from_attributes=True,
    )


class AttachmentSchema(BaseModel):
    filename: str = Field(
        min_length=1,
        max_length=255,
        description="Attachment filename.",
        examples=["blood_test_results.pdf"],
    )

    file_path: str = Field(
        min_length=1,
        max_length=1024,
        description="Path to the file in object storage.",
        examples=["attachments/2026/08/blood_test_results.pdf"],
    )

    file_size: PositiveInt = Field(
        description="Attachment size in bytes.",
        examples=[524288],
    )

    file_mime_type: str = Field(
        min_length=3,
        max_length=100,
        description="MIME type of the uploaded file.",
        examples=["application/pdf"],
    )

    patient_id: PositiveInt = Field(
        description="Patient identifier.",
        examples=[15],
    )

    appointment_id: PositiveInt = Field(
        description="Appointment identifier.",
        examples=[42],
    )
