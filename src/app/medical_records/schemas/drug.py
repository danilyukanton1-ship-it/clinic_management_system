from pydantic import BaseModel, ConfigDict
from common.enums.dosage_form import DosageForm


class DrugSchema(BaseModel):
    name: str
    international_name: str
    dosage_form: DosageForm
    strength: str
    description: str

class DrugCreateSchema(DrugSchema):
    pass

class DrugUpdateSchema(DrugSchema):
    pass

class DrugGetSchema(DrugSchema):
    pass

class DrugResponseSchema(DrugSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)