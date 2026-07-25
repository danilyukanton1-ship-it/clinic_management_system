from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from app.medical_records.schemas.diagnosis import DiagnosisCreateSchema
from app.medical_records.schemas.prescription_item import PrescriptionItemCreateSchema, PrescriptionItemResponseSchema
from app.medical_records.schemas.diagnosis import DiagnosisResponseSchema

class PrescriptionSchema(BaseModel):
    id: PositiveInt
    recommendations: str | None = Field(
        default=None,
        min_length=3,
        max_length=2000,
    )

    model_config = ConfigDict(from_attributes=True,)

class PrescriptionCreateSchema(BaseModel):
    appointment_id: PositiveInt
    recommendations: str | None = Field(
        default=None,
        min_length=3,
        max_length=2000,
    )

class FullPrescriptionCreateSchema(BaseModel):
    appointment_id: PositiveInt
    diagnoses: list[DiagnosisCreateSchema] = Field(min_length=1)
    recommendations: str | None = Field(
        default=None,
        min_length=3,
        max_length=2000,
    )
    prescription_items: list[PrescriptionItemCreateSchema] = Field(
        default_factory=list
    )

class FullPrescriptionResponseSchema(BaseModel):
    prescription: PrescriptionSchema
    diagnoses: list[DiagnosisResponseSchema]
    prescription_items: list[PrescriptionItemResponseSchema]

    model_config = ConfigDict(from_attributes=True,)

class PrescriptionUpdateSchema(BaseModel):
    recommendations: str | None = Field(
        default=None,
        min_length=3,
        max_length=2000,
    )

class PrescriptionResponseSchema(BaseModel):
    id: PositiveInt
    appointment_id: PositiveInt
    recommendations: str | None = None

    model_config = ConfigDict(from_attributes=True,)
