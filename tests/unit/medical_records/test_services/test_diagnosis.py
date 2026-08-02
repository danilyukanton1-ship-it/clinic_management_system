import pytest
from unittest.mock import AsyncMock, MagicMock

from app.appointments.exceptions.appointment import AppointmentNotFoundException
from app.medical_records.exceptions.diagnosis import (
    DiagnosisNotFoundException,
    DiagnosisCantBeEmptyInPrescriptionException,
)
from app.medical_records.exceptions.disease import DiseaseNotFoundException
from app.medical_records.exceptions.prescription import PrescriptionNotFoundException
from app.medical_records.schemas.diagnosis import DiagnosisResponseSchema
from common.permissions.exceptions import ForbiddenException
from common.pagination.schemas import PaginationResult


class TestDiagnosisService:

    @pytest.mark.asyncio
    async def test_create_diagnosis_success(
        self,
        diagnosis_service,
        diagnosis_create_schema,
        disease_1,
        prescription,
        diagnosis,
    ):
        diagnosis_service.uow.diseases.get_disease_by_id = AsyncMock(
            return_value=disease_1
        )
        diagnosis_service.uow.prescriptions.get_prescription_by_id = AsyncMock(
            return_value=prescription
        )
        diagnosis_service.uow.diagnoses.create_diagnosis = AsyncMock(
            return_value=diagnosis
        )
        result = await diagnosis_service.create(diagnosis_create_schema)
        diagnosis_service.uow.diseases.get_disease_by_id.assert_awaited_once_with(
            disease_id=1
        )
        diagnosis_service.uow.prescriptions.get_prescription_by_id.assert_awaited_once_with(
            prescription_id=1
        )
        diagnosis_service.uow.diagnoses.create_diagnosis.assert_awaited_once_with(
            data=diagnosis_create_schema
        )
        assert isinstance(result, DiagnosisResponseSchema)

    @pytest.mark.asyncio
    async def test_create_prescription_not_found(
        self,
        diagnosis_service,
        diagnosis_create_schema,
    ):
        diagnosis_service.uow.prescriptions.get_prescription_by_id = AsyncMock(
            return_value=None
        )

        with pytest.raises(PrescriptionNotFoundException):
            await diagnosis_service.create(diagnosis_create_schema)

        diagnosis_service.uow.diseases.get_disease_by_id.assert_not_called()
        diagnosis_service.uow.diagnoses.create_diagnosis.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_disease_not_found(
        self,
        diagnosis_service,
        diagnosis_create_schema,
        prescription,
    ):
        diagnosis_service.uow.prescriptions.get_prescription_by_id = AsyncMock(
            return_value=prescription
        )
        diagnosis_service.uow.diseases.get_disease_by_id = AsyncMock(return_value=None)
        with pytest.raises(DiseaseNotFoundException):
            await diagnosis_service.create(diagnosis_create_schema)
        diagnosis_service.uow.diagnoses.create_diagnosis.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_success(
        self,
        diagnosis_service,
        diagnosis,
        disease_1,
        appointment_patient_1,
        diagnosis_update_schema,
        patient_1,
    ):
        diagnosis_service.uow.diagnoses.get_diagnosis_by_id = AsyncMock(
            return_value=diagnosis
        )

        diagnosis_service.uow.diseases.get_disease_by_id = AsyncMock(
            return_value=disease_1,
        )

        diagnosis_service.uow.appointments.get_appointment_by_diagnosis_id = AsyncMock(
            return_value=appointment_patient_1
        )

        diagnosis_service.policy.can_update = MagicMock()

        diagnosis_service.uow.diagnoses.update_diagnosis = AsyncMock(
            return_value=diagnosis
        )

        result = await diagnosis_service.update(
            diagnosis_id=1,
            current_user=patient_1,
            data=diagnosis_update_schema,
        )

        diagnosis_service.uow.diagnoses.get_diagnosis_by_id.assert_awaited_once_with(
            diagnosis_id=1,
        )

        diagnosis_service.uow.diseases.get_disease_by_id.assert_awaited_once_with(
            disease_id=diagnosis_update_schema.disease_id,
        )

        diagnosis_service.uow.appointments.get_appointment_by_diagnosis_id.assert_awaited_once_with(
            diagnosis_id=1,
        )

        diagnosis_service.policy.can_update.assert_called_once_with(
            user=patient_1,
            appointment=appointment_patient_1,
        )

        diagnosis_service.uow.diagnoses.update_diagnosis.assert_awaited_once_with(
            diagnosis=diagnosis,
            data=diagnosis_update_schema,
        )

        assert result == DiagnosisResponseSchema.model_validate(diagnosis)

    @pytest.mark.asyncio
    async def test_update_diagnosis_not_found(
        self,
        diagnosis_service,
        diagnosis_update_schema,
        patient_1,
    ):
        diagnosis_service.uow.diagnoses.get_diagnosis_by_id = AsyncMock(
            return_value=None
        )
        with pytest.raises(DiagnosisNotFoundException):
            await diagnosis_service.update(
                diagnosis_id=1,
                current_user=patient_1,
                data=diagnosis_update_schema,
            )
        diagnosis_service.uow.appointments.get_appointment_by_diagnosis_id.assert_not_called()
        diagnosis_service.policy.can_update.assert_not_called()
        diagnosis_service.uow.diagnoses.update_diagnosis.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_disease_not_found(
        self,
        diagnosis_service,
        diagnosis,
        diagnosis_update_schema,
        patient_1,
    ):
        diagnosis_service.uow.diagnoses.get_diagnosis_by_id = AsyncMock(
            return_value=diagnosis
        )

        diagnosis_service.uow.diseases.get_disease_by_id = AsyncMock(
            return_value=None,
        )

        with pytest.raises(DiseaseNotFoundException):
            await diagnosis_service.update(
                diagnosis_id=1,
                current_user=patient_1,
                data=diagnosis_update_schema,
            )

        diagnosis_service.uow.appointments.get_appointment_by_diagnosis_id.assert_not_called()
        diagnosis_service.policy.can_update.assert_not_called()
        diagnosis_service.uow.diagnoses.update_diagnosis.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_appointment_not_found(
        self,
        diagnosis_service,
        diagnosis,
        disease_1,
        diagnosis_update_schema,
        patient_1,
    ):
        diagnosis_service.uow.diagnoses.get_diagnosis_by_id = AsyncMock(
            return_value=diagnosis
        )

        diagnosis_service.uow.diseases.get_disease_by_id = AsyncMock(
            return_value=disease_1,
        )

        diagnosis_service.uow.appointments.get_appointment_by_diagnosis_id = AsyncMock(
            return_value=None
        )

        with pytest.raises(AppointmentNotFoundException):
            await diagnosis_service.update(
                diagnosis_id=1,
                current_user=patient_1,
                data=diagnosis_update_schema,
            )

        diagnosis_service.uow.diagnoses.get_diagnosis_by_id.assert_awaited_once_with(
            diagnosis_id=1,
        )

        diagnosis_service.uow.diseases.get_disease_by_id.assert_awaited_once_with(
            disease_id=diagnosis_update_schema.disease_id,
        )

        diagnosis_service.uow.appointments.get_appointment_by_diagnosis_id.assert_awaited_once_with(
            diagnosis_id=1,
        )

        diagnosis_service.policy.can_update.assert_not_called()

        diagnosis_service.uow.diagnoses.update_diagnosis.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_forbidden(
        self,
        diagnosis_service,
        diagnosis,
        disease_1,
        diagnosis_update_schema,
        patient_1,
        appointment_patient_1,
    ):
        diagnosis_service.uow.diagnoses.get_diagnosis_by_id = AsyncMock(
            return_value=diagnosis
        )

        diagnosis_service.uow.diseases.get_disease_by_id = AsyncMock(
            return_value=disease_1,
        )

        diagnosis_service.uow.appointments.get_appointment_by_diagnosis_id = AsyncMock(
            return_value=appointment_patient_1
        )

        diagnosis_service.policy.can_update = MagicMock(
            side_effect=ForbiddenException()
        )

        diagnosis_service.uow.diagnoses.update_diagnosis = AsyncMock()

        with pytest.raises(ForbiddenException):
            await diagnosis_service.update(
                diagnosis_id=1,
                current_user=patient_1,
                data=diagnosis_update_schema,
            )

        diagnosis_service.uow.diagnoses.get_diagnosis_by_id.assert_awaited_once_with(
            diagnosis_id=1,
        )

        diagnosis_service.uow.diseases.get_disease_by_id.assert_awaited_once_with(
            disease_id=diagnosis_update_schema.disease_id,
        )

        diagnosis_service.uow.appointments.get_appointment_by_diagnosis_id.assert_awaited_once_with(
            diagnosis_id=1,
        )

        diagnosis_service.policy.can_update.assert_called_once_with(
            user=patient_1,
            appointment=appointment_patient_1,
        )

        diagnosis_service.uow.diagnoses.update_diagnosis.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_success(
        self,
        diagnosis_service,
        diagnosis,
        patient_1,
        appointment_patient_1,
    ):
        diagnosis_service.uow.diagnoses.get_diagnosis_by_id = AsyncMock(
            return_value=diagnosis
        )
        diagnosis_service.uow.appointments.get_appointment_by_diagnosis_id = AsyncMock(
            return_value=appointment_patient_1
        )
        diagnosis_service.policy.can_delete = MagicMock()
        diagnosis_service.uow.diagnoses.get_diagnoses_by_prescription_id = AsyncMock(
            return_value=[diagnosis, diagnosis]
        )
        diagnosis_service.uow.diagnoses.delete_diagnosis = AsyncMock()
        result = await diagnosis_service.delete(
            diagnosis_id=1,
            current_user=patient_1,
        )
        diagnosis_service.uow.diagnoses.delete_diagnosis.assert_awaited_once_with(
            diagnosis=diagnosis
        )
        assert result is None

    @pytest.mark.asyncio
    async def test_delete_diagnosis_not_found(
        self,
        diagnosis_service,
        patient_1,
    ):
        diagnosis_service.uow.diagnoses.get_diagnosis_by_id = AsyncMock(
            return_value=None
        )
        with pytest.raises(DiagnosisNotFoundException):
            await diagnosis_service.delete(
                1,
                patient_1,
            )
        diagnosis_service.uow.diagnoses.delete_diagnosis.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_appointment_not_found(
        self,
        diagnosis_service,
        diagnosis,
        patient_1,
    ):
        diagnosis_service.uow.diagnoses.get_diagnosis_by_id = AsyncMock(
            return_value=diagnosis
        )
        diagnosis_service.uow.appointments.get_appointment_by_diagnosis_id = AsyncMock(
            return_value=None
        )
        with pytest.raises(AppointmentNotFoundException):
            await diagnosis_service.delete(
                1,
                patient_1,
            )
        diagnosis_service.policy.can_delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_forbidden(
        self,
        diagnosis_service,
        diagnosis,
        patient_1,
        appointment_patient_1,
    ):
        diagnosis_service.uow.diagnoses.get_diagnosis_by_id = AsyncMock(
            return_value=diagnosis
        )
        diagnosis_service.uow.appointments.get_appointment_by_diagnosis_id = AsyncMock(
            return_value=appointment_patient_1
        )
        diagnosis_service.policy.can_delete = MagicMock(
            side_effect=ForbiddenException()
        )
        with pytest.raises(ForbiddenException):
            await diagnosis_service.delete(
                1,
                patient_1,
            )
        diagnosis_service.policy.can_delete.assert_called_once_with(
            user=patient_1,
            appointment=appointment_patient_1,
        )

    @pytest.mark.asyncio
    async def test_delete_last_diagnosis_in_prescription(
        self,
        diagnosis_service,
        diagnosis,
        patient_1,
        appointment_patient_1,
    ):
        diagnosis_service.uow.diagnoses.get_diagnosis_by_id = AsyncMock(
            return_value=diagnosis
        )
        diagnosis_service.uow.appointments.get_appointment_by_diagnosis_id = AsyncMock(
            return_value=appointment_patient_1
        )
        diagnosis_service.policy.can_delete = MagicMock()
        diagnosis_service.uow.diagnoses.get_diagnoses_by_prescription_id = AsyncMock(
            return_value=[diagnosis]
        )
        with pytest.raises(DiagnosisCantBeEmptyInPrescriptionException):
            await diagnosis_service.delete(
                1,
                patient_1,
            )
        diagnosis_service.uow.diagnoses.delete_diagnosis.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self,
        diagnosis_service,
        diagnosis,
        patient_1,
        appointment_patient_1,
    ):
        diagnosis_service.uow.diagnoses.get_diagnosis_by_id = AsyncMock(
            return_value=diagnosis
        )
        diagnosis_service.uow.appointments.get_appointment_by_diagnosis_id = AsyncMock(
            return_value=appointment_patient_1
        )
        diagnosis_service.policy.can_view = MagicMock()
        result = await diagnosis_service.get_by_id(
            1,
            patient_1,
        )
        diagnosis_service.policy.can_view.assert_called_once_with(
            user=patient_1,
            appointment=appointment_patient_1,
        )
        assert result == DiagnosisResponseSchema.model_validate(diagnosis)

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        diagnosis_service,
        patient_1,
    ):
        diagnosis_service.uow.diagnoses.get_diagnosis_by_id = AsyncMock(
            return_value=None
        )
        with pytest.raises(DiagnosisNotFoundException):
            await diagnosis_service.get_by_id(
                1,
                patient_1,
            )
        diagnosis_service.policy.can_view.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_by_id_appointment_not_found(
        self,
        diagnosis_service,
        diagnosis,
        patient_1,
    ):
        diagnosis_service.uow.diagnoses.get_diagnosis_by_id = AsyncMock(
            return_value=diagnosis
        )
        diagnosis_service.uow.appointments.get_appointment_by_diagnosis_id = AsyncMock(
            return_value=None
        )
        with pytest.raises(AppointmentNotFoundException):
            await diagnosis_service.get_by_id(
                1,
                patient_1,
            )
        diagnosis_service.policy.can_view.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_by_id_forbidden(
        self,
        diagnosis_service,
        diagnosis,
        patient_1,
        appointment_patient_1,
    ):
        diagnosis_service.uow.diagnoses.get_diagnosis_by_id = AsyncMock(
            return_value=diagnosis
        )
        diagnosis_service.uow.appointments.get_appointment_by_diagnosis_id = AsyncMock(
            return_value=appointment_patient_1
        )
        diagnosis_service.policy.can_view = MagicMock(side_effect=ForbiddenException())
        with pytest.raises(ForbiddenException):
            await diagnosis_service.get_by_id(
                1,
                patient_1,
            )
        diagnosis_service.policy.can_view.assert_called_once_with(
            user=patient_1,
            appointment=appointment_patient_1,
        )

    @pytest.mark.asyncio
    async def test_get_by_prescription_id_success(
        self,
        diagnosis_service,
        diagnosis,
        patient_1,
        appointment_patient_1,
        pagination,
    ):
        diagnosis_service.uow.diagnoses.get_diagnoses_by_prescription_id_with_pagination = AsyncMock(
            return_value=PaginationResult(
                items=[diagnosis],
                total=1,
            )
        )

        diagnosis_service.uow.appointments.get_appointment_by_diagnosis_id = AsyncMock(
            return_value=appointment_patient_1,
        )

        diagnosis_service.policy.can_view = MagicMock()

        result = await diagnosis_service.get_by_prescription_id(
            prescription_id=1,
            pagination=pagination,
            current_user=patient_1,
        )

        diagnosis_service.uow.diagnoses.get_diagnoses_by_prescription_id_with_pagination.assert_awaited_once_with(
            prescription_id=1,
            pagination=pagination,
        )

        diagnosis_service.uow.appointments.get_appointment_by_diagnosis_id.assert_awaited_once_with(
            diagnosis_id=diagnosis.id,
        )

        diagnosis_service.policy.can_view.assert_called_once_with(
            user=patient_1,
            appointment=appointment_patient_1,
        )

        assert result.total == 1
        assert result.page == 1
        assert result.page_size == 20
        assert result.pages == 1

        assert len(result.items) == 1
        assert result.items[0] == DiagnosisResponseSchema.model_validate(
            diagnosis,
        )

    @pytest.mark.asyncio
    async def test_get_by_prescription_id_appointment_not_found(
        self,
        diagnosis_service,
        diagnosis,
        patient_1,
        pagination,
    ):
        diagnosis_service.uow.diagnoses.get_diagnoses_by_prescription_id_with_pagination = AsyncMock(
            return_value=PaginationResult(
                items=[diagnosis],
                total=1,
            )
        )

        diagnosis_service.uow.appointments.get_appointment_by_diagnosis_id = AsyncMock(
            return_value=None,
        )

        with pytest.raises(AppointmentNotFoundException):
            await diagnosis_service.get_by_prescription_id(
                prescription_id=1,
                current_user=patient_1,
                pagination=pagination,
            )

        diagnosis_service.uow.diagnoses.get_diagnoses_by_prescription_id_with_pagination.assert_awaited_once_with(
            prescription_id=1,
            pagination=pagination,
        )

        diagnosis_service.uow.appointments.get_appointment_by_diagnosis_id.assert_awaited_once_with(
            diagnosis_id=diagnosis.id,
        )

        diagnosis_service.policy.can_view.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_by_prescription_id_forbidden(
        self,
        diagnosis_service,
        diagnosis,
        patient_1,
        appointment_patient_1,
        pagination,
    ):
        diagnosis_service.uow.diagnoses.get_diagnoses_by_prescription_id_with_pagination = AsyncMock(
            return_value=PaginationResult(
                items=[diagnosis],
                total=1,
            )
        )

        diagnosis_service.uow.appointments.get_appointment_by_diagnosis_id = AsyncMock(
            return_value=appointment_patient_1,
        )

        diagnosis_service.policy.can_view = MagicMock(
            side_effect=ForbiddenException(),
        )

        with pytest.raises(ForbiddenException):
            await diagnosis_service.get_by_prescription_id(
                prescription_id=1,
                current_user=patient_1,
                pagination=pagination,
            )

        diagnosis_service.uow.diagnoses.get_diagnoses_by_prescription_id_with_pagination.assert_awaited_once_with(
            prescription_id=1,
            pagination=pagination,
        )

        diagnosis_service.uow.appointments.get_appointment_by_diagnosis_id.assert_awaited_once_with(
            diagnosis_id=diagnosis.id,
        )

        diagnosis_service.policy.can_view.assert_called_once_with(
            user=patient_1,
            appointment=appointment_patient_1,
        )

    @pytest.mark.asyncio
    async def test_get_by_disease_id_success(
        self,
        diagnosis_service,
        diagnosis,
        pagination,
    ):
        diagnosis_service.uow.diagnoses.get_diagnoses_by_disease_id = AsyncMock(
            return_value=PaginationResult(
                items=[diagnosis],
                total=1,
            )
        )

        result = await diagnosis_service.get_by_disease_id(
            disease_id=1,
            pagination=pagination,
        )

        diagnosis_service.uow.diagnoses.get_diagnoses_by_disease_id.assert_awaited_once_with(
            disease_id=1,
            pagination=pagination,
        )

        assert result.total == 1
        assert result.page == 1
        assert result.page_size == 20
        assert result.pages == 1

        assert len(result.items) == 1
        assert result.items[0] == DiagnosisResponseSchema.model_validate(
            diagnosis,
        )
