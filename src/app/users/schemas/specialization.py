from pydantic import BaseModel, ConfigDict

class SpecializationSchema(BaseModel):
    name: str

    description: str

class SpecializationResponseSchema(SpecializationSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)

class SpecializationCreateSchema(SpecializationSchema):
    pass

class SpecializationUpdateSchema(SpecializationSchema):
    pass