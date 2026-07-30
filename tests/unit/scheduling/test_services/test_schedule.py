import pytest

from unittest.mock import AsyncMock, call
from datetime import date, datetime, timedelta
from app.scheduling.exceptions.schedule import (
    ScheduleNotFoundException,
    ScheduleAlreadyExistsException,
    ScheduleCanNotBeDeletedException,
)
from app.users.exceptions.user import UserNotFoundException
from common.enums.slot_status import SlotStatus
from common.enums.weekday import Weekday


class TestScheduleService:

    @pytest.mark.asyncio
    async def test_get_schedule_by_doctor_id_and_weekday_success(
        self,
        schedule_service,
        schedule_1,
    ):
        schedule_service.uow.schedules.get_by_doctor_id_and_weekday = AsyncMock(
            return_value=schedule_1
        )
        result = await schedule_service.get_schedule_by_doctor_id_and_weekday(
            doctor_id=schedule_1.doctor_id,
            weekday=schedule_1.weekday,
        )
        schedule_service.uow.schedules.get_by_doctor_id_and_weekday.assert_awaited_once_with(
            doctor_id=schedule_1.doctor_id,
            weekday=schedule_1.weekday,
        )
        assert result.id == schedule_1.id
        assert result.doctor_id == schedule_1.doctor_id
        assert result.weekday == schedule_1.weekday
        assert result.lunch_start_time == schedule_1.lunch_start_time
        assert result.lunch_end_time == schedule_1.lunch_end_time
        assert result.start_time == schedule_1.start_time
        assert result.end_time == schedule_1.end_time
        assert result.slot_duration_minutes == schedule_1.slot_duration_minutes
        assert result.is_active == schedule_1.is_active

    @pytest.mark.asyncio
    async def test_get_schedule_by_doctor_id_and_weekday_schedule_not_found(
        self,
        schedule_service,
    ):
        schedule_service.uow.schedules.get_by_doctor_id_and_weekday = AsyncMock(
            return_value=None
        )
        with pytest.raises(ScheduleNotFoundException):
            await schedule_service.get_schedule_by_doctor_id_and_weekday(
                doctor_id=1,
                weekday=Weekday.Monday,
            )
        schedule_service.uow.schedules.get_by_doctor_id_and_weekday.assert_awaited_once_with(
            doctor_id=1,
            weekday=Weekday.Monday,
        )

    @pytest.mark.asyncio
    async def test_get_schedule_by_id_success(
        self,
        schedule_service,
        schedule_1,
    ):
        schedule_service.uow.schedules.get_by_id = AsyncMock(return_value=schedule_1)

        result = await schedule_service.get_schedule_by_id(
            schedule_id=schedule_1.id,
        )

        schedule_service.uow.schedules.get_by_id.assert_awaited_once_with(
            schedule_id=schedule_1.id,
            admin=None,
        )

        assert result.id == schedule_1.id
        assert result.doctor_id == schedule_1.doctor_id
        assert result.weekday == schedule_1.weekday
        assert result.lunch_start_time == schedule_1.lunch_start_time
        assert result.lunch_end_time == schedule_1.lunch_end_time
        assert result.start_time == schedule_1.start_time
        assert result.end_time == schedule_1.end_time
        assert result.slot_duration_minutes == schedule_1.slot_duration_minutes
        assert result.is_active == schedule_1.is_active

    @pytest.mark.asyncio
    async def test_get_schedule_by_id_schedule_not_found(
        self,
        schedule_service,
    ):
        schedule_service.uow.schedules.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(ScheduleNotFoundException):
            await schedule_service.get_schedule_by_id(
                schedule_id=1,
            )

        schedule_service.uow.schedules.get_by_id.assert_awaited_once_with(
            schedule_id=1,
            admin=None,
        )

    @pytest.mark.asyncio
    async def test_get_all_schedule_by_doctor_id_success(
        self,
        schedule_service,
        schedule_1,
    ):
        schedule_service.uow.schedules.get_all_by_doctor_id = AsyncMock(
            return_value=[schedule_1]
        )

        result = await schedule_service.get_all_schedule_by_doctor_id(
            doctor_id=schedule_1.doctor_id,
        )

        schedule_service.uow.schedules.get_all_by_doctor_id.assert_awaited_once_with(
            doctor_id=schedule_1.doctor_id,
            admin=None,
        )

        assert len(result) == 1
        assert result[0].id == schedule_1.id
        assert result[0].doctor_id == schedule_1.doctor_id
        assert result[0].weekday == schedule_1.weekday
        assert result[0].lunch_start_time == schedule_1.lunch_start_time
        assert result[0].lunch_end_time == schedule_1.lunch_end_time
        assert result[0].start_time == schedule_1.start_time
        assert result[0].end_time == schedule_1.end_time
        assert result[0].slot_duration_minutes == schedule_1.slot_duration_minutes
        assert result[0].is_active == schedule_1.is_active

    @pytest.mark.asyncio
    async def test_get_all_schedule_by_doctor_id_schedule_not_found(
        self,
        schedule_service,
    ):
        schedule_service.uow.schedules.get_all_by_doctor_id = AsyncMock(return_value=[])

        with pytest.raises(ScheduleNotFoundException):
            await schedule_service.get_all_schedule_by_doctor_id(
                doctor_id=1,
            )

        schedule_service.uow.schedules.get_all_by_doctor_id.assert_awaited_once_with(
            doctor_id=1,
            admin=None,
        )

    @pytest.mark.asyncio
    async def test_create_success(
        self,
        schedule_service,
        doctor_1,
        schedule_create_schema,
        schedule_1,
    ):
        schedule_service.uow.users.get_doctor_by_id = AsyncMock(return_value=doctor_1)
        schedule_service.uow.schedules.if_exists = AsyncMock(return_value=False)
        schedule_service.uow.schedules.create_schedule = AsyncMock(
            return_value=schedule_1
        )
        result = await schedule_service.create(
            data=schedule_create_schema,
        )
        schedule_service.uow.users.get_doctor_by_id.assert_awaited_once_with(
            doctor_id=schedule_create_schema.doctor_id,
        )
        schedule_service.uow.schedules.if_exists.assert_awaited_once_with(
            doctor_id=schedule_create_schema.doctor_id,
            weekday=schedule_create_schema.weekday,
        )
        schedule_service.uow.schedules.create_schedule.assert_awaited_once_with(
            schedule=schedule_create_schema,
        )
        assert result.id == schedule_1.id
        assert result.doctor_id == schedule_1.doctor_id
        assert result.weekday == schedule_1.weekday
        assert result.lunch_start_time == schedule_1.lunch_start_time
        assert result.lunch_end_time == schedule_1.lunch_end_time
        assert result.start_time == schedule_1.start_time
        assert result.end_time == schedule_1.end_time
        assert result.slot_duration_minutes == schedule_1.slot_duration_minutes
        assert result.is_active == schedule_1.is_active

    @pytest.mark.asyncio
    async def test_create_doctor_not_found(
        self,
        schedule_service,
        schedule_create_schema,
    ):
        schedule_service.uow.users.get_doctor_by_id = AsyncMock(return_value=None)
        schedule_service.uow.schedules.if_exists = AsyncMock()
        schedule_service.uow.schedules.create_schedule = AsyncMock()

        with pytest.raises(UserNotFoundException):
            await schedule_service.create(
                data=schedule_create_schema,
            )

        schedule_service.uow.users.get_doctor_by_id.assert_awaited_once_with(
            doctor_id=schedule_create_schema.doctor_id,
        )
        schedule_service.uow.schedules.if_exists.assert_not_awaited()
        schedule_service.uow.schedules.create_schedule.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_create_schedule_already_exists(
        self,
        schedule_service,
        doctor_1,
        schedule_create_schema,
    ):
        schedule_service.uow.users.get_doctor_by_id = AsyncMock(return_value=doctor_1)
        schedule_service.uow.schedules.if_exists = AsyncMock(return_value=True)
        schedule_service.uow.schedules.create_schedule = AsyncMock()

        with pytest.raises(ScheduleAlreadyExistsException):
            await schedule_service.create(
                data=schedule_create_schema,
            )

        schedule_service.uow.users.get_doctor_by_id.assert_awaited_once_with(
            doctor_id=schedule_create_schema.doctor_id,
        )
        schedule_service.uow.schedules.if_exists.assert_awaited_once_with(
            doctor_id=schedule_create_schema.doctor_id,
            weekday=schedule_create_schema.weekday,
        )
        schedule_service.uow.schedules.create_schedule.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_success_without_last_booked(
        self,
        schedule_service,
        schedule_1,
        schedule_1_updated,
        schedule_update_schema,
        schedule_slot_1,
        schedule_slot_2,
    ):
        schedule_service.uow.schedules.get_by_doctor_id_and_weekday = AsyncMock(
            return_value=schedule_1
        )
        schedule_service.uow.schedule_slots.get_last_booked_datetime = AsyncMock(
            return_value=None
        )
        schedule_service.uow.schedule_slots.get_slots_after_date = AsyncMock(
            return_value=[schedule_slot_1, schedule_slot_2]
        )
        schedule_service.uow.schedule_slots.delete_slot = AsyncMock()
        schedule_service.uow.schedules.update_schedule = AsyncMock(
            return_value=schedule_1_updated
        )
        result = await schedule_service.update(
            doctor_id=schedule_1.doctor_id,
            weekday=schedule_1.weekday,
            data=schedule_update_schema,
        )
        schedule_service.uow.schedules.get_by_doctor_id_and_weekday.assert_awaited_once_with(
            doctor_id=schedule_1.doctor_id,
            weekday=schedule_1.weekday,
        )
        schedule_service.uow.schedule_slots.get_last_booked_datetime.assert_awaited_once_with(
            doctor_id=schedule_1.doctor_id,
            schedule_id=schedule_1.id,
        )
        schedule_service.uow.schedule_slots.get_slots_after_date.assert_awaited_once_with(
            doctor_id=schedule_1.doctor_id,
            day=date.today(),
            schedule_id=schedule_1.id,
        )
        schedule_service.uow.schedule_slots.delete_slot.assert_has_awaits(
            [
                call(slot=schedule_slot_1),
                call(slot=schedule_slot_2),
            ]
        )
        schedule_service.uow.schedules.update_schedule.assert_awaited_once_with(
            db_schedule=schedule_1,
            data=schedule_update_schema,
        )
        assert result.id == schedule_1_updated.id
        assert result.doctor_id == schedule_1_updated.doctor_id
        assert result.weekday == schedule_1_updated.weekday
        assert result.lunch_start_time == schedule_1_updated.lunch_start_time
        assert result.lunch_end_time == schedule_1_updated.lunch_end_time
        assert result.start_time == schedule_1_updated.start_time
        assert result.end_time == schedule_1_updated.end_time
        assert result.slot_duration_minutes == schedule_1_updated.slot_duration_minutes
        assert result.is_active == schedule_1_updated.is_active

    @pytest.mark.asyncio
    async def test_update_success_with_last_booked(
        self,
        schedule_service,
        schedule_1,
        schedule_1_updated,
        schedule_update_schema,
        schedule_slot_1,
        schedule_slot_2,
    ):
        last_booked = datetime(2026, 1, 10, 12, 0)
        expected_day = last_booked.date() + timedelta(days=1)

        schedule_service.uow.schedules.get_by_doctor_id_and_weekday = AsyncMock(
            return_value=schedule_1
        )
        schedule_service.uow.schedule_slots.get_last_booked_datetime = AsyncMock(
            return_value=last_booked
        )
        schedule_service.uow.schedule_slots.get_slots_after_date = AsyncMock(
            return_value=[schedule_slot_1, schedule_slot_2]
        )
        schedule_service.uow.schedule_slots.delete_slot = AsyncMock()
        schedule_service.uow.schedules.update_schedule = AsyncMock(
            return_value=schedule_1_updated
        )

        await schedule_service.update(
            doctor_id=schedule_1.doctor_id,
            weekday=schedule_1.weekday,
            data=schedule_update_schema,
        )

        schedule_service.uow.schedule_slots.get_slots_after_date.assert_awaited_once_with(
            doctor_id=schedule_1.doctor_id,
            day=expected_day,
            schedule_id=schedule_1.id,
        )

        schedule_service.uow.schedule_slots.delete_slot.assert_has_awaits(
            [
                call(slot=schedule_slot_1),
                call(slot=schedule_slot_2),
            ]
        )

    @pytest.mark.asyncio
    async def test_update_schedule_not_found(
        self,
        schedule_service,
        schedule_update_schema,
    ):
        schedule_service.uow.schedules.get_by_doctor_id_and_weekday = AsyncMock(
            return_value=None
        )
        schedule_service.uow.schedule_slots.get_last_booked_datetime = AsyncMock()
        schedule_service.uow.schedule_slots.get_slots_after_date = AsyncMock()
        schedule_service.uow.schedule_slots.delete_slot = AsyncMock()
        schedule_service.uow.schedules.update_schedule = AsyncMock()

        with pytest.raises(ScheduleNotFoundException):
            await schedule_service.update(
                doctor_id=1,
                weekday=Weekday.Monday,
                data=schedule_update_schema,
            )

        schedule_service.uow.schedules.get_by_doctor_id_and_weekday.assert_awaited_once_with(
            doctor_id=1,
            weekday=Weekday.Monday,
        )
        schedule_service.uow.schedule_slots.get_last_booked_datetime.assert_not_awaited()
        schedule_service.uow.schedule_slots.get_slots_after_date.assert_not_awaited()
        schedule_service.uow.schedule_slots.delete_slot.assert_not_awaited()
        schedule_service.uow.schedules.update_schedule.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_deactivate_schedule_success(
        self,
        schedule_service,
        schedule_1,
        schedule_slot_1,
        schedule_slot_2,
    ):
        schedule_service.uow.schedules.get_by_id = AsyncMock(return_value=schedule_1)
        schedule_service.uow.schedule_slots.get_future_slots_by_doctor_id_status = (
            AsyncMock(return_value=[])
        )
        schedule_service.uow.schedule_slots.get_slots_after_date = AsyncMock(
            return_value=[schedule_slot_1, schedule_slot_2]
        )
        schedule_service.uow.schedule_slots.delete_slot = AsyncMock()
        schedule_service.uow.schedules.make_schedule_unactive = AsyncMock()

        result = await schedule_service.deactivate_schedule(
            schedule_id=schedule_1.id,
        )

        schedule_service.uow.schedules.get_by_id.assert_awaited_once_with(
            schedule_id=schedule_1.id,
        )

        schedule_service.uow.schedule_slots.get_future_slots_by_doctor_id_status.assert_awaited_once_with(
            doctor_id=schedule_1.doctor_id,
            status=SlotStatus.BOOKED,
            weekday=schedule_1.weekday,
        )

        schedule_service.uow.schedule_slots.get_slots_after_date.assert_awaited_once_with(
            doctor_id=schedule_1.doctor_id,
            day=date.today(),
            schedule_id=schedule_1.id,
        )

        schedule_service.uow.schedule_slots.delete_slot.assert_has_awaits(
            [
                call(slot=schedule_slot_1),
                call(slot=schedule_slot_2),
            ]
        )

        schedule_service.uow.schedules.make_schedule_unactive.assert_awaited_once_with(
            schedule=schedule_1,
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_deactivate_schedule_schedule_not_found(
        self,
        schedule_service,
    ):
        schedule_service.uow.schedules.get_by_id = AsyncMock(return_value=None)
        schedule_service.uow.schedule_slots.get_future_slots_by_doctor_id_status = (
            AsyncMock()
        )
        schedule_service.uow.schedule_slots.get_slots_after_date = AsyncMock()
        schedule_service.uow.schedule_slots.delete_slot = AsyncMock()
        schedule_service.uow.schedules.make_schedule_unactive = AsyncMock()

        with pytest.raises(ScheduleNotFoundException):
            await schedule_service.deactivate_schedule(
                schedule_id=1,
            )

        schedule_service.uow.schedules.get_by_id.assert_awaited_once_with(
            schedule_id=1,
        )

        schedule_service.uow.schedule_slots.get_future_slots_by_doctor_id_status.assert_not_awaited()
        schedule_service.uow.schedule_slots.get_slots_after_date.assert_not_awaited()
        schedule_service.uow.schedule_slots.delete_slot.assert_not_awaited()
        schedule_service.uow.schedules.make_schedule_unactive.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_deactivate_schedule_can_not_be_deleted(
        self,
        schedule_service,
        schedule_1,
        schedule_slot_1,
    ):
        schedule_service.uow.schedules.get_by_id = AsyncMock(return_value=schedule_1)
        schedule_service.uow.schedule_slots.get_future_slots_by_doctor_id_status = (
            AsyncMock(return_value=[schedule_slot_1])
        )
        schedule_service.uow.schedule_slots.get_slots_after_date = AsyncMock()
        schedule_service.uow.schedule_slots.delete_slot = AsyncMock()
        schedule_service.uow.schedules.make_schedule_unactive = AsyncMock()

        with pytest.raises(ScheduleCanNotBeDeletedException):
            await schedule_service.deactivate_schedule(
                schedule_id=schedule_1.id,
            )

        schedule_service.uow.schedules.get_by_id.assert_awaited_once_with(
            schedule_id=schedule_1.id,
        )

        schedule_service.uow.schedule_slots.get_future_slots_by_doctor_id_status.assert_awaited_once_with(
            doctor_id=schedule_1.doctor_id,
            status=SlotStatus.BOOKED,
            weekday=schedule_1.weekday,
        )

        schedule_service.uow.schedule_slots.get_slots_after_date.assert_not_awaited()
        schedule_service.uow.schedule_slots.delete_slot.assert_not_awaited()
        schedule_service.uow.schedules.make_schedule_unactive.assert_not_awaited()
