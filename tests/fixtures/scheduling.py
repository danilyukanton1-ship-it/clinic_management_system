from datetime import datetime

import pytest

from app.scheduling.models.schedule_slot import ScheduleSlot
from common.enums.slot_status import SlotStatus

TEST_START_DATETIME = datetime(2030, 1, 1, 10, 0)
TEST_END_DATETIME = datetime(2030, 1, 1, 10, 30)
@pytest.fixture
def schedule_slot_free():
    return ScheduleSlot(
        id=1,
        schedule_id=1,
        doctor_id=1,
        slot_start=TEST_START_DATETIME,
        slot_end=TEST_END_DATETIME,
        status=SlotStatus.FREE
    )

@pytest.fixture
def schedule_slot_booked():
    return ScheduleSlot(
        id=1,
        schedule_id=1,
        doctor_id=1,
        slot_start=TEST_START_DATETIME,
        slot_end=TEST_END_DATETIME,
        status=SlotStatus.BOOKED
    )

@pytest.fixture
def schedule_slot_blocked():
    return ScheduleSlot(
        id=1,
        schedule_id=1,
        doctor_id=1,
        slot_start=TEST_START_DATETIME,
        slot_end=TEST_END_DATETIME,
        status=SlotStatus.BLOCKED
    )