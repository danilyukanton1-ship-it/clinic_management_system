import pytest
from unittest.mock import AsyncMock, MagicMock

from app.appointments.exceptions.appointment import AppointmentNotFoundException
from app.appointments.schemas.appointment import AppointmentResponseSchema
from app.scheduling.exceptions.schedule_slot import SlotNotFoundException, SlotNotAvailableException
from app.users.exceptions.user import UserNotFoundException
from common.enums.slot_status import SlotStatus
from common.permissions.exceptions import ForbiddenException


class TestAppointmentService:

    @pytest.mark.asyncio
    async def test_create_appointment_success(
            self,
            appointment_service,
            schedule_slot_free,
            schedule_slot_booked,
            appointment_create_schema,
            appointment_patient_1
    ):
        appointment_service.uow.schedule_slots.get_slot_by_id = AsyncMock(
            return_value=schedule_slot_free
        )
        appointment_service.uow.schedule_slots.change_slot_status = AsyncMock(
            return_value=schedule_slot_booked
        )
        appointment_service.uow.appointments.create = AsyncMock(
            return_value=appointment_patient_1
        )
        result = await appointment_service.create_appointment(
            data=appointment_create_schema
        )
        appointment_service.uow.schedule_slots.get_slot_by_id.assert_called_once_with(slot_id=1)
        appointment_service.uow.schedule_slots.change_slot_status.assert_called_once_with(
            slot=schedule_slot_free,
            status=SlotStatus.BOOKED,
        )
        appointment_service.uow.appointments.create.assert_called_once_with(
            data=appointment_create_schema
        )
        assert isinstance(result, AppointmentResponseSchema)
        assert result.id == appointment_patient_1.id

    @pytest.mark.asyncio
    async def test_create_appointment_slot_not_found(
            self,
            appointment_service,
            appointment_create_schema,
    ):
        appointment_service.uow.schedule_slots.get_slot_by_id = AsyncMock(
            return_value=None
        )
        with pytest.raises(SlotNotFoundException):
            await appointment_service.create_appointment(
                appointment_create_schema
            )
        appointment_service.uow.schedule_slots.change_slot_status.assert_not_called()
        appointment_service.uow.appointments.create.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_appointment_slot_already_booked(
            self,
            appointment_service,
            appointment_create_schema,
            schedule_slot_booked,
    ):
        appointment_service.uow.schedule_slots.get_slot_by_id = AsyncMock(
            return_value=schedule_slot_booked
        )
        with pytest.raises(SlotNotAvailableException):
            await appointment_service.create_appointment(
                appointment_create_schema
            )
        appointment_service.uow.schedule_slots.change_slot_status.assert_not_called()
        appointment_service.uow.appointments.create.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_future_apps_by_user_id_success(
        self,
        patient_1,
        appointment_service,
        appointment_patient_1
    ):
        appointment_service.uow.users.get_user_by_id = AsyncMock(
            return_value=patient_1
        )
        appointment_service.uow.appointments.get_future_appointments_by_user_id = AsyncMock(
            return_value=[appointment_patient_1,]
        )
        appointment_service.policy.can_view = MagicMock(
            return_value=True
        )
        result = await appointment_service.get_future_apps_by_user_id(
            user_id=1
        )
        appointment_service.uow.users.get_user_by_id.assert_called_once_with(
            user_id=1
        )
        appointment_service.uow.appointments.get_future_appointments_by_user_id.assert_called_once_with(
            user_id=1
        )
        appointment_service.policy.can_view.assert_called_once_with(
            user=patient_1,
            appointment=appointment_patient_1,
        )
        assert isinstance(result, list)
        assert isinstance(result[0], AppointmentResponseSchema)

    @pytest.mark.asyncio
    async def test_get_future_apps_by_user_id_not_found(
            self,
            patient_1,
            appointment_service,
    ):
        appointment_service.uow.users.get_user_by_id = AsyncMock(
            return_value=None
        )
        with pytest.raises(UserNotFoundException):
            await appointment_service.get_future_apps_by_user_id(
                user_id=1
            )
        appointment_service.uow.users.get_user_by_id.assert_awaited_once_with(
            user_id=1
        )
        appointment_service.uow.appointments.get_future_appointments_by_user_id.assert_not_called()
        appointment_service.policy.can_view.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_future_apps_by_user_id_apps_not_found(
            self,
            patient_1,
            appointment_service,
    ):
        appointment_service.uow.users.get_user_by_id = AsyncMock(
            return_value=patient_1
        )
        appointment_service.uow.appointments.get_future_appointments_by_user_id = AsyncMock(
            return_value=[]
        )
        result = await appointment_service.get_future_apps_by_user_id(1)
        appointment_service.uow.users.get_user_by_id.assert_awaited_once_with(
            user_id=1
        )
        appointment_service.uow.appointments.get_future_appointments_by_user_id.assert_awaited_once_with(
            user_id=1
        )
        appointment_service.policy.can_view.assert_not_called()
        assert isinstance(result, list)
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_get_future_apps_by_user_id_forbidden(
        self,
        patient_1,
        appointment_service,
        appointment_patient_1,
    ):
        appointment_service.uow.users.get_user_by_id = AsyncMock(
            return_value=patient_1
        )
        appointment_service.uow.appointments.get_future_appointments_by_user_id = AsyncMock(
            return_value=[appointment_patient_1, ]
        )
        appointment_service.policy.can_view = MagicMock(
            side_effect=ForbiddenException()
        )
        with pytest.raises(ForbiddenException):
            await appointment_service.get_future_apps_by_user_id(1)
        appointment_service.policy.can_view.assert_called_once_with(
            user=patient_1,
            appointment=appointment_patient_1,
        )

    @pytest.mark.asyncio
    async def test_get_past_apps_by_user_id_success(
            self,
            patient_1,
            appointment_service,
            appointment_patient_1
    ):
        appointment_service.uow.users.get_user_by_id = AsyncMock(
            return_value=patient_1
        )
        appointment_service.uow.appointments.get_past_appointments_by_user_id = AsyncMock(
            return_value=[appointment_patient_1]
        )
        appointment_service.policy.can_view = MagicMock()
        result = await appointment_service.get_past_apps_by_user_id(
            user_id=1
        )
        appointment_service.uow.users.get_user_by_id.assert_awaited_once_with(
            user_id=1
        )
        appointment_service.uow.appointments.get_past_appointments_by_user_id.assert_awaited_once_with(
            user_id=1
        )
        appointment_service.policy.can_view.assert_called_once_with(
            user=patient_1,
            appointment=appointment_patient_1,
        )
        assert len(result) == 1
        assert isinstance(result[0], AppointmentResponseSchema)

    @pytest.mark.asyncio
    async def test_get_past_apps_by_user_id_not_found(
            self,
            patient_1,
            appointment_service,
    ):
        appointment_service.uow.users.get_user_by_id = AsyncMock(
            return_value=None
        )
        with pytest.raises(UserNotFoundException):
            await appointment_service.get_past_apps_by_user_id(1)

        appointment_service.uow.appointments.get_past_appointments_by_user_id.assert_not_called()
        appointment_service.policy.can_view.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_past_apps_by_user_id_forbidden(
            self,
            patient_1,
            appointment_service,
            appointment_patient_1
    ):
        appointment_service.uow.users.get_user_by_id = AsyncMock(
            return_value=patient_1
        )
        appointment_service.uow.appointments.get_past_appointments_by_user_id = AsyncMock(
            return_value=[appointment_patient_1]
        )
        appointment_service.policy.can_view = MagicMock(
            side_effect=ForbiddenException()
        )
        with pytest.raises(ForbiddenException):
            await appointment_service.get_past_apps_by_user_id(1)
        appointment_service.policy.can_view.assert_called_once_with(
            user=patient_1,
            appointment=appointment_patient_1,
        )

    @pytest.mark.asyncio
    async def test_get_appointment_by_id(
            self,
            patient_1,
            appointment_service,
            appointment_patient_1

    ):
        appointment_service.uow.appointments.get_appointment_by_id = AsyncMock(
            return_value=appointment_patient_1
        )
        appointment_service.policy.can_view = MagicMock()
        result = await appointment_service.get_appointment_by_id(
            appointment_id=1,
            current_user=patient_1
        )
        appointment_service.uow.appointments.get_appointment_by_id.assert_awaited_once_with(appointment_id=1)
        appointment_service.policy.can_view.assert_called_once_with(
            user=patient_1,
            appointment=appointment_patient_1,
        )
        assert isinstance(result, AppointmentResponseSchema)

    @pytest.mark.asyncio
    async def test_get_appointment_by_id_not_found(
            self,
            patient_1,
            appointment_service,

    ):
        appointment_service.uow.appointments.get_appointment_by_id = AsyncMock(
            return_value=None
        )
        with pytest.raises(AppointmentNotFoundException):
            await appointment_service.get_appointment_by_id(
                appointment_id=1,
                current_user=patient_1,
            )
        appointment_service.policy.can_view.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_appointment_by_id_forbidden(
            self,
            patient_1,
            appointment_service,
            appointment_patient_1

    ):
        appointment_service.uow.appointments.get_appointment_by_id = AsyncMock(
            return_value=appointment_patient_1
        )
        appointment_service.policy.can_view = MagicMock(
            side_effect=ForbiddenException
        )
        with pytest.raises(ForbiddenException):
            await appointment_service.get_appointment_by_id(
                appointment_id=1,
                current_user=patient_1,
            )
        appointment_service.policy.can_view.assert_called_once_with(
            user=patient_1,
            appointment=appointment_patient_1,
        )

    @pytest.mark.asyncio
    async def test_delete_success(
            self,
            appointment_service,
            appointment_patient_1
    ):
        appointment_service.uow.appointments.get_appointment_by_id = AsyncMock(
            return_value=appointment_patient_1
        )
        appointment_service.uow.appointments.delete_appointment = AsyncMock()
        result = await appointment_service.delete(1)
        appointment_service.uow.appointments.get_appointment_by_id.assert_awaited_once_with(
            appointment_id=1
        )
        appointment_service.uow.appointments.delete_appointment.assert_awaited_once_with(
            appointment=appointment_patient_1,
        )
        assert result is None

    @pytest.mark.asyncio
    async def test_delete_not_found(
            self,
            appointment_service,
            appointment_patient_1
    ):
        appointment_service.uow.appointments.get_appointment_by_id = AsyncMock(
            return_value=None
        )
        with pytest.raises(AppointmentNotFoundException):
            await appointment_service.delete(1)
        appointment_service.uow.appointments.get_appointment_by_id.assert_awaited_once_with(
            appointment_id=1
        )
        appointment_service.uow.appointments.delete_appointment.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_upcoming_for_reminder_success(
            self,
            appointment_service,
            appointment_patient_1,
    ):
        appointment_service.uow.appointments.get_upcoming_appointments_for_reminder = AsyncMock(
            return_value=[appointment_patient_1]
        )
        result = await appointment_service.get_upcoming_for_reminder()
        assert result == [appointment_patient_1]
        appointment_service.uow.appointments.get_upcoming_appointments_for_reminder.assert_awaited_once()