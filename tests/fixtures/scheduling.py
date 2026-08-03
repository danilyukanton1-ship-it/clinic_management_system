from datetime import UTC, datetime, time, timedelta
from unittest.mock import MagicMock

import pytest

from app.scheduling.models.schedule import Schedule
from app.scheduling.models.schedule_absence import ScheduleAbsence
from app.scheduling.models.schedule_slot import ScheduleSlot
from app.scheduling.schemas.schedule import ScheduleCreateSchema, ScheduleUpdateSchema
from app.scheduling.schemas.schedule_absence import (
    ScheduleAbsenceCreateSchema,
    ScheduleAbsenceUpdateSchema,
)
from app.scheduling.schemas.schedule_slot import (
    ScheduleSlotCreateSchema,
    ScheduleSlotUpdateSchema,
)
from app.scheduling.services.schedule import ScheduleService
from app.scheduling.services.schedule_absence import ScheduleAbsenceService
from app.scheduling.services.schedule_slot import ScheduleSlotService
from common.enums.absence_reason import AbsenceReason
from common.enums.slot_status import SlotStatus
from common.enums.weekday import Weekday

TEST_START_DATETIME = datetime(2030, 1, 7, 10, 0, tzinfo=UTC)
TEST_END_DATETIME = datetime(2030, 1, 7, 10, 30, tzinfo=UTC)


@pytest.fixture
def schedule_service(mock_async_session, mock_uow) -> ScheduleService:
    service = ScheduleService(mock_async_session)
    service.uow = mock_uow
    return service


@pytest.fixture
def schedule_absence_service(mock_async_session, mock_uow) -> ScheduleAbsenceService:
    service = ScheduleAbsenceService(mock_async_session)
    service.uow = mock_uow
    service.policy = MagicMock()
    return service


@pytest.fixture
def schedule_slot_service(mock_async_session, mock_uow) -> ScheduleSlotService:
    service = ScheduleSlotService(mock_async_session)
    service.uow = mock_uow
    return service


@pytest.fixture
def schedule_update_schema():
    return ScheduleUpdateSchema(
        lunch_start_time=time(12, 0),
        lunch_end_time=time(13, 0),
        start_time=time(8, 0),
        end_time=time(17, 0),
        slot_duration_minutes=60,
    )


@pytest.fixture
def schedule_create_schema():
    return ScheduleCreateSchema(
        doctor_id=1,
        weekday=Weekday.Monday,
        lunch_start_time=time(13, 0),
        lunch_end_time=time(14, 0),
        start_time=time(9, 0),
        end_time=time(18, 0),
        slot_duration_minutes=30,
    )


@pytest.fixture
def schedule_1():
    return Schedule(
        id=1,
        doctor_id=1,
        weekday=Weekday.Monday,
        lunch_start_time=time(13, 0),
        lunch_end_time=time(14, 0),
        start_time=time(9, 0),
        end_time=time(18, 0),
        slot_duration_minutes=30,
        is_active=True,
    )


@pytest.fixture
def schedule_1_updated():
    return Schedule(
        id=1,
        doctor_id=1,
        weekday=Weekday.Monday,
        lunch_start_time=time(12, 0),
        lunch_end_time=time(13, 0),
        start_time=time(8, 0),
        end_time=time(17, 0),
        slot_duration_minutes=60,
        is_active=True,
    )


@pytest.fixture
def schedule_slot_free():
    return ScheduleSlot(
        id=1,
        schedule_id=1,
        doctor_id=1,
        slot_start=TEST_START_DATETIME,
        slot_end=TEST_END_DATETIME,
        status=SlotStatus.FREE,
    )


@pytest.fixture
def schedule_slot_1():
    return ScheduleSlot(
        id=1,
        schedule_id=1,
        doctor_id=1,
        slot_start=TEST_START_DATETIME,
        slot_end=TEST_END_DATETIME,
        status=SlotStatus.FREE,
    )


@pytest.fixture
def schedule_slot_2():
    return ScheduleSlot(
        id=2,
        schedule_id=1,
        doctor_id=1,
        slot_start=TEST_START_DATETIME + timedelta(hours=1),
        slot_end=TEST_END_DATETIME + timedelta(hours=1),
        status=SlotStatus.FREE,
    )


@pytest.fixture
def schedule_slot_booked():
    return ScheduleSlot(
        id=1,
        schedule_id=1,
        doctor_id=1,
        slot_start=TEST_START_DATETIME,
        slot_end=TEST_END_DATETIME,
        status=SlotStatus.BOOKED,
    )


@pytest.fixture
def schedule_slot_blocked():
    return ScheduleSlot(
        id=1,
        schedule_id=1,
        doctor_id=1,
        slot_start=TEST_START_DATETIME,
        slot_end=TEST_END_DATETIME,
        status=SlotStatus.BLOCKED,
    )


@pytest.fixture
def schedule_absence_1(doctor_1):
    now = datetime.now(UTC)
    return ScheduleAbsence(
        id=1,
        doctor_id=doctor_1.id,
        start_date=now + timedelta(days=2),
        end_date=now + timedelta(days=5),
        reason=AbsenceReason.PERSONAL,
    )


@pytest.fixture
def schedule_absence_started(doctor_1):
    now = datetime.now(UTC)
    return ScheduleAbsence(
        id=1,
        doctor_id=doctor_1.id,
        start_date=now - timedelta(days=2),
        end_date=now + timedelta(days=5),
        reason=AbsenceReason.PERSONAL,
    )


@pytest.fixture
def schedule_absence_ended(doctor_1):
    now = datetime.now(UTC)
    return ScheduleAbsence(
        id=1,
        doctor_id=doctor_1.id,
        start_date=now - timedelta(days=5),
        end_date=now - timedelta(days=2),
        reason=AbsenceReason.PERSONAL,
    )


@pytest.fixture
def schedule_absence_create_schema(doctor_1):
    now = datetime.now(UTC)
    return ScheduleAbsenceCreateSchema(
        doctor_id=doctor_1.id,
        start_date=now + timedelta(days=2),
        end_date=now + timedelta(days=5),
        reason=AbsenceReason.PERSONAL,
    )


@pytest.fixture
def schedule_absence_update_schema(doctor_1):
    now = datetime.now(UTC)
    return ScheduleAbsenceUpdateSchema(
        start_date=now + timedelta(days=3),
        end_date=now + timedelta(days=6),
        reason=AbsenceReason.TRAINING,
    )


@pytest.fixture
def started_schedule_absence_update_schema():
    now = datetime.now(UTC)
    return ScheduleAbsenceUpdateSchema(
        start_date=now - timedelta(days=2),
        end_date=now + timedelta(days=5),
        reason=AbsenceReason.PERSONAL,
    )


@pytest.fixture
def updated_schedule_absence(schedule_absence_1):
    schedule_absence_1.start_date += timedelta(days=1)
    schedule_absence_1.end_date += timedelta(days=1)

    return schedule_absence_1


@pytest.fixture
def schedule_slot_create_schema():
    return ScheduleSlotCreateSchema(
        doctor_id=1,
        schedule_id=1,
        status=SlotStatus.FREE,
        slot_start=TEST_START_DATETIME,
        slot_end=TEST_END_DATETIME,
    )


@pytest.fixture
def schedule_slot_update_schema():
    return ScheduleSlotUpdateSchema(
        slot_start=TEST_START_DATETIME + timedelta(hours=1),
        slot_end=TEST_END_DATETIME + timedelta(hours=1),
        status=SlotStatus.FREE,
    )


@pytest.fixture
def schedule_slot_1_updated():
    return ScheduleSlot(
        id=1,
        schedule_id=1,
        doctor_id=1,
        slot_start=TEST_START_DATETIME + timedelta(hours=1),
        slot_end=TEST_END_DATETIME + timedelta(hours=1),
        status=SlotStatus.FREE,
    )
