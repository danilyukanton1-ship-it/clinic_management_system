from sqlalchemy.ext.asyncio import AsyncSession
from app.medical_records.schemas.diagnosis import DiagnosisCreateSchema, DiagnosisUpdateSchema
from app.medical_records.exceptions.diagnosis import DiagnosisNotFoundException
from app.medical_records.models.diagnosis import Diagnosis
from db.unit_of_work import UnitOfWork

class DiagnosisService:

    def __init__(self, session: AsyncSession):
        self.session = session

        self.uow = UnitOfWork(session)

    async def create(self, data: DiagnosisCreateSchema) -> Diagnosis:
        async with self.uow:
            diagnosis = await self.uow.diagnoses.create_diagnosis(data=data)
        return diagnosis

    async def update(self, diagnosis_id: int, data: DiagnosisUpdateSchema) -> Diagnosis:
        diagnosis = await self.uow.diagnoses.get_diagnosis_by_id(diagnosis_id=diagnosis_id)
        if not diagnosis:
            raise DiagnosisNotFoundException()
        async with self.uow:
            updated_diagnosis = await self.uow.diagnoses.update_diagnosis(diagnosis=diagnosis, data=data)
        return updated_diagnosis

    async def delete(self, diagnosis_id: int) -> None:
        diagnosis = await self.uow.diagnoses.get_diagnosis_by_id(diagnosis_id=diagnosis_id)
        if not diagnosis:
            raise DiagnosisNotFoundException()
        async with self.uow:
            await self.uow.diagnoses.delete_diagnosis(diagnosis=diagnosis)
        return None

    async def get_by_id(self, diagnosis_id: int) -> Diagnosis:
        diagnosis = await self.uow.diagnoses.get_diagnosis_by_id(diagnosis_id)
        if not diagnosis:
            raise DiagnosisNotFoundException()
        return diagnosis

    async def get_all(self) -> list[Diagnosis]:
        diagnosis = await self.uow.diagnoses.get_all_diagnoses()
        if not diagnosis:
            raise DiagnosisNotFoundException()
        return diagnosis

    async def get_by_appointment_id(self, appointment_id: int) -> Diagnosis:
        diagnosis = await self.uow.diagnoses.get_diagnoses_by_appointment_id(appointment_id=appointment_id)
        if not diagnosis:
            raise DiagnosisNotFoundException()
        return diagnosis

    async def get_by_disease_id(self, disease_id: int) -> Diagnosis:
        diagnosis = await self.uow.diagnoses.get_diagnoses_by_disease_id(disease_id=disease_id)
        if not diagnosis:
            raise DiagnosisNotFoundException()
        return diagnosis
