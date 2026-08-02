from sqlalchemy.ext.asyncio import AsyncSession

from app.appointments.exceptions.appointment import AppointmentNotFoundException
from app.medical_records.exceptions.disease import DiseaseNotFoundException
from app.medical_records.exceptions.prescription import PrescriptionNotFoundException
from app.medical_records.schemas.diagnosis import (
    DiagnosisCreateSchema,
    DiagnosisUpdateSchema,
    DiagnosisResponseSchema,
)
from app.medical_records.exceptions.diagnosis import (
    DiagnosisNotFoundException,
    DiagnosisCantBeEmptyInPrescriptionException,
)
from app.users.models.user import User
from app.medical_records.policy.diagnosis import DiagnosisPolicy
from common.pagination.schemas import PaginationParams, PaginatedResponse
from common.pagination.utils import build_paginated_response
from db.unit_of_work import UnitOfWork


class DiagnosisService:

    def __init__(self, session: AsyncSession):
        self.policy = DiagnosisPolicy()
        self.uow = UnitOfWork(session)

    async def create(self, data: DiagnosisCreateSchema) -> DiagnosisResponseSchema:
        async with self.uow:
            prescription = await self.uow.prescriptions.get_prescription_by_id(
                prescription_id=data.prescription_id,
            )
            if not prescription:
                raise PrescriptionNotFoundException()
            disease = await self.uow.diseases.get_disease_by_id(
                disease_id=data.disease_id
            )
            if not disease:
                raise DiseaseNotFoundException()
            diagnosis = await self.uow.diagnoses.create_diagnosis(data=data)
        return DiagnosisResponseSchema.model_validate(diagnosis)

    async def update(
        self, diagnosis_id: int, current_user: User, data: DiagnosisUpdateSchema
    ) -> DiagnosisResponseSchema:
        async with self.uow:
            diagnosis = await self.uow.diagnoses.get_diagnosis_by_id(
                diagnosis_id=diagnosis_id
            )
            if not diagnosis:
                raise DiagnosisNotFoundException()
            disease = await self.uow.diseases.get_disease_by_id(
                disease_id=data.disease_id
            )
            if not disease:
                raise DiseaseNotFoundException()
            appointment = await self.uow.appointments.get_appointment_by_diagnosis_id(
                diagnosis_id=diagnosis_id
            )
            if not appointment:
                raise AppointmentNotFoundException()
            self.policy.can_update(user=current_user, appointment=appointment)
            updated_diagnosis = await self.uow.diagnoses.update_diagnosis(
                diagnosis=diagnosis, data=data
            )
        return DiagnosisResponseSchema.model_validate(updated_diagnosis)

    async def delete(self, diagnosis_id: int, current_user: User) -> None:
        async with self.uow:
            diagnosis = await self.uow.diagnoses.get_diagnosis_by_id(
                diagnosis_id=diagnosis_id
            )
            if not diagnosis:
                raise DiagnosisNotFoundException()
            appointment = await self.uow.appointments.get_appointment_by_diagnosis_id(
                diagnosis_id=diagnosis_id
            )
            if not appointment:
                raise AppointmentNotFoundException()
            self.policy.can_delete(user=current_user, appointment=appointment)
            diagnoses = await self.uow.diagnoses.get_diagnoses_by_prescription_id(
                prescription_id=diagnosis.prescription_id
            )
            if len(diagnoses) == 1:
                raise DiagnosisCantBeEmptyInPrescriptionException()

            await self.uow.diagnoses.delete_diagnosis(diagnosis=diagnosis)
        return None

    async def get_by_id(
        self, diagnosis_id: int, current_user: User
    ) -> DiagnosisResponseSchema:
        diagnosis = await self.uow.diagnoses.get_diagnosis_by_id(
            diagnosis_id=diagnosis_id
        )
        if not diagnosis:
            raise DiagnosisNotFoundException()
        appointment = await self.uow.appointments.get_appointment_by_diagnosis_id(
            diagnosis_id=diagnosis_id
        )
        if not appointment:
            raise AppointmentNotFoundException()
        self.policy.can_view(user=current_user, appointment=appointment)
        return DiagnosisResponseSchema.model_validate(diagnosis)

    async def get_by_prescription_id(
        self, prescription_id: int, pagination: PaginationParams, current_user: User
    ) -> PaginatedResponse[DiagnosisResponseSchema]:
        diagnoses = (
            await self.uow.diagnoses.get_diagnoses_by_prescription_id_with_pagination(
                prescription_id=prescription_id, pagination=pagination
            )
        )
        appointment = await self.uow.appointments.get_appointment_by_diagnosis_id(
            diagnosis_id=diagnoses.items[0].id
        )
        if not appointment:
            raise AppointmentNotFoundException()
        self.policy.can_view(user=current_user, appointment=appointment)
        return build_paginated_response(
            items=diagnoses.items,
            total=diagnoses.total,
            pagination=pagination,
            schema=DiagnosisResponseSchema,
        )

    async def get_by_disease_id(
        self, disease_id: int, pagination: PaginationParams
    ) -> PaginatedResponse[DiagnosisResponseSchema]:
        diagnoses = await self.uow.diagnoses.get_diagnoses_by_disease_id(
            disease_id=disease_id, pagination=pagination
        )
        return build_paginated_response(
            items=diagnoses.items,
            total=diagnoses.total,
            pagination=pagination,
            schema=DiagnosisResponseSchema,
        )
