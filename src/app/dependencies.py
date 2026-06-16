from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_session

from app.servicies.specialization import SpecializationService
from app.servicies.appointment import AppointmentService
from app.servicies.user import UserService
from app.servicies.schedule import ScheduleService
from app.servicies.schedule_slot import ScheduleSlotService

async def get_specialization_service(
    session: AsyncSession = Depends(get_session)
):
    return SpecializationService(session)


async def get_appointment_service(
    session: AsyncSession = Depends(get_session)
):
    return AppointmentService(session)


async def get_user_service(
    session: AsyncSession = Depends(get_session)
):
    return UserService(session)


async def get_schedule_service(
    session: AsyncSession = Depends(get_session)
):
    return ScheduleService(session)


async def get_schedule_slot_service(
    session: AsyncSession = Depends(get_session)
):
    return ScheduleSlotService(session)


