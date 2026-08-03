from pydantic import BaseModel, ConfigDict, Field, PositiveInt


class DiseaseSchema(BaseModel):
    code: str = Field(
        min_length=4,
        max_length=4,
        pattern=r"^[A-Z]{2}\d{2}$",
        description="Disease code.",
        examples=["AB12"],
    )

    name: str = Field(
        min_length=2,
        max_length=128,
        description="Disease name.",
        examples=["Acute bronchitis"],
    )

    description: str = Field(
        min_length=3,
        max_length=1000,
        description="Detailed description of the disease.",
        examples=[
            "Inflammation of the bronchial tubes causing cough and difficulty breathing."
        ],
    )


class DiseaseCreateSchema(DiseaseSchema):
    pass


class DiseaseUpdateSchema(DiseaseSchema):
    pass


class DiseaseResponseSchema(BaseModel):
    id: PositiveInt = Field(
        description="Disease identifier.",
        examples=[1],
    )

    code: str = Field(
        description="Disease code.",
        examples=["AB12"],
    )

    name: str = Field(
        description="Disease name.",
        examples=["Acute bronchitis"],
    )

    description: str = Field(
        description="Detailed description of the disease.",
        examples=[
            "Inflammation of the bronchial tubes causing cough and difficulty breathing."
        ],
    )

    model_config = ConfigDict(from_attributes=True)
