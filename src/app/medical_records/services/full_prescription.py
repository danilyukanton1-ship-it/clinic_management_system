from sqlalchemy.ext.asyncio import AsyncSession

from app.appointments.exceptions.appointment import AppointmentNotFoundException
from app.medical_records.exceptions.disease import DiseaseNotFoundException
from app.medical_records.exceptions.drug import DrugNotFoundException
from app.medical_records.exceptions.prescription import PrescriptionNotFoundException
from app.medical_records.models.diagnosis import Diagnosis
from app.medical_records.models.prescription import Prescription
from app.medical_records.models.prescription_item import PrescriptionItem
from app.medical_records.policy.prescription import PrescriptionPolicy
from app.medical_records.schemas.diagnosis import (
    DiagnosisCreateSchema,
    DiagnosisResponseSchema,
)
from app.medical_records.schemas.prescription import (
    FullPrescriptionCreateSchema,
    FullPrescriptionResponseSchema,
    PrescriptionCreateSchema,
    PrescriptionSchema,
)
from app.medical_records.schemas.prescription_item import (
    PrescriptionItemResponseSchema,
    PrescriptionItemCreateSchema,
)
from app.users.models.user import User
from db.unit_of_work import UnitOfWork


class FullPrescriptionService:
    def __init__(self, session: AsyncSession):
        self.policy = PrescriptionPolicy()
        self.uow = UnitOfWork(session)

    async def _create_prescription(
        self, data: FullPrescriptionCreateSchema
    ) -> Prescription:
        appointment = await self.uow.appointments.get_appointment_by_id(
            appointment_id=data.appointment_id
        )
        if not appointment:
            raise AppointmentNotFoundException()
        prescription_schema = PrescriptionCreateSchema(
            appointment_id=data.appointment_id,
            recommendations=data.recommendations,
        )
        prescription = await self.uow.prescriptions.create_prescription(
            data=prescription_schema
        )
        return prescription

    async def _create_prescription_items(
        self, data: FullPrescriptionCreateSchema, prescription_id: int
    ) -> list[PrescriptionItem]:
        prescription_items = []
        drug_ids = [item.drug_id for item in data.prescription_items]
        drugs = await self.uow.drugs.get_drugs_by_ids(drug_ids=drug_ids)
        drugs_map = {drug.id: drug for drug in drugs}
        for item in data.prescription_items:
            drug = drugs_map.get(item.drug_id)
            if not drug:
                raise DrugNotFoundException()
            schema = PrescriptionItemCreateSchema(
                prescription_id=prescription_id,
                drug_id=item.drug_id,
                dosage=item.dosage,
                frequency=item.frequency,
                duration_days=item.duration_days,
            )
            prescription_item = (
                await self.uow.prescription_items.create_prescription_item(data=schema)
            )
            prescription_items.append(prescription_item)
        return prescription_items

    async def _create_diagnoses(
        self, data: FullPrescriptionCreateSchema, prescription_id: int
    ) -> list[Diagnosis]:
        diagnoses = []
        disease_ids = [item.disease_id for item in data.diagnoses]
        diseases = await self.uow.diseases.get_diseases_by_ids(disease_ids=disease_ids)
        diseases_map = {disease.id: disease for disease in diseases}
        for item in data.diagnoses:
            disease = diseases_map.get(item.disease_id)
            if not disease:
                raise DiseaseNotFoundException()
            schema = DiagnosisCreateSchema(
                prescription_id=prescription_id,
                disease_id=item.disease_id,
                notes=item.notes,
            )
            diagnosis = await self.uow.diagnoses.create_diagnosis(data=schema)
            diagnoses.append(diagnosis)
        return diagnoses

    async def _get_prescription_response(
        self, prescription: Prescription
    ) -> FullPrescriptionResponseSchema:
        if not prescription:
            raise PrescriptionNotFoundException()
        diagnoses = await self.uow.diagnoses.get_diagnoses_by_prescription_id(
            prescription_id=prescription.id
        )
        prescription_items = (
            await self.uow.prescription_items.get_prescription_items_by_prescription_id(
                prescription_id=prescription.id,
            )
        )
        schema = FullPrescriptionResponseSchema(
            prescription=PrescriptionSchema.model_validate(prescription),
            diagnoses=[
                DiagnosisResponseSchema.model_validate(diagnosis)
                for diagnosis in diagnoses
            ],
            prescription_items=[
                PrescriptionItemResponseSchema.model_validate(item)
                for item in prescription_items
            ],
        )
        return schema

    async def create_full_prescription(
        self, data: FullPrescriptionCreateSchema
    ) -> FullPrescriptionResponseSchema:
        async with self.uow:
            prescription = await self._create_prescription(data=data)
            diagnoses = await self._create_diagnoses(
                data=data, prescription_id=prescription.id
            )
            prescription_items = await self._create_prescription_items(
                data=data, prescription_id=prescription.id
            )
        schema = FullPrescriptionResponseSchema(
            prescription=PrescriptionSchema.model_validate(prescription),
            diagnoses=[
                DiagnosisResponseSchema.model_validate(diagnosis)
                for diagnosis in diagnoses
            ],
            prescription_items=[
                PrescriptionItemResponseSchema.model_validate(item)
                for item in prescription_items
            ],
        )
        return FullPrescriptionResponseSchema.model_validate(schema)

    async def get_full_prescription_by_appointment_id(
        self, appointment_id: int, current_user: User
    ) -> FullPrescriptionResponseSchema:
        async with self.uow:
            prescription = (
                await self.uow.prescriptions.get_prescription_by_appointment_id(
                    appointment_id=appointment_id
                )
            )
            if not prescription:
                raise PrescriptionNotFoundException()
            appointment = await self.uow.appointments.get_appointment_by_id(
                appointment_id=appointment_id
            )
            if not appointment:
                raise AppointmentNotFoundException()
            self.policy.can_view(user=current_user, appointment=appointment)
            schema = await self._get_prescription_response(prescription=prescription)
        return FullPrescriptionResponseSchema.model_validate(schema)

    async def get_full_prescription_by_prescription_id(
        self, prescription_id: int, current_user: User
    ) -> FullPrescriptionResponseSchema:
        async with self.uow:
            prescription = await self.uow.prescriptions.get_prescription_by_id(
                prescription_id=prescription_id
            )
            if not prescription:
                raise PrescriptionNotFoundException()
            appointment = (
                await self.uow.appointments.get_appointment_by_prescription_id(
                    prescription_id=prescription.id
                )
            )
            if not appointment:
                raise AppointmentNotFoundException()
            self.policy.can_view(user=current_user, appointment=appointment)
            schema = await self._get_prescription_response(prescription=prescription)
            return FullPrescriptionResponseSchema.model_validate(schema)

    async def delete_full_prescription(
        self, prescription_id: int, current_user: User
    ) -> None:
        async with self.uow:
            prescription = await self.uow.prescriptions.get_prescription_by_id(
                prescription_id=prescription_id
            )
            if not prescription:
                raise PrescriptionNotFoundException()
            appointment = (
                await self.uow.appointments.get_appointment_by_prescription_id(
                    prescription_id=prescription.id
                )
            )
            if not appointment:
                raise AppointmentNotFoundException()
            self.policy.can_delete(user=current_user, appointment=appointment)
            await self.uow.prescriptions.delete_prescription(prescription=prescription)
