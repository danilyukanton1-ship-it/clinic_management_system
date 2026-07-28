import pytest
from unittest.mock import AsyncMock, MagicMock

from app.appointments.exceptions.appointment import AppointmentNotFoundException
from app.medical_records.exceptions.disease import DiseaseNotFoundException
from app.medical_records.exceptions.drug import DrugNotFoundException
from app.medical_records.exceptions.prescription import PrescriptionNotFoundException
from app.medical_records.schemas.diagnosis import DiagnosisCreateSchema
from app.medical_records.schemas.prescription import (
    FullPrescriptionResponseSchema,
    PrescriptionCreateSchema,
)
from app.medical_records.schemas.prescription_item import PrescriptionItemCreateSchema
from common.permissions.exceptions import ForbiddenException


class TestFullPrescriptionService:

    @pytest.mark.asyncio
    async def test_create_full_prescription_success(
        self,
        full_prescription_service,
        full_prescription_create_schema,
        appointment_patient_1,
        prescription,
        diagnosis,
        prescription_item_1,
        disease_1,
        drug_1,
    ):
        full_prescription_service.uow.appointments.get_appointment_by_id = AsyncMock(
            return_value=appointment_patient_1
        )
        full_prescription_service.uow.prescriptions.create_prescription = AsyncMock(
            return_value=prescription
        )
        full_prescription_service.uow.diseases.get_diseases_by_ids = AsyncMock(
            return_value=[disease_1]
        )
        full_prescription_service.uow.diagnoses.create_diagnosis = AsyncMock(
            return_value=diagnosis
        )
        full_prescription_service.uow.drugs.get_drugs_by_ids = AsyncMock(
            return_value=[drug_1]
        )
        full_prescription_service.uow.prescription_items.create_prescription_item = (
            AsyncMock(return_value=prescription_item_1)
        )
        result = await full_prescription_service.create_full_prescription(
            data=full_prescription_create_schema,
        )
        full_prescription_service.uow.appointments.get_appointment_by_id.assert_awaited_once_with(
            appointment_id=full_prescription_create_schema.appointment_id,
        )
        full_prescription_service.uow.prescriptions.create_prescription.assert_awaited_once_with(
            data=PrescriptionCreateSchema(
                appointment_id=full_prescription_create_schema.appointment_id,
                recommendations=full_prescription_create_schema.recommendations,
            ),
        )
        full_prescription_service.uow.diseases.get_diseases_by_ids.assert_awaited_once_with(
            disease_ids=[
                diagnosis.disease_id
                for diagnosis in full_prescription_create_schema.diagnoses
            ],
        )
        full_prescription_service.uow.diagnoses.create_diagnosis.assert_awaited_once_with(
            data=DiagnosisCreateSchema(
                prescription_id=prescription.id,
                disease_id=full_prescription_create_schema.diagnoses[0].disease_id,
                notes=full_prescription_create_schema.diagnoses[0].notes,
            ),
        )
        full_prescription_service.uow.drugs.get_drugs_by_ids.assert_awaited_once_with(
            drug_ids=[
                item.drug_id
                for item in full_prescription_create_schema.prescription_items
            ],
        )
        full_prescription_service.uow.prescription_items.create_prescription_item.assert_awaited_once_with(
            data=PrescriptionItemCreateSchema(
                prescription_id=prescription.id,
                drug_id=full_prescription_create_schema.prescription_items[0].drug_id,
                dosage=full_prescription_create_schema.prescription_items[0].dosage,
                frequency=full_prescription_create_schema.prescription_items[
                    0
                ].frequency,
                duration_days=full_prescription_create_schema.prescription_items[
                    0
                ].duration_days,
            ),
        )
        assert isinstance(result, FullPrescriptionResponseSchema)
        assert result.prescription.id == prescription.id
        assert result.prescription.recommendations == prescription.recommendations
        assert len(result.diagnoses) == 1
        assert result.diagnoses[0].id == diagnosis.id
        assert result.diagnoses[0].disease_id == diagnosis.disease_id
        assert result.diagnoses[0].prescription_id == diagnosis.prescription_id
        assert len(result.prescription_items) == 1
        assert result.prescription_items[0].id == prescription_item_1.id
        assert result.prescription_items[0].drug_id == prescription_item_1.drug_id
        assert (
            result.prescription_items[0].prescription_id
            == prescription_item_1.prescription_id
        )

    @pytest.mark.asyncio
    async def test_create_full_prescription_appointment_not_found(
        self,
        full_prescription_service,
        full_prescription_create_schema,
    ):
        full_prescription_service.uow.appointments.get_appointment_by_id = AsyncMock(
            return_value=None
        )
        full_prescription_service.uow.prescriptions.create_prescription = AsyncMock()
        full_prescription_service.uow.diseases.get_diseases_by_ids = AsyncMock()
        full_prescription_service.uow.diagnoses.create_diagnosis = AsyncMock()
        full_prescription_service.uow.drugs.get_drugs_by_ids = AsyncMock()
        full_prescription_service.uow.prescription_items.create_prescription_item = (
            AsyncMock()
        )

        with pytest.raises(AppointmentNotFoundException):
            await full_prescription_service.create_full_prescription(
                data=full_prescription_create_schema,
            )

        full_prescription_service.uow.appointments.get_appointment_by_id.assert_awaited_once_with(
            appointment_id=full_prescription_create_schema.appointment_id,
        )

        full_prescription_service.uow.prescriptions.create_prescription.assert_not_awaited()
        full_prescription_service.uow.diseases.get_diseases_by_ids.assert_not_awaited()
        full_prescription_service.uow.diagnoses.create_diagnosis.assert_not_awaited()
        full_prescription_service.uow.drugs.get_drugs_by_ids.assert_not_awaited()
        full_prescription_service.uow.prescription_items.create_prescription_item.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_create_full_prescription_disease_not_found(
        self,
        full_prescription_service,
        full_prescription_create_schema,
        appointment_patient_1,
        prescription,
    ):
        full_prescription_service.uow.appointments.get_appointment_by_id = AsyncMock(
            return_value=appointment_patient_1
        )
        full_prescription_service.uow.prescriptions.create_prescription = AsyncMock(
            return_value=prescription
        )
        full_prescription_service.uow.diseases.get_diseases_by_ids = AsyncMock(
            return_value=[]
        )
        full_prescription_service.uow.diagnoses.create_diagnosis = AsyncMock()
        full_prescription_service.uow.drugs.get_drugs_by_ids = AsyncMock()
        full_prescription_service.uow.prescription_items.create_prescription_item = (
            AsyncMock()
        )
        with pytest.raises(DiseaseNotFoundException):
            await full_prescription_service.create_full_prescription(
                data=full_prescription_create_schema,
            )
        full_prescription_service.uow.appointments.get_appointment_by_id.assert_awaited_once_with(
            appointment_id=full_prescription_create_schema.appointment_id,
        )
        full_prescription_service.uow.prescriptions.create_prescription.assert_awaited_once_with(
            data=PrescriptionCreateSchema(
                appointment_id=full_prescription_create_schema.appointment_id,
                recommendations=full_prescription_create_schema.recommendations,
            ),
        )
        full_prescription_service.uow.diseases.get_diseases_by_ids.assert_awaited_once_with(
            disease_ids=[
                diagnosis.disease_id
                for diagnosis in full_prescription_create_schema.diagnoses
            ],
        )
        full_prescription_service.uow.diagnoses.create_diagnosis.assert_not_awaited()
        full_prescription_service.uow.drugs.get_drugs_by_ids.assert_not_awaited()
        full_prescription_service.uow.prescription_items.create_prescription_item.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_create_full_prescription_drug_not_found(
        self,
        full_prescription_service,
        full_prescription_create_schema,
        appointment_patient_1,
        prescription,
        diagnosis,
        disease_1,
    ):
        full_prescription_service.uow.appointments.get_appointment_by_id = AsyncMock(
            return_value=appointment_patient_1
        )
        full_prescription_service.uow.prescriptions.create_prescription = AsyncMock(
            return_value=prescription
        )
        full_prescription_service.uow.diseases.get_diseases_by_ids = AsyncMock(
            return_value=[disease_1]
        )
        full_prescription_service.uow.diagnoses.create_diagnosis = AsyncMock(
            return_value=diagnosis
        )
        full_prescription_service.uow.drugs.get_drugs_by_ids = AsyncMock(
            return_value=[]
        )
        full_prescription_service.uow.prescription_items.create_prescription_item = (
            AsyncMock()
        )
        with pytest.raises(DrugNotFoundException):
            await full_prescription_service.create_full_prescription(
                data=full_prescription_create_schema,
            )
        full_prescription_service.uow.appointments.get_appointment_by_id.assert_awaited_once_with(
            appointment_id=full_prescription_create_schema.appointment_id,
        )
        full_prescription_service.uow.prescriptions.create_prescription.assert_awaited_once_with(
            data=PrescriptionCreateSchema(
                appointment_id=full_prescription_create_schema.appointment_id,
                recommendations=full_prescription_create_schema.recommendations,
            ),
        )
        full_prescription_service.uow.diseases.get_diseases_by_ids.assert_awaited_once_with(
            disease_ids=[
                diagnosis.disease_id
                for diagnosis in full_prescription_create_schema.diagnoses
            ],
        )
        full_prescription_service.uow.diagnoses.create_diagnosis.assert_awaited_once_with(
            data=DiagnosisCreateSchema(
                prescription_id=prescription.id,
                disease_id=full_prescription_create_schema.diagnoses[0].disease_id,
                notes=full_prescription_create_schema.diagnoses[0].notes,
            ),
        )
        full_prescription_service.uow.drugs.get_drugs_by_ids.assert_awaited_once_with(
            drug_ids=[
                item.drug_id
                for item in full_prescription_create_schema.prescription_items
            ],
        )
        full_prescription_service.uow.prescription_items.create_prescription_item.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_get_full_prescription_by_appointment_id_success(
        self,
        full_prescription_service,
        current_doctor,
        appointment_patient_1,
        prescription,
        diagnosis,
        prescription_item_1,
    ):
        full_prescription_service.uow.prescriptions.get_prescription_by_appointment_id = AsyncMock(
            return_value=prescription
        )
        full_prescription_service.uow.appointments.get_appointment_by_id = AsyncMock(
            return_value=appointment_patient_1
        )
        full_prescription_service.uow.diagnoses.get_diagnoses_by_prescription_id = (
            AsyncMock(return_value=[diagnosis])
        )
        full_prescription_service.uow.prescription_items.get_prescription_items_by_prescription_id = AsyncMock(
            return_value=[prescription_item_1]
        )
        full_prescription_service.policy.can_view = MagicMock()
        result = (
            await full_prescription_service.get_full_prescription_by_appointment_id(
                appointment_id=appointment_patient_1.id,
                current_user=current_doctor,
            )
        )
        full_prescription_service.uow.prescriptions.get_prescription_by_appointment_id.assert_awaited_once_with(
            appointment_id=appointment_patient_1.id,
        )
        full_prescription_service.uow.appointments.get_appointment_by_id.assert_awaited_once_with(
            appointment_id=appointment_patient_1.id,
        )
        full_prescription_service.policy.can_view.assert_called_once_with(
            user=current_doctor,
            appointment=appointment_patient_1,
        )
        full_prescription_service.uow.diagnoses.get_diagnoses_by_prescription_id.assert_awaited_once_with(
            prescription_id=prescription.id,
        )
        full_prescription_service.uow.prescription_items.get_prescription_items_by_prescription_id.assert_awaited_once_with(
            prescription_id=prescription.id,
        )
        assert isinstance(result, FullPrescriptionResponseSchema)
        assert result.prescription.id == prescription.id
        assert result.prescription.recommendations == prescription.recommendations
        assert len(result.diagnoses) == 1
        assert result.diagnoses[0].id == diagnosis.id
        assert result.diagnoses[0].disease_id == diagnosis.disease_id
        assert result.diagnoses[0].prescription_id == diagnosis.prescription_id
        assert len(result.prescription_items) == 1
        assert result.prescription_items[0].id == prescription_item_1.id
        assert result.prescription_items[0].drug_id == prescription_item_1.drug_id
        assert (
            result.prescription_items[0].prescription_id
            == prescription_item_1.prescription_id
        )

    @pytest.mark.asyncio
    async def test_get_full_prescription_by_appointment_id_prescription_not_found(
        self,
        full_prescription_service,
        current_doctor,
    ):
        full_prescription_service.uow.prescriptions.get_prescription_by_appointment_id = AsyncMock(
            return_value=None
        )
        full_prescription_service.uow.appointments.get_appointment_by_id = AsyncMock()
        full_prescription_service.uow.diagnoses.get_diagnoses_by_prescription_id = (
            AsyncMock()
        )
        full_prescription_service.uow.prescription_items.get_prescription_items_by_prescription_id = (
            AsyncMock()
        )
        full_prescription_service.policy.can_view = MagicMock()
        with pytest.raises(PrescriptionNotFoundException):
            await full_prescription_service.get_full_prescription_by_appointment_id(
                appointment_id=1,
                current_user=current_doctor,
            )
        full_prescription_service.uow.prescriptions.get_prescription_by_appointment_id.assert_awaited_once_with(
            appointment_id=1,
        )
        full_prescription_service.uow.appointments.get_appointment_by_id.assert_not_awaited()
        full_prescription_service.policy.can_view.assert_not_called()
        full_prescription_service.uow.diagnoses.get_diagnoses_by_prescription_id.assert_not_awaited()
        full_prescription_service.uow.prescription_items.get_prescription_items_by_prescription_id.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_get_full_prescription_by_appointment_id_appointment_not_found(
        self,
        full_prescription_service,
        current_doctor,
        prescription,
    ):
        full_prescription_service.uow.prescriptions.get_prescription_by_appointment_id = AsyncMock(
            return_value=prescription
        )
        full_prescription_service.uow.appointments.get_appointment_by_id = AsyncMock(
            return_value=None
        )
        full_prescription_service.uow.diagnoses.get_diagnoses_by_prescription_id = (
            AsyncMock()
        )
        full_prescription_service.uow.prescription_items.get_prescription_items_by_prescription_id = (
            AsyncMock()
        )
        full_prescription_service.policy.can_view = MagicMock()
        with pytest.raises(AppointmentNotFoundException):
            await full_prescription_service.get_full_prescription_by_appointment_id(
                appointment_id=1,
                current_user=current_doctor,
            )
        full_prescription_service.uow.prescriptions.get_prescription_by_appointment_id.assert_awaited_once_with(
            appointment_id=1,
        )
        full_prescription_service.uow.appointments.get_appointment_by_id.assert_awaited_once_with(
            appointment_id=1,
        )
        full_prescription_service.policy.can_view.assert_not_called()
        full_prescription_service.uow.diagnoses.get_diagnoses_by_prescription_id.assert_not_awaited()
        full_prescription_service.uow.prescription_items.get_prescription_items_by_prescription_id.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_get_full_prescription_by_appointment_id_forbidden(
        self,
        full_prescription_service,
        current_doctor,
        appointment_patient_1,
        prescription,
    ):
        full_prescription_service.uow.prescriptions.get_prescription_by_appointment_id = AsyncMock(
            return_value=prescription
        )
        full_prescription_service.uow.appointments.get_appointment_by_id = AsyncMock(
            return_value=appointment_patient_1
        )
        full_prescription_service.uow.diagnoses.get_diagnoses_by_prescription_id = (
            AsyncMock()
        )
        full_prescription_service.uow.prescription_items.get_prescription_items_by_prescription_id = (
            AsyncMock()
        )
        full_prescription_service.policy.can_view = MagicMock(
            side_effect=ForbiddenException()
        )
        with pytest.raises(ForbiddenException):
            await full_prescription_service.get_full_prescription_by_appointment_id(
                appointment_id=appointment_patient_1.id,
                current_user=current_doctor,
            )
        full_prescription_service.uow.prescriptions.get_prescription_by_appointment_id.assert_awaited_once_with(
            appointment_id=appointment_patient_1.id,
        )
        full_prescription_service.uow.appointments.get_appointment_by_id.assert_awaited_once_with(
            appointment_id=appointment_patient_1.id,
        )
        full_prescription_service.policy.can_view.assert_called_once_with(
            user=current_doctor,
            appointment=appointment_patient_1,
        )
        full_prescription_service.uow.diagnoses.get_diagnoses_by_prescription_id.assert_not_awaited()
        full_prescription_service.uow.prescription_items.get_prescription_items_by_prescription_id.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_get_full_prescription_by_prescription_id_success(
        self,
        full_prescription_service,
        current_doctor,
        prescription,
        appointment_patient_1,
        diagnosis,
        prescription_item_1,
    ):
        full_prescription_service.uow.prescriptions.get_prescription_by_id = AsyncMock(
            return_value=prescription
        )
        full_prescription_service.uow.appointments.get_appointment_by_prescription_id = AsyncMock(
            return_value=appointment_patient_1
        )
        full_prescription_service.uow.diagnoses.get_diagnoses_by_prescription_id = (
            AsyncMock(return_value=[diagnosis])
        )
        full_prescription_service.uow.prescription_items.get_prescription_items_by_prescription_id = AsyncMock(
            return_value=[prescription_item_1]
        )
        full_prescription_service.policy.can_view = MagicMock()
        result = (
            await full_prescription_service.get_full_prescription_by_prescription_id(
                prescription_id=prescription.id,
                current_user=current_doctor,
            )
        )
        full_prescription_service.uow.prescriptions.get_prescription_by_id.assert_awaited_once_with(
            prescription_id=prescription.id,
        )
        full_prescription_service.uow.appointments.get_appointment_by_prescription_id.assert_awaited_once_with(
            prescription_id=prescription.id,
        )
        full_prescription_service.policy.can_view.assert_called_once_with(
            user=current_doctor,
            appointment=appointment_patient_1,
        )
        full_prescription_service.uow.diagnoses.get_diagnoses_by_prescription_id.assert_awaited_once_with(
            prescription_id=prescription.id,
        )
        full_prescription_service.uow.prescription_items.get_prescription_items_by_prescription_id.assert_awaited_once_with(
            prescription_id=prescription.id,
        )
        assert isinstance(result, FullPrescriptionResponseSchema)
        assert result.prescription.id == prescription.id
        assert result.prescription.recommendations == prescription.recommendations
        assert len(result.diagnoses) == 1
        assert result.diagnoses[0].id == diagnosis.id
        assert result.diagnoses[0].disease_id == diagnosis.disease_id
        assert result.diagnoses[0].prescription_id == diagnosis.prescription_id
        assert len(result.prescription_items) == 1
        assert result.prescription_items[0].id == prescription_item_1.id
        assert result.prescription_items[0].drug_id == prescription_item_1.drug_id
        assert (
            result.prescription_items[0].prescription_id
            == prescription_item_1.prescription_id
        )

    @pytest.mark.asyncio
    async def test_get_full_prescription_by_prescription_id_prescription_not_found(
        self,
        full_prescription_service,
        current_doctor,
    ):
        full_prescription_service.uow.prescriptions.get_prescription_by_id = AsyncMock(
            return_value=None
        )
        full_prescription_service.uow.appointments.get_appointment_by_prescription_id = (
            AsyncMock()
        )
        full_prescription_service.uow.diagnoses.get_diagnoses_by_prescription_id = (
            AsyncMock()
        )
        full_prescription_service.uow.prescription_items.get_prescription_items_by_prescription_id = (
            AsyncMock()
        )
        full_prescription_service.policy.can_view = MagicMock()
        with pytest.raises(PrescriptionNotFoundException):
            await full_prescription_service.get_full_prescription_by_prescription_id(
                prescription_id=1,
                current_user=current_doctor,
            )
        full_prescription_service.uow.prescriptions.get_prescription_by_id.assert_awaited_once_with(
            prescription_id=1,
        )
        full_prescription_service.uow.appointments.get_appointment_by_prescription_id.assert_not_awaited()
        full_prescription_service.policy.can_view.assert_not_called()
        full_prescription_service.uow.diagnoses.get_diagnoses_by_prescription_id.assert_not_awaited()
        full_prescription_service.uow.prescription_items.get_prescription_items_by_prescription_id.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_get_full_prescription_by_prescription_id_appointment_not_found(
        self,
        full_prescription_service,
        current_doctor,
        prescription,
    ):
        full_prescription_service.uow.prescriptions.get_prescription_by_id = AsyncMock(
            return_value=prescription
        )
        full_prescription_service.uow.appointments.get_appointment_by_prescription_id = AsyncMock(
            return_value=None
        )
        full_prescription_service.uow.diagnoses.get_diagnoses_by_prescription_id = (
            AsyncMock()
        )
        full_prescription_service.uow.prescription_items.get_prescription_items_by_prescription_id = (
            AsyncMock()
        )
        full_prescription_service.policy.can_view = MagicMock()
        with pytest.raises(AppointmentNotFoundException):
            await full_prescription_service.get_full_prescription_by_prescription_id(
                prescription_id=prescription.id,
                current_user=current_doctor,
            )
        full_prescription_service.uow.prescriptions.get_prescription_by_id.assert_awaited_once_with(
            prescription_id=prescription.id,
        )
        full_prescription_service.uow.appointments.get_appointment_by_prescription_id.assert_awaited_once_with(
            prescription_id=prescription.id,
        )
        full_prescription_service.policy.can_view.assert_not_called()
        full_prescription_service.uow.diagnoses.get_diagnoses_by_prescription_id.assert_not_awaited()
        full_prescription_service.uow.prescription_items.get_prescription_items_by_prescription_id.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_get_full_prescription_by_prescription_id_forbidden(
        self,
        full_prescription_service,
        current_doctor,
        prescription,
        appointment_patient_1,
    ):
        full_prescription_service.uow.prescriptions.get_prescription_by_id = AsyncMock(
            return_value=prescription
        )
        full_prescription_service.uow.appointments.get_appointment_by_prescription_id = AsyncMock(
            return_value=appointment_patient_1
        )
        full_prescription_service.uow.diagnoses.get_diagnoses_by_prescription_id = (
            AsyncMock()
        )
        full_prescription_service.uow.prescription_items.get_prescription_items_by_prescription_id = (
            AsyncMock()
        )
        full_prescription_service.policy.can_view = MagicMock(
            side_effect=ForbiddenException()
        )
        with pytest.raises(ForbiddenException):
            await full_prescription_service.get_full_prescription_by_prescription_id(
                prescription_id=prescription.id,
                current_user=current_doctor,
            )
        full_prescription_service.uow.prescriptions.get_prescription_by_id.assert_awaited_once_with(
            prescription_id=prescription.id,
        )
        full_prescription_service.uow.appointments.get_appointment_by_prescription_id.assert_awaited_once_with(
            prescription_id=prescription.id,
        )
        full_prescription_service.policy.can_view.assert_called_once_with(
            user=current_doctor,
            appointment=appointment_patient_1,
        )
        full_prescription_service.uow.diagnoses.get_diagnoses_by_prescription_id.assert_not_awaited()
        full_prescription_service.uow.prescription_items.get_prescription_items_by_prescription_id.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_delete_full_prescription_success(
        self,
        full_prescription_service,
        current_doctor,
        prescription,
        appointment_patient_1,
    ):
        full_prescription_service.uow.prescriptions.get_prescription_by_id = AsyncMock(
            return_value=prescription
        )
        full_prescription_service.uow.appointments.get_appointment_by_prescription_id = AsyncMock(
            return_value=appointment_patient_1
        )
        full_prescription_service.uow.prescriptions.delete_prescription = AsyncMock()
        full_prescription_service.policy.can_delete = MagicMock()

        result = await full_prescription_service.delete_full_prescription(
            prescription_id=prescription.id,
            current_user=current_doctor,
        )
        full_prescription_service.uow.prescriptions.get_prescription_by_id.assert_awaited_once_with(
            prescription_id=prescription.id,
        )
        full_prescription_service.uow.appointments.get_appointment_by_prescription_id.assert_awaited_once_with(
            prescription_id=prescription.id,
        )
        full_prescription_service.policy.can_delete.assert_called_once_with(
            user=current_doctor,
            appointment=appointment_patient_1,
        )
        full_prescription_service.uow.prescriptions.delete_prescription.assert_awaited_once_with(
            prescription=prescription,
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_delete_full_prescription_prescription_not_found(
        self,
        full_prescription_service,
        current_doctor,
    ):
        full_prescription_service.uow.prescriptions.get_prescription_by_id = AsyncMock(
            return_value=None
        )
        full_prescription_service.uow.appointments.get_appointment_by_prescription_id = (
            AsyncMock()
        )
        full_prescription_service.uow.prescriptions.delete_prescription = AsyncMock()
        full_prescription_service.policy.can_delete = MagicMock()
        with pytest.raises(PrescriptionNotFoundException):
            await full_prescription_service.delete_full_prescription(
                prescription_id=1,
                current_user=current_doctor,
            )
        full_prescription_service.uow.prescriptions.get_prescription_by_id.assert_awaited_once_with(
            prescription_id=1,
        )
        full_prescription_service.uow.appointments.get_appointment_by_prescription_id.assert_not_awaited()
        full_prescription_service.policy.can_delete.assert_not_called()
        full_prescription_service.uow.prescriptions.delete_prescription.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_delete_full_prescription_appointment_not_found(
        self,
        full_prescription_service,
        current_doctor,
        prescription,
    ):
        full_prescription_service.uow.prescriptions.get_prescription_by_id = AsyncMock(
            return_value=prescription
        )
        full_prescription_service.uow.appointments.get_appointment_by_prescription_id = AsyncMock(
            return_value=None
        )
        full_prescription_service.uow.prescriptions.delete_prescription = AsyncMock()
        full_prescription_service.policy.can_delete = MagicMock()
        with pytest.raises(AppointmentNotFoundException):
            await full_prescription_service.delete_full_prescription(
                prescription_id=prescription.id,
                current_user=current_doctor,
            )
        full_prescription_service.uow.prescriptions.get_prescription_by_id.assert_awaited_once_with(
            prescription_id=prescription.id,
        )
        full_prescription_service.uow.appointments.get_appointment_by_prescription_id.assert_awaited_once_with(
            prescription_id=prescription.id,
        )
        full_prescription_service.policy.can_delete.assert_not_called()
        full_prescription_service.uow.prescriptions.delete_prescription.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_delete_full_prescription_forbidden(
        self,
        full_prescription_service,
        current_doctor,
        prescription,
        appointment_patient_1,
    ):
        full_prescription_service.uow.prescriptions.get_prescription_by_id = AsyncMock(
            return_value=prescription
        )
        full_prescription_service.uow.appointments.get_appointment_by_prescription_id = AsyncMock(
            return_value=appointment_patient_1
        )
        full_prescription_service.uow.prescriptions.delete_prescription = AsyncMock()
        full_prescription_service.policy.can_delete = MagicMock(
            side_effect=ForbiddenException()
        )
        with pytest.raises(ForbiddenException):
            await full_prescription_service.delete_full_prescription(
                prescription_id=prescription.id,
                current_user=current_doctor,
            )
        full_prescription_service.uow.prescriptions.get_prescription_by_id.assert_awaited_once_with(
            prescription_id=prescription.id,
        )
        full_prescription_service.uow.appointments.get_appointment_by_prescription_id.assert_awaited_once_with(
            prescription_id=prescription.id,
        )
        full_prescription_service.policy.can_delete.assert_called_once_with(
            user=current_doctor,
            appointment=appointment_patient_1,
        )
        full_prescription_service.uow.prescriptions.delete_prescription.assert_not_awaited()
