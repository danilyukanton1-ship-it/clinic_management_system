from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_session

from app.servicies.schedule_slot import ScheduleSlotService
from app.schemas.schedule_slot import ScheduleSlotSchema

router = APIRouter()

@router.get(
    path='/schedule-slot',
    tags=['Schedule Slots'],
    status_code=status.HTTP_200_OK,
    response_model=ScheduleSlotSchema
)
async def get_free_schedule_slot(
        session: AsyncSession = Depends(get_session),
):
    schedule_slot_service = ScheduleSlotService(session)
    return schedule_slot_service.get_free_slots()

