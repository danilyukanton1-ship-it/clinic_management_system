from pydantic import BaseModel

from app.medical_records.schemas.disease import DiseaseSchema

class DiagnosisSchema(BaseModel):
    id: int

    disease: DiseaseSchema

    notes: str | None