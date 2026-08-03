from pydantic import BaseModel, ConfigDict, Field, PositiveInt


class DiagnosisSchema(BaseModel):
    prescription_id: PositiveInt = Field(
        description="Prescription identifier.",
        examples=[12],
    )

    disease_id: PositiveInt = Field(
        description="Disease identifier.",
        examples=[45],
    )

    notes: str | None = Field(
        default=None,
        min_length=3,
        max_length=255,
        description="Additional notes about the diagnosis.",
        examples=["Patient reports mild symptoms."],
    )


class DiagnosisCreateSchema(DiagnosisSchema):
    pass


class DiagnosisCreateFullPrescriptionSchema(BaseModel):
    disease_id: PositiveInt = Field(
        description="Disease identifier.",
        examples=[45],
    )

    notes: str | None = Field(
        default=None,
        min_length=3,
        max_length=255,
        description="Additional notes about the diagnosis.",
        examples=["Patient reports mild symptoms."],
    )


class DiagnosisUpdateSchema(BaseModel):
    disease_id: PositiveInt = Field(
        description="Disease identifier.",
        examples=[45],
    )

    notes: str | None = Field(
        default=None,
        min_length=3,
        max_length=255,
        description="Additional notes about the diagnosis.",
        examples=["Symptoms have significantly improved."],
    )


class DiagnosisResponseSchema(BaseModel):
    id: PositiveInt = Field(
        description="Diagnosis identifier.",
        examples=[1],
    )

    prescription_id: PositiveInt = Field(
        description="Prescription identifier.",
        examples=[12],
    )

    disease_id: PositiveInt = Field(
        description="Disease identifier.",
        examples=[45],
    )

    notes: str | None = Field(
        default=None,
        description="Additional notes about the diagnosis.",
        examples=["Patient reports mild symptoms."],
    )

    model_config = ConfigDict(
        from_attributes=True,
    )
