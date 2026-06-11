from pydantic import BaseModel, ConfigDict


class AttachmentSchema(BaseModel):
    id: int

    filename: str
    file_mime_type: str

    model_config = ConfigDict(from_attributes=True)