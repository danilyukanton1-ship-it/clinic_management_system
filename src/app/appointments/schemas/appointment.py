import datetime

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, field_validator

from common.enums.appointment_status import AppointmentStatus


class AppointmentCreateSchema(BaseModel):
    patient_id: PositiveInt = Field(
        description="Patient identifier",
        examples=[15],
    )
    doctor_id: PositiveInt = Field(
        description="Doctor identifier",
        examples=[8],
    )

    slot_id: PositiveInt = Field(
        description="Slot identifier",
        examples=[42],
    )

    complaint: str | None = Field(
        default=None,
        min_length=3,
        max_length=1000,
        description="Patient complaints text",
        examples=["Severe headache for three days."],
    )

    @field_validator("complaint")
    @classmethod
    def validate_complaint(cls, v):
        v = v.strip()
        return v if v else None


class AppointmentUpdateSchema(BaseModel):
    complaint: str | None = Field(
        default=None,
        min_length=3,
        max_length=1000,
        description="Patient complaints text",
        examples=["Severe headache for three days."],
    )
    status: AppointmentStatus | None = Field(
        default=None, description="Appointment status", examples=["scheduled"]
    )


class AppointmentResponseSchema(BaseModel):
    id: PositiveInt = Field(description="Appointment identifier", examples=[4])

    patient_id: PositiveInt = Field(
        description="Patient identifier",
        examples=[15],
    )
    doctor_id: PositiveInt = Field(
        description="Doctor identifier",
        examples=[8],
    )

    status: AppointmentStatus = Field(
        description="Appointment status",
        examples=["scheduled"],
    )
    slot_id: PositiveInt = Field(
        description="Slot identifier",
        examples=[42],
    )

    complaint: str | None = Field(
        default=None,
        description="Patient complaints text",
        examples=["Severe headache for three days."],
    )

    created_at: datetime.datetime = Field(
        description="Timestamp when the appointment was created.",
        examples=["2026-08-03T14:25:31+00:00"],
    )

    model_config = ConfigDict(from_attributes=True)
