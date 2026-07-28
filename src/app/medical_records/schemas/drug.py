from pydantic import BaseModel, ConfigDict, Field, PositiveInt
from common.enums.dosage_form import DosageForm


class DrugSchema(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=255,
    )
    international_name: str = Field(
        min_length=2,
        max_length=255,
    )
    dosage_form: DosageForm
    strength: str = Field(
        min_length=1,
        max_length=100,
    )
    description: str = Field(
        min_length=5,
        max_length=1000,
    )


class DrugCreateSchema(DrugSchema):
    pass


class DrugUpdateSchema(DrugSchema):
    pass


class DrugResponseSchema(BaseModel):
    id: PositiveInt
    name: str
    international_name: str
    dosage_form: DosageForm
    strength: str
    description: str

    model_config = ConfigDict(from_attributes=True)
