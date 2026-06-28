from pydantic import BaseModel, ConfigDict, Field


class DiseaseCreateSchema(BaseModel):
    code: str = Field(
        pattern=r"^[A-Z]{2}\d{2}$"
    )
    name: str
    description: str

class DiseaseUpdateSchema(BaseModel):
    code: str = Field(
        pattern=r"^[A-Z]{2}\d{2}$"
    )
    name: str
    description: str

class DiseaseGetSchema(BaseModel):
    code: str
    name: str | None = None

class DiseaseResponseSchema(BaseModel):
    id: int
    code: str
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)