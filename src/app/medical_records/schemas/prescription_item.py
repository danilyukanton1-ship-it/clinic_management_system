from pydantic import BaseModel, ConfigDict, Field, PositiveInt


class PrescriptionItemSchema(BaseModel):
    prescription_id: PositiveInt = Field(
        description="Prescription identifier.",
        examples=[12],
    )

    drug_id: PositiveInt = Field(
        description="Drug identifier.",
        examples=[5],
    )

    dosage: str = Field(
        min_length=1,
        max_length=100,
        description="Medication dosage.",
        examples=["1 tablet"],
    )

    frequency: str = Field(
        min_length=1,
        max_length=100,
        description="Medication administration frequency.",
        examples=["Twice daily"],
    )

    duration_days: PositiveInt = Field(
        description="Treatment duration in days.",
        examples=[7],
    )


class PrescriptionItemCreateSchema(PrescriptionItemSchema):
    pass


class PrescriptionItemCreateFullPrescriptionSchema(BaseModel):
    drug_id: PositiveInt = Field(
        description="Drug identifier.",
        examples=[5],
    )

    dosage: str = Field(
        min_length=1,
        max_length=100,
        description="Medication dosage.",
        examples=["1 tablet"],
    )

    frequency: str = Field(
        min_length=1,
        max_length=100,
        description="Medication administration frequency.",
        examples=["Twice daily"],
    )

    duration_days: PositiveInt = Field(
        description="Treatment duration in days.",
        examples=[7],
    )


class PrescriptionItemResponseSchema(BaseModel):
    id: PositiveInt = Field(
        description="Prescription item identifier.",
        examples=[1],
    )

    prescription_id: PositiveInt = Field(
        description="Prescription identifier.",
        examples=[12],
    )

    drug_id: PositiveInt = Field(
        description="Drug identifier.",
        examples=[5],
    )

    dosage: str = Field(
        description="Medication dosage.",
        examples=["1 tablet"],
    )

    frequency: str = Field(
        description="Medication administration frequency.",
        examples=["Twice daily"],
    )

    duration_days: PositiveInt = Field(
        description="Treatment duration in days.",
        examples=[7],
    )

    model_config = ConfigDict(
        from_attributes=True,
    )


class PrescriptionItemUpdateSchema(BaseModel):
    drug_id: PositiveInt = Field(
        description="Drug identifier.",
        examples=[5],
    )

    dosage: str = Field(
        min_length=1,
        max_length=100,
        description="Medication dosage.",
        examples=["1 tablet"],
    )

    frequency: str = Field(
        min_length=1,
        max_length=100,
        description="Medication administration frequency.",
        examples=["Twice daily"],
    )

    duration_days: PositiveInt = Field(
        description="Treatment duration in days.",
        examples=[10],
    )
