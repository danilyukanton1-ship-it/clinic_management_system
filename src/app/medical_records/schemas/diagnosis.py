from pydantic import BaseModel, ConfigDict


class DiagnosisSchema(BaseModel):
    appointment_id: int
    disease_id: int
    notes: str | None = None

class DiagnosisCreateSchema(DiagnosisSchema):
    pass

class DiagnosisUpdateSchema(DiagnosisSchema):
    pass

class DiagnosisResponseSchema(DiagnosisSchema):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )