from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from app.medical_records.schemas.diagnosis import (
    DiagnosisCreateFullPrescriptionSchema,
    DiagnosisResponseSchema,
)
from app.medical_records.schemas.prescription_item import (
    PrescriptionItemCreateFullPrescriptionSchema,
    PrescriptionItemResponseSchema,
)


class PrescriptionSchema(BaseModel):
    id: PositiveInt = Field(
        description="Prescription identifier.",
        examples=[1],
    )

    appointment_id: PositiveInt = Field(
        description="Appointment identifier.",
        examples=[42],
    )

    recommendations: str | None = Field(
        default=None,
        min_length=3,
        max_length=2000,
        description="Treatment recommendations for the patient.",
        examples=["Drink plenty of fluids and rest for 5 days."],
    )

    model_config = ConfigDict(
        from_attributes=True,
    )


class PrescriptionCreateSchema(BaseModel):
    appointment_id: PositiveInt = Field(
        description="Appointment identifier.",
        examples=[42],
    )

    recommendations: str | None = Field(
        default=None,
        min_length=3,
        max_length=2000,
        description="Treatment recommendations for the patient.",
        examples=["Drink plenty of fluids and rest for 5 days."],
    )


class FullPrescriptionCreateSchema(BaseModel):
    appointment_id: PositiveInt = Field(
        description="Appointment identifier.",
        examples=[42],
    )

    diagnoses: list[DiagnosisCreateFullPrescriptionSchema] = Field(
        min_length=1,
        description="List of diagnoses included in the prescription.",
    )

    recommendations: str | None = Field(
        default=None,
        min_length=3,
        max_length=2000,
        description="Treatment recommendations for the patient.",
        examples=["Take all medications after meals."],
    )

    prescription_items: list[PrescriptionItemCreateFullPrescriptionSchema] = Field(
        default_factory=list,
        description="List of prescribed medications.",
    )


class FullPrescriptionResponseSchema(BaseModel):
    prescription: PrescriptionSchema = Field(
        description="Prescription information.",
    )

    diagnoses: list[DiagnosisResponseSchema] = Field(
        description="List of diagnoses associated with the prescription.",
    )

    prescription_items: list[PrescriptionItemResponseSchema] = Field(
        description="List of prescribed medications.",
    )

    model_config = ConfigDict(
        from_attributes=True,
    )


class PrescriptionUpdateSchema(BaseModel):
    recommendations: str | None = Field(
        default=None,
        min_length=3,
        max_length=2000,
        description="Updated treatment recommendations for the patient.",
        examples=["Continue treatment for another 7 days."],
    )


class PrescriptionResponseSchema(BaseModel):
    id: PositiveInt = Field(
        description="Prescription identifier.",
        examples=[1],
    )

    appointment_id: PositiveInt = Field(
        description="Appointment identifier.",
        examples=[42],
    )

    recommendations: str | None = Field(
        default=None,
        description="Treatment recommendations for the patient.",
        examples=["Drink plenty of fluids and rest for 5 days."],
    )

    model_config = ConfigDict(
        from_attributes=True,
    )
