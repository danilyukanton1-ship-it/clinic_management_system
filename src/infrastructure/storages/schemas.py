from pydantic import BaseModel


class StoredFileSchema(BaseModel):
    key: str
    size: int
    content_type: str


class DownloadUrl(BaseModel):
    url: str
