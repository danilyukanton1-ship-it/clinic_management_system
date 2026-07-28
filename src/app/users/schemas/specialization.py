from pydantic import BaseModel, ConfigDict, PositiveInt, Field


class SpecializationSchema(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=100,
    )

    description: str = Field(
        min_length=3,
        max_length=2000,
    )


class SpecializationResponseSchema(BaseModel):
    id: PositiveInt
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class SpecializationCreateSchema(SpecializationSchema):
    pass


class SpecializationUpdateSchema(SpecializationSchema):
    pass
