from fastapi import APIRouter, Depends, status

from app.scheduling.dependencies import get_schedule_slot_service

from app.scheduling.services.schedule_slot import ScheduleSlotService
from app.scheduling.schemas.schedule_slot import ScheduleSlotSchema

router = APIRouter()

@router.get(
    path='/schedule-slot',
    tags=['Schedule Slots'],
    status_code=status.HTTP_200_OK,
    response_model=list[ScheduleSlotSchema]
)
async def get_free_schedule_slot(
        schedule_slot_service: ScheduleSlotService = Depends(get_schedule_slot_service),
):
    return await schedule_slot_service.get_free_slots()

