from pydantic import BaseModel, ConfigDict, Field, PositiveInt


class PrescriptionItemSchema(BaseModel):
    prescription_id: PositiveInt
    drug_id: PositiveInt
    dosage: str = Field(
        min_length=1,
        max_length=100,
    )
    frequency: str = Field(
        min_length=1,
        max_length=100,
    )
    duration_days: PositiveInt


class PrescriptionItemCreateSchema(PrescriptionItemSchema):
    pass


class PrescriptionItemCreateFullPrescriptionSchema(BaseModel):
    drug_id: PositiveInt
    dosage: str = Field(
        min_length=1,
        max_length=100,
    )
    frequency: str = Field(
        min_length=1,
        max_length=100,
    )
    duration_days: PositiveInt


class PrescriptionItemResponseSchema(BaseModel):
    id: PositiveInt

    prescription_id: PositiveInt
    drug_id: PositiveInt
    dosage: str
    frequency: str
    duration_days: PositiveInt

    model_config = ConfigDict(
        from_attributes=True,
    )


class PrescriptionItemUpdateSchema(BaseModel):
    drug_id: PositiveInt
    dosage: str = Field(
        min_length=1,
        max_length=100,
    )
    frequency: str = Field(
        min_length=1,
        max_length=100,
    )
    duration_days: PositiveInt
