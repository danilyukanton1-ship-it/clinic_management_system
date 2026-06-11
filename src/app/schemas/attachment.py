from pydantic import BaseModel, ConfigDict


class AttachmentSchema(BaseModel):
    id: int

    filename: str
    file_mime_type: str
    file_size: int

    model_config = ConfigDict(from_attributes=True)