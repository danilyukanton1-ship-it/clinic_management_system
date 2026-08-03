from unittest.mock import AsyncMock, MagicMock

import pytest

from app.appointments.exceptions.appointment import AppointmentNotFoundException
from app.medical_records.exceptions.prescription import PrescriptionNotFoundException
from app.medical_records.schemas.prescription import PrescriptionResponseSchema
from common.permissions.exceptions import ForbiddenException


class TestPrescriptionService:

    @pytest.mark.asyncio
    async def test_update_prescription_success(
        self,
        prescription_service,
        prescription,
        prescription_update,
        prescription_update_schema,
        appointment_patient_1,
        current_doctor,
    ):
        prescription_service.uow.prescriptions.get_prescription_by_id = AsyncMock(
            return_value=prescription
        )
        prescription_service.uow.appointments.get_appointment_by_prescription_id = (
            AsyncMock(return_value=appointment_patient_1)
        )
        prescription_service.uow.prescriptions.update_prescription = AsyncMock(
            return_value=prescription_update
        )
        prescription_service.policy.can_update = MagicMock()
        result = await prescription_service.update(
            prescription_id=prescription.id,
            data=prescription_update_schema,
            current_user=current_doctor,
        )
        prescription_service.uow.prescriptions.get_prescription_by_id.assert_awaited_once_with(
            prescription_id=prescription.id
        )
        prescription_service.uow.appointments.get_appointment_by_prescription_id.assert_awaited_once_with(
            prescription_id=prescription.id
        )
        prescription_service.policy.can_update.assert_called_once_with(
            user=current_doctor,
            appointment=appointment_patient_1,
        )
        prescription_service.uow.prescriptions.update_prescription.assert_awaited_once_with(
            prescription=prescription,
            data=prescription_update_schema,
        )
        assert isinstance(result, PrescriptionResponseSchema)
        assert result.recommendations == prescription_update.recommendations

    @pytest.mark.asyncio
    async def test_update_prescription_not_found(
        self,
        prescription_service,
        prescription_update_schema,
        current_doctor,
    ):
        prescription_service.uow.prescriptions.get_prescription_by_id = AsyncMock(
            return_value=None
        )
        prescription_service.uow.appointments.get_appointment_by_prescription_id = (
            AsyncMock()
        )
        prescription_service.uow.prescriptions.update_prescription = AsyncMock()
        with pytest.raises(PrescriptionNotFoundException):
            await prescription_service.update(
                prescription_id=1,
                data=prescription_update_schema,
                current_user=current_doctor,
            )

        prescription_service.uow.appointments.get_appointment_by_prescription_id.assert_not_awaited()
        prescription_service.uow.prescriptions.update_prescription.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_appointment_not_found(
        self,
        prescription_service,
        prescription,
        prescription_update_schema,
        current_doctor,
    ):
        prescription_service.uow.prescriptions.get_prescription_by_id = AsyncMock(
            return_value=prescription
        )
        prescription_service.uow.appointments.get_appointment_by_prescription_id = (
            AsyncMock(return_value=None)
        )

        prescription_service.policy.can_update = MagicMock()
        prescription_service.uow.prescriptions.update_prescription = AsyncMock()
        with pytest.raises(AppointmentNotFoundException):
            await prescription_service.update(
                prescription_id=prescription.id,
                data=prescription_update_schema,
                current_user=current_doctor,
            )

        prescription_service.policy.can_update.assert_not_called()
        prescription_service.uow.prescriptions.update_prescription.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_forbidden(
        self,
        prescription_service,
        prescription,
        prescription_update_schema,
        appointment_patient_1,
        current_doctor,
    ):
        prescription_service.uow.prescriptions.get_prescription_by_id = AsyncMock(
            return_value=prescription
        )
        prescription_service.uow.appointments.get_appointment_by_prescription_id = (
            AsyncMock(return_value=appointment_patient_1)
        )
        prescription_service.policy.can_update = MagicMock(
            side_effect=ForbiddenException()
        )
        prescription_service.uow.prescriptions.update_prescription = AsyncMock()
        with pytest.raises(ForbiddenException):
            await prescription_service.update(
                prescription_id=prescription.id,
                data=prescription_update_schema,
                current_user=current_doctor,
            )
        prescription_service.uow.prescriptions.update_prescription.assert_not_awaited()
