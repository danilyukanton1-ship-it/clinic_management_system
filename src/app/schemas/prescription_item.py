from pydantic import BaseModel, ConfigDict

from app.schemas.drug import DrugSchema

class PrescriptionItemSchema(BaseModel):
    id: int
    drug: DrugSchema

    dosage: str
    frequency: str
    duration_days: int

    model_config = ConfigDict(
        from_attributes=True,
    )
