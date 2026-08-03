from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.scheduling.services.schedule import ScheduleService
from app.scheduling.services.schedule_absence import ScheduleAbsenceService
from app.scheduling.services.schedule_slot import ScheduleSlotService
from core.dependencies import get_session


async def get_schedule_service(session: AsyncSession = Depends(get_session)):
    return ScheduleService(session)


async def get_schedule_slot_service(session: AsyncSession = Depends(get_session)):
    return ScheduleSlotService(session)


async def get_schedule_absence_service(session: AsyncSession = Depends(get_session)):
    return ScheduleAbsenceService(session)
