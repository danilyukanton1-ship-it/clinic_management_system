from pydantic import BaseModel, ConfigDict


class SpecializationSchema(BaseModel):
    id: int

    name: str

    model_config = ConfigDict(from_attributes=True)

class SpecializationCreateSchema(BaseModel):
    name: str

    description: str

class SpecializationShortSchema(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)