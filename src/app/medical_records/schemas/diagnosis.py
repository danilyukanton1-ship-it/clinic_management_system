from pydantic import BaseModel, ConfigDict


class DiagnosisSchema(BaseModel):
    prescription_id: int
    disease_id: int
    notes: str | None = None

class DiagnosisCreateSchema(DiagnosisSchema):
    pass

class DiagnosisUpdateSchema(BaseModel):
    disease_id: int
    notes: str | None = None


class DiagnosisResponseSchema(DiagnosisSchema):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
