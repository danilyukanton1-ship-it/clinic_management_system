from sqlalchemy.ext.asyncio import AsyncSession

from app.appoinments.exceptions.appointment import AppointmentNotFoundException
from app.medical_records.schemas.diagnosis import DiagnosisCreateSchema, DiagnosisUpdateSchema
from app.medical_records.exceptions.diagnosis import DiagnosisNotFoundException, \
    DiagnosisCantBeEmptyInPrescriptionException
from app.medical_records.models.diagnosis import Diagnosis
from app.users.models.user import User
from app.medical_records.policy.diagnosis import DiagnosisPolicy
from db.unit_of_work import UnitOfWork

class DiagnosisService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.policy = DiagnosisPolicy()
        self.uow = UnitOfWork(session)

    async def create(self, data: DiagnosisCreateSchema) -> Diagnosis:
        async with self.uow:
            diagnosis = await self.uow.diagnoses.create_diagnosis(data=data)
        return diagnosis

    async def update(self, diagnosis_id: int, current_user: User, data: DiagnosisUpdateSchema) -> Diagnosis:
        async with self.uow:
            diagnosis = await self.uow.diagnoses.get_diagnosis_by_id(diagnosis_id=diagnosis_id)
            if not diagnosis:
                raise DiagnosisNotFoundException()
            appointment = await self.uow.appointments.get_appointment_by_diagnosis_id(diagnosis_id=diagnosis_id)
            if not appointment:
                raise AppointmentNotFoundException()
            self.policy.can_update(user=current_user, appointment=appointment)
            updated_diagnosis = await self.uow.diagnoses.update_diagnosis(diagnosis=diagnosis, data=data)
        return updated_diagnosis

    async def delete(self, diagnosis_id: int, current_user: User) -> None:
        async with self.uow:
            diagnosis = await self.uow.diagnoses.get_diagnosis_by_id(diagnosis_id=diagnosis_id)
            if not diagnosis:
                raise DiagnosisNotFoundException()
            appointment = await self.uow.appointments.get_appointment_by_diagnosis_id(diagnosis_id=diagnosis_id)
            if not appointment:
                raise AppointmentNotFoundException()
            self.policy.can_delete(user=current_user, appointment=appointment)
            diagnoses = await self.uow.diagnoses.get_diagnoses_by_prescription_id(prescription_id=diagnosis.prescription_id)
            if len(diagnoses) == 1:
                raise DiagnosisCantBeEmptyInPrescriptionException()

            await self.uow.diagnoses.delete_diagnosis(diagnosis=diagnosis)
        return None

    async def get_by_id(self, diagnosis_id: int, current_user: User) -> Diagnosis:
        diagnosis = await self.uow.diagnoses.get_diagnosis_by_id(diagnosis_id)
        if not diagnosis:
            raise DiagnosisNotFoundException()
        appointment = await self.uow.appointments.get_appointment_by_diagnosis_id(diagnosis_id=diagnosis_id)
        if not appointment:
            raise AppointmentNotFoundException()
        self.policy.can_view(user=current_user, appointment=appointment)
        return diagnosis

    async def get_all(self) -> list[Diagnosis]:
        diagnosis = await self.uow.diagnoses.get_all_diagnoses()
        if not diagnosis:
            raise DiagnosisNotFoundException()
        return diagnosis

    async def get_by_prescription_id(self, prescription_id: int, current_user: User) -> list[Diagnosis]:
        diagnoses = await self.uow.diagnoses.get_diagnoses_by_prescription_id(prescription_id=prescription_id)
        if not diagnoses:
            raise DiagnosisNotFoundException()
        appointment = await self.uow.appointments.get_appointment_by_diagnosis_id(diagnosis_id=diagnoses[0].id)
        if not appointment:
            raise AppointmentNotFoundException()
        self.policy.can_view(user=current_user, appointment=appointment)
        return diagnoses

    async def get_by_disease_id(self, disease_id: int) -> list[Diagnosis]:
        diagnosis = await self.uow.diagnoses.get_diagnoses_by_disease_id(disease_id=disease_id)
        if not diagnosis:
            raise DiagnosisNotFoundException()
        return diagnosis
