from pydantic import BaseModel, ConfigDict, Field

from app.medical_records.schemas.diagnosis import DiagnosisCreateSchema
from app.medical_records.schemas.prescription_item import PrescriptionItemCreateSchema, PrescriptionItemResponseSchema
from app.medical_records.schemas.diagnosis import DiagnosisResponseSchema

class PrescriptionSchema(BaseModel):
    id: int
    recommendations: str | None

    model_config = ConfigDict(from_attributes=True,)

class PrescriptionCreateSchema(BaseModel):
    appointment_id: int
    recommendations: str | None

class FullPrescriptionCreateSchema(BaseModel):
    appointment_id: int
    diagnoses: list[DiagnosisCreateSchema] = Field(min_length=1)
    recommendations: str | None
    prescription_items: list[PrescriptionItemCreateSchema] = []

class FullPrescriptionResponseSchema(BaseModel):
    prescription: PrescriptionSchema
    diagnoses: list[DiagnosisResponseSchema]
    prescription_items: list[PrescriptionItemResponseSchema]

    model_config = ConfigDict(from_attributes=True,)

class PrescriptionUpdateSchema(BaseModel):
    recommendations: str | None = None

class PrescriptionResponseSchema(PrescriptionSchema):
    appointment_id: int

    model_config = ConfigDict(from_attributes=True,)
