from pydantic import BaseModel, ConfigDict, Field, PositiveInt


class DiagnosisSchema(BaseModel):
    prescription_id: PositiveInt
    disease_id: PositiveInt
    notes: str | None = Field(default=None, min_length=3, max_length=255)


class DiagnosisCreateSchema(DiagnosisSchema):
    pass


class DiagnosisCreateFullPrescriptionSchema(BaseModel):
    disease_id: PositiveInt
    notes: str | None = Field(default=None, min_length=3, max_length=255)


class DiagnosisUpdateSchema(BaseModel):
    disease_id: PositiveInt
    notes: str | None = Field(default=None, min_length=3, max_length=255)


class DiagnosisResponseSchema(BaseModel):
    id: PositiveInt
    prescription_id: PositiveInt
    disease_id: PositiveInt
    notes: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )
