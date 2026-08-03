from datetime import UTC, date, datetime, time
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.scheduling.exceptions.schedule import ScheduleNotFoundException
from app.scheduling.exceptions.schedule_slot import (
    SlotAlreadyBookedException,
    SlotCanNotBeChangedException,
    SlotNotFoundException,
    SlotStatusCanNotBeChangedException,
)
from app.scheduling.models.schedule_slot import ScheduleSlot
from app.scheduling.schemas.schedule_slot import ScheduleSlotBulkCreateSchema
from app.users.exceptions.user import UserNotFoundException
from common.enums.slot_status import SlotStatus
from common.enums.weekday import Weekday
from common.pagination.schemas import PaginationResult


class TestScheduleSlotService:

    @pytest.mark.asyncio
    async def test_change_slot_status_success(
        self, schedule_slot_service, schedule_slot_free, schedule_slot_booked
    ):
        schedule_slot_service.uow.schedule_slots.get_slot_by_id = AsyncMock(
            return_value=schedule_slot_free,
        )

        schedule_slot_service.uow.schedule_slots.change_slot_status = AsyncMock(
            return_value=schedule_slot_booked,
        )

        result = await schedule_slot_service.change_slot_status(
            slot_id=schedule_slot_free.id,
            status=SlotStatus.BOOKED,
        )

        schedule_slot_service.uow.schedule_slots.get_slot_by_id.assert_awaited_once_with(
            slot_id=schedule_slot_free.id,
        )

        schedule_slot_service.uow.schedule_slots.change_slot_status.assert_awaited_once_with(
            slot=schedule_slot_free,
            status=SlotStatus.BOOKED,
        )

        assert result.id == schedule_slot_booked.id
        assert result.doctor_id == schedule_slot_booked.doctor_id
        assert result.slot_start == schedule_slot_booked.slot_start
        assert result.slot_end == schedule_slot_booked.slot_end
        assert result.status == SlotStatus.BOOKED

    @pytest.mark.asyncio
    async def test_change_slot_status_slot_not_found(
        self,
        schedule_slot_service,
    ):
        schedule_slot_service.uow.schedule_slots.get_slot_by_id = AsyncMock(
            return_value=None,
        )
        schedule_slot_service.uow.schedule_slots.change_slot_status = AsyncMock()

        with pytest.raises(SlotNotFoundException):
            await schedule_slot_service.change_slot_status(
                slot_id=1,
                status=SlotStatus.BOOKED,
            )

        schedule_slot_service.uow.schedule_slots.get_slot_by_id.assert_awaited_once_with(
            slot_id=1,
        )
        schedule_slot_service.uow.schedule_slots.change_slot_status.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_change_slot_status_already_booked(
        self,
        schedule_slot_service,
        schedule_slot_booked,
    ):
        schedule_slot_service.uow.schedule_slots.get_slot_by_id = AsyncMock(
            return_value=schedule_slot_booked,
        )
        schedule_slot_service.uow.schedule_slots.change_slot_status = AsyncMock()

        with pytest.raises(SlotAlreadyBookedException):
            await schedule_slot_service.change_slot_status(
                slot_id=schedule_slot_booked.id,
                status=SlotStatus.BOOKED,
            )

        schedule_slot_service.uow.schedule_slots.get_slot_by_id.assert_awaited_once_with(
            slot_id=schedule_slot_booked.id,
        )
        schedule_slot_service.uow.schedule_slots.change_slot_status.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_change_slot_status_same_status(
        self,
        schedule_slot_service,
        schedule_slot_free,
    ):
        schedule_slot_service.uow.schedule_slots.get_slot_by_id = AsyncMock(
            return_value=schedule_slot_free,
        )
        schedule_slot_service.uow.schedule_slots.change_slot_status = AsyncMock()

        with pytest.raises(SlotStatusCanNotBeChangedException):
            await schedule_slot_service.change_slot_status(
                slot_id=schedule_slot_free.id,
                status=SlotStatus.FREE,
            )

        schedule_slot_service.uow.schedule_slots.get_slot_by_id.assert_awaited_once_with(
            slot_id=schedule_slot_free.id,
        )
        schedule_slot_service.uow.schedule_slots.change_slot_status.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_get_future_slots_by_doctor_id_status_success(
        self,
        schedule_slot_service,
        doctor_1,
        schedule_slot_1,
        schedule_slot_2,
        pagination,
    ):
        schedule_slot_service.uow.users.get_doctor_by_id = AsyncMock(
            return_value=doctor_1,
        )

        schedule_slot_service.uow.schedule_slots.get_future_slots_by_doctor_id_status = AsyncMock(
            return_value=PaginationResult(
                items=[schedule_slot_1, schedule_slot_2],
                total=2,
            )
        )

        result = await schedule_slot_service.get_future_slots_by_doctor_id_status(
            doctor_id=doctor_1.id,
            status=SlotStatus.FREE,
            pagination=pagination,
        )

        schedule_slot_service.uow.users.get_doctor_by_id.assert_awaited_once_with(
            doctor_id=doctor_1.id,
        )

        schedule_slot_service.uow.schedule_slots.get_future_slots_by_doctor_id_status.assert_awaited_once_with(
            doctor_id=doctor_1.id,
            status=SlotStatus.FREE,
            pagination=pagination,
        )

        assert result.total == 2
        assert result.page == 1
        assert result.page_size == 20
        assert result.pages == 1

        assert len(result.items) == 2

        assert result.items[0].id == schedule_slot_1.id
        assert result.items[0].doctor_id == schedule_slot_1.doctor_id
        assert result.items[0].slot_start == schedule_slot_1.slot_start
        assert result.items[0].slot_end == schedule_slot_1.slot_end
        assert result.items[0].status == schedule_slot_1.status

        assert result.items[1].id == schedule_slot_2.id
        assert result.items[1].doctor_id == schedule_slot_2.doctor_id
        assert result.items[1].slot_start == schedule_slot_2.slot_start
        assert result.items[1].slot_end == schedule_slot_2.slot_end
        assert result.items[1].status == schedule_slot_2.status

    @pytest.mark.asyncio
    async def test_get_future_slots_by_doctor_id_status_no_slots(
        self,
        schedule_slot_service,
        doctor_1,
        pagination,
    ):
        schedule_slot_service.uow.users.get_doctor_by_id = AsyncMock(
            return_value=doctor_1,
        )

        schedule_slot_service.uow.schedule_slots.get_future_slots_by_doctor_id_status = AsyncMock(
            return_value=PaginationResult(
                items=[],
                total=0,
            )
        )

        result = await schedule_slot_service.get_future_slots_by_doctor_id_status(
            doctor_id=doctor_1.id,
            status=SlotStatus.FREE,
            pagination=pagination,
        )

        schedule_slot_service.uow.users.get_doctor_by_id.assert_awaited_once_with(
            doctor_id=doctor_1.id,
        )

        schedule_slot_service.uow.schedule_slots.get_future_slots_by_doctor_id_status.assert_awaited_once_with(
            doctor_id=doctor_1.id,
            status=SlotStatus.FREE,
            pagination=pagination,
        )

        assert result.total == 0
        assert result.page == 1
        assert result.page_size == 20
        assert (
            result.pages == 0
        )  # либо 1, если build_paginated_response использует max(1, ...)
        assert result.items == []

    @pytest.mark.asyncio
    async def test_get_future_slots_by_doctor_id_status_doctor_not_found(
        self,
        schedule_slot_service,
        pagination,
    ):
        schedule_slot_service.uow.users.get_doctor_by_id = AsyncMock(
            return_value=None,
        )

        schedule_slot_service.uow.schedule_slots.get_future_slots_by_doctor_id_status = (
            AsyncMock()
        )

        with pytest.raises(UserNotFoundException):
            await schedule_slot_service.get_future_slots_by_doctor_id_status(
                doctor_id=1,
                status=SlotStatus.FREE,
                pagination=pagination,
            )

        schedule_slot_service.uow.users.get_doctor_by_id.assert_awaited_once_with(
            doctor_id=1,
        )

        schedule_slot_service.uow.schedule_slots.get_future_slots_by_doctor_id_status.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_past_slots_by_doctor_id_status_success(
        self,
        schedule_slot_service,
        doctor_1,
        schedule_slot_1,
        schedule_slot_2,
        pagination,
    ):
        schedule_slot_service.uow.users.get_doctor_by_id = AsyncMock(
            return_value=doctor_1,
        )

        schedule_slot_service.uow.schedule_slots.get_past_slots_by_doctor_id_status = (
            AsyncMock(
                return_value=PaginationResult(
                    items=[schedule_slot_1, schedule_slot_2],
                    total=2,
                )
            )
        )

        result = await schedule_slot_service.get_past_slots_by_doctor_id_status(
            doctor_id=doctor_1.id,
            status=SlotStatus.FREE,
            pagination=pagination,
        )

        schedule_slot_service.uow.users.get_doctor_by_id.assert_awaited_once_with(
            doctor_id=doctor_1.id,
        )

        schedule_slot_service.uow.schedule_slots.get_past_slots_by_doctor_id_status.assert_awaited_once_with(
            doctor_id=doctor_1.id,
            status=SlotStatus.FREE,
            pagination=pagination,
        )

        assert result.total == 2
        assert result.page == 1
        assert result.page_size == 20
        assert result.pages == 1

        assert len(result.items) == 2

        assert result.items[0].id == schedule_slot_1.id
        assert result.items[0].doctor_id == schedule_slot_1.doctor_id
        assert result.items[0].slot_start == schedule_slot_1.slot_start
        assert result.items[0].slot_end == schedule_slot_1.slot_end
        assert result.items[0].status == schedule_slot_1.status

        assert result.items[1].id == schedule_slot_2.id
        assert result.items[1].doctor_id == schedule_slot_2.doctor_id
        assert result.items[1].slot_start == schedule_slot_2.slot_start
        assert result.items[1].slot_end == schedule_slot_2.slot_end
        assert result.items[1].status == schedule_slot_2.status

    @pytest.mark.asyncio
    async def test_get_past_slots_by_doctor_id_status_no_slots(
        self,
        schedule_slot_service,
        doctor_1,
        pagination,
    ):
        schedule_slot_service.uow.users.get_doctor_by_id = AsyncMock(
            return_value=doctor_1,
        )

        schedule_slot_service.uow.schedule_slots.get_past_slots_by_doctor_id_status = (
            AsyncMock(
                return_value=PaginationResult(
                    items=[],
                    total=0,
                )
            )
        )

        result = await schedule_slot_service.get_past_slots_by_doctor_id_status(
            doctor_id=doctor_1.id,
            status=SlotStatus.FREE,
            pagination=pagination,
        )

        schedule_slot_service.uow.users.get_doctor_by_id.assert_awaited_once_with(
            doctor_id=doctor_1.id,
        )

        schedule_slot_service.uow.schedule_slots.get_past_slots_by_doctor_id_status.assert_awaited_once_with(
            doctor_id=doctor_1.id,
            status=SlotStatus.FREE,
            pagination=pagination,
        )

        assert result.total == 0
        assert result.page == 1
        assert result.page_size == 20
        assert (
            result.pages == 0
        )  # либо 1, если build_paginated_response использует max(1, ...)
        assert result.items == []

    @pytest.mark.asyncio
    async def test_update_success(
        self,
        schedule_slot_service,
        schedule_slot_1,
        schedule_slot_1_updated,
        schedule_slot_update_schema,
    ):
        schedule_slot_service.uow.schedule_slots.get_slot_by_id = AsyncMock(
            return_value=schedule_slot_1,
        )
        schedule_slot_service.uow.schedule_slots.get_slots_overlapping_period = (
            AsyncMock(
                return_value=[],
            )
        )
        schedule_slot_service.uow.schedule_slots.update_slot = AsyncMock(
            return_value=schedule_slot_1_updated,
        )
        result = await schedule_slot_service.update(
            slot_id=schedule_slot_1.id,
            data=schedule_slot_update_schema,
        )
        schedule_slot_service.uow.schedule_slots.get_slot_by_id.assert_awaited_once_with(
            slot_id=schedule_slot_1.id,
        )
        schedule_slot_service.uow.schedule_slots.get_slots_overlapping_period.assert_awaited_once_with(
            doctor_id=schedule_slot_1.doctor_id,
            start_date=schedule_slot_update_schema.slot_start,
            end_date=schedule_slot_update_schema.slot_end,
            exclude_slot_id=schedule_slot_1.id,
        )
        schedule_slot_service.uow.schedule_slots.update_slot.assert_awaited_once_with(
            slot=schedule_slot_1,
            data=schedule_slot_update_schema,
        )
        assert result.id == schedule_slot_1_updated.id
        assert result.doctor_id == schedule_slot_1_updated.doctor_id
        assert result.slot_start == schedule_slot_1_updated.slot_start
        assert result.slot_end == schedule_slot_1_updated.slot_end
        assert result.status == schedule_slot_1_updated.status

    @pytest.mark.asyncio
    async def test_update_slot_not_found(
        self,
        schedule_slot_service,
        schedule_slot_update_schema,
    ):
        schedule_slot_service.uow.schedule_slots.get_slot_by_id = AsyncMock(
            return_value=None,
        )

        schedule_slot_service.uow.schedule_slots.get_slots_overlapping_period = (
            AsyncMock()
        )
        schedule_slot_service.uow.schedule_slots.update_slot = AsyncMock()

        with pytest.raises(SlotNotFoundException):
            await schedule_slot_service.update(
                slot_id=1,
                data=schedule_slot_update_schema,
            )

        schedule_slot_service.uow.schedule_slots.get_slot_by_id.assert_awaited_once_with(
            slot_id=1,
        )

        schedule_slot_service.uow.schedule_slots.get_slots_overlapping_period.assert_not_awaited()
        schedule_slot_service.uow.schedule_slots.update_slot.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_booked_slot(
        self,
        schedule_slot_service,
        schedule_slot_booked,
        schedule_slot_update_schema,
    ):
        schedule_slot_service.uow.schedule_slots.get_slot_by_id = AsyncMock(
            return_value=schedule_slot_booked,
        )
        schedule_slot_service.uow.schedule_slots.get_slots_overlapping_period = (
            AsyncMock()
        )
        schedule_slot_service.uow.schedule_slots.update_slot = AsyncMock()
        with pytest.raises(SlotCanNotBeChangedException):
            await schedule_slot_service.update(
                slot_id=schedule_slot_booked.id,
                data=schedule_slot_update_schema,
            )
        schedule_slot_service.uow.schedule_slots.get_slot_by_id.assert_awaited_once_with(
            slot_id=schedule_slot_booked.id,
        )
        schedule_slot_service.uow.schedule_slots.get_slots_overlapping_period.assert_not_awaited()
        schedule_slot_service.uow.schedule_slots.update_slot.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_blocked_slot(
        self,
        schedule_slot_service,
        schedule_slot_blocked,
        schedule_slot_update_schema,
    ):
        schedule_slot_service.uow.schedule_slots.get_slot_by_id = AsyncMock(
            return_value=schedule_slot_blocked,
        )
        schedule_slot_service.uow.schedule_slots.get_slots_overlapping_period = (
            AsyncMock()
        )
        schedule_slot_service.uow.schedule_slots.update_slot = AsyncMock()
        with pytest.raises(SlotCanNotBeChangedException):
            await schedule_slot_service.update(
                slot_id=schedule_slot_blocked.id,
                data=schedule_slot_update_schema,
            )
        schedule_slot_service.uow.schedule_slots.get_slot_by_id.assert_awaited_once_with(
            slot_id=schedule_slot_blocked.id,
        )
        schedule_slot_service.uow.schedule_slots.get_slots_overlapping_period.assert_not_awaited()
        schedule_slot_service.uow.schedule_slots.update_slot.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_overlapping_slots(
        self,
        schedule_slot_service,
        schedule_slot_1,
        schedule_slot_2,
        schedule_slot_update_schema,
    ):
        schedule_slot_service.uow.schedule_slots.get_slot_by_id = AsyncMock(
            return_value=schedule_slot_1,
        )
        schedule_slot_service.uow.schedule_slots.get_slots_overlapping_period = (
            AsyncMock(
                return_value=[schedule_slot_2],
            )
        )
        schedule_slot_service.uow.schedule_slots.update_slot = AsyncMock()
        with pytest.raises(SlotCanNotBeChangedException):
            await schedule_slot_service.update(
                slot_id=schedule_slot_1.id,
                data=schedule_slot_update_schema,
            )
        schedule_slot_service.uow.schedule_slots.get_slot_by_id.assert_awaited_once_with(
            slot_id=schedule_slot_1.id,
        )
        schedule_slot_service.uow.schedule_slots.get_slots_overlapping_period.assert_awaited_once_with(
            doctor_id=schedule_slot_1.doctor_id,
            start_date=schedule_slot_update_schema.slot_start,
            end_date=schedule_slot_update_schema.slot_end,
            exclude_slot_id=schedule_slot_1.id,
        )
        schedule_slot_service.uow.schedule_slots.update_slot.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_create_slots_success(
        self,
        schedule_slot_service,
        schedule_1,
    ):
        slot_start = datetime.combine(
            date(2030, 1, 7),
            schedule_1.start_time,
            tzinfo=UTC,
        )
        workday_end = datetime.combine(
            date(2030, 1, 7),
            schedule_1.end_time,
            tzinfo=UTC,
        )
        schedule_slot_service.uow.schedule_slots.slot_exists = AsyncMock(
            return_value=False,
        )
        schedule_slot_service.uow.schedule_slots.create_slot_instance = MagicMock(
            side_effect=lambda schedule_slot: ScheduleSlot(
                doctor_id=schedule_slot.doctor_id,
                schedule_id=schedule_slot.schedule_id,
                status=schedule_slot.status,
                slot_start=schedule_slot.slot_start,
                slot_end=schedule_slot.slot_end,
            )
        )

        result = await schedule_slot_service._create_slots(
            slot_start=slot_start,
            workday_end=workday_end,
            schedule=schedule_1,
        )

        assert len(result) == 16

        assert result[0].status == SlotStatus.FREE
        assert result[0].slot_start == datetime(2030, 1, 7, 9, 0, tzinfo=UTC)
        assert result[0].slot_end == datetime(2030, 1, 7, 9, 30, tzinfo=UTC)

        assert result[-1].status == SlotStatus.FREE
        assert result[-1].slot_start == datetime(2030, 1, 7, 17, 30, tzinfo=UTC)
        assert result[-1].slot_end == datetime(2030, 1, 7, 18, 0, tzinfo=UTC)

    @pytest.mark.asyncio
    async def test_create_slots_skip_lunch(
        self,
        schedule_slot_service,
        schedule_1,
    ):
        slot_start = datetime.combine(
            date(2030, 1, 7),
            schedule_1.start_time,
            tzinfo=UTC,
        )
        workday_end = datetime.combine(
            date(2030, 1, 7),
            schedule_1.end_time,
            tzinfo=UTC,
        )
        schedule_slot_service.uow.schedule_slots.slot_exists = AsyncMock(
            return_value=False,
        )
        schedule_slot_service.uow.schedule_slots.create_slot_instance = MagicMock(
            side_effect=lambda schedule_slot: ScheduleSlot(
                doctor_id=schedule_slot.doctor_id,
                schedule_id=schedule_slot.schedule_id,
                status=schedule_slot.status,
                slot_start=schedule_slot.slot_start,
                slot_end=schedule_slot.slot_end,
            )
        )

        result = await schedule_slot_service._create_slots(
            slot_start=slot_start,
            workday_end=workday_end,
            schedule=schedule_1,
        )

        assert all(
            not (
                slot.slot_start.time() < schedule_1.lunch_end_time
                and slot.slot_end.time() > schedule_1.lunch_start_time
            )
            for slot in result
        )

    @pytest.mark.asyncio
    async def test_create_slots_not_create_last_partial_slot(
        self,
        schedule_slot_service,
        schedule_1,
    ):
        schedule_1.slot_duration_minutes = 40

        slot_start = datetime.combine(
            date(2030, 1, 7),
            schedule_1.start_time,
            tzinfo=UTC,
        )
        workday_end = datetime.combine(
            date(2030, 1, 7),
            schedule_1.end_time,
            tzinfo=UTC,
        )
        schedule_slot_service.uow.schedule_slots.slot_exists = AsyncMock(
            return_value=False,
        )
        schedule_slot_service.uow.schedule_slots.create_slot_instance = MagicMock(
            side_effect=lambda schedule_slot: ScheduleSlot(
                doctor_id=schedule_slot.doctor_id,
                schedule_id=schedule_slot.schedule_id,
                status=schedule_slot.status,
                slot_start=schedule_slot.slot_start,
                slot_end=schedule_slot.slot_end,
            )
        )

        result = await schedule_slot_service._create_slots(
            slot_start=slot_start,
            workday_end=workday_end,
            schedule=schedule_1,
        )

        assert result[-1].slot_end <= workday_end
        assert all(slot.slot_end <= workday_end for slot in result)

    @pytest.mark.asyncio
    async def test_create_slots_free_slots(
        self,
        schedule_slot_service,
        schedule_1,
        schedule_slot_1,
        schedule_slot_2,
    ):
        schedule_slot_service.uow.schedules.get_all_by_doctor_id = AsyncMock(
            return_value=[schedule_1],
        )

        schedule_slot_service.uow.schedules.get_by_doctor_id_and_weekday = AsyncMock(
            return_value=schedule_1,
        )

        schedule_slot_service.uow.absences.get_overlapping_absence = AsyncMock(
            return_value=[],
        )

        schedule_slot_service._create_slots = AsyncMock(
            return_value=[schedule_slot_1, schedule_slot_2],
        )

        schedule_slot_service.uow.schedule_slots.bulk_create_slots = AsyncMock()

        result = await schedule_slot_service.create_slots(
            ScheduleSlotBulkCreateSchema(
                start_date=date(2030, 1, 7),
                end_date=date(2030, 1, 7),
                doctor_id=1,
            )
        )

        schedule_slot_service.uow.schedules.get_all_by_doctor_id.assert_awaited_once_with(
            doctor_id=1,
        )

        schedule_slot_service.uow.schedules.get_by_doctor_id_and_weekday.assert_awaited_once_with(
            doctor_id=1,
            weekday=Weekday.Monday,
        )

        schedule_slot_service.uow.absences.get_overlapping_absence.assert_awaited_once_with(
            doctor_id=1,
            start_date=datetime.combine(date(2030, 1, 7), time.min, tzinfo=UTC),
            end_date=datetime.combine(date(2030, 1, 7), time.max, tzinfo=UTC),
        )

        schedule_slot_service._create_slots.assert_awaited_once_with(
            slot_start=datetime.combine(
                date(2030, 1, 7),
                schedule_1.start_time,
                tzinfo=UTC,
            ),
            workday_end=datetime.combine(
                date(2030, 1, 7),
                schedule_1.end_time,
                tzinfo=UTC,
            ),
            schedule=schedule_1,
            absences=[],
        )

        schedule_slot_service.uow.schedule_slots.bulk_create_slots.assert_awaited_once_with(
            [schedule_slot_1, schedule_slot_2],
        )

        assert len(result) == 2

        assert result[0].id == schedule_slot_1.id
        assert result[0].doctor_id == schedule_slot_1.doctor_id
        assert result[0].slot_start == schedule_slot_1.slot_start
        assert result[0].slot_end == schedule_slot_1.slot_end
        assert result[0].status == schedule_slot_1.status

        assert result[1].id == schedule_slot_2.id
        assert result[1].doctor_id == schedule_slot_2.doctor_id
        assert result[1].slot_start == schedule_slot_2.slot_start
        assert result[1].slot_end == schedule_slot_2.slot_end
        assert result[1].status == schedule_slot_2.status

    @pytest.mark.asyncio
    async def test_create_slots_blocked_slots(
        self,
        schedule_slot_service,
        schedule_1,
        schedule_slot_1,
        schedule_slot_2,
        schedule_absence_1,
    ):
        schedule_slot_service.uow.schedules.get_all_by_doctor_id = AsyncMock(
            return_value=[schedule_1],
        )

        schedule_slot_service.uow.schedules.get_by_doctor_id_and_weekday = AsyncMock(
            return_value=schedule_1,
        )

        schedule_slot_service.uow.absences.get_overlapping_absence = AsyncMock(
            return_value=[schedule_absence_1],
        )

        schedule_slot_service._create_slots = AsyncMock(
            return_value=[schedule_slot_1, schedule_slot_2],
        )

        schedule_slot_service.uow.schedule_slots.bulk_create_slots = AsyncMock()

        await schedule_slot_service.create_slots(
            ScheduleSlotBulkCreateSchema(
                start_date=date(2030, 1, 7),
                end_date=date(2030, 1, 7),
                doctor_id=1,
            )
        )

        schedule_slot_service._create_slots.assert_awaited_once_with(
            slot_start=datetime.combine(
                date(2030, 1, 7),
                schedule_1.start_time,
                tzinfo=UTC,
            ),
            workday_end=datetime.combine(
                date(2030, 1, 7),
                schedule_1.end_time,
                tzinfo=UTC,
            ),
            schedule=schedule_1,
            absences=[schedule_absence_1],
        )

        schedule_slot_service.uow.schedule_slots.bulk_create_slots.assert_awaited_once_with(
            [schedule_slot_1, schedule_slot_2],
        )

    @pytest.mark.asyncio
    async def test_create_slots_skip_day_without_schedule(
        self,
        schedule_slot_service,
        schedule_1,
    ):
        schedule_slot_service.uow.schedules.get_all_by_doctor_id = AsyncMock(
            return_value=[schedule_1],
        )

        schedule_slot_service.uow.schedules.get_by_doctor_id_and_weekday = AsyncMock(
            return_value=None,
        )

        schedule_slot_service.uow.absences.get_overlapping_absence = AsyncMock()
        schedule_slot_service._create_slots = AsyncMock()
        schedule_slot_service.uow.schedule_slots.bulk_create_slots = AsyncMock()

        result = await schedule_slot_service.create_slots(
            ScheduleSlotBulkCreateSchema(
                start_date=date(2030, 1, 7),
                end_date=date(2030, 1, 7),
                doctor_id=1,
            )
        )

        assert result == []

        schedule_slot_service.uow.absences.get_overlapping_absence.assert_not_awaited()
        schedule_slot_service._create_slots.assert_not_awaited()
        schedule_slot_service.uow.schedule_slots.bulk_create_slots.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_create_slots_schedule_not_found(
        self,
        schedule_slot_service,
    ):
        schedule_slot_service.uow.schedules.get_all_by_doctor_id = AsyncMock(
            return_value=[],
        )

        schedule_slot_service.uow.schedules.get_by_doctor_id_and_weekday = AsyncMock()
        schedule_slot_service.uow.absences.get_overlapping_absence = AsyncMock()
        schedule_slot_service._create_slots = AsyncMock()
        schedule_slot_service.uow.schedule_slots.bulk_create_slots = AsyncMock()

        with pytest.raises(ScheduleNotFoundException):
            await schedule_slot_service.create_slots(
                ScheduleSlotBulkCreateSchema(
                    start_date=date(2030, 1, 7),
                    end_date=date(2030, 1, 7),
                    doctor_id=1,
                )
            )

        schedule_slot_service.uow.schedules.get_all_by_doctor_id.assert_awaited_once_with(
            doctor_id=1,
        )

        schedule_slot_service.uow.schedules.get_by_doctor_id_and_weekday.assert_not_awaited()
        schedule_slot_service.uow.absences.get_overlapping_absence.assert_not_awaited()
        schedule_slot_service._create_slots.assert_not_awaited()
        schedule_slot_service.uow.schedule_slots.bulk_create_slots.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_create_slots_empty_created_slots(
        self,
        schedule_slot_service,
        schedule_1,
    ):
        schedule_slot_service.uow.schedules.get_all_by_doctor_id = AsyncMock(
            return_value=[schedule_1],
        )

        schedule_slot_service.uow.schedules.get_by_doctor_id_and_weekday = AsyncMock(
            return_value=schedule_1,
        )

        schedule_slot_service.uow.absences.get_overlapping_absence = AsyncMock(
            return_value=None,
        )

        schedule_slot_service._create_slots = AsyncMock(
            return_value=[],
        )

        schedule_slot_service.uow.schedule_slots.bulk_create_slots = AsyncMock()

        result = await schedule_slot_service.create_slots(
            ScheduleSlotBulkCreateSchema(
                start_date=date(2030, 1, 7),
                end_date=date(2030, 1, 7),
                doctor_id=1,
            )
        )

        assert result == []

        schedule_slot_service.uow.schedule_slots.bulk_create_slots.assert_not_awaited()
