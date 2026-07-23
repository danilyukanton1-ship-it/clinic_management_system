from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AttachmentSchema(BaseModel):

    filename: str
    file_path: str
    file_size: int
    file_mime_type: str



class AttachmentCreateSchema(AttachmentSchema):
    patient_id: int
    appointment_id: int

class AttachmentUpdateSchema(AttachmentSchema):
    pass

class AttachmentResponseSchema(AttachmentSchema):
    id: int
    patient_id: int
    appointment_id: int
    uploaded_by_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(
        from_attributes=True,
    )


