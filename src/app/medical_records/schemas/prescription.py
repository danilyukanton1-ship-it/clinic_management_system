from pydantic import BaseModel, ConfigDict


class PrescriptionSchema(BaseModel):
    id: int
    recommendations: str | None

    model_config = ConfigDict(from_attributes=True)
