from pydantic import BaseModel

from app.schemas.disease import DiseaseSchema

class DiagnosisSchema(BaseModel):
    id: int

    disease: DiseaseSchema

    notes: str | None