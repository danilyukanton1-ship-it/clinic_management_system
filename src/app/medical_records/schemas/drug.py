from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from common.enums.dosage_form import DosageForm


class DrugSchema(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=255,
        description="Drug trade name.",
        examples=["Nurofen"],
    )

    international_name: str = Field(
        min_length=2,
        max_length=255,
        description="International nonproprietary name (INN).",
        examples=["Ibuprofen"],
    )

    dosage_form: DosageForm = Field(
        description="Pharmaceutical dosage form.",
        examples=["TABLET"],
    )

    strength: str = Field(
        min_length=1,
        max_length=100,
        description="Drug strength.",
        examples=["200 mg"],
    )

    description: str = Field(
        min_length=5,
        max_length=1000,
        description="Detailed description of the drug.",
        examples=[
            "Nonsteroidal anti-inflammatory drug used to relieve pain, reduce inflammation, and lower fever."
        ],
    )


class DrugCreateSchema(DrugSchema):
    pass


class DrugUpdateSchema(DrugSchema):
    pass


class DrugResponseSchema(BaseModel):
    id: PositiveInt = Field(
        description="Drug identifier.",
        examples=[1],
    )

    name: str = Field(
        description="Drug trade name.",
        examples=["Nurofen"],
    )

    international_name: str = Field(
        description="International nonproprietary name (INN).",
        examples=["Ibuprofen"],
    )

    dosage_form: DosageForm = Field(
        description="Pharmaceutical dosage form.",
        examples=["TABLET"],
    )

    strength: str = Field(
        description="Drug strength.",
        examples=["200 mg"],
    )

    description: str = Field(
        description="Detailed description of the drug.",
        examples=[
            "Nonsteroidal anti-inflammatory drug used to relieve pain, reduce inflammation, and lower fever."
        ],
    )

    model_config = ConfigDict(from_attributes=True)
