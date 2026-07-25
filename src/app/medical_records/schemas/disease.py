from pydantic import BaseModel, ConfigDict, Field, PositiveInt

class DiseaseSchema(BaseModel):
    code: str = Field(
        min_length=4,
        max_length=4,
        pattern=r"^[A-Z]{2}\d{2}$"
    )
    name: str = Field(
        min_length=2,
        max_length=255,
    )
    description: str = Field(
        min_length=3,
        max_length=1000,
    )

class DiseaseCreateSchema(BaseModel):
    pass

class DiseaseUpdateSchema(BaseModel):
    pass

class DiseaseResponseSchema(BaseModel):
    id: PositiveInt
    code: str
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)