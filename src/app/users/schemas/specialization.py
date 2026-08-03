from pydantic import BaseModel, ConfigDict, Field, PositiveInt


class SpecializationSchema(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=100,
        description="Medical specialization name.",
        examples=["Cardiology"],
    )

    description: str = Field(
        min_length=3,
        max_length=2000,
        description="Detailed description of the medical specialization.",
        examples=[
            "Medical specialty focused on the diagnosis, treatment, and prevention of cardiovascular diseases."
        ],
    )


class SpecializationResponseSchema(BaseModel):
    id: PositiveInt = Field(
        description="Medical specialization identifier.",
        examples=[1],
    )

    name: str = Field(
        description="Medical specialization name.",
        examples=["Cardiology"],
    )

    description: str = Field(
        description="Detailed description of the medical specialization.",
        examples=[
            "Medical specialty focused on the diagnosis, treatment, and prevention of cardiovascular diseases."
        ],
    )

    model_config = ConfigDict(from_attributes=True)


class SpecializationCreateSchema(SpecializationSchema):
    pass


class SpecializationUpdateSchema(SpecializationSchema):
    pass
