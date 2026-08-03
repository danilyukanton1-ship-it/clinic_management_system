from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.scheduling.exceptions.schedule_absence import (
    AbsenceAlreadyFinishedException,
    AbsenceAlreadyScheduledException,
    AbsenceAlreadyStartedException,
    AbsenceCanNotBeChangedException,
    AbsenceNotFoundException,
)
from app.scheduling.schemas.schedule_absence import ScheduleAbsenceResponseSchema
from app.users.exceptions.user import UserNotFoundException
from common.pagination.schemas import PaginationResult
from common.permissions.exceptions import ForbiddenException


class TestScheduleAbsence:

    @pytest.mark.asyncio
    async def test_create_absence_success(
        self,
        schedule_absence_service,
        doctor_1,
        schedule_absence_create_schema,
        schedule_absence_1,
    ):
        schedule_absence_service.uow.users.get_doctor_by_id = AsyncMock(
            return_value=doctor_1
        )
        schedule_absence_service.uow.absences.get_overlapping_absence = AsyncMock(
            return_value=None
        )
        schedule_absence_service.uow.absences.create_absence = AsyncMock(
            return_value=schedule_absence_1
        )
        schedule_absence_service._make_slots_unavailable = AsyncMock()
        result = await schedule_absence_service.create(
            data=schedule_absence_create_schema
        )
        schedule_absence_service.uow.users.get_doctor_by_id.assert_awaited_once_with(
            doctor_id=schedule_absence_create_schema.doctor_id
        )
        schedule_absence_service.uow.absences.get_overlapping_absence.assert_awaited_once_with(
            doctor_id=schedule_absence_create_schema.doctor_id,
            start_date=schedule_absence_create_schema.start_date,
            end_date=schedule_absence_create_schema.end_date,
        )
        schedule_absence_service.uow.absences.create_absence.assert_awaited_once_with(
            data=schedule_absence_create_schema
        )
        schedule_absence_service._make_slots_unavailable.assert_awaited_once_with(
            doctor_id=schedule_absence_create_schema.doctor_id,
            start_date=schedule_absence_create_schema.start_date,
            end_date=schedule_absence_create_schema.end_date,
        )

        assert isinstance(result, ScheduleAbsenceResponseSchema)
        assert result.id == schedule_absence_1.id
        assert result.doctor_id == schedule_absence_1.doctor_id
        assert result.start_date == schedule_absence_1.start_date
        assert result.end_date == schedule_absence_1.end_date

    @pytest.mark.asyncio
    async def test_create_absence_doctor_not_found(
        self,
        schedule_absence_service,
        schedule_absence_create_schema,
    ):
        schedule_absence_service.uow.users.get_doctor_by_id = AsyncMock(
            return_value=None
        )
        schedule_absence_service.uow.absences.get_overlapping_absence = AsyncMock()
        schedule_absence_service.uow.absences.create_absence = AsyncMock()
        schedule_absence_service._make_slots_unavailable = AsyncMock()

        with pytest.raises(UserNotFoundException):
            await schedule_absence_service.create(data=schedule_absence_create_schema)

        schedule_absence_service.uow.users.get_doctor_by_id.assert_awaited_once_with(
            doctor_id=schedule_absence_create_schema.doctor_id
        )
        schedule_absence_service.uow.absences.get_overlapping_absence.assert_not_awaited()
        schedule_absence_service.uow.absences.create_absence.assert_not_awaited()
        schedule_absence_service._make_slots_unavailable.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_create_absence_already_scheduled(
        self,
        schedule_absence_service,
        doctor_1,
        schedule_absence_create_schema,
        schedule_absence_1,
    ):
        schedule_absence_service.uow.users.get_doctor_by_id = AsyncMock(
            return_value=doctor_1
        )
        schedule_absence_service.uow.absences.get_overlapping_absence = AsyncMock(
            return_value=schedule_absence_1
        )
        schedule_absence_service.uow.absences.create_absence = AsyncMock()
        schedule_absence_service._make_slots_unavailable = AsyncMock()

        with pytest.raises(AbsenceAlreadyScheduledException):
            await schedule_absence_service.create(data=schedule_absence_create_schema)

        schedule_absence_service.uow.users.get_doctor_by_id.assert_awaited_once_with(
            doctor_id=schedule_absence_create_schema.doctor_id
        )
        schedule_absence_service.uow.absences.get_overlapping_absence.assert_awaited_once_with(
            doctor_id=schedule_absence_create_schema.doctor_id,
            start_date=schedule_absence_create_schema.start_date,
            end_date=schedule_absence_create_schema.end_date,
        )
        schedule_absence_service.uow.absences.create_absence.assert_not_awaited()
        schedule_absence_service._make_slots_unavailable.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_future_absence_success(
        self,
        schedule_absence_service,
        schedule_absence_1,
        updated_schedule_absence,
        schedule_absence_update_schema,
    ):
        schedule_absence_service.uow.absences.get_absence_by_id = AsyncMock(
            return_value=schedule_absence_1
        )
        schedule_absence_service.uow.absences.get_overlapping_absence = AsyncMock(
            return_value=None
        )
        schedule_absence_service.uow.absences.update_absence = AsyncMock(
            return_value=updated_schedule_absence
        )

        schedule_absence_service._unblock_slots_for_absence = AsyncMock()
        schedule_absence_service._make_slots_unavailable = AsyncMock()

        result = await schedule_absence_service.update(
            absence_id=schedule_absence_1.id,
            data=schedule_absence_update_schema,
        )

        schedule_absence_service.uow.absences.get_absence_by_id.assert_awaited_once_with(
            absence_id=schedule_absence_1.id
        )
        schedule_absence_service.uow.absences.get_overlapping_absence.assert_awaited_once()
        schedule_absence_service.uow.absences.update_absence.assert_awaited_once_with(
            absence=schedule_absence_1,
            data=schedule_absence_update_schema,
        )

        schedule_absence_service._unblock_slots_for_absence.assert_awaited_once()
        schedule_absence_service._make_slots_unavailable.assert_awaited_once()

        assert isinstance(result, ScheduleAbsenceResponseSchema)
        assert result.id == updated_schedule_absence.id
        assert result.doctor_id == updated_schedule_absence.doctor_id
        assert result.start_date == updated_schedule_absence.start_date
        assert result.end_date == updated_schedule_absence.end_date

    @pytest.mark.asyncio
    async def test_update_absence_not_found(
        self,
        schedule_absence_service,
        schedule_absence_update_schema,
    ):
        schedule_absence_service.uow.absences.get_absence_by_id = AsyncMock(
            return_value=None
        )
        schedule_absence_service.uow.absences.get_overlapping_absence = AsyncMock()
        schedule_absence_service.uow.absences.update_absence = AsyncMock()

        schedule_absence_service._unblock_slots_for_absence = AsyncMock()
        schedule_absence_service._make_slots_unavailable = AsyncMock()

        with pytest.raises(AbsenceNotFoundException):
            await schedule_absence_service.update(
                absence_id=1,
                data=schedule_absence_update_schema,
            )

        schedule_absence_service.uow.absences.get_absence_by_id.assert_awaited_once_with(
            absence_id=1
        )
        schedule_absence_service.uow.absences.get_overlapping_absence.assert_not_awaited()
        schedule_absence_service.uow.absences.update_absence.assert_not_awaited()

        schedule_absence_service._unblock_slots_for_absence.assert_not_awaited()
        schedule_absence_service._make_slots_unavailable.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_absence_already_finished(
        self,
        schedule_absence_service,
        schedule_absence_ended,
        schedule_absence_update_schema,
    ):
        schedule_absence_service.uow.absences.get_absence_by_id = AsyncMock(
            return_value=schedule_absence_ended
        )
        schedule_absence_service.uow.absences.get_overlapping_absence = AsyncMock()
        schedule_absence_service.uow.absences.update_absence = AsyncMock()

        schedule_absence_service._unblock_slots_for_absence = AsyncMock()
        schedule_absence_service._make_slots_unavailable = AsyncMock()

        with pytest.raises(AbsenceAlreadyFinishedException):
            await schedule_absence_service.update(
                absence_id=schedule_absence_ended.id,
                data=schedule_absence_update_schema,
            )

        schedule_absence_service.uow.absences.get_absence_by_id.assert_awaited_once_with(
            absence_id=schedule_absence_ended.id
        )

        schedule_absence_service.uow.absences.get_overlapping_absence.assert_not_awaited()
        schedule_absence_service.uow.absences.update_absence.assert_not_awaited()

        schedule_absence_service._unblock_slots_for_absence.assert_not_awaited()
        schedule_absence_service._make_slots_unavailable.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_started_absence_start_date_changed(
        self,
        schedule_absence_service,
        schedule_absence_started,
        started_schedule_absence_update_schema,
    ):
        schedule_absence_service.uow.absences.get_absence_by_id = AsyncMock(
            return_value=schedule_absence_started
        )

        started_schedule_absence_update_schema.start_date = (
            started_schedule_absence_update_schema.start_date + timedelta(days=1)
        )

        schedule_absence_service.uow.absences.get_overlapping_absence = AsyncMock()
        schedule_absence_service.uow.absences.update_absence = AsyncMock()

        schedule_absence_service._unblock_slots_for_absence = AsyncMock()
        schedule_absence_service._make_slots_unavailable = AsyncMock()

        with pytest.raises(AbsenceAlreadyStartedException):
            await schedule_absence_service.update(
                absence_id=schedule_absence_started.id,
                data=started_schedule_absence_update_schema,
            )

        schedule_absence_service.uow.absences.get_absence_by_id.assert_awaited_once_with(
            absence_id=schedule_absence_started.id
        )

        schedule_absence_service.uow.absences.get_overlapping_absence.assert_not_awaited()
        schedule_absence_service.uow.absences.update_absence.assert_not_awaited()

        schedule_absence_service._unblock_slots_for_absence.assert_not_awaited()
        schedule_absence_service._make_slots_unavailable.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_started_absence_end_date_in_past(
        self,
        schedule_absence_service,
        schedule_absence_started,
        started_schedule_absence_update_schema,
    ):
        schedule_absence_service.uow.absences.get_absence_by_id = AsyncMock(
            return_value=schedule_absence_started
        )

        started_schedule_absence_update_schema.start_date = (
            schedule_absence_started.start_date
        )
        started_schedule_absence_update_schema.end_date = datetime.now(UTC) - timedelta(
            days=1
        )

        schedule_absence_service.uow.absences.get_overlapping_absence = AsyncMock()
        schedule_absence_service.uow.absences.update_absence = AsyncMock()

        schedule_absence_service._unblock_slots_for_absence = AsyncMock()
        schedule_absence_service._make_slots_unavailable = AsyncMock()

        with pytest.raises(AbsenceCanNotBeChangedException):
            await schedule_absence_service.update(
                absence_id=schedule_absence_started.id,
                data=started_schedule_absence_update_schema,
            )

        schedule_absence_service.uow.absences.get_absence_by_id.assert_awaited_once_with(
            absence_id=schedule_absence_started.id
        )
        schedule_absence_service.uow.absences.get_overlapping_absence.assert_not_awaited()
        schedule_absence_service.uow.absences.update_absence.assert_not_awaited()

        schedule_absence_service._unblock_slots_for_absence.assert_not_awaited()
        schedule_absence_service._make_slots_unavailable.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_started_absence_success(
        self,
        schedule_absence_service,
        schedule_absence_started,
        started_schedule_absence_update_schema,
        updated_schedule_absence,
    ):
        started_schedule_absence_update_schema.start_date = (
            schedule_absence_started.start_date
        )

        schedule_absence_service.uow.absences.get_absence_by_id = AsyncMock(
            return_value=schedule_absence_started
        )
        schedule_absence_service.uow.absences.get_overlapping_absence = AsyncMock(
            return_value=None
        )
        schedule_absence_service.uow.absences.update_absence = AsyncMock(
            return_value=updated_schedule_absence
        )

        schedule_absence_service._unblock_slots_for_absence = AsyncMock()
        schedule_absence_service._make_slots_unavailable = AsyncMock()

        result = await schedule_absence_service.update(
            absence_id=schedule_absence_started.id,
            data=started_schedule_absence_update_schema,
        )

        schedule_absence_service.uow.absences.get_absence_by_id.assert_awaited_once_with(
            absence_id=schedule_absence_started.id
        )
        schedule_absence_service.uow.absences.get_overlapping_absence.assert_awaited_once()
        schedule_absence_service.uow.absences.update_absence.assert_awaited_once_with(
            absence=schedule_absence_started,
            data=started_schedule_absence_update_schema,
        )

        schedule_absence_service._unblock_slots_for_absence.assert_awaited_once()
        schedule_absence_service._make_slots_unavailable.assert_awaited_once()

        assert isinstance(result, ScheduleAbsenceResponseSchema)
        assert result.id == updated_schedule_absence.id
        assert result.doctor_id == updated_schedule_absence.doctor_id
        assert result.start_date == updated_schedule_absence.start_date
        assert result.end_date == updated_schedule_absence.end_date

    @pytest.mark.asyncio
    async def test_update_overlapping_absence(
        self,
        schedule_absence_service,
        schedule_absence_1,
        schedule_absence_update_schema,
    ):
        schedule_absence_service.uow.absences.get_absence_by_id = AsyncMock(
            return_value=schedule_absence_1
        )
        schedule_absence_service.uow.absences.get_overlapping_absence = AsyncMock(
            return_value=schedule_absence_1
        )
        schedule_absence_service.uow.absences.update_absence = AsyncMock()

        schedule_absence_service._unblock_slots_for_absence = AsyncMock()
        schedule_absence_service._make_slots_unavailable = AsyncMock()

        with pytest.raises(AbsenceAlreadyScheduledException):
            await schedule_absence_service.update(
                absence_id=schedule_absence_1.id,
                data=schedule_absence_update_schema,
            )

        schedule_absence_service.uow.absences.get_absence_by_id.assert_awaited_once_with(
            absence_id=schedule_absence_1.id
        )
        schedule_absence_service.uow.absences.get_overlapping_absence.assert_awaited_once()
        schedule_absence_service.uow.absences.update_absence.assert_not_awaited()

        schedule_absence_service._unblock_slots_for_absence.assert_not_awaited()
        schedule_absence_service._make_slots_unavailable.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_started_absence_reason_changed(
        self,
        schedule_absence_service,
        schedule_absence_started,
        started_schedule_absence_update_schema,
    ):
        schedule_absence_service.uow.absences.get_absence_by_id = AsyncMock(
            return_value=schedule_absence_started
        )

        started_schedule_absence_update_schema.start_date = (
            schedule_absence_started.start_date
        )
        started_schedule_absence_update_schema.reason = "New reason"

        schedule_absence_service.uow.absences.get_overlapping_absence = AsyncMock()
        schedule_absence_service.uow.absences.update_absence = AsyncMock()

        schedule_absence_service._unblock_slots_for_absence = AsyncMock()
        schedule_absence_service._make_slots_unavailable = AsyncMock()

        with pytest.raises(AbsenceCanNotBeChangedException):
            await schedule_absence_service.update(
                absence_id=schedule_absence_started.id,
                data=started_schedule_absence_update_schema,
            )

        schedule_absence_service.uow.absences.get_absence_by_id.assert_awaited_once_with(
            absence_id=schedule_absence_started.id
        )

        schedule_absence_service.uow.absences.get_overlapping_absence.assert_not_awaited()
        schedule_absence_service.uow.absences.update_absence.assert_not_awaited()

        schedule_absence_service._unblock_slots_for_absence.assert_not_awaited()
        schedule_absence_service._make_slots_unavailable.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_delete_success(
        self,
        schedule_absence_service,
        schedule_absence_1,
    ):
        schedule_absence_service.uow.absences.get_absence_by_id = AsyncMock(
            return_value=schedule_absence_1
        )
        schedule_absence_service.uow.absences.delete_absence = AsyncMock()

        schedule_absence_service._unblock_slots_for_absence = AsyncMock()

        result = await schedule_absence_service.delete(absence_id=schedule_absence_1.id)

        schedule_absence_service.uow.absences.get_absence_by_id.assert_awaited_once_with(
            schedule_absence_1.id
        )
        schedule_absence_service._unblock_slots_for_absence.assert_awaited_once_with(
            doctor_id=schedule_absence_1.doctor_id,
            start_date=schedule_absence_1.start_date,
            end_date=schedule_absence_1.end_date,
        )
        schedule_absence_service.uow.absences.delete_absence.assert_awaited_once_with(
            schedule_absence_1
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_delete_absence_not_found(
        self,
        schedule_absence_service,
    ):
        schedule_absence_service.uow.absences.get_absence_by_id = AsyncMock(
            return_value=None
        )
        schedule_absence_service.uow.absences.delete_absence = AsyncMock()

        schedule_absence_service._unblock_slots_for_absence = AsyncMock()

        with pytest.raises(AbsenceNotFoundException):
            await schedule_absence_service.delete(absence_id=1)

        schedule_absence_service.uow.absences.get_absence_by_id.assert_awaited_once_with(
            1
        )
        schedule_absence_service._unblock_slots_for_absence.assert_not_awaited()
        schedule_absence_service.uow.absences.delete_absence.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_delete_started_absence(
        self,
        schedule_absence_service,
        schedule_absence_started,
    ):
        schedule_absence_service.uow.absences.get_absence_by_id = AsyncMock(
            return_value=schedule_absence_started
        )
        schedule_absence_service.uow.absences.delete_absence = AsyncMock()

        schedule_absence_service._unblock_slots_for_absence = AsyncMock()

        with pytest.raises(AbsenceAlreadyStartedException):
            await schedule_absence_service.delete(
                absence_id=schedule_absence_started.id
            )

        schedule_absence_service.uow.absences.get_absence_by_id.assert_awaited_once_with(
            schedule_absence_started.id
        )
        schedule_absence_service._unblock_slots_for_absence.assert_not_awaited()
        schedule_absence_service.uow.absences.delete_absence.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_get_future_by_doctor_id_success(
        self,
        schedule_absence_service,
        doctor_1,
        admin_1,
        schedule_absence_1,
        pagination,
    ):
        schedule_absence_service.uow.users.get_doctor_by_id = AsyncMock(
            return_value=doctor_1,
        )

        schedule_absence_service.uow.absences.get_future_absences_by_doctor_id = (
            AsyncMock(
                return_value=PaginationResult(
                    items=[schedule_absence_1],
                    total=1,
                )
            )
        )

        schedule_absence_service.policy.can_view = MagicMock()

        result = await schedule_absence_service.get_future_by_doctor_id(
            doctor_id=doctor_1.id,
            current_user=admin_1,
            pagination=pagination,
        )

        schedule_absence_service.uow.users.get_doctor_by_id.assert_awaited_once_with(
            doctor_id=doctor_1.id,
        )

        schedule_absence_service.uow.absences.get_future_absences_by_doctor_id.assert_awaited_once_with(
            doctor_id=doctor_1.id,
            pagination=pagination,
        )

        schedule_absence_service.policy.can_view.assert_called_once_with(
            user=admin_1,
            schedule_absence=schedule_absence_1,
        )

        assert result.total == 1
        assert result.page == 1
        assert result.page_size == 20
        assert result.pages == 1

        assert len(result.items) == 1
        assert isinstance(result.items[0], ScheduleAbsenceResponseSchema)
        assert result.items[0].id == schedule_absence_1.id

    @pytest.mark.asyncio
    async def test_get_future_by_doctor_id_doctor_not_found(
        self,
        schedule_absence_service,
        admin_1,
        pagination,
    ):
        schedule_absence_service.uow.users.get_doctor_by_id = AsyncMock(
            return_value=None,
        )

        schedule_absence_service.uow.absences.get_future_absences_by_doctor_id = (
            AsyncMock()
        )

        schedule_absence_service.policy.can_view = MagicMock()

        with pytest.raises(UserNotFoundException):
            await schedule_absence_service.get_future_by_doctor_id(
                doctor_id=1,
                current_user=admin_1,
                pagination=pagination,
            )

        schedule_absence_service.uow.users.get_doctor_by_id.assert_awaited_once_with(
            doctor_id=1,
        )

        schedule_absence_service.uow.absences.get_future_absences_by_doctor_id.assert_not_called()

        schedule_absence_service.policy.can_view.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_future_by_doctor_id_no_absences(
        self,
        schedule_absence_service,
        doctor_1,
        admin_1,
        pagination,
    ):
        schedule_absence_service.uow.users.get_doctor_by_id = AsyncMock(
            return_value=doctor_1,
        )

        schedule_absence_service.uow.absences.get_future_absences_by_doctor_id = (
            AsyncMock(
                return_value=PaginationResult(
                    items=[],
                    total=0,
                )
            )
        )

        schedule_absence_service.policy.can_view = MagicMock()

        result = await schedule_absence_service.get_future_by_doctor_id(
            doctor_id=doctor_1.id,
            current_user=admin_1,
            pagination=pagination,
        )

        schedule_absence_service.uow.users.get_doctor_by_id.assert_awaited_once_with(
            doctor_id=doctor_1.id,
        )

        schedule_absence_service.uow.absences.get_future_absences_by_doctor_id.assert_awaited_once_with(
            doctor_id=doctor_1.id,
            pagination=pagination,
        )

        schedule_absence_service.policy.can_view.assert_not_called()

        assert result.total == 0
        assert result.page == 1
        assert result.page_size == 20
        assert (
            result.pages == 0
        )  # либо 1, если в build_paginated_response используется max(1, ...)
        assert result.items == []

    @pytest.mark.asyncio
    async def test_get_future_by_doctor_id_forbidden(
        self,
        schedule_absence_service,
        doctor_1,
        current_patient,
        schedule_absence_1,
        pagination,
    ):
        schedule_absence_service.uow.users.get_doctor_by_id = AsyncMock(
            return_value=doctor_1,
        )

        schedule_absence_service.uow.absences.get_future_absences_by_doctor_id = (
            AsyncMock(
                return_value=PaginationResult(
                    items=[schedule_absence_1],
                    total=1,
                )
            )
        )

        schedule_absence_service.policy.can_view = MagicMock(
            side_effect=ForbiddenException(),
        )

        with pytest.raises(ForbiddenException):
            await schedule_absence_service.get_future_by_doctor_id(
                doctor_id=doctor_1.id,
                current_user=current_patient,
                pagination=pagination,
            )

        schedule_absence_service.uow.users.get_doctor_by_id.assert_awaited_once_with(
            doctor_id=doctor_1.id,
        )

        schedule_absence_service.uow.absences.get_future_absences_by_doctor_id.assert_awaited_once_with(
            doctor_id=doctor_1.id,
            pagination=pagination,
        )

        schedule_absence_service.policy.can_view.assert_called_once_with(
            user=current_patient,
            schedule_absence=schedule_absence_1,
        )

    @pytest.mark.asyncio
    async def test_get_past_by_doctor_id_success(
        self,
        schedule_absence_service,
        doctor_1,
        admin_1,
        schedule_absence_ended,
        pagination,
    ):
        schedule_absence_service.uow.users.get_doctor_by_id = AsyncMock(
            return_value=doctor_1,
        )

        schedule_absence_service.uow.absences.get_past_absences_by_doctor_id = (
            AsyncMock(
                return_value=PaginationResult(
                    items=[schedule_absence_ended],
                    total=1,
                )
            )
        )

        schedule_absence_service.policy.can_view = MagicMock()

        result = await schedule_absence_service.get_past_by_doctor_id(
            doctor_id=doctor_1.id,
            current_user=admin_1,
            pagination=pagination,
        )

        schedule_absence_service.uow.users.get_doctor_by_id.assert_awaited_once_with(
            doctor_id=doctor_1.id,
        )

        schedule_absence_service.uow.absences.get_past_absences_by_doctor_id.assert_awaited_once_with(
            doctor_id=doctor_1.id,
            pagination=pagination,
        )

        schedule_absence_service.policy.can_view.assert_called_once_with(
            user=admin_1,
            schedule_absence=schedule_absence_ended,
        )

        assert result.total == 1
        assert result.page == 1
        assert result.page_size == 20
        assert result.pages == 1

        assert len(result.items) == 1
        assert isinstance(result.items[0], ScheduleAbsenceResponseSchema)
        assert result.items[0].id == schedule_absence_ended.id

    @pytest.mark.asyncio
    async def test_get_past_by_doctor_id_doctor_not_found(
        self,
        schedule_absence_service,
        admin_1,
        pagination,
    ):
        schedule_absence_service.uow.users.get_doctor_by_id = AsyncMock(
            return_value=None,
        )

        schedule_absence_service.uow.absences.get_past_absences_by_doctor_id = (
            AsyncMock()
        )

        schedule_absence_service.policy.can_view = MagicMock()

        with pytest.raises(UserNotFoundException):
            await schedule_absence_service.get_past_by_doctor_id(
                doctor_id=1,
                current_user=admin_1,
                pagination=pagination,
            )

        schedule_absence_service.uow.users.get_doctor_by_id.assert_awaited_once_with(
            doctor_id=1,
        )

        schedule_absence_service.uow.absences.get_past_absences_by_doctor_id.assert_not_called()

        schedule_absence_service.policy.can_view.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_past_by_doctor_id_no_absences(
        self,
        schedule_absence_service,
        doctor_1,
        admin_1,
        pagination,
    ):
        schedule_absence_service.uow.users.get_doctor_by_id = AsyncMock(
            return_value=doctor_1,
        )

        schedule_absence_service.uow.absences.get_past_absences_by_doctor_id = (
            AsyncMock(
                return_value=PaginationResult(
                    items=[],
                    total=0,
                )
            )
        )

        schedule_absence_service.policy.can_view = MagicMock()

        result = await schedule_absence_service.get_past_by_doctor_id(
            doctor_id=doctor_1.id,
            current_user=admin_1,
            pagination=pagination,
        )

        schedule_absence_service.uow.users.get_doctor_by_id.assert_awaited_once_with(
            doctor_id=doctor_1.id,
        )

        schedule_absence_service.uow.absences.get_past_absences_by_doctor_id.assert_awaited_once_with(
            doctor_id=doctor_1.id,
            pagination=pagination,
        )

        schedule_absence_service.policy.can_view.assert_not_called()

        assert result.total == 0
        assert result.page == 1
        assert result.page_size == 20
        assert (
            result.pages == 0
        )  # или 1, если build_paginated_response использует max(1, ...)
        assert result.items == []

    @pytest.mark.asyncio
    async def test_get_past_by_doctor_id_forbidden(
        self,
        schedule_absence_service,
        doctor_1,
        current_patient,
        schedule_absence_ended,
        pagination,
    ):
        schedule_absence_service.uow.users.get_doctor_by_id = AsyncMock(
            return_value=doctor_1,
        )

        schedule_absence_service.uow.absences.get_past_absences_by_doctor_id = (
            AsyncMock(
                return_value=PaginationResult(
                    items=[schedule_absence_ended],
                    total=1,
                )
            )
        )

        schedule_absence_service.policy.can_view = MagicMock(
            side_effect=ForbiddenException(),
        )

        with pytest.raises(ForbiddenException):
            await schedule_absence_service.get_past_by_doctor_id(
                doctor_id=doctor_1.id,
                current_user=current_patient,
                pagination=pagination,
            )

        schedule_absence_service.uow.users.get_doctor_by_id.assert_awaited_once_with(
            doctor_id=doctor_1.id,
        )

        schedule_absence_service.uow.absences.get_past_absences_by_doctor_id.assert_awaited_once_with(
            doctor_id=doctor_1.id,
            pagination=pagination,
        )

        schedule_absence_service.policy.can_view.assert_called_once_with(
            user=current_patient,
            schedule_absence=schedule_absence_ended,
        )

    @pytest.mark.asyncio
    async def test_get_absence_by_id_success(
        self,
        schedule_absence_service,
        admin_1,
        schedule_absence_1,
    ):
        schedule_absence_service.uow.absences.get_absence_by_id = AsyncMock(
            return_value=schedule_absence_1
        )
        schedule_absence_service.policy.can_view = MagicMock()

        result = await schedule_absence_service.get_absence_by_id(
            absence_id=schedule_absence_1.id,
            current_user=admin_1,
        )

        schedule_absence_service.uow.absences.get_absence_by_id.assert_awaited_once_with(
            absence_id=schedule_absence_1.id
        )
        schedule_absence_service.policy.can_view.assert_called_once_with(
            user=admin_1,
            schedule_absence=schedule_absence_1,
        )

        assert isinstance(result, ScheduleAbsenceResponseSchema)
        assert result.id == schedule_absence_1.id
        assert result.doctor_id == schedule_absence_1.doctor_id
        assert result.start_date == schedule_absence_1.start_date
        assert result.end_date == schedule_absence_1.end_date

    @pytest.mark.asyncio
    async def test_get_absence_by_id_not_found(
        self,
        schedule_absence_service,
        admin_1,
    ):
        schedule_absence_service.uow.absences.get_absence_by_id = AsyncMock(
            return_value=None
        )
        schedule_absence_service.policy.can_view = MagicMock()

        with pytest.raises(AbsenceNotFoundException):
            await schedule_absence_service.get_absence_by_id(
                absence_id=1,
                current_user=admin_1,
            )

        schedule_absence_service.uow.absences.get_absence_by_id.assert_awaited_once_with(
            absence_id=1
        )
        schedule_absence_service.policy.can_view.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_absence_by_id_forbidden(
        self,
        schedule_absence_service,
        current_patient,
        schedule_absence_1,
    ):
        schedule_absence_service.uow.absences.get_absence_by_id = AsyncMock(
            return_value=schedule_absence_1
        )
        schedule_absence_service.policy.can_view = MagicMock(
            side_effect=ForbiddenException()
        )

        with pytest.raises(ForbiddenException):
            await schedule_absence_service.get_absence_by_id(
                absence_id=schedule_absence_1.id,
                current_user=current_patient,
            )

        schedule_absence_service.uow.absences.get_absence_by_id.assert_awaited_once_with(
            absence_id=schedule_absence_1.id
        )
        schedule_absence_service.policy.can_view.assert_called_once_with(
            user=current_patient,
            schedule_absence=schedule_absence_1,
        )
