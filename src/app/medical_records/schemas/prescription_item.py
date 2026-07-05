from pydantic import BaseModel, ConfigDict

class PrescriptionItemSchema(BaseModel):
    prescription_id: int
    drug_id: int
    dosage: str
    frequency: str
    duration_days: int

class PrescriptionItemCreateSchema(PrescriptionItemSchema):
    pass

class PrescriptionItemResponseSchema(PrescriptionItemSchema):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )

class PrescriptionItemUpdateSchema(BaseModel):
    drug_id: int
    dosage: str
    frequency: str
    duration_days: int